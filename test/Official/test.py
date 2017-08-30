import cv2
import numpy as np


def test():
    img = cv2.VideoCapture(0)
    keep = True
    while keep:
        _,frame = img.read()
        frameR = cv2.resize(frame, (640,360))
        cv2.imshow("IMG", frameR)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            keep =   False

    cv2.destroAllWindows()
    cv2.release()

test()
