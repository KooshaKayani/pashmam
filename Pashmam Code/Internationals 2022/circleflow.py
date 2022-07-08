from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
from ast import Global
import time
import os
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
import cv2
import numpy as np
# importing the required module
import gpiozero
from simple_pid import PID
pid = PID(.9, 0.08, 0, setpoint=0)

factory = PiGPIOFactory()
LeftArm = AngularServo(19, min_pulse_width=0.0003, max_pulse_width=0.003,pin_factory=factory)
RightArm = AngularServo(13, min_pulse_width=0.0003, max_pulse_width=0.003,pin_factory=factory)
Gripper = AngularServo(26,min_pulse_width=0.0006, max_pulse_width=0.0023, pin_factory=factory)
CameraServo = AngularServo(6,min_pulse_width=0.0006, max_pulse_width=0.0023, pin_factory=factory)


Gripper.angle = None
LeftArm.angle = None
RightArm.angle = None
CameraServo.angle = None

MotorA = gpiozero.PhaseEnableMotor("BOARD12", "BOARD16", pwm=True)
MotorB = gpiozero.PhaseEnableMotor("BOARD11", "BOARD18", pwm=True)
global cap
cap = cv2.VideoCapture(0)

#direction 1 for front 0 for down 
def Camera_control(Direction):
    if Direction == 1:
        CameraServo.angle = -70
    if Direction == 0:
        CameraServo.angle = -35
    sleep(0.2)
    Gripper.angle = None


#direction 1 for open 0 for close 
def Gripper_control(Direction):
    if Direction == 1:
        for i in range(40,85):
            Gripper.angle = i
            sleep(0.01)
    if Direction == 0:
        for i in range(85,36,-1):
            Gripper.angle = i
            sleep(0.01)
    sleep(0.3)
    Gripper.angle = None

#direction 1 for up 0 for down  
def Lift_control(Direction):
    if Direction == 1:
        for i in range(0,180,2):
            LeftArm.angle = 90 - i
            RightArm.angle = -90 + i
            sleep(0.02)
        sleep(1)
    if Direction == 0:
        for i in range(0,180,2):
            LeftArm.angle = -90 + i
            RightArm.angle = 90 - i
            sleep(0.02)
        sleep(1)
    LeftArm.angle = None
    RightArm.angle = None

#input:
#	value, values rage, output range
#output: a value whithin the output rage in respect to the given value and range
#to change the line follow value to a usable range for the motors 
def scale (val, src, dst):
    result = (float(val - src[0]) / (src[1] - src[0]))
    result = result * (dst[1]- dst[0]) + dst[0]
    return result


#input the speed and the target motor
#output PMW frequency to the motordriver board 
# the if conditions ensure the speed wont exceed the [-1,1] limit for the motor driver board and the GPIO zero library 
def MotorRun(motor,speed):
    if speed > 1:
        speed = 1 
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

def filter():
    global cap
    a ,raw_image =cap.read()
    #blared = cv2.GaussianBlur(raw_image,(21,21),0)
        #adjusting the picture
    alpha =1.6
    beta = 50
    frame = cv2. addWeighted(raw_image, alpha, np.zeros(raw_image.shape, raw_image.dtype), gamma=1.2, beta=beta)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray, 13)
    cv2.imshow("gray",gray)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=30, maxRadius=90)
    detected_circles = np.round(circles[0,:]).astype("int")
    detected_circles = sorted(detected_circles , key = lambda v: [v[0], v[1]],reverse=True)

    i = 0
    for (x, y ,r) in detected_circles:
        i+=1
        print(r)
        cv2.circle(raw_image, (x, y), r, (0, 0, 0), 3)
        cv2.putText(raw_image, "#{}".format(i), (x , y), cv2.FONT_HERSHEY_SIMPLEX,1.0, (255, 255, 255), 2)
    return detected_circles

            
def vic_Grab():
    global cap		
    # Webcamera no 0 is used to capture the frames
    rescue = False
    while rescue == False:	
        
        a ,frame =cap.read()
        victms = filter()

        print(victms[0][0])
        if victms[0][1] < (frame.shape[0]*0.90):
            Error_rate =  (frame.shape[1]/2) - victms[0][0]
            print(victms[0][1])
            if Error_rate not in range(-60,60) and Error_rate > 0:
                MotorRun("A",-1*0.7)
                MotorRun("B",0)
            elif Error_rate not in range(-60,60) and Error_rate < 0:
                MotorRun("A",0)
                MotorRun("B",-1*0.7)

            else:

                MotorRun("A",-1*0.7)
                MotorRun("B",-1*0.7)
    

            
        else:
            MotorRun("A",0)
            MotorRun("B",0)
            Gripper_control(0)
            Lift_control(1)
            sleep(1)
            rescue == True
            return

while True:
    #_ , raw_image = cap.read()
    Camera_control(1)
    Lift_control(0)
    Gripper_control(1)
    sleep(1)
    try:
        vic_Grab()
    except:
        None


    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()