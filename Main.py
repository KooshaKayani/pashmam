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
left_motor = Motor(Port.D)
right_motor = Motor(Port.B)
small_motor = Motor(Port.A)
arm_motor = Motor(Port.C)

# Initialize the color sensor.
L_line_sensor = ColorSensor(Port.S2)    
R_line_sensor = ColorSensor(Port.S1)

# Initialize the Infrared sensor.
IR_sensor = InfraredSensor(Port.S4)

# Initialize the pixycam.
pixycam = I2CDevice(Port.S3, 0x54)
lampOn= [174, 193, 22, 2, 0, 0]


pixycam.write(0, bytes(lampOn))

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=43, axle_track=174)
robot.settings(turn_rate=30)




# Set the gain of the proportional line controller. This means that for every
# percentage point of light deviating from the threshold, we set the turn
# rate of the drivebase to 1.2 degrees per second.

# For example, if the light value deviates from the threshold by 10, the robot
# steers at 10*1.2 = 12 degrees per second.


def Line_follow(PG, Speed):
    # Calculate the deviation from the threshold.
    LL_val = L_line_sensor.reflection()
    RL_val = R_line_sensor.reflection()


    # Calculate the turn rate.
    turn_rate = ((LL_val-20 ) - (RL_val -10) )* abs(2.5-(LL_val+RL_val)/100)

    # Set the drive speed at 100 millimeters per second.
    Drive_speed = Speed - abs(turn_rate) * PG
    
    # Set the drive base speed and turn rate.
    robot.drive(Drive_speed, turn_rate)



#def pixy2():


def res_kit():
    small_motor.reset_angle(0)
    arm_motor.reset_angle(0)

    small_motor.run_angle(200,200)
    arm_motor.run_angle(80,140,Stop.COAST)
    robot.straight(100)
    while small_motor.angle() > -10 :
        small_motor.run(-200)
    wait(10)

    small_motor.reset_angle(0)
    small_motor.run_angle(180,230)

    while arm_motor.angle() > 1 :
        arm_motor.run(-80)

    while small_motor.angle() > 1 :
        small_motor.run(-200)
    small_motor.stop()



def obstacles():
    while IR_sensor.distance() < 13:
        robot.drive(-100,0)
    robot.turn(-76)
    robot.straight(20)
    while L_line_sensor.reflection() > 10:
        robot.drive(90,25)
    robot.turn(-50)



#finds how many greens there is so its easier to turn
def green_decision():
    ev3.speaker.beep()
    robot.stop()
    #re checking the values of the sensors
    LL_col = L_line_sensor.color()
    RL_col = R_line_sensor.color()
    ignore = False
    #reseting the distance


 ##   #if there was a black line behind the green this means that the robot should ignore it
#    while abs(robot.distance()) < 30:
#        robot.drive(-50,0)
#        
#        if L_line_sensor.reflection() < 9 and R_line_sensor.reflection() < 9:
#            ev3.speaker.play_file(SoundFile.BLACK)
#            ignore == True
#            robot.straight(150)
#
#    while robot.distance()<-1:
#        robot.drive(50,0)
 


    #Green left in front (Turning Left)
    if LL_col == Color.GREEN and RL_col != Color.GREEN:
        #to go forward until it finds the line
        while L_line_sensor.reflection() > 12:
            Line_follow(2.3,120)
        robot.straight(10)
        robot.turn(-75)
        robot.straight(46)
        return()

    #Green Right in front (Turning right)
    if RL_col == Color.GREEN and LL_col != Color.GREEN:
        #to go forward until it finds the line
        while R_line_sensor.reflection() > 9:
            Line_follow(2.3,120)
        robot.straight(10)
        robot.turn(75)
        robot.straight(46)
        return()
#        straightening(1)
#        #to go forward until it finds the line
#        while R_line_sensor.reflection() > 9:
#            robot.drive(80,0)
#        robot.straight(10)
#        robot.turn(75)
#        while R_line_sensor.reflection() < 18 :
#            robot.drive(120,0)
#        return()
    
    #Double Green in front ( Turning Back )
    if LL_col == Color.GREEN and RL_col == Color.GREEN:
        print(robot.distance())
        if robot.distance() > 40:
            robot.turn(160)
            robot.straight(50)
            
        else:
            robot.straight(50)
        return()
    
    

# Start following the line endlessly.
while True:
    res_kit()

    LL_val = L_line_sensor.reflection()
    RL_val = R_line_sensor.reflection()

    if LL_val < 11 and RL_val < 11:
        #ev3.speaker.play_file(SoundFile.BLACK)
        robot.reset()
        robot.straight(8)


    #check to see if the reflection is same as a green square 
    if LL_val in range(14,15) or RL_val in range(13,14):
        robot.straight(1)
        
        
        #change the mood from reflection to color
        LL_col = L_line_sensor.color()
        RL_col = R_line_sensor.color()
        robot.straight(5)
        #running the green turn function 
        if LL_col == Color.GREEN or RL_col == Color.GREEN:
            green_decision()
        elif RL_col == Color.BLACK and LL_col == Color.BLACK:
            robot.straight(10)
       
    print(IR_sensor.distance())
    if IR_sensor.distance() < 15 :
        obstacles()
        

        
    Line_follow(2.3,170)

