#!/usr/bin/env pybricks-micropython

from os import system
from pybricks.ev3devices import InfraredSensor, Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Button, Color, SoundFile, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.hubs import EV3Brick 
from pybricks.iodevices import I2CDevice
from time import sleep
# Initialize the EV3 Brick.
ev3 = EV3Brick()



# Initialize the motors.
left_motor = Motor(Port.C)
right_motor = Motor(Port.B)
GrabMotor = Motor(Port.A)
LiftMotor = Motor(Port.D)
# Initialize the sensors.
L_line_sensor = ColorSensor(Port.S3)    
R_line_sensor = ColorSensor(Port.S2)
Infra = InfraredSensor(Port.S1)
# Initialize the pixycam.
pixycam = I2CDevice(Port.S4, 0x54)
lampOn= [174, 193, 22, 2, 0, 0]
lampOn= [174, 193, 22, 2, 1, 0]
pixycam.write(0, bytes(lampOn))
#byets for askign for sig 1 (already given to the pixy cam with PixyMon software) 
data = [174, 193, 32, 2, 1, 1]

# Initialize the drive base. 
robot = DriveBase(left_motor, right_motor, wheel_diameter=58, axle_track=120)
robot.settings(turn_rate=55,straight_speed=80)

######### Straight grab #########
robot.straight(466)
GrabMotor.run_time(-1000, 2000, then=Stop.HOLD, wait=True)
if Infra.distance() < 8 :
	print("grabing")
	LiftMotor.run_angle(2000, -230, then=Stop.HOLD, wait=True)
	while Infra.distance() > 5:
		robot.drive(30,0)
	robot.straight(20)
	robot.stop()
	LiftMotor.stop()
	GrabMotor.run_angle(1000, 1000, then=Stop.HOLD, wait=True)
	robot.straight(-460)
else:
	print("not here")
	GrabMotor.run_angle(1000, 1000, then=Stop.HOLD, wait=True)
	robot.straight(-200)
	robot.turn(25)
	while Infra.distance() > 50 :
		print(Infra.distance())
		robot.drive(15,50)
	robot.turn(10)
	robot.stop()
	robot.reset()
	while Infra.distance() > 1:
		print("Relative distance to the can:", Infra.distance())
		robot.drive(60,0)
	robot.straight(50)
	robot.stop()
	GrabMotor.run_time(-1000, 2000, then=Stop.HOLD, wait=True)
	robot.straight(-(robot.distance()))

	pixycam.write(0, bytes(data))
	while pixycam.read(0,20)[8] not in range(145,160):
		print(pixycam.read(0,20)[8])
		robot.drive(10,-40)
		pixycam.write(0, bytes(data))
	robot.turn(10)
	LiftMotor.run_time(-2500, 1200, then=Stop.HOLD, wait=True)
	while Infra.distance() > 5:
		robot.drive(50,0)
	robot.straight(40)
	robot.stop()
	LiftMotor.stop()
	GrabMotor.run_angle(1000, 1000, then=Stop.HOLD, wait=True)
	robot.straight(10)
	robot.straight(-460)


	
######### END ######### 

