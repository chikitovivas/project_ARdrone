import time, sys
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron')
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron/drone/libs/XboxController')
import numpy as nptest
import cv2
import ps_drone
import xbox

##############################################################
######### Inicializacion de configuracion del dron. ##########
##############################################################
#Configuraciones basicas
drone = ps_drone.Drone()                                    # Variable de la libreria del dron
drone.startup()                                             # Coneccion con el dron y los sub-procesos
drone.reset()                                               # Cambiar a estatus de LISTO al dron (Cambiar luces rojas a verde)
while (drone.getBattery()[0] == -1):      time.sleep(0.1)   # Esperar hasta que el dron termine de reset()
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])	# Bateria del dron
drone.useDemoMode(True)                                     # Modo Demo (15 dataset por segundo)
#Configuracion de video y otros
drone.setConfigAllID()                                      # Modo Multiconfiguracion
#drone.setConfig("control:altitude_max", "2500")             # Altitud Maxima
drone.sdVideo()                                             # Resolucion de video (sdVideo() o hdVideo())
drone.groundCam(0)
drone.frontCam()                                           # Camara frontal (frontCam(0) para camara terrestre)
drone.fastVideo()                                           # Velocidad del video
drone.videoFPS(60)                                          # FPS del video
#drone.getSelfRotation(5)                                         # Getting value for auto-alteration of gyroscope-sensor
#print "Auto-alternation: "+str(drone.selfRotation)+" dec/sec"    # Showing value for auto-alteration
drone.trim()                                                # Recalibrar sensores
#Resincronizacion
CDC = drone.ConfigDataCount                                 # Resincronizar el dron con las nuevas configuraciones
#while CDC == drone.ConfigDataCount:       time.sleep(0.0001)# Esperar hasta que este listo (despues de resincronizar esta listo)
##############################
######### Empezamos ##########
##############################
drone.startVideo()                                          # Empezar la funcion de video

CODEC = cv2.cv.CV_FOURCC('D','I','V','X') # MPEG-4 = MPEG-1
#Xbox Controller
joy = xbox.Joystick()
W, H = 640, 360
FLAG_LEFTX = False
FLAG_LEFTY = False
FLAG_RIGHTX = False
FLAG_RIGHTY = False

def savingVideo():
    stop = False
    automatic = False
    recording = False
    cont = 0
    #drone.takeoff()
    #cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture("Video.avi")
    # Define the codec and create VideoWriter object
    out = cv2.VideoWriter('Video3.avi',CODEC, 60.0, (640,360))
    out1 = cv2.VideoWriter('Video4.avi',CODEC, 60.0, (640,360))
    out2 = cv2.VideoWriter('Video5.avi',CODEC, 60.0, (640,360))
    out3 = cv2.VideoWriter('Video6.avi',CODEC, 60.0, (640,360))
    out4 = cv2.VideoWriter('Video7.avi',CODEC, 60.0, (640,360))
    #.0.avi',CODEC, 60.0, (640,360))
    while not stop :
        automatic = controller(automatic)
        if joy.A():
            time.sleep(0.5)
            if recording:
                recording = False
                cont += 1
            else:
                recording = True
        if joy.B():
            time.sleep(0.5)
            drone.groundCam()
        if joy.Y():
            time.sleep(0.5)
            drone.frontCam()
        try:
            # Leyendo frames del video del dron
            frameFirst = drone.VideoImage
            #_,frameFirst = cap.read()
            if not(frameFirst is None):
                #frame = cv2.resize(frameFirst, (W, H))
                print("Demo - Altitude: " +str(drone.NavData["demo"][3]))

                if recording:
                    print("RECORDING video-" + str(cont))
                    if cont == 0:
                        out.write(frameFirst)
                    elif cont == 1:
                        out1.write(frameFirst)
                    elif cont == 2:
                        out2.write(frameFirst)
                    elif cont == 3:
                        out3.write(frameFirst)
                    elif cont == 4:
                        out4.write(frameFirst)
                else:
                    print("No recording")

                cv2.imshow("Drone", frameFirst)

        except Exception as e:
            print "Error: " + str(e)
            print "Failed"

        if cv2.waitKey(1) & 0xFF == ord('q'):   stop =   True
        if joy.Back():   stop =   True

    # Release everything if job is finished
    out.release()
    out1.release()
    out2.release()
    out3.release()
    out4.release()
    drone.land()
    cv2.destroyAllWindows()
    joy.close()

def showingVideo():
    stop = False
    cap = cv2.VideoCapture("Video6.avi")

    while not stop :
        try:
            _,frameFirst = cap.read()
            if not(frameFirst is None):
                cv2.imshow("Drone", frameFirst)
            else:
                stop = True

        except Exception as e:
            print "Error: " + str(e)
            print "Failed"

        if cv2.waitKey(1) & 0xFF == ord('q'):   stop =   True

    # Release everything if job is finished
    cv2.destroyAllWindows()

def controller(automatic):
    global FLAG_LEFTX
    global FLAG_LEFTY
    global FLAG_RIGHTX
    global FLAG_RIGHTY

    if joy.Start():
        print("START")
        if automatic:
            return False
        else:
            return True
    else:
        #Para entrar en movimiento con el control, automatico debe estar desactivado
        if(not automatic):
            #Palanca izquierda del control
            #EJE X
            if(joy.leftX()):
                if(joy.leftX() < -0.900):
                    drone.moveLeft()
                    print("Moviendo Izquierda")
                    FLAG_LEFTX = True
                elif(joy.leftX() > 0.900):
                    drone.moveRight()
                    print("Moviendo Derecha")
                    FLAG_LEFTX = True
                elif (FLAG_LEFTX == True) and (joy.leftX() > -0.900) and (joy.leftX() < 0.900):
                    print("Deteniendo movimiento por movimiento de palanca (Izquierda-Derecha)")
                    drone.stop()
                    FLAG_LEFTX = False
            elif FLAG_LEFTX:
                print("Deteniendo movimiento por captar otro tipo de movimiento (Izquierda-Derecha)")
                drone.stop()
                FLAG_LEFTX = False

            #EJE Y
            if(joy.leftY()):
                if(joy.leftY() < -0.900):
                    drone.moveBackward()
                    print("Moviendo hacia Atras")
                    FLAG_LEFTY = 1
                elif(joy.leftY() > 0.900):
                    drone.moveForward()
                    print("Moviendo hacia Adelante")
                    FLAG_LEFTY = 1
                elif (FLAG_LEFTY) and (joy.leftY() > -0.900) and (joy.leftY() < 0.900):
                    print("Deteniendo movimiento por movimiento de palanca (Adelante-Atras)")
                    drone.stop()
                    FLAG_LEFTY = 0
            elif FLAG_LEFTY:
                print("Deteniendo movimiento por captar otro tipo de movimiento (Adelante-Atras)")
                drone.stop()
                FLAG_LEFTY = 0

            #Palanca derecha del control
            #EJE X
            if(joy.rightX()):
                if(joy.rightX() < -0.900):
                    drone.turnLeft()
                    print("Rotacion hacia izquierda")
                    FLAG_RIGHTX = 1
                elif(joy.rightX() > 0.900):
                    print("Rotacion hacia derecha")
                    drone.turnRight()
                    FLAG_RIGHTX = 1
                elif (FLAG_RIGHTX) and (joy.rightX() > -0.900) and (joy.rightX() < 0.900):
                    print("Deteniendo ROTACION por movimiento de palanca (Izquierda-Derecha)")
                    drone.stop()
                    FLAG_RIGHTX = 0
            elif FLAG_RIGHTX:
                print("Deteniendo ROTACION por captar otro tipo de movimiento (Izquierda-Derecha)")
                drone.stop()
                FLAG_RIGHTX = 0

            #EJE Y
            if(joy.rightY()):
                if(joy.rightY() < -0.900):
                    print("Bajando")
                    drone.moveDown(0.6)
                    FLAG_RIGHTY = True
                elif(joy.rightY() > 0.900):
                    print("Subiendo")
                    drone.moveUp(0.6)
                    FLAG_RIGHTY = True
                elif (FLAG_RIGHTY) and (joy.rightY() > -0.900) and (joy.rightY() < 0.900):
                    print("Deteniendo movimiento por movimiento de palanca (Arriba-Abajo)")
                    drone.stop()
                    FLAG_RIGHTY = False
            elif FLAG_RIGHTY:
                print("Deteniendo movimiento por captar otro tipo de movimiento (Arriba-Abajo)")
                drone.stop()
                FLAG_RIGHTY = False

        #Retorna misma condicion de modo automatico
        return automatic

savingVideo()
#showingVideo()
