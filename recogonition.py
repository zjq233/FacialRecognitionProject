# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:07:43 2019

@author: Administrator
"""

import cv2,math
import numpy as np
import os
from PIL import Image
from yuchuli import  Distance,takeSecond, ScaleRotateTranslate,CropFace
cascadePath = 'haarcascade_frontalface_default.xml'
faceCascade=cv2.CascadeClassifier(cascadePath)
eyeCascade= cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
recognizer=cv2.face.EigenFaceRecognizer_create()
recognizer.read('trainer1.yml')

font =cv2.FONT_HERSHEY_SIMPLEX
id = 0
names=['None','Marcelo','HT','LDK','CJY']
cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)
dict={'Marcele':0,'HT':0,'LDK':0,'CJY':0}
count =0 
for i in range(1,3000):
    ret,img=cam.read()
    img=cv2.flip(img,-1)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(int(minW),int(minH)),)
    for (x,y,w,h) in faces:
         if len(faces)==1:
             cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
             face_numpy=img[y:y+h,x:x+w]
             dst = cv2.equalizeHist(face_numpy)
             rows,cols= face_numpy.shape
             eyes = eyeCascade.detectMultiScale(dst)
             eye=[]
             if len(eyes)==2:
                 count +=1
                 PIL_img=Image.fromarray(face_numpy.astype('uint8')).convert('L')
                 eye.append([ math.floor((eyes[0,0]+eyes[0,2]/2)), math.floor((eyes[0,1]+eyes[0,3]/2))])
                 eye.append([ math.floor((eyes[1,0]+eyes[1,2]/2)), math.floor((eyes[1,1]+eyes[1,3]/2))]) 
                 eye.sort(key=takeSecond)
                 img1=CropFace(PIL_img, eye[0], eye[1], offset_pct=(0.2,0.2), dest_sz=(200,200))
                 img2 = np.array(img1,'uint8')
                 id,confidence=recognizer.predict(img2)
                 if (confidence<4000):
                     id =names[id]
                     dict[id] = dict[id]+1
                     confidence=' {0}%'.format(round(confidence,2))
                     print(confidence)
                     print(id)
                 else:
                    id ='unknow'
                    print(confidence)
         
                 cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,255),2)
                 cv2.putText(img,str(confidence),(x+5,y+h-5),font,1,(255,255,0),1)
    cv2.namedWindow('video',0)
    cv2.resizeWindow('video',640,480)
    cv2.imshow('video',img)
    k = cv2.waitKey(100)&0xff
    if k==27:
        break
    elif count >=100:
        print(dict)
        #motor.forward(5,500)
        #count =0
        break