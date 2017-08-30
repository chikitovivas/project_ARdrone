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
def main():
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

    #cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture("Video.avi")
    #Mientras no se mande a parar
    while not stop :
        flagTime,seconds = F.timePass(flagTime,seconds)
        automatic = F.controller(automatic)                     #Valor de automatic, cuando se da el boton START, cambia el valor
        try:
            # Leyendo frames del video del dron
            frameFirst = G.DRONE.VideoImage                     #Leyendo frames del dron
            if not(frameFirst is None):
                #_,frameFirst = cap.read()
                frame = cv2.resize(frameFirst, (G.W, G.H))      #Cambiar tamano al frame


                # Conversion de los frames a tono de grises
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #Gris al frame

                #test
                #edges = cv2.Canny(frame,100,200)
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)     #Filtro
                _,tresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)    #Filtro de blanco y negro
                cv2.imshow("tresh", tresh)                      #Se muestra el filtro blanco y negro

                # Creacion de los circulos de velocidad
                for i in range(1, 5):
                    cv2.circle(frame, (G.SCREENMIDX, G.SCREENMIDY), G.DIFF*i,(0,0,255),2) ##(,(),G.RADIUSCENTER,(),)
                    
                if G.STEP == 0:
                    frame,center,flag = F.draw(frame,tresh)         #Se manda a dibujar sobre el objeto detectado
                elif G.STEP == 1:
                    frame,center,flag = F.drawLine(frame,tresh)         #Se manda a dibujar sobre el objeto detectado

                #Si se detecta algo
                if flag:
                    # Centro del objeto
                    x1 = center[0]
                    y1 = center[1]

                    acum_x += x1
                    acum_y += y1
                    cantidad += 1
                    #hort_speed, vert_speed = calculationSpeed(center) # NO CREO USAR
                    if flagTime:
                        print("X: " + str(x1))
                        print("Y: " + str(y1))
                        print("---------------")
                        once = True

                    #Funcion para movimientos del dron con respecto al objeto detectadoq
                    #followFront(x1,y1)
                    if automatic and flagTime:
                        if ((x1 > prom_x - 30) and (x1 < prom_x + 30)) and ((y1 > prom_y - 30) and (y1 < prom_y + 30)):
                            if G.STEP == 0:
                                F.followFront(prom_x,prom_y)
                            elif G.STEP == 1:
                                #Seguimiento de la linea, reconocimiento
                                G.DRONE.stop()
                                G.DRONE.land()
                                #F.followLine(prom_x,prom_y)
                        #else:
                        #    F.followFront(x1,y1)
                        #F.followFront(prom_x,prom_y)
                        cantidad = 0
                        acum_x = 0
                        acum_y = 0
                        #F.followBottom(x1,y1)
                        #time.sleep(0.0001)
                    elif automatic and not flagTime:
                        prom_x,prom_y = F.promediar(acum_x,acum_y,cantidad)
                    once = False
                else:
                    if not once:
                        print("NO DETECTA OBJETO")
                        once = True

                    if automatic:
                        G.DRONE.stop()
                        #F.stopMovementFront()                      #Si se pierde el objeto detectado
                        #F.stopMovementBottom()                    #Si se pierde el objeto detectado

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
                #print("DRONE State:"+ str(DRONE.State))
                #print("Angular speed control:"+ str(DRONE.State[3]))
                #print("Altitude control active:"+ str(DRONE.State[4]))
                #if(DRONE.State[20]):        print("MUCHO VIENTO!")
                #print("Demo - Altitude: " +str(G.DRONE.NavData["demo"][3]))

                if bat < 12:
                    stop = True
                    print "Bateria Baja: "+str(bat)
                    print("----------------------------------")
                    print("----------------------------------")
                # Guarda imagen en video
                #out.write(frame)
                # Muestra imagen
                cv2.imshow("DRONE", frame)
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

#def searchingObject():
#    print "DRONE turns 120 degree to the left"
#    DRONE.turnAngle(-120,0.1,1)                                   # Turn 120 deg to the left, full speed, accuracy of 1 deg
    #time.sleep(1)

if __name__ == '__main__':
	main()
