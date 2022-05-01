import RPi.GPIO as GPIO     # Import Standard GPIO Module


class MotorDriver:
	def __init__(self, PWM1,PWM2,DIR1,DIR2):
		GPIO.setmode(GPIO.BOARD)      # Set GPIO mode to BCM
		GPIO.setwarnings(False)	
		# Setup Pins for motor controller
		GPIO.setup(PWM1, GPIO.OUT)    # PWM1
		GPIO.setup(DIR1, GPIO.OUT)    # DIR1
	
		GPIO.setup(PWM2, GPIO.OUT)    # PWM2
		GPIO.setup(DIR2, GPIO.OUT)    # DIR2

		#sets the initial speed
		# PWM Frequency
		pwmFreq = 100
		pwma = GPIO.PWM(PWM1, pwmFreq)    # pin 18 to PWM  
		pwmb = GPIO.PWM(PWM2, pwmFreq)    # pin 13 to PWM

		pwma.start(100)
		pwmb.start(100)

	def run(Direction,Speed):
		DIRA = GPIO.HIGH
		DIRB = GPIO.HIGH


		if Direction < -50:
			DIRA = GPIO.LOW
		if Direction > 50:
			DIRB = GPIO.LOW
			







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
