import cv2
import os
import numpy as np
from PIL import Image

path = 'dataset1'

recognizer = cv2.face.EigenFaceRecognizer_create()
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def getImagesAndLabels(path):
    width_d,height_d = 250,250
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    ids=[]
    for imagePath in imagePaths:
        PIL_img=Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(cv2.resize(img_numpy[y:y+h,x:x+w],(width_d,height_d)))
            ids.append(id)
    return faceSamples,ids

print("\n [INFO] Training faces. It will take a few seconds,Wait ...")
faces, ids = getImagesAndLabels(path)
recognizer.train(faces,np.array(ids))
recognizer.write('trainer/trainer3.yml')

print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))

      

