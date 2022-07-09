#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
import os

#from msilib.schema import Error
from  time import sleep
import gpiozero    # Import Standard GPIO Module
from gpiozero import AngularServo , Button
# importing the required module
from simple_pid import PID
pid = PID(0.8, 0.08, 0.04, setpoint=0)
import cv2
import sys
import numpy as np
from gpiozero.pins.pigpio import PiGPIOFactory
from VideoGet import VideoGet
from ImageDetection import PashmamAI
ObjectDetection = PashmamAI()
video_getter = VideoGet(0).start()
frame = video_getter.frame
factory = PiGPIOFactory()
# record from the raspberry camera

raw_image = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
frame_x_lentgh = raw_image.shape[1]
from SensorController import SensorController
from MotorController import MotorController
sensors = SensorController()
Motors = MotorController()

global captured
global Resc_num


Resc_num=  0
captured = False

def Restart():
	print("restarting...")
	video_getter.stop()

	Motors.stopAll()

	sleep(0.2)
	sys.stdout.flush() #flushing the buffer

	os.execl(sys.executable, 'python3.7', __file__, *sys.argv[1:])
button = Button(4)
button.when_pressed = Restart

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


def positioning(boundries):
    
    centered = False
    #while centered == False:
    frame = video_getter.frame

    objects = ObjectDetection.Victim_finder(frame)
    if objects == []:
        return 0 

    ObjectPID = (frame_x_lentgh/2)-objects[0][0] # Error Rate
    print("found ",len(objects)," Off by ",ObjectPID)    
    if ObjectPID > boundries or ObjectPID < -1* boundries:
        RightFrontMotor_PWM = scale(ObjectPID,((frame_x_lentgh/2),-(frame_x_lentgh/2)),(-0.7,0.7))
        LeftFrontMotor_PWM = scale(ObjectPID,(-(frame_x_lentgh/2),(frame_x_lentgh/2)),(-0.7,0.7))
        Motors.MotorRun("Right",LeftFrontMotor_PWM)
        Motors.MotorRun("Left",RightFrontMotor_PWM)
        sleep(0.5)
        return 1
    elif ObjectPID <= boundries or ObjectPID >= -1* boundries:
        centered = True
        return 1
    
    return 0
            
        
def approaching():
    global captured, Resc_num
    Not_found = 0
    captured = False

    found = False
    Motors.MotorRun("Right",0.0)
    Motors.MotorRun("Left",0.0)
    sleep(0.1)
    while found == False:
        try :
            frame = video_getter.frame
            objects = ObjectDetection.Victim_finder(frame)
            print("approaching ",objects[0][2])
            found = True
            Not_found += 1
            if Not_found == 7:
                return
        except:
            None
    
    if objects[0][2] > 35:
        Motors.MotorRun("Right",0.60)
        Motors.MotorRun("Left",0.60)
        sleep((objects[0][2]-20)/24)
    if objects[0][2] <= 35 and objects[0][2] > 16:
        Motors.MotorRun("Right",0.50)
        Motors.MotorRun("Left",0.50)
        sleep(((objects[0][2]-13)/15))
    if objects[0][2] <= 16:
        if objects[0][2] <= 13:
            Motors.MotorRun("Right",-0.40)
            Motors.MotorRun("Left",-0.40)
            sleep(0.4)
            Motors.stopAll()

        Motors.Lift_control(0)
        Motors.MotorRun("Right",0.40)
        Motors.MotorRun("Left",0.40)
        sleep(0.8)
        Motors.Gripper_control(0)
        Motors.Gripper.angle = 2
        sleep(0.2)
        Motors.MotorRun("Right",-0.50)
        Motors.MotorRun("Left",-0.50)
        sleep(0.6)
        Motors.MotorRun("Right",0.0)
        Motors.MotorRun("Left",0.0)
        sleep(0.5)
        captured = True
        Resc_num = Resc_num + 1



#input:
#	value, values rage, output range
#output: a value whithin the output rage in respect to the given value and range
#to change the line follow value to a usable range for the motors 
def scale (val, src, dst):
    result = (float(val - src[0]) / (src[1] - src[0]))
    result = result * (dst[1]- dst[0]) + dst[0]
    return result

Motors.Gripper_control(1)
Motors.Cam_controll(220)
sleep(0.3)
Motors.Cam_controll(220)
sleep(0.3)

Motors.MotorRun("Right",0.60)
Motors.MotorRun("Left",0.60)
sleep(2.5)
Motors.Turn("L",0.8,0.7)
while True:

    frame = video_getter.frame

    if video_getter.grabbed == True:
        if positioning(20) == 1 and Resc_num != 4 :
            approaching()
            if captured == True:
                Motors.Lift_control(2)
                sleep(0.2)
                Motors.Gripper_control(1)
                captured = False

        if positioning(20) != 1 and Resc_num !=4:
            if sensors.Front_Distance() < 200:
                Motors.MotorRun("Right",-0.60)
                Motors.MotorRun("Left",-0.60)
                sleep(1.5)
                Motors.stopAll()
                continue

            if sensors.Front_Distance() > 600:
                Motors.MotorRun("Right",0.60)
                Motors.MotorRun("Left",0.60)
                sleep(0.8)
                Motors.stopAll()
                continue

            if sensors.Right_Distance() < 80:
                Motors.MotorRun("Right",-0.60)
                
                Motors.MotorRun("Left",0.60)
                sleep(1)
                Motors.MotorRun("Left",0.60)
                Motors.MotorRun("Right",0.60)
                sleep(0.5)  
                continue         

            if sensors.Left_Distance() < 80:
                Motors.MotorRun("Left",0.60)
                Motors.MotorRun("Right",-0.60)
                sleep(1)
                Motors.MotorRun("Left",0.60)
                Motors.MotorRun("Right",0.60)
                sleep(0.5)
                Motors.stopAll()
                continue
            print("here")
            Motors.MotorRun("Right",0.50)
            Motors.MotorRun("Left",-0.50)
            sleep(0.7)

        if Resc_num == 4:
            while ObjectDetection.Evacuation_zone_finder(frame)[0] != True:
                Motors.MotorRun("Right",-0.50)
                Motors.MotorRun("Left",0.50)
                sleep(0.45)
                while sensors.Front_Distance() < 250:
                    Motors.MotorRun("Right",-0.60)
                    Motors.MotorRun("Left",-0.60) 

                Motors.stopAll()
                sleep(0.3)
            try:    
                print(ObjectDetection.Evacuation_zone_finder(frame))
                if ObjectDetection.Evacuation_zone_finder(frame)[0] == True:
                    ObjectPID = (frame_x_lentgh/2)-ObjectDetection.Evacuation_zone_finder(frame)[1][0][0]
                    if ObjectPID > 36 or ObjectPID < -1* 36:
                        RightFrontMotor_PWM = scale(ObjectPID,((frame_x_lentgh/2),-(frame_x_lentgh/2)),(-0.7,0.7))
                        LeftFrontMotor_PWM = scale(ObjectPID,(-(frame_x_lentgh/2),(frame_x_lentgh/2)),(-0.7,0.7))
                        Motors.MotorRun("Right",LeftFrontMotor_PWM)
                        Motors.MotorRun("Left",RightFrontMotor_PWM)
                        sleep(1)
                    
                        while sensors.Front_Distance() > 50:
                            Motors.MotorRun("Right",0.50)
                            Motors.MotorRun("Left",0.50) 
                        Motors.Turn("L",3.7,0.6)
                        sleep(0.8)
                        Motors.MotorRun("Right",-0.50)
                        Motors.MotorRun("Left",-0.50) 
                        sleep(0.8)
                        Motors.stopAll()
                        Motors.Lift_control(0)
                        Motors.Resc_box(1)
                        Motors.Resc_box(0)
                        Motors.Resc_box(1)
                        Motors.Resc_box(0)
                        Motors.Gripper_control(0)
                        Motors.Lift_control(1)



      


            except Exception as e:
                print("Error ",e)
                
    

        Motors.MotorRun("Right",0.0)
        Motors.MotorRun("Left",0.0)
        sleep(0.5)

    
   
    
