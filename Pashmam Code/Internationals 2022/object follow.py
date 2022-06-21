#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals
from pickletools import floatnl
import time
import RPi.GPIO as GPIO     # Import Standard GPIO Module

# importing the required module
import matplotlib.pyplot as plt
from simple_pid import PID
pid = PID(0.7, 0.08, 0.004, setpoint=0)
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




#initializing the motor controller
GPIO.setmode(GPIO.BOARD)      # Set GPIO mode to BCM
GPIO.setwarnings(False)
# PWM Frequency
pwmFreq = 100
# Setup Pins for motor controller
GPIO.setup(12, GPIO.OUT)    # PWM1
GPIO.setup(16, GPIO.OUT)    # DIR1

GPIO.setup(11, GPIO.OUT)    # PWM2
GPIO.setup(18, GPIO.OUT)    # DIR2

pwma = GPIO.PWM(12, pwmFreq)    # pin 18 to PWM  
pwmb = GPIO.PWM(11, pwmFreq)    # pin 13 to PWM

try:
	pwma.start(20)
	pwmb.start(20)
except:
	print("there was a problem in running the motors")

def filter(frame):
	blared = cv2.GaussianBlur(frame,(21,21),0)
		#adjusting the picture
	alpha =1.6
	beta = 50
	frame = cv2. addWeighted(blared, alpha, np.zeros(frame.shape, frame.dtype), gamma=1.2, beta=beta)
	img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# apply binary thresh holding
	ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
	return ret, thresh

#input the original frame and the binary thresh holding
#output detected contours and their middle point
#finds the evacuation zone and the victims within the evacuation zone. 
def analyzing(frame,image):


#input motor name A or B and the speed (-100,100)
#output: to the motor driver which rotates the motors
def runMotor(motor, spd):
	DIR = GPIO.HIGH
	# applying a limit to prevent out of range speed
	# and changing the negative numbers to positive and backwards direction.
	if spd > 100:
		spd = 100

	if spd < -100:
		spd=-100

	if spd < 0:
		spd=spd*-1
		DIR = GPIO.LOW

	# sending the data to motor driver board.
	if(motor == "B"):
		GPIO.output(16, DIR)
		pwma.ChangeDutyCycle(spd)

	elif(motor == "A"):
		GPIO.output(18, DIR)
		pwmb.ChangeDutyCycle(spd)


min_speed = 0
max_speed = 50
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

def main():

	while True:

		#A, B = line_follow(25)

		#3runMotor("A",A)
		#runMotor("B",B)
		#line_graph.append(Left_Sensor-Right_Sensor)
		ret, frame = cap.read()
		if ret == True:
			try:
				ret, thresh = filter(frame)
			except:
				print("Error while applying filter to the frame")
			
			#applying tge contours detection
			analyzing(frame,thresh)


		# Press Q on keyboard to  exit
		if cv2.waitKey(25) & 0xFF == ord('q'):
			break
	


main()