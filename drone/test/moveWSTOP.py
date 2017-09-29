import time, sys
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron/drone/libs')
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron/')
import ps_drone

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
#DRONE.startVideo()                                          # Empezar la funcion de video
#DRONE.setSpeed(0.1)                                         # Velocidad de los movimientos del dron
DRONE.takeoff()                                            # Poner en vuelo al dron
while DRONE.NavData["demo"][0][2]:    time.sleep(0.1)      # Wait until the DRONE is really flying (not in landed-mode anymore)

print("Moviendo hacia adelante")
DRONE.move(0,0.1,0,0)
time.sleep(2)
DRONE.stop()
print("Moviendo hacia adelante y girando hacia la derecha")
DRONE.move(0,0.1,0,0.1)
time.sleep(2)
DRONE.stop()
print("Moviendo hacia adelante y girando hacia la izquierda")
DRONE.move(0,0.1,0,-0.1)
time.sleep(2)
DRONE.stop()
print("Moviendo hacia adelante")
DRONE.move(0,0.1,0,0)
time.sleep(2)
DRONE.land()
