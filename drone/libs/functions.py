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
        time.sleep(1)
        if automatic:
            print("MANUAL")
            return False                                    #Retorna MANUAL
        else:
            print("AUTOMATICO")
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
                    G.DRONE.moveBackward(0.2)
                    #print("Moviendo hacia Atras")
                    G.FLAG_LEFTY = 1
                elif(G.JOY.leftY() > 0.900):                #Palanca izquierda hacia arriba
                    G.DRONE.moveForward(0.2)
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


def findEdge(contours):

    cont = 0
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        if h > 50:
            cont += 1
    array = list(range(cont))
    cont = 0
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        if h > 50:
            array[cont] = c
            cont += 1

    if(len(array) == 1):
        cnt = array[0]
        topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
        bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
        leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
        rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
        return (topmost,bottommost,leftmost,rightmost,True)

    elif(len(array) > 1):
        cnt_down = array[0]
        cnt_up = array[len(array) - 1]
        topmost = tuple(cnt_up[cnt_up[:,:,1].argmin()][0])
        bottommost = tuple(cnt_down[cnt_down[:,:,1].argmax()][0])

        leftmost_up = tuple(cnt_up[cnt_up[:,:,0].argmin()][0])
        rightmost_up = tuple(cnt_up[cnt_up[:,:,0].argmax()][0])
        leftmost_down = tuple(cnt_down[cnt_down[:,:,0].argmin()][0])
        rightmost_down = tuple(cnt_down[cnt_down[:,:,0].argmax()][0])
        if(leftmost_up[0] <= leftmost_down[0]):
            leftmost = leftmost_up
        else:
            leftmost = leftmost_down
        if(rightmost_up[0] >= rightmost_down[0]):
            rightmost = rightmost_up
        else:
            rightmost = rightmost_down
        return (topmost,bottommost,leftmost,rightmost,True)
    else:
        return (0,0,0,0,False)


def drawLineCHANGE(frame,dilate):

    full_line = [G.FULL]
    find = False

    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Frame de la camara completa
    cv2.drawContours(frame,contours, -1, (0, 255, 0), 1)

    cv2.line(frame, (G.SCREENMIDX, 0), (G.SCREENMIDX, G.H), (0,255,0),2)    #LINEA VERTICAL MEDIO VERDE

    cv2.line(frame,(G.SCREENMIDX,G.H),((G.W * 10/ 100),0), (0,0,255),1)    #LINEA de angulos izquierda
    cv2.line(frame,(G.SCREENMIDX,G.H),((G.W * 90/ 100),0), (0,0,255),1)    #LINEA de angulos derecha
    cv2.line(frame,(G.SCREENMIDX - G.RADIUSCENTER, (G.H * 1) / 3),(G.SCREENMIDX - G.RADIUSCENTER, (G.H * 2) / 3), (0,0,255),1)  #LINEA delimitadora izquierda
    cv2.line(frame,(G.SCREENMIDX + G.RADIUSCENTER, (G.H * 1) / 3),(G.SCREENMIDX + G.RADIUSCENTER, (G.H * 2) / 3), (0,0,255),1)  #LINEA delimitadora derecha

    if (len(contours) != 0):
        top, bot, left, right, flag = findEdge(contours)
        if flag:
            cv2.line(frame, (G.SCREENMIDX, G.SCREENMIDY), (bot), (127,0,255),2)
            cv2.line(frame, (G.SCREENMIDX, G.SCREENMIDY), (top), (127,0,255),2)
            cv2.line(frame, (0, top[1]), (G.W, top[1]), (0,255,0),2)
            cv2.circle(frame, (left), 3, (127,0,255),2)
            cv2.circle(frame, (right), 3, (127,0,255),2)
            full_line = [top,bot,left,right]
            find = True

    return (frame, full_line, find)

def drawLine(frame, array_tresh):
    cont = 0
    center = [G.XY_line[0],G.XY_line[1]]
    flag = False
    cont_1 = False

    for t in array_tresh:
        #DETECTAR LINEA y retornar coordenadas
        contours, hierarchy = cv2.findContours(t, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if cont == 2 and len(contours) != 0:
            cv2.drawContours(frame,contours, -1, (0, 255, 0), 1)

        if len(contours) != 0 and cont != 2:
            if cont == 1:
                for c in contours:
                    x,y,w,h = cv2.boundingRect(c)
                    if h > 30:
                        cont_1 = True
                        cnt = c
                if cont_1:
                    topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
                    cv2.circle(frame,topmost, 5, (0,0,255), -1)
                    M = cv2.moments(cnt)
            else:
                cnt = findLargerContour(contours)
                x,y,w,h = cv2.boundingRect(cnt)
                if h > 30:
                    cont_1 = True
                    M = cv2.moments(cnt)

            if cont_1:
                if M['m00'] != 0:
                    x_center = int(M['m10']/M['m00'])
                    y_center = int(M['m01']/M['m00']) + G.H/3 if cont == 0 else 0

                    cv2.line(frame,(G.SCREENMIDX,0),(G.SCREENMIDX,G.H), (255,0,0),1)
                    cv2.line(frame,(0,G.SCREENMIDY),(G.W,G.SCREENMIDY), (255,0,0),1)
                    cv2.line(frame,(G.SCREENMIDX,G.SCREENMIDY),((G.W * 19/ 100),0), (0,0,255),2)
                    cv2.line(frame,(G.SCREENMIDX,G.SCREENMIDY),((G.W * 81/ 100),0), (0,0,255),2)
                    #cv2.line(frame,(G.SCREENMIDX,G.SCREENMIDY),(0,(G.H * 39) / 100), (0,0,255),2)
                    #cv2.line(frame,(G.SCREENMIDX,G.SCREENMIDY),(G.W ,(G.H * 39) / 100), (0,0,255),2)
                    for i in range(1, 5):
                        cv2.circle(frame, (G.SCREENMIDX, G.SCREENMIDY), G.RADIUSCENTER*i,(0,255,0),2) ##(,(),G.RADIUSCENTER,(),)
                    if cont == 1:
                        cv2.line(frame, (G.SCREENMIDX, G.SCREENMIDY), (topmost), (127,0,255),2)
                        center[cont] = topmost
                    else:
                        cv2.line(frame, (G.SCREENMIDX, G.SCREENMIDY), (x_center,y_center), (127,0,255),2)
                        center[cont] = (x_center,y_center)

                    flag = True
        cont += 1

    if flag == False:
        return (frame,None,False)
    else:
        return (frame,center,True)


#move(right,forward,up,turn right)
def followLineSpin():
    giro = 0.00
    horizontal = 0.0
    vertical = 0.0
    frente = 0.0
    var_giro = 0.3
    Kp = 0.2
    Kp_frente = 0.05
    Ki = 0
    Kd = 0

    #MOVIMIENTO HORIZONTAL
    print("               |=============================|")
    #if (G.SCREENMIDX - G.RADIUSCENTER) < G.CENTER[0][0] < (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 0:   # Si el objeto esta en el centro
    if (G.SCREENMIDX - G.RADIUSCENTER) < G.FULL[0][0] < (G.SCREENMIDX + G.RADIUSCENTER):
        horizontal = (Kp + Ki + Kd) * 0 / G.SCREENMIDX
        print "               |       SEGUIR DERECHO        |"
        print("               |-----------------------------|")

    # En el eje de las x (Horizontal) -> Note: Inverse
    #elif G.CENTER[0][0] > (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 1:                  # Si el objeto esta a la derecha del centro
    elif G.FULL[0][0] > (G.SCREENMIDX + G.RADIUSCENTER):
        error = (G.FULL[0][0] - (G.SCREENMIDX + G.RADIUSCENTER))
        horizontal = ((Kp + Ki + Kd) * error) / (G.W - (G.SCREENMIDX + G.RADIUSCENTER))
        print "               |       IR A LA DERECHA       |"
        print("               |-----------------------------|")

    #elif G.CENTER[0][0] < (G.SCREENMIDX - G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 2:                   # Si el objeto esta a la izquierda del centro
    elif G.FULL[0][0] < (G.SCREENMIDX - G.RADIUSCENTER):
        error = (G.FULL[0][0] - (G.SCREENMIDX - G.RADIUSCENTER))
        horizontal = ((Kp + Ki + Kd) * error) / (G.SCREENMIDX - G.RADIUSCENTER)
        print "               |       IR A LA IZQUIERDA     |"                                  #Llevar al centro de la linea al dron
        print("               |-----------------------------|")


    #MOVIMIENTO DE GIRO
    if(G.FULL[0] != []) :
        grados_error = gradosPoint(G.FULL[0])
        if grados_error >= 0:
            giro = float ((grados_error * (Kp + Ki + Kd)) / 60.00)
            frente = Kp_frente
            print "               |       GIRO DE DERECHA       |"
            print("               |-----------------------------|")
            print "               |       GRADOS: %.3f" % grados_error + "       |"
            print("               |=============================|")
        elif grados_error < 0:
            giro = float ((grados_error * (Kp + Ki + Kd)) / 60.00)
            frente = Kp_frente
            print "               |       GIRO DE IZQUIERDA     |"
            print("               |-----------------------------|")
            print "               |       GRADOS: %.3f" % grados_error + "       |"
            print("               |=============================|")


    """if G.FULL[0][1] < G.SCREENMIDY and G.FULL[1][1] < G.SCREENMIDY: #SI el topmost y botmost estan en la parte de arriba del frame
        gradosRight = gradosPoint(G.FULL[3])
        gradosLeft = gradosPoint(G.FULL[2])
        if gradosRight > 20 or gradosLeft < -20:
            frente = 0.0
            print("--------------------------------------------------")
            print("LOS DOS EXTREMOS ESTAN ARRIBA Y NO ESTAN ALINEADOS")
            print("--------------------------------------------------")
    elif G.FULL[0][1] > G.SCREENMIDY:
        frente = -Kp_frente
        print("--------------------------------------------------")
        print("LOS DOS EXTREMOS ESTAN ABAJO")
        print("--------------------------------------------------")"""

    #if(G.notFound) and
    """if G.DRONE.NavData["demo"][3] > 200 and G.FLAG_MOVEMENT_V != 1:
        vertical = -0.1
        G.FLAG_MOVEMENT_V = 1
    elif G.DRONE.NavData["demo"][3] < 150 and G.FLAG_MOVEMENT_V != 2:
        vertical = 0.1
        G.FLAG_MOVEMENT_V = 2
    elif G.FLAG_MOVEMENT_V != 3:
        vertical = 0
        G.FLAG_MOVEMENT_V = 3"""


    #Movimiento, hacer un flag para que no mande mismos movimientos
    #if not (H_ant == G.FLAG_MOVEMENT_H and V_ant == G.FLAG_MOVEMENT_V and G_ant == G.FLAG_MOVEMENT_G):
    G.DRONE.move(horizontal,frente,vertical,giro)

    print("               |   VARIABLES DE MOVIMIENTO   |")
    print("               |-----------------------------|")
    if frente >= 0:
        print("               |     FRENTE: " + str(frente)) + "             |"
    else:
        print("               |     FRENTE: " + str(frente)) + "            |"
    if horizontal >= 0:
        print("               |     HORIZONTAL: " + str(horizontal)) + "         |"
    else:
        print("               |     HORIZONTAL: " + str(horizontal)) + "        |"
    if vertical >= 0:
        print("               |     VERTICAL: " + str(vertical)) + "           |"
    else:
        print("               |     VERTICAL: " + str(vertical)) + "          |"
    if giro >= 0:
        print("               |     GIRO: %.3f" % giro + "             |")
    else:
        print("               |     GIRO: %.3f" % giro + "            |")
    print("               |=============================| \n\n\n\n")
    time.sleep(1)
    G.DRONE.stop()
    time.sleep(1)

def followLineSpinContinuos():
    H_ant = G.FLAG_MOVEMENT_H
    V_ant = G.FLAG_MOVEMENT_V
    G_ant = G.FLAG_MOVEMENT_G
    giro = 0.00
    horizontal = 0.0
    vertical = 0.0
    frente = 0.0
    var_giro = 0.2
    Kp = 0.1
    Kp_frente = 0.05
    Ki = 0
    Kd = 0

    #MOVIMIENTO HORIZONTAL
    #if (G.SCREENMIDX - G.RADIUSCENTER) < G.CENTER[0][0] < (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 0:   # Si el objeto esta en el centro
    if (G.SCREENMIDX - G.RADIUSCENTER) < G.FULL[0][0] < (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 0:
        horizontal = ((Kp + Ki + Kd) * 0) / G.SCREENMIDX
        G.FLAG_MOVEMENT_H = 0
        frente = Kp_frente
        print("               |=============================|")
        print "               |       SEGUIR DERECHO        |"
        print("               |-----------------------------|")

    # En el eje de las x (Horizontal) -> Note: Inverse
    #elif G.CENTER[0][0] > (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 1:                  # Si el objeto esta a la derecha del centro
    elif G.FULL[0][0] > (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 1:
        error = (G.FULL[0][0] - (G.SCREENMIDX + G.RADIUSCENTER))
        horizontal = ((Kp + Ki + Kd) * error) / (G.W - (G.SCREENMIDX + G.RADIUSCENTER))
        G.FLAG_MOVEMENT_H = 1
        frente = Kp_frente
        print("               |=============================|")
        print "               |       IR A LA DERECHA       |"
        print("               |-----------------------------|")

    #elif G.CENTER[0][0] < (G.SCREENMIDX - G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 2:                   # Si el objeto esta a la izquierda del centro
    elif G.FULL[0][0] < (G.SCREENMIDX - G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 2:
        error = ((G.RADIUSCENTER - G.SCREENMIDX) + G.FULL[0][0])
        horizontal = ((Kp + Ki + Kd) * error) / (G.SCREENMIDX - G.RADIUSCENTER)
        G.FLAG_MOVEMENT_H = 2
        frente = Kp_frente
        print("               |=============================|")
        print "               |       IR A LA IZQUIERDA     |"                                  #Llevar al centro de la linea al dron
        print("               |-----------------------------|")


    #MOVIMIENTO DE GIRO
    if(G.FULL[0] != []) :
        grados_error = gradosPoint(G.FULL[0])
        if grados_error >= 0 and G.FLAG_MOVEMENT_G != 1:
            giro = float ((grados_error * (Kp + Ki + Kd)) / (60.00))
            frente = Kp_frente
            G.FLAG_MOVEMENT_G = 1
            print "               |       GIRO DE DERECHA       |"
            print("               |-----------------------------|")
            print "               |       GRADOS: %.3f" % grados_error + "       |"
            print("               |=============================|")
        elif grados_error < 0 and G.FLAG_MOVEMENT_G != 2:
            giro = float ((grados_error * (Kp + Ki + Kd)) / 60.00)
            frente = Kp_frente
            G.FLAG_MOVEMENT_G = 2
            print "               |       GIRO DE IZQUIERDA     |"
            print("               |-----------------------------|")
            print "               |       GRADOS: %.3f" % grados_error + "       |"
            print("               |=============================|")

    #Movimiento, hacer un flag para que no mande mismos movimientos
    if not (H_ant == G.FLAG_MOVEMENT_H and G_ant == G.FLAG_MOVEMENT_G):
        G.DRONE.move(horizontal,frente,vertical,giro)
        print("CAMBIO DE MOVIMIENTO")

        print("               |   VARIABLES DE MOVIMIENTO   |")
        print("               |-----------------------------|")
        if frente >= 0:
            print("               |     FRENTE: " + str(frente)) + "             |"
        else:
            print("               |     FRENTE: " + str(frente)) + "            |"
        if horizontal >= 0:
            print("               |     HORIZONTAL: " + str(horizontal)) + "         |"
        else:
            print("               |     HORIZONTAL: " + str(horizontal)) + "        |"
        if vertical >= 0:
            print("               |     VERTICAL: " + str(vertical)) + "           |"
        else:
            print("               |     VERTICAL: " + str(vertical)) + "          |"
        if giro >= 0:
            print("               |     GIRO: %.3f" % giro + "             |")
        else:
            print("               |     GIRO: %.3f" % giro + "            |")
        print("               |=============================| \n\n\n\n")

    #time.sleep(0.5)

def followLineSpinContinuosNOSTOP():
    giro = 0.00
    horizontal = 0.0
    vertical = 0.0
    frente = 0.0
    Kp = 0.1
    Kp_frente = 0.1
    Ki = 0
    Kd = 0

    #MOVIMIENTO HORIZONTAL
    #if (G.SCREENMIDX - G.RADIUSCENTER) < G.CENTER[0][0] < (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 0:   # Si el objeto esta en el centro
    if (G.SCREENMIDX - G.RADIUSCENTER) < G.FULL[0][0] < (G.SCREENMIDX + G.RADIUSCENTER):
        horizontal = ((Kp + Ki + Kd) * 0) / G.SCREENMIDX
        print("               |=============================|")
        print "               |       SEGUIR DERECHO        |"
        print("               |-----------------------------|")

    # En el eje de las x (Horizontal) -> Note: Inverse
    #elif G.CENTER[0][0] > (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 1:                  # Si el objeto esta a la derecha del centro
    elif G.FULL[0][0] > (G.SCREENMIDX + G.RADIUSCENTER):
        error = (G.FULL[0][0] - (G.SCREENMIDX + G.RADIUSCENTER))
        horizontal = ((Kp + Ki + Kd) * error) / (G.W - (G.SCREENMIDX + G.RADIUSCENTER))
        print("               |=============================|")
        print "               |       IR A LA DERECHA       |"
        print("               |-----------------------------|")

    #elif G.CENTER[0][0] < (G.SCREENMIDX - G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 2:                   # Si el objeto esta a la izquierda del centro
    elif G.FULL[0][0] < (G.SCREENMIDX - G.RADIUSCENTER):
        error = ((G.RADIUSCENTER - G.SCREENMIDX) + G.FULL[0][0])
        horizontal = ((Kp + Ki + Kd) * error) / (G.SCREENMIDX - G.RADIUSCENTER)
        print("               |=============================|")
        print "               |       IR A LA IZQUIERDA     |"                                  #Llevar al centro de la linea al dron
        print("               |-----------------------------|")


    #MOVIMIENTO DE GIRO
    if(G.FULL[0] != []) :
        grados_error = gradosPoint(G.FULL[0])
        if grados_error >= 0:
            giro = float ((grados_error * (Kp + Ki + Kd)) / 60.00)
            frente = Kp_frente
            print "               |       GIRO DE DERECHA       |"
            print("               |-----------------------------|")
            print "               |       GRADOS: %.3f" % grados_error + "       |"
            print("               |=============================|")
        elif grados_error < 0:
            giro = float ((grados_error * (Kp + Ki + Kd)) / 60.00)
            frente = Kp_frente
            print "               |       GIRO DE IZQUIERDA     |"
            print("               |-----------------------------|")
            print "               |       GRADOS: %.3f" % grados_error + "       |"
            print("               |=============================|")

    #Movimiento, hacer un flag para que no mande mismos movimientos
    G.DRONE.move(horizontal,frente,vertical,giro)

    print("               |   VARIABLES DE MOVIMIENTO   |")
    print("               |-----------------------------|")
    if frente >= 0:
        print("               |     FRENTE: " + str(frente)) + "             |"
    else:
        print("               |     FRENTE: " + str(frente)) + "            |"
    if horizontal >= 0:
        print("               |     HORIZONTAL: " + str(horizontal)) + "         |"
    else:
        print("               |     HORIZONTAL: " + str(horizontal)) + "        |"
    if vertical >= 0:
        print("               |     VERTICAL: " + str(vertical)) + "           |"
    else:
        print("               |     VERTICAL: " + str(vertical)) + "          |"
    if giro >= 0:
        print("               |     GIRO: %.3f" % giro + "             |")
    else:
        print("               |     GIRO: %.3f" % giro + "            |")
    print("               |=============================| \n\n\n\n")

    time.sleep(0.5)

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

def gradosPoint(punto):
    #Regla de tres para los puntos en x , y
    line_x = (punto[0] * 100.0) / G.W
    line_y = (punto[1] * 100.0) / G.H
    #Pendiente de la linea
    if (line_x - G.MX) != 0:
        line_m = (line_y - G.MY) / (line_x - G.MX)
    else:
        return 0

    if line_x > 50:
        return (90 + math.degrees(math.atan(line_m)))

    elif line_x < 50:
        return (math.degrees(math.atan(line_m)) - 90)

def detection(frame,array_tresh):
    flag = False

    for t in array_tresh:
        #Revisar si hay algo en la region de interes
        contours, hierarchy = cv2.findContours(t, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0 and flag == False:
            flag = True

    if not flag:
        G.in_use = False

    elif not G.in_use:
        G.conteo += 1
        G.in_use = True


    """if G.in_use:
        cv2.rectangle(frame,(0,G.H/3),(G.W,2*(G.H/3)),(0,255,0),1)
    else:
        cv2.rectangle(frame,(0,G.H/3),(G.W,2*(G.H/3)),(0,0,255),1)
"""
    return frame
