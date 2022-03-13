#!/usr/bin/env pybricks-micropython


from pybricks.ev3devices import InfraredSensor, Motor, ColorSensor
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

# Initialize the color sensor.
L_line_sensor = ColorSensor(Port.S3)    
R_line_sensor = ColorSensor(Port.S2)

# Initialize the drive base. 
robot = DriveBase(left_motor, right_motor, wheel_diameter=58, axle_track=120)
robot.settings(turn_rate=30)
#print(robot.heading_control.pid(1,1,1,0,0,0))

# Initializing PID values 
Error = 0
Integral = 0
Derivate = 0

lastError = 0
def greenFollow(PG, Speed):
    # Calculate the deviation from the threshold.
    T_hold = 45
    RL_val = R_line_sensor.reflection()


    # Calculate the turn rate.
    turn_rate = (T_hold - RL_val )* abs(2.8-(T_hold+RL_val)/100)

    # Set the drive speed at 100 millimeters per second.
    Drive_speed = Speed - abs(turn_rate) * PG
    
    # Set the drive base speed and turn rate.
    robot.drive(Drive_speed, -turn_rate)




robot.straight(-300)

robot.turn(115)

#to go out of the rescue zone
while L_line_sensor.reflection() < 18 or R_line_sensor.reflection() < 18:
	robot.drive(70,0)
robot.stop()
robot.straight(20)
robot.turn(110)

#to find the line
while L_line_sensor.reflection() < 100 and R_line_sensor.reflection() < 100:
	greenFollow(1.5,170)
	
robot.stop()
robot.straight(40)
robot.turn(-40)
robot.straight(10)

