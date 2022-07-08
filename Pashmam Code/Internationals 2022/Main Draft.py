
import os
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo, Button
import cv2
import numpy as np
# importing the required module
import gpiozero
from simple_pid import PID
pid = PID(1, 0.01, 0.008, setpoint=0)
import time
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

from BlueCheck import BlueCheck
import sys

factory = PiGPIOFactory()


button = Button(4)



LeftArm = AngularServo(19, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)
RightArm = AngularServo(13, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)
Gripper = AngularServo(26, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)
CameraServo = AngularServo(6, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)
boxServo = AngularServo(12, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)

Gripper.angle = None
LeftArm.angle = None
RightArm.angle = None
CameraServo.angle = None
boxServo.angle = None
RightBackMotor = gpiozero.PhaseEnableMotor("BOARD12", "BOARD16", pwm=True)
LeftBackMotor = gpiozero.PhaseEnableMotor("BOARD11", "BOARD18", pwm=True)
LeftBackMotor.stop()
RightBackMotor.stop()
RightFrontMotor = gpiozero.PhaseEnableMotor(7, 11, pwm=True)
LeftFrontMotor = gpiozero.PhaseEnableMotor(25,9, pwm=True)
LeftFrontMotor.stop()
RightFrontMotor.stop()
from VideoGet import VideoGet
global video_getter
global Rescue_finder
#video_getter = VideoGet(0).start()
#frame = video_getter.frame
#Rescue_finder = BlueCheck(frame).start()


#input: null 
#output: null
#function: clears the buffer manually and then executes the program
def Restart():
	print("restarting...")
	video_getter.stop()
	try:
		Rescue_finder.stop()
	except:
		None
	Gripper.angle = None
	LeftArm.angle = None
	RightArm.angle = None
	CameraServo.angle = None
	boxServo.angle = None
	LeftFrontMotor.backward(0)
	RightFrontMotor.backward(0)
	sleep(0.2)
	sys.stdout.flush() #flushing the buffer
	exit()
	os.execl(sys.executable, 'python3.7', __file__, *sys.argv[1:])

button.when_pressed = Restart
LeftFrontMotor.stop()
RightFrontMotor.stop()

#intruducing the line follow sensor
IR_Array = ADCPi(0x68, 0x69, 12)

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
		for i in range(2,40):
			Gripper.angle = i
			sleep(0.01)
	if Direction == 0:
		for i in range(40,2,-1):
			Gripper.angle = i
			
	sleep(1)
	Gripper.angle = None

#direction 2 for middle 1 for up 0 for down  
def Lift_control(Direction):
	if Direction == 2:
		LeftArm.angle=80
		RightArm.angle= 225-80
		sleep(1)
	if Direction == 1:
		LeftArm.angle=40
		RightArm.angle= 225-40
		sleep(1)
	if Direction == 0:
		LeftArm.angle=225
		RightArm.angle= 0
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
			LeftFrontMotor.backward(speed*-1)
			LeftBackMotor.backward(speed*-1)
			
		else:
			LeftFrontMotor.forward(speed)
			LeftBackMotor.forward(speed)

	if motor == 'B':
		if speed < 0:
			RightFrontMotor.backward(speed*-1)
			RightBackMotor.backward(speed*-1)

		else:
			RightFrontMotor.forward(speed)
			RightBackMotor.forward(speed)


#input the error rate , max speed of the motors
#output speed for each motor
#process: using a PID method scales different values for each motor for tank movement for more check the youtube of teampashmam
def PID_controller(Error,Speed):

	controll = pid(Error)
	LeftFrontMotor_PWM = scale(controll,(0,-100),(Speed,-Speed))
	RightFrontMotor_PWM = scale(controll,(0,100),(Speed,-Speed))  

	return LeftFrontMotor_PWM,RightFrontMotor_PWM



def Rescue_detector():
	frame = video_getter.frame

	# Converts images from BGR to HSV
	blared = cv2.GaussianBlur(frame,(21,21),0)
	hsv = cv2.cvtColor(blared, cv2.COLOR_BGR2HSV)
	lower_blue = np.array([85,120,90])
	upper_blue = np.array([125,225,255])

	# Here we are defining range of bluecolor in HSV
	# This creates a mask of blue coloured
	# objects found in the frame.
	mask = cv2.inRange(hsv, lower_blue, upper_blue)
	contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)


	
	if len(contours) > 0:
		try:
			c = max(contours, key=cv2.contourArea)
			M = cv2.moments(c)
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			x,y,w,h = cv2.boundingRect(c)

			
			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)   
			print([w,cY])
			if w > 80 and cY > 270:
				return True,cX,cY
			return False,0,0

		except Exception as e:
			print("problme in analyzing ",e)
			return False,0,0
	
	return False,0,0
			
def ResKit_Grab():
	global video_getter
	global Rescue_finder
	# Webcamera no 0 is used to capture the frames
	rescue = False
	while rescue == False:	
		
		frame = video_getter.frame
		Rescue_finder.raw = frame
		Kit, cX, cY = Rescue_finder.result
		print(cY)
		Error_rate =  (frame.shape[1]/2) -cX
		
		if Error_rate not in range(-50,50) and Error_rate > 0:
			MotorRun("A",1*0.6)
			
		elif Error_rate not in range(-50,50) and Error_rate < 0 :
			MotorRun("B",1*0.6)
			

		else:

			MotorRun("A",1*0.5)
			MotorRun("B",1*0.5)
				

			
		if cY < 450 and cY > 370:
			LeftFrontMotor.stop()
			RightFrontMotor.stop()
			Gripper_control(0)
			Lift_control(1)
			sleep(1)
			rescue = True
			return

def main():
	#global video_getter
	#global Rescue_finder
	LeftFrontMotor.stop()
	RightFrontMotor.stop()
	sleep(0.1)
	#frame = video_getter.frame
	


	while True:
		#frame = video_getter.frame
		#Rescue_finder.raw = frame
		#print(Rescue_finder.result)
		# clear the console
		#os.system('clear')
		#reading the output form the IR sensors (the furthure the sensor from the line the greater impact)
		Left_Sensor=(IR_Array.read_voltage(8)*15+IR_Array.read_voltage(7)*8+IR_Array.read_voltage(6)*3+IR_Array.read_voltage(5))
		Right_Sensor=(IR_Array.read_voltage(1)+IR_Array.read_voltage(2)*3+IR_Array.read_voltage(3)*8+IR_Array.read_voltage(4)*15)
		print(Right_Sensor-Left_Sensor)
		Error_rate= scale(Right_Sensor-Left_Sensor,(-8,10),(-100,100))
		#getting vaues for each motor to function 
		LeftMotors , RightMotors = PID_controller(Error_rate,Speed=0.45)


		MotorRun("A",LeftMotors)
		MotorRun("B",RightMotors)



		# # Captures the live stream frame-by-frame
		# if Rescue_finder.result[0] == True:
		# 	LeftFrontMotor.stop()
		# 	RightFrontMotor.stop()

		# 	sleep(0.2)
		# 	back = time.time() + 2
		# 	while time.time() < back:
		# 		MotorRun("A",-0.65)
		# 		MotorRun("B",-0.65)

		# 	LeftFrontMotor.stop()
		# 	RightFrontMotor.stop()
		# 	sleep(0.1)
		# 	Lift_control(0)
		# 	sleep(0.5)
			
		# 	Gripper_control(1)
		# 	sleep(0.5)
		# 	ResKit_Grab()
		# 	Rescue_finder.result[0] = False
		# else:
		# 	None

		

		# This displays the frame, mask
		# and res which we created in 3 separate windows.
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			break

	# Destroys all of the HighGUI windows.
	cv2.destroyAllWindows()
	video_getter.stop()
	Rescue_finder.stop()
main()