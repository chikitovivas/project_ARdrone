import time, sys
import cv2
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron/drone/libs')
import webcamvideostream as W

running = True
vs = W.WebcamVideoStream().start()

while running:
    try:
        # get current frame of video
        frame = vs.read()
        if not(frame is None):
            frame = cv2.resize(frame, (640, 360))
            cv2.imshow('frame', frame)
    except:
        print("pa que veas")

cam.release()
cv2.destroyAllWindows()
