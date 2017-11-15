import cv2
import numpy as np
import time

H_MIN = 10
H_MAX = 40
S_MIN = 55
S_MAX = 175
V_MIN = 23
V_MAX = 92

 # VIDEO 5: 68, 91, 61, 255, 69, 146
 # VIDEO 6: 68, 95, 64, 255, 39, 255
 # VIDEO 7: 65, 96, 62, 255, 53, 154
 # VIDEO 8: 61, 125, 60, 200, 34, 151
 # VIDEO 9: 10, 40, 55, 175, 23, 92
 # AMARILLO
 # VIDEO 16: 0, 27, 26, 200, 76, 255
 # VIDEO 17: NO GUSTA
 # VIDEO 18: 5, 28, 40, 192, 120, 214  #Amarillo sombra cerca EL MEJOR
 # VIDEO 19: 10, 22, 81, 179, 119, 233  #Amarillo
 # VIDEO 20: 13, 35, 31, 109, 111, 158  #Amarillo LEJOS
 # VIDEO 30: 16, 32, 66, 228, 110, 255  #Amarillo volando


 # BLANCO VASO: 10, 116, 0, 25, 187, 255
 # AZUL VASO: 85, 120, 22, 111, 225, 255

#VERDE manguera anterior: 50, 90, 50, 180, 40, 220


W = 640
H = 360
ERROR = 50
DIFF = H/7

#cam = cv2.VideoCapture(0)
cam = cv2.VideoCapture("/home/chikitovivas/Descargas/Python-control-dron/drone/Videos/Video9.avi")

def nothing(x):
    pass


# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('H_MIN','image',H_MIN,H_MAX,nothing)
cv2.createTrackbar('H_MAX','image',H_MAX,H_MAX,nothing)
cv2.createTrackbar('S_MIN','image',S_MIN,S_MAX,nothing)
cv2.createTrackbar('S_MAX','image',S_MAX,S_MAX,nothing)
cv2.createTrackbar('V_MIN','image',V_MIN,V_MAX,nothing)
cv2.createTrackbar('V_MAX','image',V_MAX,V_MAX,nothing)
kernel = np.ones((3,3),np.uint8)
while(1):
    while not cam.isOpened():
        cam = cv2.VideoCapture("/home/chikitovivas/Descargas/Python-control-dron/drone/Videos/Video15.avi")
        cv2.waitKey(1000)
        print ("Wait for the header")

    while(1):
        time.sleep(0.1)
        flag,frame = cam.read()

        if(flag):

            frame = cv2.resize(frame,(W,H))
            blurred = cv2.GaussianBlur(frame, (5, 5), 0)

            HSV = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(HSV, np.array([H_MIN,S_MIN,V_MIN]), np.array([H_MAX,S_MAX,V_MAX]))
            output = cv2.bitwise_and(frame, frame, mask = mask)


            erode = cv2.erode(output, kernel, iterations=1)
            opening = cv2.morphologyEx(erode, cv2.MORPH_OPEN, kernel)
            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

            dilate = cv2.dilate(closing, kernel, iterations=5)

            gray = cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY)


            _,tresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)    #Filtro de blanco y negro
            edges = cv2.Canny(tresh,20,100)



            im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            #cnt = findLargerContour(contours)

            if len(contours) != 0:
                x,y,w,h = cv2.boundingRect(contours[0])
                aspect_ratio = float(w)/h

                #print ("ANCHO:" + str (w))
                #print ("LARGO:" + str (h))
                #print ("DIAMETRO: " + str(aspect_ratio))
                cv2.drawContours(frame,contours, -1, (0, 255, 0), 5)

                M = cv2.moments(contours[0])
                if  M['m00'] != 0 and h > 50:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])

                    for i in range(1, 5):
                        cv2.circle(frame, (W/2, H/2), DIFF*i,(0,255,0),2) ##(,(),G.RADIUSCENTER,(),)

                    cv2.line(frame, (W/2, H/2), (cx,cy), (0,255,0),2)
                    cv2.putText(output, ".", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    cv2.circle(output,(cx, cy),1,(0,0,255),1)


            #cv2.imshow('dilate',dilate)
            #cv2.imshow('erode',erode)
            #cv2.imshow('opening',opening)
            #cv2.imshow('closing',closing)
            #cv2.imshow('edges',edges)
            #cv2.imshow('tresh',tresh)
            #cv2.imshow('gray',gray)
            #cv2.imshow('medianBlur',medianBlur)
            #cv2.imshow('bilateralFilter',bilateralFilter)
            cv2.imshow('image',output)
            cv2.imshow('frame',frame)
            #cv2.imshow('Histogram equalization',equ)
            #cv2.imshow('Histogram equalization-1',cl1)
            #cv2.imshow('Histogram equalization-2',cl2)
            #cv2.imshow('Histogram equalization-original',cl)


            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
            if k == ord(' '):
                cv2.imwrite("img_finish.jpg",img)

            # get current positions of six trackbars
            H_MIN = cv2.getTrackbarPos('H_MIN','image')
            H_MAX = cv2.getTrackbarPos('H_MAX','image')
            S_MIN = cv2.getTrackbarPos('S_MIN','image')
            S_MAX = cv2.getTrackbarPos('S_MAX','image')
            V_MIN = cv2.getTrackbarPos('V_MIN','image')
            V_MAX = cv2.getTrackbarPos('V_MAX','image')
        #else:
            #cam.set(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO,0)
            #while not cam.isOpened():
            #    cv2.waitKey(1000)
            #    print "Wait for the header again"

cv2.destroyAllWindows()
