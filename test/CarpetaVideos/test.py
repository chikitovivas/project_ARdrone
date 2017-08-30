import cv2
import sys, time, os
import numpy as np

def showVideos():
    i = 0
    cont_frames = 1
    while i <= 3:
        img = cv2.VideoCapture("videos_neg/Video"+str(i)+".avi")
        flag = True

        while flag:
            flag,frame = img.read()

            if flag:
                gray = gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                resized_image = cv2.resize(gray, (100, 100))
                #cv2.imshow("Video",resized_image)
                cont_frames += 1
                cv2.imwrite("imgs"+str(i)+"/"+str(cont_frames)+".jpg",resized_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):   flag =   False
        i += 1
        #cv2.destroyAllWindows()
        print("Cantidad frames:", str(cont_frames))

def create_pos_n_neg():
    for file_type in ['neg']:

        for img in os.listdir(file_type):

            #if file_type == 'pos':
            #    line = file_type+'/'+img+' 1 0 0 50 50\n'
            #    with open('info.dat','a') as f:
            #        f.write(line)
            if file_type == 'neg':
                line = file_type+'/'+img+'\n'
                with open("bg.txt",'a') as f:
                    f.write(line)

def changeNumbers():
    i = 382
    cont = 2755
    while i <= 5702:
        try:
            img = cv2.imread("neg/"+str(i)+".jpg")

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            resized_image = cv2.resize(gray, (100, 100))

            cv2.imwrite("neg/"+str(cont)+".jpg",resized_image)
            i += 1
            cont += 1
        except:
            print("No hay foto")
            i += 1

def changeNumbersInfo():
    i = 1
    cont = 2330
    while i <= 362:
        try:
            img = cv2.imread("neg/"+str(i)+".jpg")

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            resized_image = cv2.resize(gray, (100, 100))

            cv2.imwrite("neg/"+str(cont)+".jpg",resized_image)
            i += 1
            cont += 1
        except:
            print("No hay foto")
            i += 1
#showVideos()
create_pos_n_neg()
#changeNumbers()
