#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from ast import Return
import os

#from msilib.schema import Error
from  time import sleep
from psutil import sensors_battery

# importing the required module
from simple_pid import PID
pid = PID(0.8, 0.08, 0.04, setpoint=0)
import cv2
import sys
import numpy as np
from VideoGet import VideoGet
from SensorController import SensorController
from MotorController import MotorController
sensors = SensorController()
Motors = MotorController()
video_getter = VideoGet(0).start()
frame = video_getter.frame

def Dis_estimate(y):
    return 1 / (((2.6441*(10**-4))*y)-0.012871)



def E_zone_location():
    raw_image = video_getter.frame
    raw_image = cv2.rotate(raw_image, cv2.ROTATE_90_CLOCKWISE)
    try:
        
        alpha =1.2
        beta = 50
        raw_image = cv2. addWeighted(raw_image, alpha, np.zeros(raw_image.shape, raw_image.dtype), gamma=1.2, beta=beta)
        gray = cv2.cvtColor(raw_image, cv2.COLOR_RGB2GRAY)
        blured = cv2.medianBlur(gray, 9)
        ret, thresh = cv2.threshold(blured, 90, 255, cv2.THRESH_BINARY)
        cv2.imshow("gray",thresh)
        blured = cv2.medianBlur(gray, 13)
        ret, thresh = cv2.threshold(blured, 30, 255, cv2.THRESH_BINARY)
        edged = cv2.Canny(blured, 190, 255)
        cv2.imshow("gray",edged)
        contours, hierarchy = cv2.findContours(image=edged, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        hierarchy = hierarchy[0] 
        Evacuation_zone= []
 
        # For each contour, find the bounding rectangle and draw the parent and childe at the bottom
        maxC = max (contours, key=cv2.contourArea)
        mx,my,mw,mh = cv2.boundingRect(maxC)

        for component in zip(contours, hierarchy):
            try:

                M = cv2.moments(component[0])
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                currentContour = component[0]
                currentHierarchy = component[1]
                x,y,w,h = cv2.boundingRect(currentContour)
          

                if currentHierarchy[2] < 0 and w*h > 20000 and cY < 160 :
                    
                    # these are the innermost child components
                    cv2.rectangle(raw_image,(x,y),(x+w,y+h),(0,0,0),3)
                    print(x,y,w,h)
                    cv2.putText(raw_image, "#{}".format(cY), (x , y), cv2.FONT_HERSHEY_SIMPLEX,1.0, (255, 255, 255), 2)

                    print(Dis_estimate(y))
                    Evacuation_zone.append([cX,cY])

                elif currentHierarchy[3] < 0 :
                    # these are the outermost parent components
                    cv2.rectangle(raw_image,(x,y),(x+w,y+h),(0,255,0),3)   

                elif currentHierarchy[1] < 0:
                    cv2.rectangle(raw_image,(x,y),(x+w,y+h),(255,255,225),3) 

            except Exception as e:
                print("problme in analyzing ",e)

            # draw contours on the original image
            cv2.drawContours(image=raw_image, contours=contours, contourIdx=-1, color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)

        cv2.imshow('output',raw_image)
        if len(Evacuation_zone) == 1:

            return True, Evacuation_zone
        return False,[]
    except:
        None
  
def E_zone_front():
    Motors.Turn("L",2.1,0.7)


def find_E_zone():
    E_zone = E_zone_location()
    print(E_zone)
    if E_zone[0] == True:
        Motors.MotorRun("Left",0.6)
        Motors.MotorRun("Right",0.6)
        print(Dis_estimate(E_zone[1][0][1]))
        sleep(Dis_estimate(E_zone[1][0][1])/18)
        Motors.stopAll()
        Motors.MotorRun("Right",0.5)
        sleep(5)
        Motors.stopAll()
        Motors.MotorRun("Left",0.5)
        Motors.MotorRun("Right",0.5)
        sleep(1)
        Motors.MotorRun("Left",-0.5)
        sleep(1.8)
        Motors.stopAll()

        Motors.MotorRun("Left",-0.5)
        Motors.MotorRun("Right",-0.5)
        sleep(2)
        Motors.stopAll()

        return

    Motors.Turn("L",2,0.6)
    E_zone = E_zone_location()
    print(E_zone)
    if E_zone[0] == True:
        return None
        #1 forward turn 

    Motors.Turn("R",1,0.6)
    E_zone = E_zone_location()
    print(E_zone)
    if E_zone[0] == True:
        return None
        #1 forward turn 

    




while True:
    try:    
        E_zone_location()
        #sleep(10)
    except Exception as e:
        print("what the hell", e)
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
