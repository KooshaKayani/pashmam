from __future__ import absolute_import, division, print_function, unicode_literals
from cgitb import grey
from operator import truediv
import time
import os
from time import sleep
from tokenize import Special
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo

# importing the required module
import gpiozero
from simple_pid import PID
from ADCPi import ADCPi
#intruducing the line follow sensor


''' ----> Import everything for the color sensor and multiplexer Here <-----'''


import adafruit_tca9548a
from PiicoDev_VEML6040 import PiicoDev_VEML6040
from PiicoDev_VL53L1X import PiicoDev_VL53L1X
from time import sleep
import smbus
import tca9548a

Multiplexer = tca9548a.TCA9548A(0x70)

Multiplexer.set_channel(0,1)
Multiplexer.set_channel(1,1)

colourLeft = PiicoDev_VEML6040()
colourRight = PiicoDev_VEML6040()
# distFront = PiicoDev_VL53L1X(None, None, None, None, tca[2])
# distLeft = PiicoDev_VL53L1X(address=tca[3])
# distRight = PiicoDev_VL53L1X(address=tca[4])


IR_Array = ADCPi(0x68, 0x69, 12)

pid = PID(.9, 0.08, 0, setpoint=0)
global MotorA
global MotorB
MotorA = gpiozero.PhaseEnableMotor("BOARD12", "BOARD16", pwm=True)
MotorB = gpiozero.PhaseEnableMotor("BOARD11", "BOARD18", pwm=True)

#input:
#	value, values rage, output range
#output: a value within the output rage in respect to the given value and range
#to change the line follow value to a usable range for the motors 
def scale (val, src, dst):
	result = (float(val - src[0]) / (src[1] - src[0]))
	result = result * (dst[1]- dst[0]) + dst[0]
	return result


#input the error rate , max speed of the motors
#output speed for each motor
#process: using a PID method scales different values for each motor for tank movement for more check the youtube of teampashmam
def PID_controller(Error,Speed):

	controll = pid(Error)
	MotorA_PWM = scale(controll,(0,100),(Speed,-Speed))
	MotorB_PWM = scale(controll,(0,-100),(Speed,-Speed))  

	return MotorA_PWM,MotorB_PWM


'''You have to calibrate this first so put this in the main function only and try different durations and stuff till you know how much time we need for 90 and 180 turns and if the direction is wrong just change the -speed '''
#input direction R for right L for Left
def Turn(Direction, Duration, speed ):
	global MotorA
	global MotorB
	if Direction == 'R':
		MotorRun("A",-speed)
		
		sleep(Duration)

	elif Direction == 'L':

		MotorRun("B",-speed)
		sleep(Duration)
	else:
		print("Wrong Input")
		return

	MotorRun("A",0)
	MotorRun("B",0)
	sleep(0.1)

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



'''just a little example. you ca run this function to check for green value so you can extract the G from the RGB or something similar if you experienced something that works better the function will return true
	thresh would be the min value accepted for green so we can adjust if necessary 
	'''
def Green_check(Ls,Rs):
	if (Ls['hue'] >= 85 and Ls['sat'] >= 0.7 ) or (Rs['hue'] >=85  and Rs['sat'] >= 0.7) :
		return True
	else:
		return False
	
def Green_direction(Ls,Rs):
	direction = None
	if (Ls['hue'] >= 85 and Ls['sat'] >= 0.7 ) and (Rs['hue'] >=85  and Rs['sat'] >= 0.7) :
		print("both")#Green_turn(both)
	elif (Ls['hue'] >= 85 and Ls['sat'] >= 0.7 ):
		direction = "L"	
	elif (Rs['hue'] >=85  and Rs['sat'] >= 0.7) :
		direction = "R"	

	if direction == "L":
		Turn("L", 1.1, 0.7)
	if direction == "R":
		Turn("R", 1.1, 0.7)
	
def main():
	MotorRun("A",0)
	MotorRun("B",0)
	sleep(0.1)



	while True:
		# clear the console
		#os.system('clear')
		#reading the output form the IR sensors (the furthure the sensor from the line the greater impact)
		Left_Sensor=(IR_Array.read_voltage(8)*5+IR_Array.read_voltage(7)*3+IR_Array.read_voltage(6)*2.5+IR_Array.read_voltage(5)*0.6)
		Right_Sensor=(IR_Array.read_voltage(1)*0.6+IR_Array.read_voltage(2)*2.5+IR_Array.read_voltage(3)*3+IR_Array.read_voltage(4)*5)
		Error_rate= scale(Right_Sensor-Left_Sensor,(-10,10),(-100,100))
		#getting vaues for each motor to function 
		MotorA , MotorB = PID_controller(Error_rate,Speed=0.75)  # ----> Change the speed if cant do sharp turns decrease to 0.62 and to test start as slow as you can"

		Multiplexer.set_channel(0,1)
		Multiplexer.set_channel(1,0)

		colourL = colourLeft.readHSV()

		Multiplexer.set_channel(0,0)
		Multiplexer.set_channel(1,1)
		colourR = colourRight.readHSV()
		print(colourL,colourR)

		if Green_check(colourL,colourR) == True:
			MotorRun("A",0) #to stop the motors from moving 
			MotorRun("B",0)
			Green_direction(colourL,colourR)
			MotorRun("A",0) #to stop the motors from moving 
			MotorRun("B",0)
			MotorRun("A",-0.75) #to stop the motors from moving 
			MotorRun("B",-0.75)
			sleep(0.4)

		MotorRun("A",MotorA*-1)
		MotorRun("B",MotorB*-1)

Multiplexer.set_channel(0,1)
Multiplexer.set_channel(1,0)

colourL = colourLeft.readHSV()

Multiplexer.set_channel(0,0)
Multiplexer.set_channel(1,1)
colourR = colourRight.readHSV()
print(colourL,colourR)