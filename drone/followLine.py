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
    #Variables adicionales
    waiting = 0
    stop =   False
    flagTime = False
    seconds = time.localtime().tm_sec
    once = True
    kernel = np.ones((5,5),np.uint8)

    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("Videos/Video6.avi")
    #Mientras no se mande a parar
    while not stop :
        #time.sleep(0.01)
        flagTime,seconds = F.timePass(flagTime,seconds)
        try:
            # Leyendo frames del video del dron
            frameFirst = G.DRONE.VideoImage                     #Leyendo frames del dron
            if not(frameFirst is None):
                G.activation = True
                _,frameFirst = cap.read()
                frame = cv2.resize(frameFirst, (G.W, G.H))      #Cambiar tamano al frame
                #G.STEP = 0
                if G.STEP == 0:
                    frame = cv2.resize(frame,(G.W,G.H))
                    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    #MARCA
                    mask = cv2.inRange(HSV, np.array([G.H_MIN_T,G.S_MIN_T,G.V_MIN_T]), np.array([G.H_MAX_T,G.S_MAX_T,G.V_MAX_T]))
                    output = cv2.bitwise_and(frame, frame, mask = mask)

                    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
                    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                    _,tresh = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)    #Filtro de blanco y negro
                    #erode = cv2.erode(tresh, kernel, iterations=2)
                    dilate = cv2.dilate(tresh, kernel, iterations=8)
                    frame,center,flag = F.draw(frame,dilate)         #Se manda a dibujar sobre el objeto detectado

                    #LINEA
                    mask = cv2.inRange(HSV, np.array([G.H_MIN,G.S_MIN,G.V_MIN]), np.array([G.H_MAX,G.S_MAX,G.V_MAX]))
                    output = cv2.bitwise_and(frame, frame, mask = mask)

                    blurred = cv2.GaussianBlur(output, (5, 5), 0)

                    erode = cv2.erode(blurred, kernel, iterations=2)
                    dilate = cv2.dilate(erode, kernel, iterations=5)

                    gray = cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY)
                    _,tresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)    #Filtro de blanco y negro

                    array_tresh = [tresh[(G.H/3):2*(G.H/3),0:G.W],tresh[0:(G.H/3),0:G.W]]

                    frame,center_line,flag_line = F.drawLine(frame,array_tresh)         #Se manda a dibujar sobre el objeto detectado
                elif G.STEP == 1:
                    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    mask = cv2.inRange(HSV, np.array([G.H_MIN,G.S_MIN,G.V_MIN]), np.array([G.H_MAX,G.S_MAX,G.V_MAX]))
                    output = cv2.bitwise_and(frame, frame, mask = mask)

                    blurred = cv2.GaussianBlur(output, (5, 5), 0)

                    erode = cv2.erode(blurred, kernel, iterations=2)
                    dilate = cv2.dilate(erode, kernel, iterations=5)

                    gray = cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY)
                    _,tresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)    #Filtro de blanco y negro

                    array_tresh = [tresh[(G.H/3):2*(G.H/3),0:G.W],tresh[0:(G.H/3),0:G.W]]

                    frame,array_center_line,flag = F.drawLine(frame,array_tresh)         #Se manda a dibujar sobre el objeto detectado
                    #flagTime = True
                #Si se detecta algo
                if flag:
                    """if(G.firstFind == False):
                        G.firstFind = True
                        automatic = True"""

                    #Funcion para movimientos del dron con respecto al objeto detectadoq

                    with G.XY_locking:
                        if G.STEP == 0:
                            G.XY_mark = (center[0],center[1])
                            G.LAST_X_mark = center[0]
                            G.LAST_Y_mark = center[1]
                            if flag_line:
                                G.XY_line = (center_line[0],center_line[1])
                                G.LAST_X_line = center_line[0]
                                G.LAST_Y_line = center_line[1]
                        elif G.STEP == 1:
                            print ("ENTRA STEP 1")
                            G.XY_line = array_center_line

                        G.vision_var = True
                        G.notFound = False
                    once = False
                else:
                    if G.notFoundActivation:
                        if G.STEP == 0: #prueba
                            G.vision_var = False
                        G.notFound = True
                    if not once:
                        print("NO DETECTA OBJETO")
                        once = True

                # Estatus de la bateria
                bat = G.DRONE.getBattery()[0]
                """if flagTime:
                    print "Bateria: " + str(bat)
                    if automatic:
                        print("Modo: Automatico!")
                    else:
                        print("Modo: MANUAL")
                    print("----------------------------------")
                    print("----------------------------------")
                    print("Viento: OK" if G.DRONE.State[20] == 0 else "Viento: MUCHO VIENTO")
                    print("Motor: OK" if G.DRONE.State[12] == 0 else "Motor: Problem")
                    print("Ultrasonido: OK" if G.DRONE.State[21] == 0 else "Ultrasonido: Problem")
                    print("Magnetometro: OK" if G.DRONE.State[18] == 0 else "Magnetometro: Problem")
                    print("----------------------------------")
                    print("----------------------------------")"""

                """if bat < 15:
                    stop = True
                    print "Bateria Baja: "+str(bat)
                    print("----------------------------------")
                    print("----------------------------------")"""
                # Muestra imagen
                cv2.imshow("DRONE", frame)
                #cv2.imshow("DRONE-tresh", tresh)
                #cv2.imshow("DRONE-erode", erode)
                #cv2.imshow("DRONE-dilate", dilate)
                #cv2.imshow("DRONE-GRAY", tresh)
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
    cv2.destroyAllWindows()
    G.DRONE.land()
    G.JOY.close()
    print "Terminado."
