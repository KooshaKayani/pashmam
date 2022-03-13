##
 # Original code from Maker's Digest
 # Edited by Koosha from team pashmam 
 # DC Motor Control with TB6612FNG SKU DRI0044 by DFROBOT
##
from time import sleep
from turtle import delay      # Import sleep from time
import RPi.GPIO as GPIO     # Import Standard GPIO Module

GPIO.setmode(GPIO.BOARD)      # Set GPIO mode to BCM
GPIO.setwarnings(False)

# PWM Frequency
pwmFreq = 100

# Setup Pins for motor controller
GPIO.setup(12, GPIO.OUT)    # PWM1
GPIO.setup(16, GPIO.OUT)    # DIR1

 
GPIO.setup(11, GPIO.OUT)    # PWM2
GPIO.setup(18, GPIO.OUT)    # DIR2



pwma = GPIO.PWM(12, pwmFreq)    # pin 18 to PWM  
pwmb = GPIO.PWM(11, pwmFreq)    # pin 13 to PWM
pwma.start(100)
pwmb.start(100)



# ## Functions
# ###############################################################################
def forward(spd):
    runMotor(0, spd, 0)
    runMotor(1, spd, 0)

# def reverse(spd):
#     runMotor(0, spd, 1)
#     runMotor(1, spd, 1)

# def turnLeft(spd):
#     runMotor(0, spd, 0)
#     runMotor(1, spd, 1)

# def turnRight(spd):
#     runMotor(0, spd, 1)
#     runMotor(1, spd, 0)

def runMotor(motor, spd, direction):
    in1 = GPIO.HIGH


    if(direction == 1):
        in1 = GPIO.LOW


    if(motor == 0):
        GPIO.output(16, in1)
        pwma.ChangeDutyCycle(spd)

    elif(motor == 1):
        GPIO.output(18, in1)
        pwmb.ChangeDutyCycle(spd)


# def motorStop():
#     GPIO.output(22, GPIO.LOW)

## Main
##############################################################################
def main(args=None):
	while True:
		forward(50)     # run motor forward


if __name__ == "__main__":
    main()
