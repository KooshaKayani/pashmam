from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep
factory = PiGPIOFactory()
LeftArm = AngularServo(13, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)
RightArm = AngularServo(19, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)
Gripper = AngularServo(26, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)
CameraServo = AngularServo(6, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)
boxServo = AngularServo(12, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)

Gripper.angle = None
LeftArm.angle = None
RightArm.angle = None
CameraServo.angle = None
boxServo.angle = None
# boxServo.angle=70
# sleep(1)
# boxServo.angle=0
# sleep(1)


Gripper.angle = None
LeftArm.angle = None
RightArm.angle = None
CameraServo.angle = None
boxServo.angle = None
# Gripper.angle = 6
# sleep(0.5)
# LeftArm.angle = 40
# RightArm.angle = 140
# #sleep(2)
# #Gripper.angle = 7
# sleep(1)
# Gripper.angle = 44

# LeftArm.angle = None
# RightArm.angle = None
# sleep(2)
# Gripper.angle = None
# #print(LeftArm.angle())

#direction 1 for front 0 for down 
def Camera_control(Direction):
    if Direction == 1:
        CameraServo.angle = -70
    if Direction == 0:
        CameraServo.angle = -35
    sleep(0.2)
    Gripper.angle = None

#direction 1 for open 0 for close 
def Gripper_control(Direction):
    if Direction == 1:
        for i in range(2,40):
            Gripper.angle = i
            sleep(0.01)
    if Direction == 0:
        for i in range(40,2,-1):
            Gripper.angle = i
            
    sleep(1)
    Gripper.angle = None

#direction 2 for middle 1 for up 0 for down  
def Lift_control(Direction):
    if Direction == 2:
        LeftArm.angle=80
        RightArm.angle= 225-80
        sleep(1)
    if Direction == 1:
        LeftArm.angle=40
        RightArm.angle= 225-40
        sleep(1)
    if Direction == 0:
        LeftArm.angle=225
        RightArm.angle= 0
        sleep(1)
    LeftArm.angle = None
    RightArm.angle = None

def Grab_Control():
    Lift_control(0)
    Gripper_control(1)
    Lift_control(1)
    Gripper_control(0)

# Lift_control(0)
# sleep(1)
Gripper_control(0)
sleep(1)
# Lift_control(2)
# Gripper.angle =20
# sleep(0.5)
# Gripper.angle =None
# RightArm.angle= None 
#Lift_control(2)

# Gripper_control(0)
# Lift_control(1) 	
#Camera_control(1)




#CameraServo.angle= None