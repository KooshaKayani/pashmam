#!/usr/bin/env pybricks-micropython
from os import system
from pybricks.ev3devices import InfraredSensor, Motor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.hubs import EV3Brick 
from pybricks.iodevices import I2CDevice
from time import sleep
# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the color sensor.
L_line_sensor = ColorSensor(Port.S3)    
R_line_sensor = ColorSensor(Port.S2)

while True:
	_ = system('clear')
	print ("Left: ", L_line_sensor.reflection(),"	Right: ", R_line_sensor.reflection())\
	
	sleep(0.1)

