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

# Initialize the drive base. 
robot = DriveBase(left_motor, right_motor, wheel_diameter=58, axle_track=120)
robot.settings(turn_rate=55,straight_speed=80)

robot.straight(-300)a

robot.turn(150)

#to go out of the rescue zone
while L_line_sensor.reflection() < 18 or R_line_sensor.reflection() < 18:
	robot.drive(70,0)
robot.stop()
robot.straight(50)
robot.turn(75)

#to find the line
while L_line_sensor.reflection() > 18 and R_line_sensor.reflection() > 18:

	robot.drive(70,0)
robot.stop()
robot.straight(20)
robot.turn(-30)

