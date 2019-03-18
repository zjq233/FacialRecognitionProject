import cv2
import os

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade= cv2.CascadeClassifier('haarcascade_eye.xml')
face_id = input('\n enter user id end press <return>==> ')

print("\n [INFO] Initiali face capture. Look the camera and wait...")

count =0 

while(True):
    ret,img = cap.read()
    img=cv2.flip(img,-1)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
         cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
         roi_gray=gray[y:y+h,x:x+w]
         roi_color= img[y:y+h,x:x+w]
        
         eyes = eyeCascade.detectMultiScale(roi_gray)
         for (ex,ey,ew,eh) in eyes:
             cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

         count +=1

         cv2.imwrite("User."+str(face_id)+'.'+str(count)+".jpg",cv2.resize(gray[y:y+h,x:x+w],(250,250)))
         
    cv2.namedWindow('video',0)
    cv2.resizeWindow('video',640,480)
    cv2.imshow('video',img)
                     

    k = cv2.waitKey(100)&0xff
    if k==27:
        break
    elif count >=30:
        break

print("\n [INFO]Exiting Program and cleanup stuff")

cap.release()
cv2.destroyAllWindows()

