import time, sys
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron')
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron/drone/libs')
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron/drone/libs/XboxController')
import ps_drone
import xbox
import cv2
import numpy as np
import globalVars as G


def controller(automatic):

    if G.JOY.Start():                                       # Si se le da al boton START
        print("START")
        if automatic:
            return False                                    #Retorna MANUAL
        else:
            return True                                     #Retorna AUTOMATICO
    else:
        #Para entrar en movimiento con el control, automatico debe estar desactivado
        if(not automatic):
            #Palanca izquierda del control
            #EJE X
            if(G.JOY.leftX()):
                if(G.JOY.leftX() < -0.900):                 # Palanca izquierda hacia la izquierda
                    G.DRONE.moveLeft()
                    print("Moviendo Izquierda")
                    G.FLAG_LEFTX = True
                elif(G.JOY.leftX() > 0.900):                # Palanca izquierda hacia la derecha
                    G.DRONE.moveRight()
                    print("Moviendo Derecha")
                    G.FLAG_LEFTX = True
                elif (G.FLAG_LEFTX == True) and (G.JOY.leftX() > -0.900) and (G.JOY.leftX() < 0.900):   #Palanca izquierda paro
                    print("Deteniendo movimiento por movimiento de palanca (Izquierda-Derecha)")
                    G.DRONE.stop()
                    G.FLAG_LEFTX = False
            elif G.FLAG_LEFTX:                              # Palanca izquierda paro por captar otro tipo de movimiento
                print("Deteniendo movimiento por captar otro tipo de movimiento (Izquierda-Derecha)")
                G.DRONE.stop()
                G.FLAG_LEFTX = False

            #EJE Y
            if(G.JOY.leftY()):
                if(G.JOY.leftY() < -0.900):                 #Palanca izquierda hacia abajo
                    G.DRONE.moveBackward()
                    print("Moviendo hacia Atras")
                    G.FLAG_LEFTY = 1
                elif(G.JOY.leftY() > 0.900):                #Palanca izquierda hacia arriba
                    G.DRONE.moveForward()
                    print("Moviendo hacia Adelante")
                    G.FLAG_LEFTY = 1
                elif (G.FLAG_LEFTY) and (G.JOY.leftY() > -0.900) and (G.JOY.leftY() < 0.900):   #Palanca izquierda paro
                    print("Deteniendo movimiento por movimiento de palanca (Adelante-Atras)")
                    G.DRONE.stop()
                    G.FLAG_LEFTY = 0
            elif G.FLAG_LEFTY:                              #Palanca izquierda paro por otro movimiento
                print("Deteniendo movimiento por captar otro tipo de movimiento (Adelante-Atras)")
                G.DRONE.stop()
                G.FLAG_LEFTY = 0

            #Palanca derecha del control
            #EJE X
            if(G.JOY.rightX()):
                if(G.JOY.rightX() < -0.900):                #Palanca derecha hacia la izquierda
                    G.DRONE.turnLeft()
                    print("Rotacion hacia izquierda")
                    G.FLAG_RIGHTX = 1
                elif(G.JOY.rightX() > 0.900):
                    print("Rotacion hacia derecha")         #Palanca derecha hacia la izquierda
                    G.DRONE.turnRight()
                    G.FLAG_RIGHTX = 1
                elif (G.FLAG_RIGHTX) and (G.JOY.rightX() > -0.900) and (G.JOY.rightX() < 0.900):
                    print("Deteniendo ROTACION por movimiento de palanca (Izquierda-Derecha)")      #Palanca derecha pato
                    G.DRONE.stop()
                    G.FLAG_RIGHTX = 0
            elif G.FLAG_RIGHTX:                             #Palanca derecha paro por otro movimiento
                print("Deteniendo ROTACION por captar otro tipo de movimiento (Izquierda-Derecha)")
                G.DRONE.stop()
                G.FLAG_RIGHTX = 0

            #EJE Y
            if(G.JOY.rightY()):                             #Palanca derecha hacia arriba
                if(G.JOY.rightY() < -0.900):
                    print("Bajando")
                    G.DRONE.moveDown(0.6)
                    G.FLAG_RIGHTY = True
                elif(G.JOY.rightY() > 0.900):               #Palanca derecha hacia abajo
                    print("Subiendo")
                    G.DRONE.moveUp(0.6)
                    G.FLAG_RIGHTY = True
                elif (G.FLAG_RIGHTY) and (G.JOY.rightY() > -0.900) and (G.JOY.rightY() < 0.900):    #Palanca derecha paro
                    print("Deteniendo movimiento por movimiento de palanca (Arriba-Abajo)")
                    G.DRONE.stop()
                    G.FLAG_RIGHTY = False
            elif G.FLAG_RIGHTY:                             #Palanca derecha paro por otro movimiento
                print("Deteniendo movimiento por captar otro tipo de movimiento (Arriba-Abajo)")
                G.DRONE.stop()
                G.FLAG_RIGHTY = False

        #Retorna misma condicion de modo automatico
        return automatic                                    #Retorna valor de automatic

"""def draw(frame, gray):
    roundel = G.ROUNDEL.detectMultiScale(gray, 1.20, 50, 0, (20,20))
    #Video = 1.31
    #Video1 = 1.25
    #Video2 = 1.37
    # Para cada deteccion se obtendran los puntos de coordenadas
    for (x,y,w,h) in roundel:
        #Creando el rectangulo
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)

        # El centro del rectangulo
        x_center = int(w/2) + x
        y_center = int(h/2) + y

        # El punto mas lejano entre los puntos medios del rectangulo
        x_far = x_center - x
        y_far = y_center - y

        center = (x_center,y_center)                        # El centro del rectangulo ahora sera el centro del circulo

        radius = int(x_far)                                 # El radio del circulo
        # Creando el circulo
        cv2.circle(frame,center,radius,(255,0,255),2)

        # Creando la linea apuntando el centro del rectangulo y el circulo
        cv2.line(frame, (G.SCREENMIDX, G.SCREENMIDY), center, (0,0,255),2)

        return (frame,center,1)
    return (frame,None,0)"""
def draw(frame, dilate):
    #DETECTAR LINEA y retornar coordenadas
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt = findLargerContour(contours)
    #cv2.drawContours(frame,cnt, -1, (0, 255, 0), 5)
    if cnt != []:
        cv2.drawContours(frame,cnt, -1, (0, 255, 0), 5)

        M = cv2.moments(cnt)
        if  M['m00'] != 0:
            x_center = int(M['m10']/M['m00'])
            y_center = int(M['m01']/M['m00'])
            for i in range(1, 5):
                cv2.circle(frame, (G.SCREENMIDX, G.SCREENMIDY), G.DIFF*i,(0,255,0),2) ##(,(),G.RADIUSCENTER,(),)

            cv2.line(frame, (G.SCREENMIDX, G.SCREENMIDY), (x_center,y_center), (0,255,0),2)
            cv2.circle(frame,(x_center, y_center),1,(0,0,255),1)

            center = (x_center,y_center)

            return (frame,center,True)
    else:
        return  (frame,None,False)

def drawLine(frame, dilate):
    #DETECTAR LINEA y retornar coordenadas
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt = findLargerContour(contours)
    #cv2.drawContours(frame,cnt, -1, (0, 255, 0), 5)
    if cnt != []:
        M = cv2.moments(cnt)
        if  M['m00'] != 0:
            x_center = int(M['m10']/M['m00'])
            y_center = int(M['m01']/M['m00'])

            for i in range(1, 5):
                cv2.circle(frame, (G.SCREENMIDX, G.SCREENMIDY), G.DIFF*i,(0,255,0),2) ##(,(),G.RADIUSCENTER,(),)

            cv2.line(frame, (G.SCREENMIDX, G.SCREENMIDY), (x_center,y_center), (0,255,0),2)
            cv2.circle(frame,(x_center, y_center),1,(0,0,255),1)

            center = (x_center,y_center)

            return (frame,center,True)
    else:
        return (frame,None,False)


def followBottom(center_x, center_y):
    doneHorizontal = False
    doneVertical = False
    timeS = 1

    #EJE DE LAS X
    if (G.SCREENMIDX - G.RADIUSCENTER) < center_x < (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT != 0:   # Si el objeto esta en el centro
        G.DRONE.stop()
        G.FLAG_MOVEMENT = 0
        doneHorizontal = True
        print "DETENER (Izquierda - Derecha)"

    # En el eje de las x (Horizontal) -> Note: Inverse
    elif center_x > (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT != 1:                  # Si el objeto esta a la derecha del centro
        G.DRONE.moveRight()
        G.FLAG_MOVEMENT = 1
        doneHorizontal = False

    elif center_x < (G.SCREENMIDX - G.RADIUSCENTER) and G.FLAG_MOVEMENT != 2:                   # Si el objeto esta a la izquierda del centro
        G.DRONE.moveLeft()
        G.FLAG_MOVEMENT = 2
        doneHorizontal = False

    if G.FLAG_MOVEMENT == 1:
        print("DERECHA")
    elif G.FLAG_MOVEMENT == 2:
        print("IZQUIERDA")
    #elif G.FLAG_MOVEMENT == 0:
    #    print("NO HAY MOVIMIENTO")

    #EJE DE LAS Y
    if (G.SCREENMIDY - G.RADIUSCENTER) < center_y < (G.SCREENMIDY + G.RADIUSCENTER) and G.FLAG_MOVEMENT != 10 and doneHorizontal:   # Si el objeto esta en el centro
        G.DRONE.stop()
        G.FLAG_MOVEMENT = 10
        doneVertical = True
        print "DETENER (Al frente - Hacia atras)"

    # En el eje de las Y (Vertical)
    elif center_y < (G.SCREENMIDY - G.RADIUSCENTER) and G.FLAG_MOVEMENT != 3 and doneHorizontal:                  # Si el objeto esta por Arriba del centro
        G.DRONE.moveUp()
        G.FLAG_MOVEMENT = 3

    elif center_y > (G.SCREENMIDY + G.RADIUSCENTER) and G.FLAG_MOVEMENT != 4 and doneHorizontal:                   # Si el objeto esta por debajo del centro
        G.DRONE.moveDown()
        G.FLAG_MOVEMENT = 4

    if G.FLAG_MOVEMENT == 3:
        print("HACIA EL FRENTE")
    elif G.FLAG_MOVEMENT == 4:
        print("HACIA ATRAS")
    #elif G.FLAG_MOVEMENT == 0:
    #    print("NO HAY MOVIMIENTO")

    G.LAST_X = center_x
    G.LAST_Y = center_y

    print (str(doneVertical))
    print (str(doneHorizontal))

    #Cambio de funcionalidad
    if(doneVertical and doneHorizontal):
        print("Entra")
        G.STEP = 1

def stopMovementBottom():

    if G.LAST_X != 0 and G.LAST_Y != 0:

        if G.LAST_X > (G.SCREENMIDX + G.RADIUSCENTER):                  # Si el objeto esta a la derecha del centro
            G.DRONE.moveRight()
            print("Buscando DERECHA")
            time.sleep(0.1)
            G.DRONE.stop()

        elif G.LAST_X < (G.SCREENMIDX - G.RADIUSCENTER):                # Si el objeto esta a la izquierda del centro
            G.DRONE.moveLeft()
            print("Buscando IZQUIERDA")
            time.sleep(0.1)
            G.DRONE.stop()

        if G.LAST_Y < (G.SCREENMIDY - G.RADIUSCENTER):                  # Si el objeto esta por encima del centro
            G.DRONE.moveForward()
            print("Buscando POR DELANTE")
            time.sleep(0.1)
            G.DRONE.stop()

        elif G.LAST_Y > (G.SCREENMIDY + G.RADIUSCENTER):                # Si el objeto esta por debajo del centro
            G.DRONE.moveBackward()
            print("Buscando POR ATRAS")
            time.sleep(0.1)
            G.DRONE.stop()

        print("Buscando...")
        print("======================")
    else:
        print("NUNCA HE DETECTADO ALGO")

def stopMovementFront():

    if G.LAST_X != 0 and G.LAST_Y != 0:

        if G.LAST_X > (G.SCREENMIDX + G.RADIUSCENTER):                  # Si el objeto esta a la derecha del centro
            G.DRONE.moveRight()
            print("Buscando DERECHA")
            time.sleep(0.1)
            G.DRONE.stop()

        elif G.LAST_X < (G.SCREENMIDX - G.RADIUSCENTER):                   # Si el objeto esta a la izquierda del centro
            G.DRONE.moveLeft()
            print("Buscando IZQUIERDA")
            time.sleep(0.1)
            G.DRONE.stop()

        if G.LAST_Y < (G.SCREENMIDY - G.RADIUSCENTER):                  # Si el objeto esta por debajo del centro
            G.DRONE.moveUp()
            print("Buscando POR ARRIBA")
            time.sleep(0.1)
            G.DRONE.stop()

        elif G.LAST_Y > (G.SCREENMIDY + G.RADIUSCENTER):                   # Si el objeto esta por encima del centro
            G.DRONE.moveDown()
            print("Buscando POR ABAJO")
            time.sleep(0.1)
            G.DRONE.stop()

        print("Buscando...")
        print("======================")

def calculationSpeed(center): #NO CREO USAR
    # Centro del objeto
    x1 = center[0]
    y1 = center[1]
    #Calculo de velocidad necesaria para horizontal
    for i in range(1, 10):
        _diff = G.DIFF*i
        if (320-_diff)<x1<(320+_diff): # On the x axis
            hor_speed = (i-1)/10.0
            print("Horizontal speed: %.2f" % (hor_speed))
            break
    #Calculo de velocidad necesaria para vertical
    for i in range(1, 10):
        _diff = diff*i
        if (180-_diff)<y1<(180+_diff): # On the y axis
            vert_speed = (i-1)/10.0
            print("Vertical speed: %.2f" % (vert_speed))
            break

    return(hor_speed,vert_speed)

def followFront(center_x, center_y):
    doneHorizontal = False
    doneVertical = False

    #EJE DE LAS X
    if (G.SCREENMIDX - G.RADIUSCENTER) < center_x < (G.SCREENMIDX + G.RADIUSCENTER):   # Si el objeto esta en el centro
        G.DRONE.stop()
        G.FLAG_MOVEMENT = 0
        doneHorizontal = True
        print "DETENER (Izquierda - Derecha)"

    # En el eje de las x (Horizontal) -> Note: Inverse
    elif center_x > (G.SCREENMIDX + G.RADIUSCENTER):                  # Si el objeto esta a la derecha del centro
        G.DRONE.moveRight()
        time.sleep(1)
        G.DRONE.stop()
        G.FLAG_MOVEMENT = 1

    elif center_x < (G.SCREENMIDX - G.RADIUSCENTER):                   # Si el objeto esta a la izquierda del centro
        G.DRONE.moveLeft()
        time.sleep(1)
        G.DRONE.stop()
        G.FLAG_MOVEMENT = 2

    if G.FLAG_MOVEMENT == 1:
        print("DERECHA")
    elif G.FLAG_MOVEMENT == 2:
        print("IZQUIERDA")
    elif G.FLAG_MOVEMENT == 0:
        print("NO HAY MOVIMIENTO")

    #EJE DE LAS Y
    if (G.SCREENMIDY - G.RADIUSCENTER) < center_y < (G.SCREENMIDY + G.RADIUSCENTER):   # Si el objeto esta en el centro
        G.DRONE.stop()
        G.FLAG_MOVEMENT = 0
        doneVertical = True
        print "DETENER (Arriba-Abajo)"

    # En el eje de las Y (Vertical)
    elif center_y < (G.SCREENMIDY - G.RADIUSCENTER):                  # Si el objeto esta por Arriba del centro
        G.DRONE.moveUp()
        time.sleep(1)
        G.DRONE.stop()
        G.FLAG_MOVEMENT = 3

    elif center_y > (G.SCREENMIDY + G.RADIUSCENTER):                   # Si el objeto esta por debajo del centro
        G.DRONE.moveDown()
        time.sleep(1)
        G.DRONE.stop()
        G.FLAG_MOVEMENT = 4

    if G.FLAG_MOVEMENT == 3:
        print("HACIA ARRIBA")
    elif G.FLAG_MOVEMENT == 4:
        print("HACIA ABAJO")
    elif G.FLAG_MOVEMENT == 0:
        print("NO HAY MOVIMIENTO")

    G.LAST_X = center_x
    G.LAST_Y = center_y

    #Cambio de funcionalidad
    if(doneVertical and doneHorizontal):
        G.STEP = 1

def followLineSpin(center_x, center_y):

    #EJE DE LAS X
    if (G.SCREENMIDX - G.RADIUSCENTER) < center_x < (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT != 0:   # Si el objeto esta en el centro
        if G.FLAG_MOVEMENT == 1:
            G.DRONE.move(0,0.1,0,-0.1)  #Estabilizo al lado contrario
            time.sleep(0.5)
            G.DRONE.move(0,0.1,0,0)     #Derecho
        elif G.FLAG_MOVEMENT == 1:
            G.DRONE.move(0,0.1,0,0.1)   #Estabilizo al lado contrario
            time.sleep(0.5)
            G.DRONE.move(0,0.1,0,0)     #Derecho
        G.FLAG_MOVEMENT = 0
        print "SEGUIR DERECHO"

    # En el eje de las x (Horizontal) -> Note: Inverse
    elif center_x > (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT != 1:                  # Si el objeto esta a la derecha del centro
        G.DRONE.move(0,0.1,0,0.1)                                     #Llevar al centro de la linea al dron
        G.FLAG_MOVEMENT = 1
        print "DERECHA"

    elif center_x < (G.SCREENMIDX - G.RADIUSCENTER) and G.FLAG_MOVEMENT != 2:                   # Si el objeto esta a la izquierda del centro
        G.DRONE.move(0,0.1,0,-0.1)
        G.FLAG_MOVEMENT = 2
        print "IZQUIERDA"                                  #Llevar al centro de la linea al dron

    if G.FLAG_MOVEMENT == 0:
        print("DERECHO")
    elif G.FLAG_MOVEMENT == 1:
        print("GIRO HACIA LA DERECHA")
    elif G.FLAG_MOVEMENT == 2:
        print("GIRO HACIA LA IZQUIERDA")

    G.LAST_X = center_x
    G.LAST_Y = center_y

def followLineSIDE(center_x, center_y):

    #EJE DE LAS X
    if (G.SCREENMIDX - G.RADIUSCENTER) < center_x < (G.SCREENMIDX + G.RADIUSCENTER):   # Si el objeto esta en el centro
        G.DRONE.move(0,0.1,0,0)
        G.FLAG_MOVEMENT = 0
        print "SEGUIR DERECHO"

    # En el eje de las x (Horizontal) -> Note: Inverse
    elif center_x > (G.SCREENMIDX + G.RADIUSCENTER):                  # Si el objeto esta a la derecha del centro
        G.DRONE.move(0.1,0.1,0,0)                                     #Llevar al centro de la linea al dron
        time.sleep(1)
        G.DRONE.move(-0.1,0.1,0,0)                                    #Estabilizar con el movimiento contrario y menos tiempo sobre la linea
        time.sleep(0.5)
        G.DRONE.move(0,0.1,0,0)                                       #Seguir derecho
        G.FLAG_MOVEMENT = 1

    elif center_x < (G.SCREENMIDX - G.RADIUSCENTER):                   # Si el objeto esta a la izquierda del centro
        G.DRONE.move(-0.1,0.1,0,0)                                     #Llevar al centro de la linea al dron
        time.sleep(1)
        G.DRONE.move(0.1,0.1,0,0)                                      #Estabilizar con el movimiento contrario y menos tiempo sobre la linea
        time.sleep(0.5)
        G.DRONE.move(0,0.1,0,0)                                        #Seguir derecho
        G.FLAG_MOVEMENT = 2

    if G.FLAG_MOVEMENT == 0:
        print("DERECHO")
    elif G.FLAG_MOVEMENT == 1:
        print("GIRO HACIA LA DERECHA")
    elif G.FLAG_MOVEMENT == 2:
        print("GIRO HACIA LA IZQUIERDA")

    G.LAST_X = center_x
    G.LAST_Y = center_y

def followLineSideNSpin(center_x, center_y):

    #EJE DE LAS X
    if (G.SCREENMIDX - G.RADIUSCENTER) < center_x < (G.SCREENMIDX + G.RADIUSCENTER):   # Si el objeto esta en el centro
        G.DRONE.move(0,0.1,0,0)
        G.FLAG_MOVEMENT = 0
        print "SEGUIR DERECHO"

    # En el eje de las x (Horizontal) -> Note: Inverse
    elif center_x > (G.SCREENMIDX + G.RADIUSCENTER):                  # Si el objeto esta a la derecha del centro
        G.DRONE.move(0.1,0.1,0,0.1)                                     #Llevar al centro de la linea al dron
        time.sleep(1)
        G.DRONE.move(-0.1,0.1,0,-0.1)                                    #Estabilizar con el movimiento contrario y menos tiempo sobre la linea
        time.sleep(0.5)
        G.DRONE.move(0,0.1,0,0)                                       #Seguir derecho
        G.FLAG_MOVEMENT = 1

    elif center_x < (G.SCREENMIDX - G.RADIUSCENTER):                   # Si el objeto esta a la izquierda del centro
        G.DRONE.move(-0.1,0.1,0,-0.1)                                     #Llevar al centro de la linea al dron
        time.sleep(1)
        G.DRONE.move(0.1,0.1,0,0.1)                                      #Estabilizar con el movimiento contrario y menos tiempo sobre la linea
        time.sleep(0.5)
        G.DRONE.move(0,0.1,0,0)                                        #Seguir derecho
        G.FLAG_MOVEMENT = 2

    if G.FLAG_MOVEMENT == 0:
        print("DERECHO")
    elif G.FLAG_MOVEMENT == 1:
        print("GIRO HACIA LA DERECHA")
    elif G.FLAG_MOVEMENT == 2:
        print("GIRO HACIA LA IZQUIERDA")

    G.LAST_X = center_x
    G.LAST_Y = center_y

def timePass(flagTime,seconds):

    if(flagTime):
        flagTime = False
        if(time.localtime().tm_sec >= 57):
            seconds = (time.localtime().tm_sec) - 60
        else:
            seconds = time.localtime().tm_sec

    if(time.localtime().tm_sec == seconds + 3):
        #print("Paso por aqui cada 3 seg!")
        flagTime = True
    #print("SEG: " + str(time.localtime().tm_sec))
    return flagTime, seconds

def promediar(acum_x,acum_y,cantidad):

    prom_x = acum_x / cantidad
    prom_y = acum_y / cantidad

    return prom_x, prom_y

def findLargerContour(cnts):
    if cnts != []:
        largest_contour = cnts[0]
        for c in cnts:
            if cv2.contourArea(c) > cv2.contourArea(largest_contour):
                largest_contour = c
        return largest_contour
    else:
        return cnts
