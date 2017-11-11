    global H_MIN_1, H_MIN_2, H_MIN_3, H_MIN_4, H_MIN_5, H_MIN_6, H_MIN_7, H_MIN_8, H_MIN_9, H_MIN_10, H_MIN_11, H_MIN_12, H_MIN_13
    H_MIN_1, H_MIN_2, H_MIN_3, H_MIN_4, H_MIN_5, H_MIN_6, H_MIN_7, H_MIN_8, H_MIN_9, H_MIN_10, H_MIN_11, H_MIN_12, H_MIN_13 = 42, 68, 68, 65, 61, 52, 60, 66, 65, 70, 52, 57, 68

    global H_MAX_1, H_MAX_2, H_MAX_3, H_MAX_4, H_MAX_5, H_MAX_6, H_MAX_7, H_MAX_8, H_MAX_9, H_MAX_10, H_MAX_11, H_MAX_12, H_MAX_13
    H_MAX_1, H_MAX_2, H_MAX_3, H_MAX_4, H_MAX_5, H_MAX_6, H_MAX_7, H_MAX_8, H_MAX_9, H_MAX_10, H_MAX_11, H_MAX_12, H_MAX_13 = 104, 91, 95, 96, 125, 89, 87, 89, 102, 103, 86, 100, 79

    global S_MIN_1, S_MIN_2, S_MIN_3, S_MIN_4, S_MIN_5, S_MIN_6, S_MIN_7, S_MIN_8, S_MIN_9, S_MIN_10, S_MIN_11, S_MIN_12, S_MIN_13
    S_MIN_1, S_MIN_2, S_MIN_3, S_MIN_4, S_MIN_5, S_MIN_6, S_MIN_7, S_MIN_8, S_MIN_9, S_MIN_10, S_MIN_11, S_MIN_12, S_MIN_13 = 75, 61, 64, 62, 60, 48, 44, 46, 41, 28, 31, 40, 61,

    global S_MAX_1, S_MAX_2, S_MAX_3, S_MAX_4, S_MAX_5, S_MAX_6, S_MAX_7, S_MAX_8, S_MAX_9, S_MAX_10, S_MAX_11, S_MAX_12, S_MAX_13
    S_MAX_1, S_MAX_2, S_MAX_3, S_MAX_4, S_MAX_5, S_MAX_6, S_MAX_7, S_MAX_8, S_MAX_9, S_MAX_10, S_MAX_11, S_MAX_12, S_MAX_13 = 255, 255, 255, 255, 200, 161, 169, 184, 176, 255, 255, 255, 255

    global V_MIN_1, V_MIN_2, V_MIN_3, V_MIN_4, V_MIN_5, V_MIN_6, V_MIN_7, V_MIN_8, V_MIN_9, V_MIN_10, V_MIN_11, V_MIN_12, V_MIN_13
    V_MIN_1, V_MIN_2, V_MIN_3, V_MIN_4, V_MIN_5, V_MIN_6, V_MIN_7, V_MIN_8, V_MIN_9, V_MIN_10, V_MIN_11, V_MIN_12, V_MIN_13 = 44, 69, 39, 53, 34, 49, 66, 24, 64, 4, 40, 40, 29

    global V_MAX_1, V_MAX_2, V_MAX_3, V_MAX_4, V_MAX_5, V_MAX_6, V_MAX_7, V_MAX_8, V_MAX_9, V_MAX_10, V_MAX_11, V_MAX_12, V_MAX_13
    V_MAX_1, V_MAX_2, V_MAX_3, V_MAX_4, V_MAX_5, V_MAX_6, V_MAX_7, V_MAX_8, V_MAX_9, V_MAX_10, V_MAX_11, V_MAX_12, V_MAX_13 = 148, 146, 255, 154, 151, 141, 128, 175, 146, 200, 255, 255, 111


def followLineSpinContinuos():
    H_ant = G.FLAG_MOVEMENT_H
    V_ant = G.FLAG_MOVEMENT_V
    G_ant = G.FLAG_MOVEMENT_G
    giro = 0.00
    horizontal = 0.0
    vertical = 0.0
    frente = 0.0
    var_giro = 0.4

    # G.XY_line[0] = Espacio de imagen del medio x,y
    # G.XY_line[1] = Espacio de imagen del frente x,y
    #print("G.XY_line[0][0]: " + str(G.XY_line[0][0]))
    #MOVIMIENTO HORIZONTAL
    print("               |=============================|")
    #if (G.SCREENMIDX - G.RADIUSCENTER) < G.CENTER[0][0] < (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 0:   # Si el objeto esta en el centro
    if (G.SCREENMIDX - G.RADIUSCENTER) < G.CENTER[0][0] < (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 0:
        horizontal = 0.0
        G.FLAG_MOVEMENT_H = 0
        print "               |       SEGUIR DERECHO        |"
        print("               |-----------------------------|")

    # En el eje de las x (Horizontal) -> Note: Inverse
    #elif G.CENTER[0][0] > (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 1:                  # Si el objeto esta a la derecha del centro
    elif G.CENTER[0][0] > (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 1:
        horizontal = 0.1
        G.FLAG_MOVEMENT_H = 1
        print "               |       IR A LA DERECHA       |"
        print("               |-----------------------------|")

    #elif G.CENTER[0][0] < (G.SCREENMIDX - G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 2:                   # Si el objeto esta a la izquierda del centro
    elif G.CENTER[0][0] < (G.SCREENMIDX - G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 2:
        horizontal = -0.1
        G.FLAG_MOVEMENT_H = 2
        print "               |       IR A LA IZQUIERDA     |"                                  #Llevar al centro de la linea al dron
        print("               |-----------------------------|")


    #MOVIMIENTO DE GIRO
    if(G.FULL[0] != []) :
        grados = gradosPoint(G.FULL[0])
        if grados >= 0:
            if grados < 36 and G.FLAG_MOVEMENT_G != 1:
                G.FLAG_MOVEMENT_G = 1
                giro  = 0.000
                frente = 0.1
                print "               |            CENTRO           |"
                print("               |-----------------------------|")
                print "               |       GRADOS: %.3f" % grados + "        |"
                print("               |=============================|")
            elif grados > 36 and G.FLAG_MOVEMENT_G != 2:
                G.FLAG_MOVEMENT_G = 2
                giro = float ((grados * var_giro) / 90.00)
                print "               |   GIRAR HACIA LA DERECHA    |"
                print("               |-----------------------------|")
                print "               |       GRADOS: %.3f" % grados + "        |"
                print("               |=============================|")
                if grados < 54:
                    frente = 0.1
        elif grados < 0:
            if grados > -36 and G.FLAG_MOVEMENT_G != 3: #PROBAR CON 45
                G.FLAG_MOVEMENT_G = 3
                giro  = 0.000
                frente = 0.1
                print "               |            CENTRO           |"
                print("               |-----------------------------|")
                print "               |       GRADOS: %.3f" % grados + "       |"
                print("               |=============================|")
            elif grados < -36 and G.FLAG_MOVEMENT_G != 4:
                G.FLAG_MOVEMENT_G = 4
                giro = float ((grados * var_giro) / 90.00)
                print "               |   GIRAR HACIA LA IZQUIERDA  |"
                print("               |-----------------------------|")
                print "               |       GRADOS: %.3f" % grados + "       |"
                print("               |=============================|")
                if grados > -54:
                    frente = 0.1

    if G.FULL[0][1] < G.SCREENMIDY and G.FULL[1][1] < G.SCREENMIDY: #SI el topmost y botmost estan en la parte de arriba del frame
        gradosRight = gradosPoint(G.FULL[3])
        gradosLeft = gradosPoint(G.FULL[2])
        if gradosRight > 20 or gradosLeft < -20:
            frente = 0.0
            print("--------------------------------------------------")
            print("LOS DOS EXTREMOS ESTAN ARRIBA Y NO ESTAN ALINEADOS")
            print("--------------------------------------------------")
    elif G.FULL[0][1] > G.SCREENMIDY:
        frente = -0.1
        print("--------------------------------------------------")
        print("LOS DOS EXTREMOS ESTAN ABAJO")
        print("--------------------------------------------------")

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
    if not (H_ant == G.FLAG_MOVEMENT_H and V_ant == G.FLAG_MOVEMENT_V and G_ant == G.FLAG_MOVEMENT_G):
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

def followLineSpin():
    giro = 0.00
    horizontal = 0.0
    vertical = 0.0
    frente = 0.0
    kp_giro = 0.3
    kp_horizontal = 0.1
    kp_frente = 0.2


    #MOVIMIENTO HORIZONTAL
    print("               |=============================|")
    #if (G.SCREENMIDX - G.RADIUSCENTER) < G.CENTER[0][0] < (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 0:   # Si el objeto esta en el centro
    if (G.SCREENMIDX - G.RADIUSCENTER) < G.FULL[0][0] < (G.SCREENMIDX + G.RADIUSCENTER) :
        horizontal = kp_horizontal * 0
        print "               |       SEGUIR DERECHO        |"
        print("               |-----------------------------|")

    # En el eje de las x (Horizontal) -> Note: Inverse
    #elif G.CENTER[0][0] > (G.SCREENMIDX + G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 1:                  # Si el objeto esta a la derecha del centro
    elif G.FULL[0][0] > (G.SCREENMIDX + G.RADIUSCENTER):
        horizontal = kp_horizontal
        print "               |       IR A LA DERECHA       |"
        print("               |-----------------------------|")

    #elif G.CENTER[0][0] < (G.SCREENMIDX - G.RADIUSCENTER) and G.FLAG_MOVEMENT_H != 2:                   # Si el objeto esta a la izquierda del centro
    elif G.FULL[0][0] < (G.SCREENMIDX - G.RADIUSCENTER):
        horizontal = -kp_horizontal
        print "               |       IR A LA IZQUIERDA     |"                                  #Llevar al centro de la linea al dron
        print("               |-----------------------------|")


    #MOVIMIENTO DE GIRO
    if(G.FULL[0] != []) :
        grados = gradosPoint(G.FULL[0])
        if grados >= 0:
            if grados < 36:
                giro  = 0.000
                frente = kp_frente
                print "               |            CENTRO           |"
                print("               |-----------------------------|")
                print "               |       GRADOS: %.3f" % grados + "        |"
                print("               |=============================|")
            elif grados > 36:
                giro = float ((grados * kp_giro) / 90.00)
                print "               |   GIRAR HACIA LA DERECHA    |"
                print("               |-----------------------------|")
                print "               |       GRADOS: %.3f" % grados + "        |"
                print("               |=============================|")
                if grados < 54:
                    frente = kp_frente
        elif grados < 0:
            if grados > -36 : #PROBAR CON 45
                giro  = 0.000
                frente = kp_frente
                print "               |            CENTRO           |"
                print("               |-----------------------------|")
                print "               |       GRADOS: %.3f" % grados + "       |"
                print("               |=============================|")
            elif grados < -36 :
                giro = float ((grados * kp_giro) / 90.00)
                print "               |   GIRAR HACIA LA IZQUIERDA  |"
                print("               |-----------------------------|")
                print "               |       GRADOS: %.3f" % grados + "       |"
                print("               |=============================|")
                if grados > -54:
                    frente = kp_frente

    if G.FULL[0][1] < G.SCREENMIDY and G.FULL[1][1] < G.SCREENMIDY: #SI el topmost y botmost estan en la parte de arriba del frame
        gradosRight = gradosPoint(G.FULL[3])
        gradosLeft = gradosPoint(G.FULL[2])
        if gradosRight > 20 or gradosLeft < -20:
            frente = kp_frente * 0
            print("--------------------------------------------------")
            print("LOS DOS EXTREMOS ESTAN ARRIBA Y NO ESTAN ALINEADOS")
            print("--------------------------------------------------")
    elif G.FULL[0][1] > G.SCREENMIDY:
        frente = -kp_frente
        print("--------------------------------------------------")
        print("LOS DOS EXTREMOS ESTAN ABAJO")
        print("--------------------------------------------------")

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
