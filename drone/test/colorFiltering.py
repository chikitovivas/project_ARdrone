import cv2
import numpy as np
import time

"""H_MIN = 0
H_MAX = 255
S_MIN = 0
S_MAX = 255
V_MIN = 0
V_MAX = 255"""


H_MIN = 50
H_MAX = 90
S_MIN = 50
S_MAX = 180
V_MIN = 40
V_MAX = 220

W = 640
H = 360
ERROR = 50
DIFF = H/7

lower = np.array([10,69,139],dtype = "uint8")
upper = np.array([100,133,205], dtype = "uint8")

#cam = cv2.VideoCapture(0)
cam = cv2.VideoCapture("/home/chikitovivas/Descargas/Python-control-dron/drone/Videos/Video14.avi")

def nothing(x):
    pass

def findLargerContour(cnts):
    if cnts != []:
        largest_contour = cnts[0]
        for c in cnts:
            if cv2.contourArea(c) > cv2.contourArea(largest_contour):
                largest_contour = c
        return largest_contour
    else:
        return cnts

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('H_MIN','image',H_MIN,H_MAX,nothing)
cv2.createTrackbar('H_MAX','image',V_MAX,H_MAX,nothing)
cv2.createTrackbar('S_MIN','image',S_MIN,S_MAX,nothing)
cv2.createTrackbar('S_MAX','image',V_MAX,S_MAX,nothing)
cv2.createTrackbar('V_MIN','image',V_MIN,V_MAX,nothing)
cv2.createTrackbar('V_MAX','image',V_MAX,V_MAX,nothing)
kernel = np.ones((5,5),np.uint8)
while(1):
    while not cam.isOpened():
        cam = cv2.VideoCapture("/home/chikitovivas/Descargas/Python-control-dron/drone/Videos/Video6.avi")
        cv2.waitKey(1000)
        print ("Wait for the header")

    while(1):
        time.sleep(0.1)
        flag,frame = cam.read()
        #frame = cv2.imread("img_start.jpg")
        #flag = True
        img = frame
        HThird = H/3

        if(flag):
            frame = cv2.resize(frame,(W,H))
            HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(HSV, np.array([H_MIN,S_MIN,V_MIN]), np.array([H_MAX,S_MAX,V_MAX]))
            output = cv2.bitwise_and(frame, frame, mask = mask)
            blurred = cv2.GaussianBlur(output, (5, 5), 0)

            erode = cv2.erode(blurred, kernel, iterations=2)
            dilate = cv2.dilate(erode, kernel, iterations=5)

            gray = cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY)
            _,tresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)    #Filtro de blanco y negro

            test = [tresh[0:HThird,0:W],tresh[HThird:2*(HThird),0:W],tresh[2*(HThird):3*(HThird),0:W]]
            cont = 1
            for t in test:
                im2, contours, hierarchy = cv2.findContours(t, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                cnt = findLargerContour(contours)
                #peri = cv2.arcLength(cnt, True)
                #approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
                #if len(approx) == 4:
                if cnt != []:
                    #cv2.drawContours(frame,cnt, -1, (0, 255, 0), 5)

                    M = cv2.moments(cnt)
                    if  M['m00'] != 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00']) if cont == 1 else int(M['m01']/M['m00']) + HThird if cont == 2 else int(M['m01']/M['m00']) + 2*(HThird)

                        for i in range(1, 5):
                            cv2.circle(frame, (W/2, H/2), DIFF*i,(0,255,0),2) ##(,(),G.RADIUSCENTER,(),)

                        cv2.line(frame, (W/2, H/2), (cx,cy), (0,255,0),2)
                        cv2.putText(output, ".", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        cv2.circle(output,(cx, cy),1,(0,0,255),1)
                cont += 1

            #cv2.imshow('dilate',dilate)
            #cv2.imshow('erode',erode)
            #cv2.imshow('gray',gray)
            #cv2.imshow('blurred',blurred)
            #cv2.imshow('erode',erode)
            #cv2.imshow('tresh',tresh)
            cv2.imshow('image',output)
            cv2.imshow('frame',frame)



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
