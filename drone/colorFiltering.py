import cv2
import numpy as np

H_MIN = 0
H_MAX = 256
S_MIN = 0
S_MAX = 256
V_MIN = 0
V_MAX = 256

lower = np.array([10,69,139],dtype = "uint8")
upper = np.array([100,133,205], dtype = "uint8")

cam = cv2.VideoCapture(0)

def nothing(x):
    pass

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

while(1):
    _,frame = cam.read()
    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(HSV, np.array([H_MIN,S_MIN,V_MIN]), np.array([H_MAX,S_MAX,V_MAX]))
    output = cv2.bitwise_and(frame, frame, mask = mask)

    cv2.imshow('output',output)
    cv2.imshow('HSV',HSV)
    cv2.imshow('frame',frame)
    cv2.imshow('image',img)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of six trackbars
    H_MIN = cv2.getTrackbarPos('H_MIN','image')
    H_MAX = cv2.getTrackbarPos('H_MAX','image')
    S_MIN = cv2.getTrackbarPos('S_MIN','image')
    S_MAX = cv2.getTrackbarPos('S_MAX','image')
    V_MIN = cv2.getTrackbarPos('V_MIN','image')
    V_MAX = cv2.getTrackbarPos('V_MAX','image')

cv2.destroyAllWindows()
