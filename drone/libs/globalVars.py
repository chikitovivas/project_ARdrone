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
    #global ROUNDEL                                              # La cascade del objeto a detectar
    #ROUNDEL = cv2.CascadeClassifier('/home/chikitovivas/Escritorio/OpenCV/tracking/TrackRoundelBetterBetter/data/cascade.xml')
    global DRONE                                                # El dron
    DRONE = init_drone()                                        # Inicializacion del dron
    #
    global W, H                                            # Weight y Height, Anchura y altura
    W, H = 640, 360
    global SCREENMIDY, SCREENMIDX, DIFF, MX, MY                        # Punto medio en Y, Punto medio en X, Cantidad de circulos
    SCREENMIDX,SCREENMIDY, DIFF, MX, MY = W/2, H/2, H/7, (W/2 * 100) / W, (H/2 * 100) / H
    global RADIUSCENTER                                         # Radio del circulo central de la camara
    RADIUSCENTER = 220
    #
    global FLAG_LEFTX,FLAG_LEFTY,FLAG_RIGHTX,FLAG_RIGHTY        # Banderas
    FLAG_LEFTX,FLAG_LEFTY,FLAG_RIGHTX,FLAG_RIGHTY = False,False,False,False
    global FLAG_MOVEMENT_H,  FLAG_MOVEMENT_V, FLAG_MOVEMENT_F, FLAG_MOVEMENT_G                                       # Bandera de movimiento
    FLAG_MOVEMENT_H,  FLAG_MOVEMENT_V, FLAG_MOVEMENT_F, FLAG_MOVEMENT_G = -1,-1,-1,-1
    #
    global JOY                                                  # El control de xbox
    JOY = xbox.Joystick()
    #
    global LAST_X_mark, LAST_Y_mark, LAST_X_line, LAST_Y_line                                     # Ultimos valores de X y Y
    LAST_X, LAST_Y = 0, 0
    #Variables globales para el movimiento
    global STOP_X,STOP_Y                                        # Banderas de movmiento en X y en Y
    STOP_X,STOP_Y = True,True
    global COLA
    COLA = 0
    global IN_MOVEMENT                                          # Bandera de movimiento
    IN_MOVEMENT = False

    global CENTER, FULL
    CENTER, FULL = [(0,0),(0,0)] , [(0,0),(0,0),(0,0),(0,0)]

    global STEP
    STEP = 1
    global firstFind
    firstFind = False

    global conteo, in_use
    conteo, in_use = 0, False

    global vision_var
    vision_var = False
    global XY_locking
    XY_locking = threading.Lock()
    global XY_mark, XY_line
    XY_mark, XY_line = (0,0), [(0,0),(0,0)]
    global notFound
    notFound = False
    global activation
    activation = False
    global notFoundActivation
    notFoundActivation = False
    #VASO BLANCO
    global H_MIN_V_B,H_MAX_V_B,S_MIN_V_B,S_MAX_V_B,V_MIN_V_B,V_MAX_V_B
    H_MIN_V_B,H_MAX_V_B,S_MIN_V_B,S_MAX_V_B,V_MIN_V_B,V_MAX_V_B = 10, 116, 0, 25, 187, 255

# VIDEO 3: 42,       104,            75, 255,             44, 148
# VIDEO 5: 68,      91,             61, 255,             69, 146
# VIDEO 6: 68,      95,          64, 255,           39, 255
# VIDEO 7: 65,      96,             62, 255,             53, 154
# VIDEO 8: 61,      125,             60, 200,            34, 151
# VIDEO 9: 52,      89,             48, 161,             49, 141
# VIDEO 10: 60,      87,             44, 169,            66, 128
# VIDEO 11: 66,         89,            46, 184,            24, 175
# VIDEO 12: 65,         102,            41, 176,           64, 146
# VIDEO 13: 70,         103,            28, 255,            4, 200
# VIDEO 14: 52,         86,             31, 255,           40, 255
# VIDEO 15: 57,      100,            40, 255,            40, 255
    global H_MIN_1, H_MIN_2, H_MIN_3, H_MIN_4, H_MIN_5, H_MIN_6, H_MIN_7, H_MIN_8, H_MIN_9, H_MIN_10, H_MIN_11, H_MIN_12
    H_MIN_1, H_MIN_2, H_MIN_3, H_MIN_4, H_MIN_5, H_MIN_6, H_MIN_7, H_MIN_8, H_MIN_9, H_MIN_10, H_MIN_11, H_MIN_12, H_MIN_13 = 42, 68, 68, 65, 61, 52, 60, 66, 65, 70, 52, 57, 68

    global H_MAX_1, H_MAX_2, H_MAX_3, H_MAX_4, H_MAX_5, H_MAX_6, H_MAX_7, H_MAX_8, H_MAX_9, H_MAX_10, H_MAX_11, H_MAX_12
    H_MAX_1, H_MAX_2, H_MAX_3, H_MAX_4, H_MAX_5, H_MAX_6, H_MAX_7, H_MAX_8, H_MAX_9, H_MAX_10, H_MAX_11, H_MAX_12, H_MAX_13 = 104, 91, 95, 96, 125, 89, 87, 89, 102, 103, 86, 100, 79

    global S_MIN_1, S_MIN_2, S_MIN_3, S_MIN_4, S_MIN_5, S_MIN_6, S_MIN_7, S_MIN_8, S_MIN_9, S_MIN_10, S_MIN_11, S_MIN_12
    S_MIN_1, S_MIN_2, S_MIN_3, S_MIN_4, S_MIN_5, S_MIN_6, S_MIN_7, S_MIN_8, S_MIN_9, S_MIN_10, S_MIN_11, S_MIN_12, S_MIN_13 = 75, 61, 64, 62, 60, 48, 44, 46, 41, 28, 31, 40, 61,

    global S_MAX_1, S_MAX_2, S_MAX_3, S_MAX_4, S_MAX_5, S_MAX_6, S_MAX_7, S_MAX_8, S_MAX_9, S_MAX_10, S_MAX_11, S_MAX_12
    S_MAX_1, S_MAX_2, S_MAX_3, S_MAX_4, S_MAX_5, S_MAX_6, S_MAX_7, S_MAX_8, S_MAX_9, S_MAX_10, S_MAX_11, S_MAX_12, S_MAX_13 = 255, 255, 255, 255, 200, 161, 169, 184, 176, 255, 255, 255, 255

    global V_MIN_1, V_MIN_2, V_MIN_3, V_MIN_4, V_MIN_5, V_MIN_6, V_MIN_7, V_MIN_8, V_MIN_9, V_MIN_10, V_MIN_11, V_MIN_12
    V_MIN_1, V_MIN_2, V_MIN_3, V_MIN_4, V_MIN_5, V_MIN_6, V_MIN_7, V_MIN_8, V_MIN_9, V_MIN_10, V_MIN_11, V_MIN_12, V_MIN_13 = 44, 69, 39, 53, 34, 49, 66, 24, 64, 4, 40, 40, 29

    global V_MAX_1, V_MAX_2, V_MAX_3, V_MAX_4, V_MAX_5, V_MAX_6, V_MAX_7, V_MAX_8, V_MAX_9, V_MAX_10, V_MAX_11, V_MAX_12
    V_MAX_1, V_MAX_2, V_MAX_3, V_MAX_4, V_MAX_5, V_MAX_6, V_MAX_7, V_MAX_8, V_MAX_9, V_MAX_10, V_MAX_11, V_MAX_12, V_MAX_13 = 148, 146, 255, 154, 151, 141, 128, 175, 146, 200, 255, 255, 111

    global H_MIN_A, H_MAX_A, S_MIN_A, S_MAX_A, V_MIN_A, V_MAX_A
    H_MIN_A, H_MAX_A, S_MIN_A, S_MAX_A, V_MIN_A, V_MAX_A = 5, 28, 40, 192, 120, 214

    #TARGET
    global H_MIN_T,H_MAX_T,S_MIN_T,S_MAX_T,V_MIN_T,V_MAX_T
    H_MIN_T,H_MAX_T,S_MIN_T,S_MAX_T,V_MIN_T,V_MAX_T = 165, 180, 144, 255, 210, 255


def init_drone():
    global DRONE
                        ##############################################################
                        ######### Inicializacion de configuracion del dron. ##########
                        ##############################################################
    #Configuraciones basicas
    DRONE = ps_drone.Drone()                                    # Variable de la libreria del dron
    DRONE.startup()                                             # Coneccion con el dron y los sub-procesos
    DRONE.reset()                                               # Cambiar a estatus de LISTO al dron (Cambiar luces rojas a verde)
    DRONE.reset()
    DRONE.reset()
    while (DRONE.getBattery()[0] == -1):      time.sleep(0.1)   # Esperar hasta que el dron termine de reset()
    print "Battery: "+str(DRONE.getBattery()[0])+"%  "+str(DRONE.getBattery()[1])	# Bateria del dron
    DRONE.useDemoMode(True)                                     # Modo Demo (15 dataset por segundo)
    #Configuracion de video y otros
    DRONE.setConfigAllID()                                      # Modo Multiconfiguracion
    DRONE.setConfig("control:altitude_max", "2500")             # Altitud Maxima
    DRONE.sdVideo()                                             # Resolucion de video (sdVideo() o hdVideo())
    DRONE.groundCam()
    DRONE.frontCam(0)                                            # Camara frontal (frontCam(0) para camara terrestre)
    DRONE.fastVideo()                                           # Velocidad del video
    DRONE.videoFPS(60)                                          # FPS del video
    DRONE.videoBitrate(20000)
    #DRONE.getSelfRotation(5)                                         # Getting value for auto-alteration of gyroscope-sensor
    #print "Auto-alternation: "+str(DRONE.selfRotation)+" dec/sec"    # Showing value for auto-alteration
    DRONE.trim()
    DRONE.trim()                                                # Recalibrar sensores
    DRONE.getSelfRotation(5)
    print "Auto-alternation: "+str(DRONE.selfRotation)+" dec/sec"    # Showing value for auto-alteration
    #Resincronizacion
    CDC = DRONE.ConfigDataCount                                 # Resincronizar el dron con las nuevas configuraciones
    #while CDC == DRONE.ConfigDataCount:       time.sleep(0.0001)# Esperar hasta que este listo (despues de resincronizar esta listo)
    ##############################
    ######### Empezamos ##########
    ##############################
    DRONE.startVideo()                                          # Empezar la funcion de video
    #DRONE.setSpeed(0.1)                                         # Velocidad de los movimientos del dron
    #DRONE.takeoff()                                            # Poner en vuelo al dron
    #while DRONE.NavData["demo"][0][2]:    time.sleep(0.1)      # Wait until the DRONE is really flying (not in landed-mode anymore)

    return DRONE                                                # Se retorna el dron configurado
