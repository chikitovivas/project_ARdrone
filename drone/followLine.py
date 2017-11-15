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
import math
import numpy as np
import globalVars as G
import functions as F

#Guardar Video
#CODEC = cv2.cv.CV_FOURCC('D','I','V','3') # MPEG 4.3
#out = cv2.VideoWriter('output.avi',CODEC, 10.0, (640,480))

def run():
    #Variables adicionales
    waiting = 0
    stop =   False
    flagTime = False
    seconds = time.localtime().tm_sec
    once = True
    kernel = np.ones((3,3   ),np.uint8)
    cap = cv2.VideoCapture("Videos/Video9.avi")

    #Mientras no se mande a parar
    while not stop :
        #time.sleep(0.01)
        flagTime,seconds = F.timePass(flagTime,seconds)
        try:
            # Leyendo frames del video del dron
            frameFirst = G.DRONE.VideoImage                     #Leyendo frames del dron
            if len(sys.argv) < 3 or sys.argv[1].lower() != '-real':
                _,frameFirst = cap.read()
            if not(frameFirst is None):
                G.activation = True
                frame = cv2.resize(frameFirst, (G.W, G.H))      #Cambiar tamano al frame
                blurred = cv2.GaussianBlur(frame, (5, 5), 0)
                HSV = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

                mask = cv2.inRange(HSV, np.array([G.H_MIN_V_B,G.S_MIN_V_B,G.V_MIN_V_B]), np.array([G.H_MAX_V_B,G.S_MAX_V_B,G.V_MAX_V_B]))
                output = cv2.bitwise_and(frame, frame, mask = mask)

                erode = cv2.erode(blurred, kernel, iterations=2)
                dilate = cv2.dilate(erode, kernel, iterations=5)

                gray = cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY)
                _,tresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)    #Filtro de blanco y negro

                tresh_vasos = [tresh[(G.H/3):2*(G.H/3),0:G.W]]
                frame = F.detection(frame,tresh_vasos)         #Vasos a detectar

                if sys.argv[len(sys.argv) - 1].lower() == 'noche':
                    mask = cv2.inRange(HSV, np.array([G.H_MIN_A_NOCHE,G.S_MIN_A_NOCHE,G.V_MIN_A_NOCHE]), np.array([G.H_MAX_A_NOCHE,G.S_MAX_A_NOCHE,G.V_MAX_A_NOCHE]))
                    output = cv2.bitwise_and(frame, frame, mask = mask)

                    erode = cv2.erode(output, kernel, iterations=1)
                    opening = cv2.morphologyEx(erode, cv2.MORPH_OPEN, kernel)

                    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
                    dilate = cv2.dilate(opening, kernel, iterations=5)

                    gray = cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY)
                    _,tresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)    #Filtro de blanco y negro
                    edges = cv2.Canny(tresh,20,100)

                elif sys.argv[len(sys.argv) - 1].lower() == 'amarillo':
                    mask = cv2.inRange(HSV, np.array([G.H_MIN_A,G.S_MIN_A,G.V_MIN_A]), np.array([G.H_MAX_A,G.S_MAX_A,G.V_MAX_A]))
                    output = cv2.bitwise_and(frame, frame, mask = mask)

                    erode = cv2.erode(output, kernel, iterations=1)
                    opening = cv2.morphologyEx(erode, cv2.MORPH_OPEN, kernel)

                    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
                    dilate = cv2.dilate(opening, kernel, iterations=5)

                    gray = cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY)
                    _,tresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)    #Filtro de blanco y negro
                    edges = cv2.Canny(tresh,20,100)

                elif sys.argv[len(sys.argv) - 1].lower() == 'rojo':
                    print 'red'
                else:
                    print 'Introduce valores de parametros (1), Verde, Amarillo o Rojo'
                    stop = True

                frame, full, flag = F.drawLineCHANGE(frame,edges)

                #Si se detecta algo
                if flag:
                    #Funcion para movimientos del dron con respecto al objeto detectadoq
                    with G.XY_locking:

                        G.FULL = full

                        G.vision_var = True

                    once = False
                else:

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
                #cv2.imshow("frame", edges)
                #cv2.imshow("blurred", blurred)
                #cv2.imshow("DRONE-tresh", gray)
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
    print("VASOS CONTADOS: " + str(G.conteo))
    print "Aterrizando..."
    #out.release()
    cv2.destroyAllWindows()
    G.DRONE.land()
    G.DRONE.shutdown()
    G.JOY.close()
    print "Terminado."
