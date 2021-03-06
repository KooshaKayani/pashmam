#!/usr/bin/env pybricks-micropython

# For more information and documentation 

from pybricks.ev3devices import InfraredSensor, Motor, ColorSensor
from pybricks.parameters import Port, Button, Color, SoundFile, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.hubs import EV3Brick 
from pybricks.iodevices import I2CDevice
from time import sleep
# Initialize the EV3 Brick.
ev3 = EV3Brick()



GrabMotor = Motor(Port.A)
LiftMotor = Motor(Port.D)
# Initialize the motors.
left_motor = Motor(Port.C)
right_motor = Motor(Port.B)

GrabMotor.run_angle(1000, 2000, then=Stop.HOLD, wait=True)
#GrabMotor.run_angle(1000, 1000, then=Stop.HOLD, wait=True)
LiftMotor.run_angle(1000, -230, then=Stop.HOLD, wait=True)
#GrabMotor.run_angle(1000, -1000, then=Stop.HOLD, wait=True)
#GrabMotor.run_angle(1000, 1000, then=Stop.HOLD, wait=True)


# while True:
# 	print(LiftMotor.angle())