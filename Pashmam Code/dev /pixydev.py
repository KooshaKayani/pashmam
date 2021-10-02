#!/usr/bin/env pybricks-micropython

from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.hubs import EV3Brick 
from pybricks.iodevices import I2CDevice
# Initialize the EV3 Brick.
ev3 = EV3Brick()


# Initialize the pixycam.
pixycam = I2CDevice(Port.S4, 0x54)
lampOn= [174, 193, 22, 2, 0, 0]
lampOn= [174, 193, 22, 2, 1, 0]
pixycam.write(0, bytes(lampOn))
#byets for askign for sig 1 (already given to the pixy cam with PixyMon software) 
data = [174, 193, 32, 2, 1, 1]

# Request block
pixycam.write(0, bytes(data))
# Read block
block = pixycam.read(0,20)
# Extract data
sig = block[7]*256 + block[6]
x = block[9]*256 + block[8]
y = block[11]*256 + block[10]
w = block[13]*256 + block[12]
h = block[15]*256 + block[14]
print(block[6])
print(sig)
print(x,y)