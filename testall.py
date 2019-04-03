import cv2
import numpy as np
import os
import RPi.GPIO as GPIO
import time
from motor import Step_motor

def my_callback(channel):
    print('intrrupt')
    camera()
    a=1
def camera():
   
    global count
    count=0
    while True:
        
        ret,img=cam.read()
        img=cv2.flip(img,-1)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(int(minW),int(minH)),)
        for (x,y,w,h) in faces:
             cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
             id,confidence=recognizer.predict(gray[y:y+h,x:x+w])

             if (confidence<100):
                 id =names[id]
                 confidence=' {0}%'.format(round(100-confidence))
                 print(confidence)
                 print(id)
                 if id =='cjy' or 'Marcelo':
                     count=count+1
                     print (count)
             else:
                 id ='unknow'
                 confidence=' {0}%'.format(round(100-confidence))
        
             cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,255),2)
             cv2.putText(img,str(confidence),(x+5,y+h-5),font,1,(255,255,0),1)
        cv2.namedWindow('video',0)
        cv2.resizeWindow('video',640,480)
        cv2.imshow('video',img)
        k = cv2.waitKey(100)&0xff
        if k==27:
            break
        elif count >=10:
            motor.forward(5,500)
            count =0
            break

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
HRC505=18
recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = 'haarcascade_frontalface_default.xml'
faceCascade=cv2.CascadeClassifier(cascadePath)

font =cv2.FONT_HERSHEY_SIMPLEX

id = 0

names=['None','Marcelo','HT','LDK','cjy']
cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)
GPIO.setup(HRC505,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
motor=Step_motor(2,3,14,15)
GPIO.add_event_detect(18,GPIO.RISING,callback=my_callback)
global a
a=0
try:
    while (True):
        time.sleep(1)
        if a == 1:
            motor.forward(5,500)
            a=0
finally:
    print('clean')
    GPIO.cleanup()

         
