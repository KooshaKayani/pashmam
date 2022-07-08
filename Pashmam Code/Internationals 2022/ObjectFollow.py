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




def Dis_estimate(y):
    return 1 / (((2.6441*(10**-4))*y)-0.012871)

def Evacuation_zone_finder():
    raw_image = video_getter.frame
    raw_image = cv2.rotate(raw_image, cv2.ROTATE_90_CLOCKWISE)
    try:
        
        alpha =1.2
        beta = 50
        raw_image = cv2. addWeighted(raw_image, alpha, np.zeros(raw_image.shape, raw_image.dtype), gamma=1.2, beta=beta)
        gray = cv2.cvtColor(raw_image, cv2.COLOR_RGB2GRAY)
        blured = cv2.medianBlur(gray, 9)
        #ret, thresh = cv2.threshold(blured, 90, 255, cv2.THRESH_BINARY)
        #blured = cv2.medianBlur(gray, 13)
        blured = cv2.medianBlur(gray, 13)
        ret, thresh = cv2.threshold(blured, 30, 255, cv2.THRESH_BINARY)
        edged = cv2.Canny(blured, 190, 255)
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
          


                if currentHierarchy[2] < 0 and w*h > 20000 and cY < 160  :
                    
                    # these are the innermost child components
                    cv2.rectangle(raw_image,(x,y),(x+w,y+h),(0,0,0),3)
                    print(x,y,w,h)
                    print(Dis_estimate(y))
                    Evacuation_zone.append([cX,cY])

                elif currentHierarchy[3] < 0 :
                    # these are the outermost parent components
                    cv2.rectangle(raw_image,(x,y),(x+w,y+h),(0,255,0),3)   

                elif currentHierarchy[1] < 0:
                    cv2.rectangle(raw_image,(x,y),(x+w,y+h),(255,255,225),3) 

            except Exception as e:
                print("problme in evacuation zone finder ",e)

            # draw contours on the original image
            cv2.drawContours(image=raw_image, contours=contours, contourIdx=-1, color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)

        cv2.imshow('output',raw_image)
        if len(Evacuation_zone) == 1:

            return True, Evacuation_zone
        return False,[]
    except:
        return False,[]


def Victim_finder(raw_image):
    detected_victms = []
    raw_image = cv2.rotate(raw_image, cv2.ROTATE_90_CLOCKWISE)
    try:
        #blared = cv2.GaussianBlur(raw_image,(21,21),0)
            #adjusting the picture
        alpha =1.6
        beta = 50
        #frame = cv2. addWeighted(raw_image, alpha, np.zeros(raw_image.shape, raw_image.dtype), gamma=1.2, beta=beta)
        gray = cv2.cvtColor(raw_image, cv2.COLOR_RGB2GRAY)
        gray = cv2.medianBlur(gray, 9)
        
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=110, param2=25, minRadius=0, maxRadius=120)
        detected_circles = np.round(circles[0,:]).astype("int")
        detected_circles = sorted(detected_circles , key = lambda v: [v[1], v[1]],reverse=True)
        print(detected_circles)
        i = 0
        for (x, y ,r) in detected_circles:
            if y < 345:
                i+=1
                #print(y)
                cv2.circle(raw_image, (x, y), r, (0, 0, 0), 3)
                cv2.putText(raw_image, "#{}".format(i), (x , y), cv2.FONT_HERSHEY_SIMPLEX,1.0, (255, 255, 255), 2)
                aproximate_distance = Dis_estimate(y)
                detected_victms.append([x,y,aproximate_distance])
        
        
        return detected_victms
    except Exception as e:
        print("what the hell", e)
    return []

def positioning(boundries):
    
    centered = False
    #while centered == False:
    frame = video_getter.frame

    objects = Victim_finder(frame)
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
            objects = Victim_finder(frame)
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
            while Evacuation_zone_finder()[0] != True:
                Motors.MotorRun("Right",-0.50)
                Motors.MotorRun("Left",0.50)
                sleep(0.45)
                while sensors.Front_Distance() < 250:
                    Motors.MotorRun("Right",-0.60)
                    Motors.MotorRun("Left",-0.60) 

                Motors.stopAll()
                sleep(0.3)
            try:    
                print(Evacuation_zone_finder())
                if Evacuation_zone_finder()[0] == True:
                    ObjectPID = (frame_x_lentgh/2)-Evacuation_zone_finder()[1][0][0]
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

    
   
    
