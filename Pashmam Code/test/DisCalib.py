#!/usr/bin/env pybricks-micropython

# For more information and documentation 
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


ultra = UltrasonicSensor(Port.S4)
Infra = InfraredSensor(Port.S1)

while True:
	_ = system('clear')
	print(
		"Ultra sonic: " + str(ultra.distance()),"\n",
		"Infrared: " + str(Infra.distance())
	)
	sleep(0.2)
