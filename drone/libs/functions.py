import time, sys
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron')
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron/drone/libs')
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron/drone/libs/XboxController')
import ps_drone
import xbox
import cv2
import numpy as np
import math
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
                    #print("Moviendo Izquierda")
                    G.FLAG_LEFTX = True
                elif(G.JOY.leftX() > 0.900):                # Palanca izquierda hacia la derecha
                    G.DRONE.moveRight()
                    #print("Moviendo Derecha")
                    G.FLAG_LEFTX = True
                elif (G.FLAG_LEFTX == True) and (G.JOY.leftX() > -0.900) and (G.JOY.leftX() < 0.900):   #Palanca izquierda paro
                    #print("Deteniendo movimiento por movimiento de palanca (Izquierda-Derecha)")
                    G.DRONE.stop()
                    G.FLAG_LEFTX = False
            elif G.FLAG_LEFTX:                              # Palanca izquierda paro por captar otro tipo de movimiento
                #print("Deteniendo movimiento por captar otro tipo de movimiento (Izquierda-Derecha)")
                G.DRONE.stop()
                G.FLAG_LEFTX = False

            #EJE Y
            if(G.JOY.leftY()):
                if(G.JOY.leftY() < -0.900):                 #Palanca izquierda hacia abajo
                    G.DRONE.moveBackward()
                    #print("Moviendo hacia Atras")
                    G.FLAG_LEFTY = 1
                elif(G.JOY.leftY() > 0.900):                #Palanca izquierda hacia arriba
                    G.DRONE.moveForward()
                    #print("Moviendo hacia Adelante")
                    G.FLAG_LEFTY = 1
                elif (G.FLAG_LEFTY) and (G.JOY.leftY() > -0.900) and (G.JOY.leftY() < 0.900):   #Palanca izquierda paro
                    #print("Deteniendo movimiento por movimiento de palanca (Adelante-Atras)")
                    G.DRONE.stop()
                    G.FLAG_LEFTY = 0
            elif G.FLAG_LEFTY:                              #Palanca izquierda paro por otro movimiento
                #print("Deteniendo movimiento por captar otro tipo de movimiento (Adelante-Atras)")
                G.DRONE.stop()
                G.FLAG_LEFTY = 0

            #Palanca derecha del control
            #EJE X
            if(G.JOY.rightX()):
                if(G.JOY.rightX() < -0.900):                #Palanca derecha hacia la izquierda
                    G.DRONE.turnLeft()
                    #print("Rotacion hacia izquierda")
                    G.FLAG_RIGHTX = 1
                elif(G.JOY.rightX() > 0.900):
                    #print("Rotacion hacia derecha")         #Palanca derecha hacia la izquierda
                    G.DRONE.turnRight()
                    G.FLAG_RIGHTX = 1
                elif (G.FLAG_RIGHTX) and (G.JOY.rightX() > -0.900) and (G.JOY.rightX() < 0.900):
                    #print("Deteniendo ROTACION por movimiento de palanca (Izquierda-Derecha)")      #Palanca derecha pato
                    G.DRONE.stop()
                    G.FLAG_RIGHTX = 0
            elif G.FLAG_RIGHTX:                             #Palanca derecha paro por otro movimiento
                #print("Deteniendo ROTACION por captar otro tipo de movimiento (Izquierda-Derecha)")
                G.DRONE.stop()
                G.FLAG_RIGHTX = 0

            #EJE Y
            if(G.JOY.rightY()):                             #Palanca derecha hacia arriba
                if(G.JOY.rightY() < -0.900):
                    #print("Bajando")
                    G.DRONE.moveDown(0.6)
                    G.FLAG_RIGHTY = True
                elif(G.JOY.rightY() > 0.900):               #Palanca derecha hacia abajo
                    #print("Subiendo")
                    G.DRONE.moveUp(0.6)
                    G.FLAG_RIGHTY = True
                elif (G.FLAG_RIGHTY) and (G.JOY.rightY() > -0.900) and (G.JOY.rightY() < 0.900):    #Palanca derecha paro
                    #print("Deteniendo movimiento por movimiento de palanca (Arriba-Abajo)")
                    G.DRONE.stop()
                    G.FLAG_RIGHTY = False
            elif G.FLAG_RIGHTY:                             #Palanca derecha paro por otro movimiento
                #print("Deteniendo movimiento por captar otro tipo de movimiento (Arriba-Abajo)")
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
                cv2.circle(frame, (G.SCREENMIDX, G.SCREENMIDY), G.RADIUSCENTER*i,(0,255,0),2) ##(,(),G.RADIUSCENTER,(),)

            cv2.line(frame, (G.SCREENMIDX, G.SCREENMIDY), (x_center,y_center), (0,255,0),2)
            cv2.circle(frame,(x_center, y_center),1,(0,0,255),1)

            center = (x_center,y_center)

            return (frame,center,True)
    else:
        return  (frame,None,False)

def drawLine(frame, array_tresh):
    cont = 0
    center = [[],[],[]]
    for t in array_tresh:
        #DETECTAR LINEA y retornar coordenadas
        contours, hierarchy = cv2.findContours(t, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnt = findLargerContour(contours)
        #cv2.drawContours(frame,cnt, -1, (0, 255, 0), 5)
        if cnt != []:
            M = cv2.moments(cnt)
            if  M['m00'] != 0:
                x_center = int(M['m10']/M['m00'])
                y_center = int(M['m01']/M['m00']) if cont == 1 else int(M['m01']/M['m00']) + G.H/3

                cv2.line(frame,(G.SCREENMIDX,0),(G.SCREENMIDX,G.H), (255,0,0),1)
                cv2.line(frame,(0,G.SCREENMIDY),(G.W,G.SCREENMIDY), (255,0,0),1)
                cv2.line(frame,(G.SCREENMIDX,G.SCREENMIDY),((G.W * 39) / 100,0), (0,0,255),2)
                cv2.line(frame,(G.SCREENMIDX,G.SCREENMIDY),((G.W * 61) / 100,0), (0,0,255),2)
                cv2.line(frame,(G.SCREENMIDX,G.SCREENMIDY),(0,(G.H * 39) / 100), (0,0,255),2)
                cv2.line(frame,(G.SCREENMIDX,G.SCREENMIDY),(G.W ,(G.H * 39) / 100), (0,0,255),2)
                for i in range(1, 5):
                    cv2.circle(frame, (G.SCREENMIDX, G.SCREENMIDY), G.RADIUSCENTER*i,(0,255,0),2) ##(,(),G.RADIUSCENTER,(),)

                cv2.line(frame, (G.SCREENMIDX, G.SCREENMIDY), (x_center,y_center), (127,0,255),2)
                cv2.circle(frame,(x_center, y_center),1,(0,0,255),1)

                center[cont] = (x_center,y_center)
                cont += 1

    if cont == 0:
        return (frame,None,False)
    else:
        return (frame,center,True)

def followBottom():
    doneHorizontal = False
    doneVertical = False
    timeS = 1
    speed = 0.05
    #EJE DE LAS X
    if (G.SCREENMIDX - G.RADIUSCENTER) < G.XY_mark[0] < (G.SCREENMIDX + G.RADIUSCENTER):   # Si el objeto esta en el centro
        G.DRONE.stop()
        G.FLAG_MOVEMENT = 0
        doneHorizontal = True
        print "followBottom: DETENER (Izquierda - Derecha)"

    # En el eje de las x (Horizontal) -> Note: Inverse
    elif G.XY_mark[0] > (G.SCREENMIDX + G.RADIUSCENTER) and not G.notFound:                  # Si el objeto esta a la derecha del centro
        G.DRONE.moveRight(speed)
        print("followBottom: DERECHA")
        time.sleep(2)
        G.DRONE.stop()
        time.sleep(2)
        doneHorizontal = False

    elif G.XY_mark[0] < (G.SCREENMIDX - G.RADIUSCENTER) and not G.notFound:                   # Si el objeto esta a la izquierda del centro
        G.DRONE.moveLeft(speed)
        print("followBottom: IZQUIERDA")
        time.sleep(2)
        G.DRONE.stop()
        time.sleep(2)
        doneHorizontal = False

    #EJE DE LAS Y
    if (G.SCREENMIDY - G.RADIUSCENTER) < G.XY_mark[1] < (G.SCREENMIDY + G.RADIUSCENTER) :   # Si el objeto esta en el centro
        G.DRONE.stop()
        G.FLAG_MOVEMENT = 10
        doneVertical = True
        print "followBottom: DETENER (Al frente - Hacia atras)"

    # En el eje de las Y (Vertical)
    elif G.XY_mark[1] < (G.SCREENMIDY - G.RADIUSCENTER)  and not G.notFound:                  # Si el objeto esta por Arriba del centro
        G.DRONE.moveForward(speed)
        print("followBottom: HACIA EL FRENTE")
        time.sleep(2)
        G.DRONE.stop()
        time.sleep(2)
        doneVertical = False

    elif G.XY_mark[1] > (G.SCREENMIDY + G.RADIUSCENTER) and not G.notFound:                   # Si el objeto esta por debajo del centro
        G.DRONE.moveBackward(speed)
        print("followBottom: HACIA ATRAS")
        time.sleep(2)
        G.DRONE.stop()
        time.sleep(2)
        doneVertical = False

    #Cambio de funcionalidad
    if(doneVertical and doneHorizontal) or (G.XY_line[0] != 0 and G.XY_line[1] != 0):
        #G.DRONE.land()  #prueba
        print "YA CENTRO o ENCONTRO LINEA"
        G.DRONE.stop()
        G.STEP = 1
        time.sleep(3)
        #lineCalibration()

"""def followBottom(center_x, center_y):
    doneHorizontal = False
    doneVertical = False
    timeS = 1

    #EJE DE LAS X
    if (G.SCREENMIDX - G.RADIUSCENTER) < center_x < (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT != 0:   # Si el objeto esta en el centro
        G.DRONE.stop()
        G.FLAG_MOVEMENT = 0
        doneHorizontal = True
        print "followBottom: DETENER (Izquierda - Derecha)"

    # En el eje de las x (Horizontal) -> Note: Inverse
    elif center_x > (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT != 1:                  # Si el objeto esta a la derecha del centro
        G.DRONE.moveRight(0.1)
        print("followBottom: DERECHA")
        G.FLAG_MOVEMENT = 1
        doneHorizontal = False

    elif center_x < (G.SCREENMIDX - G.RADIUSCENTER) and G.FLAG_MOVEMENT != 2:                   # Si el objeto esta a la izquierda del centro
        G.DRONE.moveLeft(0.1)
        print("followBottom: IZQUIERDA")
        G.FLAG_MOVEMENT = 2
        doneHorizontal = False

    #EJE DE LAS Y
    if (G.SCREENMIDY - G.RADIUSCENTER) < center_y < (G.SCREENMIDY + G.RADIUSCENTER) and G.FLAG_MOVEMENT != 10 and doneHorizontal:   # Si el objeto esta en el centro
        G.DRONE.stop()
        G.FLAG_MOVEMENT = 10
        doneVertical = True
        print "followBottom: DETENER (Al frente - Hacia atras)"

    # En el eje de las Y (Vertical)
    elif center_y < (G.SCREENMIDY - G.RADIUSCENTER) and G.FLAG_MOVEMENT != 3 and doneHorizontal:                  # Si el objeto esta por Arriba del centro
        G.DRONE.moveForward(0.1)
        print("followBottom: HACIA EL FRENTE")
        G.FLAG_MOVEMENT = 3

    elif center_y > (G.SCREENMIDY + G.RADIUSCENTER) and G.FLAG_MOVEMENT != 4 and doneHorizontal:                   # Si el objeto esta por debajo del centro
        G.DRONE.moveBackward(0.1)
        print("followBottom: HACIA ATRAS")
        G.FLAG_MOVEMENT = 4

    G.LAST_X = center_x
    G.LAST_Y = center_y

    #Cambio de funcionalidad
    if(doneVertical and doneHorizontal):
        G.DRONE.land()
        #var = F.lineCalibration()
        G.STEP = 1"""

def stopMovementBottom():

    if G.XY_line[0][0] != 0 :

        if G.XY_line[0][0] > (G.SCREENMIDX) and G.notFound:                  # Si el objeto esta a la derecha del centro
            G.DRONE.moveRight()
            print("stopMovementBottom: Buscando DERECHA")
            time.sleep(1)
            G.DRONE.stop()
            time.sleep(2)

        elif G.XY_line[0][0] < (G.SCREENMIDX) and G.notFound:                # Si el objeto esta a la izquierda del centro
            G.DRONE.moveLeft()
            print("stopMovementBottom: Buscando IZQUIERDA")
            time.sleep(1)
            G.DRONE.stop()
            time.sleep(2)

        print("stopMovementBottom: Buscando...")
        print("stopMovementBottom: LAST_X: " + str(G.XY_line[0][0]))
        print("======================")
    else:
        print("stopMovementBottom:: NUNCA HE DETECTADO ALGO")

def lineCalibration():
    #Regla de tres para los puntos en x , y
    line_x = (G.XY_line[0] * 100.0) / G.W
    line_y = (G.XY_line[1] * 100.0) / G.H
    print("line_x " + str(line_x))
    print("line_y " + str(line_y))
    #Pendiente de la linea
    line_m = (line_y - G.MY) / (line_x - G.MX)
    print("line_m " + str(line_m))
    #Si esta en el centro, o no hago nada o giro 180 grados
    if line_x == 50:
        if line_y > 50:
            #var = G.DRONE.turnAngle(90,0.5)
            time.sleep(5)
            #var = G.DRONE.turnAngle(90,0.5)
    elif line_x > 50 and line_y < 50:
        print("X: " + str (G.XY_line[0]))
        print("Y: " + str (G.XY_line[1]))
        print("I CUADRANTE: " + str(90 + math.degrees(math.atan(line_m))))
        #var = G.DRONE.turnAngle(90 + math.degrees(math.atan(line_m)),0.5)
    elif line_x > 50 and line_y > 50:
        print("X: " + str (G.XY_line[0]))
        print("Y: " + str (G.XY_line[1]))
        print("II CUADRANTE: " + str(90 + math.degrees(math.atan(line_m))))
        #var = G.DRONE.turnAngle(90 + math.degrees(math.atan(line_m)),0.5)
    elif line_x < 50 and line_y < 50:
        print("X: " + str (G.XY_line[0]))
        print("Y: " + str (G.XY_line[1]))
        print("IV CUADRANTE: " + str(math.degrees(math.atan(line_m)) - 90))
        #var = G.DRONE.turnAngle(math.degrees(math.atan(line_m)) - 90,0.5)
    elif line_x < 50 and line_y > 50:
        print("X: " + str (G.XY_line[0]))
        print("Y: " + str (G.XY_line[1]))
        print("III CUADRANTE: " + str(math.degrees(math.atan(line_m)) - 90))
        #var = G.DRONE.turnAngle(math.degrees(math.atan(line_m)) - 90,0.5)

    time.sleep(2)
    print("Termine GIRO")

#move(right,forward,up,turn right)
def followLineSpin():
    giro = 0
    horizontal = 0
    vertical = 0
    frente = 0
    # G.XY_line[0] = Espacio de imagen del medio x,y
    # G.XY_line[1] = Espacio de imagen del frente x,y
    print("G.XY_line[0][0]: " + str(G.XY_line[0][0]))
    #MOVIMIENTO HORIZONTAL
    if (G.SCREENMIDX - G.RADIUSCENTER) < G.XY_line[0][0] < (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT != 0:   # Si el objeto esta en el centro
        horizontal = 0
        G.FLAG_MOVEMENT = 0
        print "followLineSpin: SEGUIR DERECHO"

    # En el eje de las x (Horizontal) -> Note: Inverse
    elif G.XY_line[0][0] > (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT != 1:                  # Si el objeto esta a la derecha del centro
        horizontal = 0.1
        #G.DRONE.move(0.1,0.1,0,0)                                     #Llevar al centro de la linea al dron
        G.FLAG_MOVEMENT = 1
        print "followLineSpin: DERECHA"

    elif G.XY_line[0][0] < (G.SCREENMIDX - G.RADIUSCENTER) and G.FLAG_MOVEMENT != 2:                   # Si el objeto esta a la izquierda del centro
        horizontal = -0.1
        #G.DRONE.move(-0.1,0.1,0,0)
        G.FLAG_MOVEMENT = 2
        print "followLineSpin: IZQUIERDA"                                  #Llevar al centro de la linea al dron


    #MOVIMIENTO DE GIRO
    if(G.XY_line[1] != []):
        #Regla de tres para los puntos en x , y
        line_x = (G.XY_line[1][0] * 100.0) / G.W
        line_y = (G.XY_line[1][1] * 100.0) / G.H
        #Pendiente de la linea
        if (line_x - G.MX) != 0:
            line_m = (line_y - G.MY) / (line_x - G.MX)

        if line_x > 50:
            grados = (90 + math.degrees(math.atan(line_m)))

            if grados < 54:
                giro  = 0
                frente = 0.1
                print "CENTRO"
                print "followLineSpin: GRADOS: " +  str(grados)
            else:
                giro = float ((grados * 0.3) / 90.00)
                print "followLineSpin: giro DERECHA: " + str (giro)
                print "followLineSpin: GRADOS: " +  str(grados)
                if grados < 72:
                    frente = 0.1
        elif line_x < 50:
            grados = (math.degrees(math.atan(line_m)) - 90)

            if grados > -54:
                giro  = 0
                frente = 0.1
                print "CENTRO"
                print "followLineSpin: GRADOS: " +  str(grados)
            else:
                giro = float ((grados * 0.3) / 90.00)
                print "followLineSpin: giro DERECHA: " + str (giro)
                print "followLineSpin: GRADOS: " +  str(grados)
                if grados > -72:
                    frente = 0.1

    if G.DRONE.NavData["demo"][3] > 250:
        vertical = -0.1
    elif G.DRONE.NavData["demo"][3] < 150:
        vertical = 0.1
    else:
        vertical = 0

    print "============================="
    print "Horizontal: " + str (horizontal)
    print "Vertical: " + str (vertical)
    print "Frente: " + str (frente)
    print "============================="
    print "============================="
    print "============================="
    print "============================="
    print "============================="
    print "============================="
    print "============================="

    #Movimiento, hacer un flag para que no mande mismos movimientos
    G.DRONE.move(horizontal,frente,vertical,giro)
    time.sleep(1)
    G.DRONE.stop()
    time.sleep(1)

def timePass(flagTime,seconds):
    secondsWait = 5

    if(flagTime):
        flagTime = False
        if(time.localtime().tm_sec >= 60 - secondsWait):
            seconds = (time.localtime().tm_sec) - 60
        else:
            seconds = time.localtime().tm_sec

    if(time.localtime().tm_sec == seconds + secondsWait):
        #print("Paso por aqui cada 3 seg!")
        flagTime = True
    #print("SEG: " + str(time.localtime().tm_sec))
    return flagTime, seconds

def findLargerContour(cnts):
    if cnts != []:
        largest_contour = cnts[0]
        for c in cnts:
            if cv2.contourArea(c) > cv2.contourArea(largest_contour):
                largest_contour = c
        return largest_contour
    else:
        return cnts

#def detection(frame):
