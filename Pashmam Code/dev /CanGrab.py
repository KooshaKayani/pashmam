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
# Initialize the distance sensors.
ultra = UltrasonicSensor(Port.S4)
Infra = InfraredSensor(Port.S1)
# Initialize the color sensor.
L_line_sensor = ColorSensor(Port.S3)    
R_line_sensor = ColorSensor(Port.S2)


# Initialize the drive base. 
robot = DriveBase(left_motor, right_motor, wheel_diameter=58, axle_track=120)
robot.settings(turn_rate=55,straight_speed=80)

######### Straight grab #########
robot.straight(466)
GrabMotor.run_angle(1000, -980, then=Stop.HOLD, wait=True)
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
######### END ######### 
