#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import InfraredSensor, Motor, ColorSensor , UltrasonicSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.hubs import EV3Brick 
from pybricks.iodevices import I2CDevice
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
robot.settings(turn_rate=55,straight_speed=70)

# Request block
pixycam.write(0, bytes(data))
# Read block
block = pixycam.read(0,20)
# Extract data
sig = block[7]*256 + block[6]
x = block[9]*256 + block[8]
y = block[11]*256 + block[10]
print(block[6])
print(sig)
print(x,y)

if x < 90 :
	print('In right tile')
	robot.turn(-84)
	robot.straight(140)
	robot.turn(88)
if x > 225 :
	print('In left tile')
	robot.turn(84)
	robot.straight(140)
	robot.turn(-88)
if x in range(100,215):
	print("in the middle")