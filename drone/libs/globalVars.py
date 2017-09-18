                                ######################################
                                ############# IMPORTS ################
                                ######################################
import time, sys
import threading
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron')
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron/drone/libs')
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron/drone/libs/XboxController')
import ps_drone
import xbox
import cv2
import numpy as np
#roundel_40x40 = cv2.CascadeClassifier('../../../../Escritorio/OpenCV/tracking/TrackRoundelBetter/data/cascade.xml')
#roundel_40x40 = cv2.CascadeClassifier('../../../../Escritorio/OpenCV/tracking/TrackRoundelGreen/data/cascade.xml')
#roundel_40x40 = cv2.CascadeClassifier('CascadeRoundelBest/data/cascade.xml')



def init():
    global ROUNDEL                                              # La cascade del objeto a detectar
    ROUNDEL = cv2.CascadeClassifier('/home/chikitovivas/Escritorio/OpenCV/tracking/TrackRoundelBetterBetter/data/cascade.xml')
    global DRONE                                                # El dron
    DRONE = init_drone()                                        # Inicializacion del dron
    #
    global W, H                                                 # Weight y Height, Anchura y altura
    W, H = 640, 360
    global SCREENMIDY, SCREENMIDX, DIFF                         # Punto medio en Y, Punto medio en X, Cantidad de circulos
    SCREENMIDX,SCREENMIDY, DIFF = W/2, H/2, H/7
    global RADIUSCENTER                                         # Radio del circulo central de la camara
    RADIUSCENTER = 50
    #
    global FLAG_LEFTX,FLAG_LEFTY,FLAG_RIGHTX,FLAG_RIGHTY        # Banderas
    FLAG_LEFTX,FLAG_LEFTY,FLAG_RIGHTX,FLAG_RIGHTY = False,False,False,False
    global FLAG_MOVEMENT                                        # Bandera de movimiento
    FLAG_MOVEMENT = 0
    #
    global JOY                                                  # El control de xbox
    JOY = xbox.Joystick()
    #
    global LAST_X, LAST_Y                                       # Ultimos valores de X y Y
    LAST_X, LAST_Y = 0, 0
    #Variables globales para el movimiento
    global STOP_X,STOP_Y                                        # Banderas de movmiento en X y en Y
    STOP_X,STOP_Y = True,True
    global COLA
    COLA = 0
    global IN_MOVEMENT                                          # Bandera de movimiento
    IN_MOVEMENT = False

    global STEP
    STEP = 0

    global vision_var
    vision_var = False
    global XY_locking
    XY_locking = threading.Lock()
    global XY
    XY = (0,0)
    global notFound
    notFound = False


def init_drone():
    global DRONE
                        ##############################################################
                        ######### Inicializacion de configuracion del dron. ##########
                        ##############################################################
    #Configuraciones basicas
    DRONE = ps_drone.Drone()                                    # Variable de la libreria del dron
    DRONE.startup()                                             # Coneccion con el dron y los sub-procesos
    DRONE.reset()                                               # Cambiar a estatus de LISTO al dron (Cambiar luces rojas a verde)
    while (DRONE.getBattery()[0] == -1):      time.sleep(0.1)   # Esperar hasta que el dron termine de reset()
    print "Battery: "+str(DRONE.getBattery()[0])+"%  "+str(DRONE.getBattery()[1])	# Bateria del dron
    DRONE.useDemoMode(True)                                     # Modo Demo (15 dataset por segundo)
    #Configuracion de video y otros
    DRONE.setConfigAllID()                                      # Modo Multiconfiguracion
    DRONE.setConfig("control:altitude_max", "2500")             # Altitud Maxima
    DRONE.sdVideo()                                             # Resolucion de video (sdVideo() o hdVideo())
    DRONE.groundCam(0)
    DRONE.frontCam()                                            # Camara frontal (frontCam(0) para camara terrestre)
    DRONE.fastVideo()                                           # Velocidad del video
    DRONE.videoFPS(60)                                          # FPS del video
    #DRONE.getSelfRotation(5)                                         # Getting value for auto-alteration of gyroscope-sensor
    #print "Auto-alternation: "+str(DRONE.selfRotation)+" dec/sec"    # Showing value for auto-alteration
    DRONE.trim()                                                # Recalibrar sensores
    #Resincronizacion
    CDC = DRONE.ConfigDataCount                                 # Resincronizar el dron con las nuevas configuraciones
    #while CDC == DRONE.ConfigDataCount:       time.sleep(0.0001)# Esperar hasta que este listo (despues de resincronizar esta listo)
    ##############################
    ######### Empezamos ##########
    ##############################
    DRONE.startVideo()                                          # Empezar la funcion de video
    DRONE.setSpeed(0.1)                                         # Velocidad de los movimientos del dron
    #DRONE.takeoff()                                            # Poner en vuelo al dron
    #while DRONE.NavData["demo"][0][2]:    time.sleep(0.1)      # Wait until the DRONE is really flying (not in landed-mode anymore)

    return DRONE                                                # Se retorna el dron configurado
