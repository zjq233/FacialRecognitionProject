# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 23:21:42 2019

@author: Administrator
"""

import cv2,math
import numpy as np
import os
from PIL import Image

def takeSecond(elem):
    return elem[0]




def Distance(p1,p2):
  dx = p2[0] - p1[0]
  dy = p2[1] - p1[1]
  return math.sqrt(dx*dx+dy*dy)

def ScaleRotateTranslate(image, angle, center = None, new_center = None, scale = None, resample=Image.BICUBIC):
  if (scale is None) and (center is None):
    return image.rotate(angle=angle, resample=resample)
  nx,ny = x,y = center
  sx=sy=1.0
  if new_center:
    (nx,ny) = new_center
  if scale:
    (sx,sy) = (scale, scale)
  cosine = math.cos(angle)
  sine = math.sin(angle)
  a = cosine/sx
  b = sine/sx
  c = x-nx*a-ny*b
  d = -sine/sy
  e = cosine/sy
  f = y-nx*d-ny*e
  return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=resample)

def CropFace(image, eye_left=(0,0), eye_right=(0,0), offset_pct=(0.2,0.2), dest_sz = (70,70)):
  # calculate offsets in original image
  offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
  offset_v = math.floor(float(offset_pct[1])*dest_sz[1])
  # get the direction
  eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
  # calc rotation angle in radians
  rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
  # distance between them
  dist = Distance(eye_left, eye_right)
  # calculate the reference eye-width
  reference = dest_sz[0] - 2.0*offset_h
  # scale factor
  scale = float(dist)/float(reference)
  # rotate original around the left eye
  image = ScaleRotateTranslate(image, center=eye_left, angle=rotation)
  # crop the rotated image
  crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
  crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
  image = image.crop((int(crop_xy[0]), int(crop_xy[1]), int(crop_xy[0]+crop_size[0]), int(crop_xy[1]+crop_size[1])))
  # resize it
  image = image.resize(dest_sz, Image.ANTIALIAS)
  return image


eyeCascade= cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
recognizer=cv2.face.EigenFaceRecognizer_create()
recognizer.read('trainer1.yml')

font =cv2.FONT_HERSHEY_SIMPLEX
id = 0
names=['None','Marcelo','HT','LDK','CJY']
PIL_img=Image.open('User.1.3.jpg').convert('L')
img_numpy = np.array(PIL_img,'uint8')
dst = cv2.equalizeHist(img_numpy)
rows,cols= img_numpy.shape
eyes = eyeCascade.detectMultiScale(dst)
eye=[]
if len(eyes)==2:
    eye.append([ math.floor((eyes[0,0]+eyes[0,2]/2)), math.floor((eyes[0,1]+eyes[0,3]/2))])
    eye.append([ math.floor((eyes[1,0]+eyes[1,2]/2)), math.floor((eyes[1,1]+eyes[1,3]/2))]) 
    eye.sort(key=takeSecond)
    img1=CropFace(PIL_img, eye[0], eye[1], offset_pct=(0.2,0.2), dest_sz=(200,200))
    img = np.array(img1,'uint8')
    id,confidence=recognizer.predict(img)
    if (confidence<4000):
        id =names[id]
        confidence=' {0}%'.format(round(confidence,2))
        print(confidence)
        print(id)
    else:
        id ='unknow'
        print(confidence)
cv2.putText(img_numpy,str(id),(0,30),font,1,(255,255,255),2)
cv2.putText(img_numpy,str(confidence),(0,50),font,1,(255,255,0),1)
cv2.imshow('img',img_numpy)
cv2.waitKey(0)
cv2.destroyAllWindows()