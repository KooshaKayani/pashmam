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
def Line_follow(PG, Speed):
    # Calculate the deviation from the threshold.
    LL_val = L_line_sensor.reflection()
    RL_val = R_line_sensor.reflection()


    # Calculate the turn rate.
    turn_rate = ((LL_val-5) - RL_val )* abs(2.5-(LL_val+RL_val)/100)

    # Set the drive speed at 100 millimeters per second.
    Drive_speed = Speed - abs(turn_rate) * PG
    
    # Set the drive base speed and turn rate.
    robot.drive(Drive_speed, turn_rate)



def line(kp,ki,kd,Speed):
    global Integral
    global lastError
    # Calculate the deviation from the threshold.
    LL_val = L_line_sensor.reflection()
    RL_val = R_line_sensor.reflection()


    # Calculate the turn rate.
    Error = (LL_val-36) - (RL_val - 30)
    Integral += Error
    Derivate = lastError - Error 

    turn_rate = (Error * kp) + (Integral * ki) + (Derivate * kd)
    lastError = Error

    Drive_speed = Speed - abs(turn_rate) * 1.7
    print(turn_rate)
    # Set the drive base speed and turn rate.
    robot.drive(Drive_speed, turn_rate)




while True:
    Line_follow(1.5,170)
    #line(2,0,3,170)

