#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import InfraredSensor, Motor, ColorSensor , UltrasonicSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.hubs import EV3Brick 
from pybricks.iodevices import I2CDevice
# Initialize the EV3 Brick.
ev3 = EV3Brick()

#globlas
global TurnLeft # (takes less time to process boolean)
global TurnRight # (takes less time to process boolean)

#Initializing the adjustable values:
#(some valuse have to be adjusted based on the environment using the test programs)
global GreenMax #to adjust the range of the green turn 
global GreenMin
global WhiteMin
global BlackMax
global DriveSpeed
global ObstacleDis

DriveSpeed = 80
GreenMax = 16
GreenMin = 14
WhiteMin = 40
BlackMax = 13
ObstacleDis = 10
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
robot.settings(turn_rate=55,straight_speed=30)


#this function will be used in a loop to follow the line using custom PID
#input: speed, and prepositional gain
#output: turns the wheels
def Line_follow(PG, Speed):
    # updates the value of light sensor (the reflection)
    LL_val = L_line_sensor.reflection()
    RL_val = R_line_sensor.reflection()+5


    # Calculate the turn rate. based on a PID algorithm 
    # in depth description in the GitHub page ;)
    turn_rate = ((LL_val) - RL_val )* abs(2.5-(LL_val+RL_val)/100)

    # Set the drive speed at 100 millimeters per second.
    Drive_speed = Speed - abs(turn_rate) * PG
    
    # Set the drive base speed and turn rate.
    robot.drive(Drive_speed, turn_rate)



#turns based on the valuse of green check 
def GreenTurn():
    global DriveSpeed
    global TurnLeft
    global TurnRight
    global WhiteMin
    global BlackMax

    #Right Turn
    
    if TurnRight == True:
        while R_line_sensor.reflection()  > BlackMax:
            robot.drive(DriveSpeed,0)
        robot.straight(30)
        robot.turn(30)
        robot.straight(10)
        #robot.straight(10)
        return()

    #Left Turn
    if TurnLeft == True:		
        while L_line_sensor.reflection()  > BlackMax:
            robot.drive(DriveSpeed,0)
        robot.straight(30)
        robot.turn(-30)
        robot.straight(10)
        #robot.straight(10)
        return()	

#input: null 
#output : True or False
#this function will be used to check if there is actually a green box 
def GreenCheck():
    global TurnLeft
    global TurnRight
    global GreenMin
    global GreenMax

    TurnLeft = False #reseting the values
    TurnRight = False #reseting the values
    #to change the position and decrease the probabilities of an error
    robot.straight(1)
    # updates the value of light sensor (the reflection)
    LL_val = L_line_sensor.reflection() + 2
    RL_val = R_line_sensor.reflection() + 2

    #to break the function if there was a wrong call
    if LL_val in range(GreenMin,GreenMax) or RL_val in range(GreenMin,GreenMax):
        LL_val = L_line_sensor.color()
        RL_val = R_line_sensor.color()
    else:
        return False
    
    #Indicating which side to turn 
    if LL_val == Color.GREEN:
        TurnLeft = True
    #Indicating which side to turn 
    if RL_val == Color.GREEN:
        TurnRight = True
    
    if RL_val == True and LL_val == True :
        print("x_x") #This only happens when both sensors are on green which can cause problems we can fix it later. 
        # as this is not in the scope of the current competition 
        return False

    return True

#input None
#output None
#description: turns and looks for the can
def CanSearchAndGrab():
    robot.turn(25) #avoid the zone

    #search for the can 
    while Infra.distance() > 50 :
        print("distance to the nearest object" ,Infra.distance())
        robot.drive(15,50)
    robot.turn(10) #adjustments for th positioning

    robot.stop() # stop the movement
    robot.reset() # reset the angles 

    # grabbing the can
    while Infra.distance() > 1:
        print("Relative distance to the can:", Infra.distance())
        robot.drive(60,0)
    robot.straight(50) # Adjustments
    robot.stop() # stopping the movement 
    GrabMotor.run_time(-1000, 2000, then=Stop.HOLD, wait=True)
    # going back to the middle of the zone and getting ready to find the evacuation zone
    robot.straight(-(robot.distance()))

def evacuation():
    pixycam.write(0, bytes(data)) # Sending the configuration to the pixy cam
    # for more information check https://docs.pixycam.com/wiki/doku.php?id=wiki:v2:porting_guide#setlamp-upper-lower

    # Turning until the center of the evacuation zone is within the given range
    while pixycam.read(0,20)[8] not in range(145,160):

        robot.drive(10,-40)
        pixycam.write(0, bytes(data))
    robot.turn(10) # Adjusting the alignment

    LiftMotor.run_time(-2500, 1200, then=Stop.HOLD, wait=True) #lifting the can so that the infrared sensor can locate the evacuation zone

    # approaching the evacuation zone
    while Infra.distance() > 5:
        robot.drive(50,0)
    robot.straight(40) #extera adjustments

    robot.stop()
    
    LiftMotor.stop() #dropping the can 

    GrabMotor.run_angle(1000, 1000, then=Stop.HOLD, wait=True) #letting go of the can 
    robot.straight(10) #pushing the can 


#input None
#output None
#description: when this function is called it will try to avoid the obstacle ahead by going around it
def Obstacle():
    robot.turn(90)
    robot.drive(30,30)

#input: none
#output 0 not found 1 found
#description: making sure that the can is not in the way of the evacuation zone
def straightGrab():
    robot.stop()
    robot.settings(turn_rate=55,straight_speed=80)

    robot.straight(466) # pushing the can forward if it was in the middle

    GrabMotor.run_time(-1000, 2000, then=Stop.HOLD, wait=True) #grabbing it so that the sensor can detect it
    print("the distance to the nearest object: " ,Infra.distance()) # for debuging 

    # Rescuing if the can is in the arms or continuing to look for it
    if Infra.distance() < 10 :
        print("grabing")

        LiftMotor.run_time(-2500, 1200, then=Stop.HOLD, wait=True) #clearing the way for the infrared sensor

        # approaching the evacuation zone
        while Infra.distance() > 2:
            robot.drive(40,0)
        robot.straight(40) # final adjustments
        robot.stop()

        LiftMotor.stop() # letting go if the can 

        GrabMotor.run_angle(1000, 1000, then=Stop.HOLD, wait=True)
        robot.straight(10) #final push
        robot.straight(-460)
        return 1 # the can has been rescued

    else:
        print("not here")
        GrabMotor.run_angle(1000, 1000, then=Stop.HOLD, wait=True)
        robot.straight(-200)
        return 0



#input the location of the robot in relative to the zone
#output None
#description: to performe the search and rescue of the can 
def CanGrab(loc):
    robot.stop()
    robot.settings(turn_rate=55,straight_speed=80)

    #if the zone is in front if the silver tape
    if loc == 0:

        #looking for the can 
        result = straightGrab()
        if result == 0:
            CanSearchAndGrab()
            evacuation()

        robot.straight(-300)

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
    #if the zone is on the left of the silver tape ( right tile )
    if loc == 1:
        #moving to the middle of the zone
        robot.turn(-84)
        robot.straight(140)
        robot.turn(84)

        #looking for the can 
        result = straightGrab()
        if result == 0:
            CanSearchAndGrab()
            evacuation()

    #if the zone is on the left of the silver tape ( left tile )
    if loc == 2:
        #moving to the middle of the zone
        robot.turn(84)
        robot.straight(140)
        robot.turn(-84)

        #looking for the can 
        result = straightGrab()
        if result == 0:
            CanSearchAndGrab()
            evacuation()
        robot.straight(-300)
        #to go out of the rescue zone
        while L_line_sensor.reflection() < 18 or R_line_sensor.reflection() < 18:
            robot.drive(-70,0)
        robot.stop()

        robot.turn(-84)

        #to find the line
        while L_line_sensor.reflection() > 18 and R_line_sensor.reflection() > 18:
            print(L_line_sensor.reflection())
            robot.drive(70,0)
        robot.stop()

        robot.turn(-40)
#input None
#output None
#description: to align itself with the silver tape
def silverAlign():
    robot.stop()
    robot.settings(turn_rate=55,straight_speed=80)
    robot.straight(10)
    robot.stop()
    while R_line_sensor.reflection() > 90 :
        right_motor.run(-100)
    right_motor.stop()
    while L_line_sensor.reflection() > 90 : # to go past the silver tape
        left_motor.run(-100)
    left_motor.stop()

    robot.straight(45)
    robot.stop()

    while R_line_sensor.reflection() < 100 :
        right_motor.run(-60)
    right_motor.stop()
    while L_line_sensor.reflection() < 100 : # to go past the silver tape
        left_motor.run(-60)
    left_motor.stop()

    while R_line_sensor.reflection() > 80 :
        right_motor.run(60)
    right_motor.stop()
    while L_line_sensor.reflection() > 80 : # to go past the silver tape
        left_motor.run(60)
    left_motor.stop()

    robot.turn(-4)
    robot.stop()

#input: none
#output: 0 : middle , 1: the right tile, 2: the left tile
#it will detect the location of the robot by using pixy and comparing the relative location of the evacuation zone
def location ():
    robot.stop()
    robot.settings(turn_rate=55,straight_speed=80)
    # Request block
    pixycam.write(0, bytes(data))
    # Read block
    block = pixycam.read(0,20)
    # Extract data
    x = block[9]*256 + block[8]
    robot.straight(200)
    print("the zone's x:" ,x)

    if x < 110 :
        print('In right tile')
        robot.straight(-200)
        return 1 
    if x > 205 :
        print('In left tile')
        robot.straight(-200)
        return 2
    if x in range(110,205):
        print("in the middle")
        robot.straight(-200)
        return(0)

while True:
    global GreenMin
    global GreenMax
    global ObstacleDis
    #to follow the line
    Line_follow(1.5,170)

    # updates the value of light sensor (the reflection)
    LL_val = L_line_sensor.reflection() + 2 #difference in the sensor value
    RL_val = R_line_sensor.reflection() + 2 #difference in the sensor value

    #looking for green range of reflection 
    if LL_val in range(GreenMin,GreenMax) or RL_val in range(GreenMin,GreenMax):
        print("might be green\n")
        if GreenCheck() == True:
            print("green detected\n")
            GreenTurn()

    #looking for an obstacle 
    # if ultra.distance() <= ObstacleDis:
    #     print("Obstacle detected\n")
    #     Obstacle()

    #performing the rescue
    if LL_val > 98 or RL_val > 98 :
        print("Aligning\n")
        silverAlign() # to straighten the robots position 
        print("Detecting the location\n")
        print("Performing rescue\n")

        # CanGrab performs the rescue and the location returns the relative postition of the robot 
        # in comparison to the evacuation zone
        CanGrab(location()) 
