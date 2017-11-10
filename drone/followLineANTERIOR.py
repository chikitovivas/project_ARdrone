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
