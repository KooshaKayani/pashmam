from __future__ import absolute_import, division, print_function, \
													unicode_literals
import time
import os

import RPi.GPIO as GPIO     # Import Standard GPIO Module
# importing the required module
import gpiozero
from simple_pid import PID
pid = PID(.9, 0.08, 0, setpoint=0)

try:
	from ADCPi import ADCPi
except ImportError:
	print("Failed to import ADCPi from python system path")
	print("Importing from parent folder instead")
	try:
		import sys
		sys.path.append('..')
		from ADCPi import ADCPi
	except ImportError:
		raise ImportError(
			"Failed to import library from parent folder")

# GPIO.setmode(GPIO.BOARD)      # Set GPIO mode to BCM
# GPIO.setwarnings(False)
MotorA = gpiozero.PhaseEnableMotor("BOARD12", "BOARD16", pwm=True)
MotorB = gpiozero.PhaseEnableMotor("BOARD11", "BOARD18", pwm=True)

# PWM Frequency
pwmFreq = 100 

# Setup Pins for motor controller
# GPIO.setup(12, GPIO.OUT)    # PWM1
# GPIO.setup(16, GPIO.OUT)    # DIR1


# GPIO.setup(11, GPIO.OUT)    # PWM2
# GPIO.setup(18, GPIO.OUT)    # DIR2



# pwma = GPIO.PWM(12, pwmFreq)    # pin 18 to PWM  
# pwmb = GPIO.PWM(11, pwmFreq)    # pin 13 to PWM

# try:
# 	pwma.start(20)
# 	pwmb.start(20)
# except:
# 	print("there was a problem running the engine")



#input motor name A or B and the speed (-100,100)
#output: to the motor driver which rotates the motors
# def runMotor(motor, spd):
# 	DIR = GPIO.HIGH
# 	# applying a limit to prevent out of range speed
# 	# and changing the negative numbers to positive and backwards direction.
# 	if spd > 100:
# 		spd = 100

# 	if spd < -100:
# 		spd=-100

# 	if spd < 0:
# 		spd=spd*-1
# 		DIR = GPIO.LOW

# 	# sending the data to motor driver board.
# 	if(motor == "B"):
# 		GPIO.output(16, DIR)
# 		pwma.ChangeDutyCycle(spd)

# 	elif(motor == "A"):
# 		GPIO.output(18, DIR)
# 		pwmb.ChangeDutyCycle(spd)


min_speed = 0
max_speed = 0.69
#input:
#	value, values rage, output range
#output: a value whithin the output rage in respect to the given value and range
#to change the line follow value to a usable range for the motors 
def scale (val, src, dst):
	result = (float(val - src[0]) / (src[1] - src[0]))
	result = result * (dst[1]- dst[0]) + dst[0]
	return result

def MotorRun(motor,speed):
	if speed > 1:
		speed = 1 
	if speed < -1:
		speed = -1

	if motor == 'A':
		if speed < 0:
			MotorA.backward(speed*-1)
		else:
			MotorA.forward(speed)
	if motor == 'B':
		if speed < 0:
			MotorB.backward(speed*-1)
		else:
			MotorB.forward(speed)

def main():

	adc = ADCPi(0x68, 0x69, 12)

	t_end = time.time() + 20
	line_graph=[]
	line_graphY=[]

	while time.time() < t_end:
		# clear the console
		#os.system('clear')

		# # read from adc channels and print to screen
		print("Channel 1: %02f" % adc.read_voltage(1))#1
		print("Channel 2: %02f" % adc.read_voltage(4))#5
		print("Channel 3: %02f" % adc.read_voltage(2))#6
		print("Channel 4: %02f" % adc.read_voltage(3))

		print("Channel 5: %02f" % adc.read_voltage(5))#8
		print("Channel 6: %02f" % adc.read_voltage(6))#9
		print("Channel 6: %02f" % adc.read_voltage(8))#9
		print("Channel 7: %02f" % adc.read_voltage(7))#13

		Left_Sensor=(adc.read_voltage(1)*5+adc.read_voltage(4)*3+adc.read_voltage(2)*2.5+adc.read_voltage(3)*0.6)
		Right_Sensor=(adc.read_voltage(5)*0.6+adc.read_voltage(6)*2.5+adc.read_voltage(8)*3+adc.read_voltage(7)*5)
		print(Left_Sensor)
		print(Right_Sensor)
		Line_pos= scale(Right_Sensor-Left_Sensor,(-10,10),(-100,100))
		controll = pid(Line_pos)
		print(controll)
		MotorA_PWM = scale(controll,(0,100),(max_speed,-max_speed))
		MotorB_PWM = scale(controll,(0,-100),(max_speed,-max_speed))     

		print(MotorA_PWM)

		MotorRun("A",MotorA_PWM*-1)
		MotorRun("B",MotorB_PWM*-1)




		#runMotor("B",MotorB_PWM)
		#line_graph.append(Left_Sensor-Right_Sensor)
	


main()