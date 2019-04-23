# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
from picamera import PiCamera,Color
from picamera.array import PiRGBArray


red_min = np.array([0,128,46])

red_max = np.array([5,255,255])


red2_min = np.array([156,128,46])

red2_max = np.array([180,255,255])


green_min = np.array([35,128,46])

green_max = np.array([77,255,255])


blue_min = np.array([100,128,46])

blue_max = np.array([124,255,255])

yellow_min = np.array([15,128,46])

yellow_max = np.array([34,255,255])


black_min = np.array([0,0,0])

black_max = np.array([180,255,10])


white_min = np.array([0,0,70])

white_max = np.array([180,30,255])



COLOR_ARRAY = [[ red_min, red_max, 'red'],[ red2_min, red2_max, 'red'],[ green_min, green_max, 'green'],[ blue_min, blue_max, 'blue'],
[yellow_min, yellow_max, 'yellow'],[ black_min, black_max, 'black'],[ white_min, white_max, 'white']]


#camera=cv2.VideoCapture(0)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
camera.hflip = True
camera.vflip = True
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(2)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame=frame.array
    '''
    if ret==False:
        
        print("video is erro")'''
    #cv2.imshow('01',frame)

    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    for (color_min,coler_max,name) in COLOR_ARRAY:

        mask=cv2.inRange(hsv,color_min,coler_max)

        res = cv2.bitwise_and(frame, frame, mask=mask)

    
    mask=cv2.dilate(mask,None,iterations=25)

    ret, binary = cv2.threshold(mask,15, 255, cv2.THRESH_BINARY)

    #cv2.imshow('result',binary)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))

    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    #cv2.imshow('closed', closed)

    #erode = cv2.erode(closed, None, iterations=4)

    #cv2.imshow('erode', erode)

    dilate = cv2.dilate(closed, None, iterations=50)

    #cv2.imshow('dilate', dilate)

    
    (_,cnts, hierarchy) = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #res=_.copy()

    for con in cnts:

        x, y, w, h = cv2.boundingRect(con)
  # œ«ÂÖÀª·ÖœâÎªÊ¶±ð¶ÔÏóµÄ×óÉÏœÇ×ø±êºÍ¿í¡¢žß

        # ÔÚÍŒÏñÉÏ»­ÉÏŸØÐÎ£šÍŒÆ¬¡¢×óÉÏœÇ×ø±ê¡¢ÓÒÏÂœÇ×ø±ê¡¢ÑÕÉ«¡¢ÏßÌõ¿í¶È£©
        
    cv2.rectangle(res, (x, y), (x + w, y + h), (255, 0,0), 3)

    #cv2.imshow('01',frame)
    cv2.imshow('res',res)

    key=cv2.waitKey(1)
    rawCapture.truncate(0)
    if key==ord('q'):

        break
    
    #camera.release()

    #cv2.destroyAllWindows()
