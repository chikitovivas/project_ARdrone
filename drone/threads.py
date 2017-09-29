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
running = True

def controller():
    once = False
    global running

    while(running):
        if G.vision_var:
            with G.XY_locking:
                if(G.STEP == 0):
                    F.followBottom(G.XY[0],G.XY[1])
                elif(G.STEP == 1):
                    F.followLineSpin(G.XY[0],G.XY[1])  
                G.XY = (0,0)
                G.vision_var = False
            once = False
        elif G.notFound:
            F.stopMovementBottom()
            G.notFound = False

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
