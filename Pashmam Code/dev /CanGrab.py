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
# Initialize the distance sensors.
ultra = UltrasonicSensor(Port.S4)
Infra = InfraredSensor(Port.S1)
# Initialize the color sensor.
L_line_sensor = ColorSensor(Port.S3)    
R_line_sensor = ColorSensor(Port.S2)


# Initialize the drive base. 
robot = DriveBase(left_motor, right_motor, wheel_diameter=58, axle_track=120)
robot.settings(turn_rate=55,straight_speed=30)






