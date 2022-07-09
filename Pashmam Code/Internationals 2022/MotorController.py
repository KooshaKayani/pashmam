from gpiozero.pins.pigpio import PiGPIOFactory
import gpiozero    # Import Standard GPIO Module
from gpiozero import AngularServo
from time import sleep
factory = PiGPIOFactory()
LeftBackMotor = gpiozero.PhaseEnableMotor("BOARD12", "BOARD16", pwm=True)
RightBackMotor = gpiozero.PhaseEnableMotor("BOARD11", "BOARD18", pwm=True)

LeftFrontMotor = gpiozero.PhaseEnableMotor(7, 11, pwm=True)
RightFrontMotor = gpiozero.PhaseEnableMotor(25,9, pwm=True)
LeftBackMotor.stop()
RightBackMotor.stop()
LeftFrontMotor.stop()
RightFrontMotor.stop()
LeftArm = AngularServo(19, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)
RightArm = AngularServo(13, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)
Gripper = AngularServo(26, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)
CameraServo = AngularServo(6, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)
boxServo = AngularServo(5, min_angle=0 , max_angle=225,min_pulse_width=0.00046, max_pulse_width=0.00245, pin_factory=factory)
Gripper.angle = None
LeftArm.angle = None
RightArm.angle = None
CameraServo.angle = None
boxServo.angle = None



class MotorController:



    def __init__(self):
        self.idn = 0
        self.Cam_controll(220)
        self.Gripper = Gripper
        self.boxServo = boxServo

        self.Resc_box(0)
     

    #direction 1 for open 0 for close 
    def Resc_box( self, Direction):
        if Direction == 1:
            self.boxServo.angle = 95
        if Direction == 0:
            self.boxServo.angle = 0     
        sleep(0.9)
        self.boxServo.angle = None

    #direction 1 for open 0 for close 
    def Gripper_control( self, Direction):
        if Direction == 1:
            for i in range(2,40):
                self.Gripper.angle = i
                sleep(0.01)
        if Direction == 0:
            for i in range(40,2,-1):
                self.Gripper.angle = i
                
        sleep(1.5)
        self.Gripper.angle = None

    #direction 1 for open 0 for close 
    def Cam_controll( self, ang):
        CameraServo.angle = ang
        sleep(1)
        CameraServo.angle = None

    #direction 2 for middle 1 for up 0 for down  
    def Lift_control( self, Direction):
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

    def Run_RightBackMotor(self, speed = 1):
        if speed > 0 :
            RightBackMotor.forward(speed)
        if speed < 0 :
            RightBackMotor.backward(-1*speed)
        if speed == 0:
            RightBackMotor.stop()

    def Run_LeftBackMotor(self, speed = 1):
        if speed > 0 :
            LeftBackMotor.forward(speed)
        if speed < 0 :
            LeftBackMotor.backward(-1*speed)
        if speed == 0:
            LeftBackMotor.stop()

    def Run_RightFrontMotor(self, speed = 1):
        if speed > 0 :
            RightFrontMotor.forward(speed)
        if speed < 0 :
            RightFrontMotor.backward(-1*speed)
        if speed == 0:
            RightFrontMotor.stop()

    def Run_LeftFrontMotor(self, speed = 1):
        if speed > 0 :
            LeftFrontMotor.forward(speed)
        if speed < 0 :
            LeftFrontMotor.backward(-1*speed)
        if speed == 0:
            LeftFrontMotor.stop()

   
    def MotorRun(self, motor,speed):
        if speed > 1:
            speed = 1 
        if speed < -1:
            speed = -1

        if motor == 'Left':
            if speed < 0:
                LeftFrontMotor.backward(speed*-1)
                LeftBackMotor.backward(speed*-1)
                
            else:
                LeftFrontMotor.forward(speed)
                LeftBackMotor.forward(speed)

        if motor == 'Right':
            if speed < 0:
                RightFrontMotor.backward(speed*-1)
                RightBackMotor.backward(speed*-1)

            else:
                RightFrontMotor.forward(speed)
                RightBackMotor.forward(speed)
                
    def Turn(self, Direction, Duration, speed ):


        if Direction == 'L':
            self.MotorRun("Left",-speed)
            self.MotorRun("Right",speed)

            
            sleep(Duration)

        elif Direction == 'R':

            self.MotorRun("Right",-speed)
            self.MotorRun("Left",speed)

            sleep(Duration)


        self.MotorRun("Left",0)
        self.MotorRun("Right",0)
        sleep(0.1)

    def stopAll(self):
        RightBackMotor.stop()
        LeftBackMotor.stop()
        RightFrontMotor.stop()
        LeftFrontMotor.stop()

        LeftArm.angle = None
        RightArm.angle = None
        self.Gripper.angle = None
        CameraServo.angle = None
        boxServo.angle = None