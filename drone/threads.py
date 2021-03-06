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
import globalVars as G
import functions as F
import followLine as FL
#import followLineFPS as FL
G.init()
running = True

def controller():
    once = False
    global running
    automatic = False
    print("DESPEGANDO..")
    if sys.argv[1].lower() == '-real':
        G.DRONE.takeoff()
        time.sleep(5)
        G.DRONE.mtrim()
        while G.activation == False or G.DRONE.State[0] == 0:
            var = 2

    #Loop hasta que encuentre el objeto
    print "--------------------------"
    print "     BUSCANDO OBJETO      "
    print "--------------------------"

    while(running):
        automatic = F.controller(automatic)
        if G.vision_var and automatic:
            #F.followLineSpin()
            #F.followLineSpinContinuos()
            F.followLineSpinContinuosNOSTOP()
            once = False
        if G.JOY.Back():   running =   False

    print("Terminando hilo de control....")

def vision():
    FL.run()

    print("Terminando hilo de vision....")


def main():
    global running
    controlt = threading.Thread(target=controller)
    visiont = threading.Thread(target=vision)

    controlt.start()
    visiont.start()

    while running:
        if G.JOY.Back():   running =   False
        #if cv2.waitKey(1) & 0xFF == ord('q'):   running =   True

    controlt.join()
    visiont.join()

    print "Terminando Ejecucion.."

if __name__ == '__main__':
	main()
