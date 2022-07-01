#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals
#from msilib.schema import Error
import time
import gpiozero    # Import Standard GPIO Module
# importing the required module
from simple_pid import PID
pid = PID(0.8, 0.08, 0.04, setpoint=0)
import cv2
import numpy as np
# record from the raspberry camera
cap = cv2.VideoCapture(0)

# We need to check if camera
# is opened previously or not
if (cap.isOpened() == False): 
    print("Error reading video file")

# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
size = (frame_width, frame_height)

try:
    from ADCPi import ADCPi
except ImportError:
    print("Failed to import ADCPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from ADCPi import ADCPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")




MotorB = gpiozero.PhaseEnableMotor("BOARD16", "BOARD12", pwm=True)
MotorA = gpiozero.PhaseEnableMotor("BOARD18", "BOARD11", pwm=True)

def MotorRun(motor,speed):
    if speed > 1:
        speed= 1 
    if speed < -1:
        speed = -1

    if motor == 'A':
        if speed < 0:
            MotorA.backward(speed*-1)
        else:
            MotorA.forward(speed)
    if motor == 'B':
        if speed < 0:
            MotorB.backward(speed*-1)
        else:
            MotorB.forward(speed)

def filter(frame,min):
    blared = cv2.GaussianBlur(frame,(21,21),0)
        #adjusting the picture
    alpha =1.6
    beta = 50
    frame = cv2. addWeighted(blared, alpha, np.zeros(frame.shape, frame.dtype), gamma=1.2, beta=beta)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # apply binary thresh holding
    ret, thresh = cv2.threshold(img_gray, min, 255, cv2.THRESH_BINARY)

    return frame, ret, thresh

#input the original frame and the binary thresh holding
#output detected contours and their middle point
#finds the evacuation zone and the victims within the evacuation zone. 
def analyzing(frame,image):

    DetectedObjects = []
    # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    contours, hierarchy = cv2.findContours(image=image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    hierarchy = hierarchy[0] # get the actual inner list of hierarchy descriptions

    #find the bigest y value 
    cordinatesList=[]
    for component in zip(contours, hierarchy):
        currentContour = component[0]
        currentHierarchy = component[1]

        x,y,w,h = cv2.boundingRect(currentContour)

        if currentHierarchy[3] < 0 and w*h > 1000:
            cordinatesList.append(y)

    cordinatesList.sort()
    (contours, hierarchy) = zip(*sorted(zip(contours, hierarchy),key=lambda b:b[1][1], reverse=False))

    i=0
# For each contour, find the bounding rectangle and draw the parent and childe at the bottom
    for component in zip(contours, hierarchy):
        try:
            M = cv2.moments(component[0])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            currentContour = component[0]
            currentHierarchy = component[1]
            x,y,w,h = cv2.boundingRect(currentContour)

            if currentHierarchy[2] < 0 and y > cordinatesList[-1] and w*h > 2000:
                i+=1
                # these are the innermost child components
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),3)
                cv2.putText(frame, "#{}".format(i), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,1.0, (255, 255, 255), 2)
                DetectedObjects.append([cX,cY])

            elif currentHierarchy[3] < 0 and y == cordinatesList[-1]:
                # these are the outermost parent components
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)   

            elif currentHierarchy[1] < 0 and y > cordinatesList[-1] and w*h>2000:
                i+=1
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,225),3) 
                cv2.putText(frame, "#{}".format(i), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,1.0, (255, 255, 255), 2)
                DetectedObjects.append([cX,cY])
        except Exception as e:
            print("problme in analyzing ",e)


        # draw contours on the original image
        cv2.drawContours(image=frame, contours=contours, contourIdx=-1, color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)
        
    # Display the resulting frame
    #qcv2.imshow('Frame',frame)

    return DetectedObjects


#input motor name A or B and the speed (-100,100)
#output: to the motor driver which rotates the motors

#input:
#	value, values rage, output range
#output: a value whithin the output rage in respect to the given value and range
#to change the line follow value to a usable range for the motors 
def scale (val, src, dst):
    result = (float(val - src[0]) / (src[1] - src[0]))
    result = result * (dst[1]- dst[0]) + dst[0]
    return result

#input speed 
#output speed for left and right motor
#reads the light sensor array values and then scales them and applies PID to give speed values for each motor.
def line_follow(speed):
    adc = ADCPi(0x68, 0x69, 12)
    Left_Sensor=(adc.read_voltage(1)*4+adc.read_voltage(2)*2+adc.read_voltage(3))
    Right_Sensor=(adc.read_voltage(5)+adc.read_voltage(6)*2+adc.read_voltage(7)*4)
    Line_pos= scale(Left_Sensor-Right_Sensor,(-2,2),(-100,100))
    control = pid(Line_pos)
    print(Line_pos)
    print(control)
    MotorA_PWM = scale(control,(0,-100),(speed,speed*-1))
    MotorB_PWM = scale(control,(0,100),(speed,speed*-1))
    return MotorA_PWM , MotorB_PWM

while True:
    

    ret, frame = cap.read()
    if ret == True:
        try:
            contrast, ret, thresh = filter(frame,min=140)
            ObjectLocation = analyzing(contrast,thresh)
            ObjectPID = (contrast.shape[1]/2)-ObjectLocation[0][0]
            #print(ObjectPID)    
            
            MotorA_PWM = scale(ObjectPID,(-320,320),(-0.1,-0.35))
            MotorB_PWM = scale(ObjectPID,(320,-320),(-0.1,-0.35))
            MotorRun("A",MotorA_PWM)
            MotorRun("B",MotorB_PWM)
        except Exception as e:
            MotorRun("B",0)
            MotorRun("A",-0.3)
            #print("Error while applying filter to the frame: ",e)
        # Press Q on keyboard to  exit
        #if cv2.waitKey(25) & 0xFF == ord('q'):
            #break
    
