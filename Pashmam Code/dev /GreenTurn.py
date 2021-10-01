#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import InfraredSensor, Motor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.hubs import EV3Brick 
from pybricks.iodevices import I2CDevice
# Initialize the EV3 Brick.
ev3 = EV3Brick()

#globlas
global TurnLeft # (takes less time to process boolean)
global TurnRight # (takes less time to process boolean)

#Initializing the adjustable values:
#(some valuse have to be adjusted based on the environment using the test programs)
global GreenMax #to adjust the range of the green turn 
global GreenMin
global WhiteMin
global BlackMax
global DriveSpeed

DriveSpeed = 80
GreenMax = 16
GreenMin = 14
WhiteMin = 40
BlackMax = 13
# Initialize the motors.
left_motor = Motor(Port.C)
right_motor = Motor(Port.B)

# Initialize the color sensor.
L_line_sensor = ColorSensor(Port.S3)    
R_line_sensor = ColorSensor(Port.S2)


# Initialize the drive base. 
robot = DriveBase(left_motor, right_motor, wheel_diameter=58, axle_track=120)
robot.settings(turn_rate=55,straight_speed=30)


#this function will be used in a loop to follow the line using custom PID
#input: speed, and prepositional gain
#output: turns the wheels
def Line_follow(PG, Speed):
    # updates the value of light sensor (the reflection)
    LL_val = L_line_sensor.reflection()-3
    RL_val = R_line_sensor.reflection()


    # Calculate the turn rate. based on a PID algorithm 
	# in depth description in the GitHub page ;)
    turn_rate = ((LL_val) - RL_val )* abs(2.5-(LL_val+RL_val)/100)

    # Set the drive speed at 100 millimeters per second.
    Drive_speed = Speed - abs(turn_rate) * PG
    
    # Set the drive base speed and turn rate.
    robot.drive(Drive_speed, turn_rate)



#turns based on the valuse of green check 
def GreenTurn():
	global DriveSpeed
	global TurnLeft
	global TurnRight
	global WhiteMin
	global BlackMax

	#Right Turn
	
	if TurnRight == True:
		while R_line_sensor.reflection() > BlackMax:
			robot.drive(DriveSpeed,0)
		robot.straight(20)
		robot.turn(30)
		#robot.straight(10)
		return()

	#Left Turn
	if TurnLeft == True:		
		while L_line_sensor.reflection() > BlackMax:
			robot.drive(DriveSpeed,0)
		robot.straight(20)
		robot.turn(-30)
		#robot.straight(10)
		return()	

#input: null 
#output : True or False
#this function will be used to check if there is actually a green box 
def GreenCheck():
	global TurnLeft
	global TurnRight
	global GreenMin
	global GreenMax

	TurnLeft = False #reseting the values
	TurnRight = False #reseting the values
	#to change the position and decrease the probabilities of an error
	robot.straight(1)
	# updates the value of light sensor (the reflection)
	LL_val = L_line_sensor.reflection()
	RL_val = R_line_sensor.reflection() - 1

	#to break the function if there was a wrong call
	if LL_val in range(GreenMin,GreenMax) or RL_val in range(GreenMin,GreenMax):
		LL_val = L_line_sensor.color()
		RL_val = R_line_sensor.color() 
	else:
		return False
	
	#Indicating which side to turn 
	if LL_val == Color.GREEN:
		TurnLeft = True
	#Indicating which side to turn 
	if RL_val == Color.GREEN:
		TurnRight = True
	
	if RL_val == True and LL_val == True :
		print("x_x") #This only happens when both sensors are on green which can cause problems we can fix it later.
		return False

	return True




while True:
	global GreenMin
	global GreenMax
	#to follow the line
	Line_follow(1.5,170)

	# updates the value of light sensor (the reflection)
	LL_val = L_line_sensor.reflection()
	RL_val = R_line_sensor.reflection() - 1 #difference in the sencor value
	
	if LL_val in range(GreenMin,GreenMax) or RL_val in range(GreenMin,GreenMax):
		if GreenCheck() == True:
			GreenTurn()


