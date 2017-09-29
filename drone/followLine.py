######################################
############# IMPORTS ################
######################################
import time, sys
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron')
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron/drone/libs')
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron/drone/libs/XboxController')
import ps_drone
import xbox
import cv2
import numpy as np
import globalVars as G
import functions as F

#Guardar Video
#CODEC = cv2.cv.CV_FOURCC('D','I','V','3') # MPEG 4.3
#out = cv2.VideoWriter('output.avi',CODEC, 10.0, (640,480))
G.init()
def run():
    #G.DRONE.takeoff()
    #Variables adicionales
    waiting = 0
    stop =   False
    ground = False
    automatic = True
    flagTime = False
    seconds = time.localtime().tm_sec
    acum_x = 0
    acum_y = 0
    cantidad = 0
    once = True
    kernel = np.ones((5,5),np.uint8)

    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("Videos/Video8.avi")
    #Mientras no se mande a parar
    while not stop :
        flagTime,seconds = F.timePass(flagTime,seconds)
        automatic = F.controller(automatic)                     #Valor de automatic, cuando se da el boton START, cambia el valor
        try:
            # Leyendo frames del video del dron
            frameFirst = G.DRONE.VideoImage                     #Leyendo frames del dron
            if not(frameFirst is None):
                _,frameFirst = cap.read()
                frame = cv2.resize(frameFirst, (G.W, G.H))      #Cambiar tamano al frame
                #G.STEP = 0
                if G.STEP == 0:
                    frame = cv2.resize(frame,(G.W,G.H))
                    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    mask = cv2.inRange(HSV, np.array([G.H_MIN_T,G.S_MIN_T,G.V_MIN_T]), np.array([G.H_MAX_T,G.S_MAX_T,G.V_MAX_T]))
                    output = cv2.bitwise_and(frame, frame, mask = mask)

                    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
                    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                    _,tresh = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)    #Filtro de blanco y negro
                    #erode = cv2.erode(tresh, kernel, iterations=2)
                    dilate = cv2.dilate(tresh, kernel, iterations=8)

                    frame,center,flag = F.draw(frame,dilate)         #Se manda a dibujar sobre el objeto detectado
                elif G.STEP == 1:
                    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    mask = cv2.inRange(HSV, np.array([G.H_MIN,G.S_MIN,G.V_MIN]), np.array([G.H_MAX,G.S_MAX,G.V_MAX]))
                    output = cv2.bitwise_and(frame, frame, mask = mask)

                    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
                    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                    _,tresh = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)    #Filtro de blanco y negro
                    erode = cv2.erode(tresh, kernel, iterations=2)
                    dilate = cv2.dilate(erode, kernel, iterations=5)

                    frame,center,flag = F.drawLine(frame,dilate)         #Se manda a dibujar sobre el objeto detectado
                    #flagTime = True
                #Si se detecta algo
                if flag:
                    # Centro del objeto
                    x1 = center[0]
                    y1 = center[1]

                    acum_x += x1
                    acum_y += y1
                    cantidad += 1

                    if flagTime:
                        print("X: " + str(x1))
                        print("Y: " + str(y1))
                        print("---------------")
                        once = True

                    #Funcion para movimientos del dron con respecto al objeto detectadoq
                    if (automatic):
                        with G.XY_locking:
                            G.XY = (x1,y1)
                            G.vision_var = True

                        cantidad = 0
                        acum_x = 0
                        acum_y = 0
                    once = False
                else:
                    if automatic:
                        G.notFound = True
                    if not once:
                        print("NO DETECTA OBJETO")
                        once = True

                # Estatus de la bateria
                bat = G.DRONE.getBattery()[0]
                if flagTime:
                    print "Bateria: " + str(bat)
                    if automatic:
                        print("Modo: Automatico!")
                    else:
                        print("Modo: MANUAL")
                    print("----------------------------------")
                    print("----------------------------------")

                if bat < 15:
                    stop = True
                    print "Bateria Baja: "+str(bat)
                    print("----------------------------------")
                    print("----------------------------------")
                # Muestra imagen
                cv2.imshow("DRONE", frame)
                #cv2.imshow("DRONE-tresh", tresh)
                #cv2.imshow("DRONE-erode", erode)
                #cv2.imshow("DRONE-dilate", dilate)
                #cv2.imshow("DRONE-GRAY", tresh)
                print(str(G.STEP))
            else:
                if(waiting == 0):
                    print("Esperando...")
                waiting += 1
        except Exception as e:
            print "Error: " + str(e)
            print "Failed"

        if cv2.waitKey(1) & 0xFF == ord('q'):   stop =   True
        if G.JOY.Back():   stop =   True

    # Apagando
    print "Aterrizando..."
    #out.release()
    G.DRONE.land()
    G.JOY.close()
    print "Terminado."
