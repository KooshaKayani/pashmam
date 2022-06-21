from gpiozero import AngularServo
from time import sleep

LeftArm = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)
RightArm = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)
Gripper = AngularServo(18, min_angle = 0 , max_angle = 180 min_pulse_width=0.0006, max_pulse_width=0.0023)

#Camera = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)
#EvacuationDoor = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)

#direction 1 for open 0 for close 
def Gripper_control(Direction):
	if Direction == 1:
		Gripper.angle = 44
		sleep(0.2)
	if Direction == 0:
		Gripper.angle = 6
		sleep(0.2)
	Gripper.angle = None

#direction 1 for up 0 for down  
def Lift_control(Direction):
	if Direction == 1:
		LeftArm.angle = -x
		RightArm.angle = x
		sleep(0.2)
	if Direction == 0:
		LeftArm.angle = x
		RightArm.angle = -x
		sleep(0.2)
	LeftArm.angle = None
	RightArm.angle = None

def Grab_Control():
	Lift_control(0)
	Gripper_control(1)
	Lift_control(1)
	Gripper_control(0)	
	
