import cv2
import numpy as np
import os

recognizer=cv2.face.EigenFaceRecognizer_create()
recognizer.read('trainer/trainer3.yml')
cascadePath = 'haarcascade_frontalface_default.xml'
faceCascade=cv2.CascadeClassifier(cascadePath)

font =cv2.FONT_HERSHEY_SIMPLEX

id = 0

names=['None','Marcelo','HT','LDK']
cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

#while True:
for i in range(1,3000):
    ret,img=cam.read()
    img=cv2.flip(img,-1)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(int(minW),int(minH)),)
    for (x,y,w,h) in faces:
         cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
         id,confidence=recognizer.predict(cv2.resize(gray[y:y+h,x:x+w],(250,250)))

         if (confidence<4000):
             id =names[id]
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
print("\n [INFO]Exiting Program and cleanup stuff")

cam.release()
cv2.destroyAllWindows()
             
         
