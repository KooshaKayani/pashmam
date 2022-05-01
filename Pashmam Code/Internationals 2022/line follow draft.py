#!/usr/bin/env python
from tkinter import Scale
from __future__ import absolute_import, division, print_function, \
													unicode_literals
import time
import os
from turtle import right

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





min_speed = 0
max_speed = 50
#input:
#	value, values rage, output range
#output: a value whithin the output rage in respect to the given value and range
#to change the line follow value to a usable range for the motors 
def scale (val, src, dst):
	result = (float(val - src[0]) / (src[1] - src[0]))
	result = result * (dst[1]- dst[0]) + dst[0]
	return result




def main():
	'''
	Main program function
	'''

	adc = ADCPi(0x68, 0x69, 12)

	while True:

		# clear the console
		os.system('clear')

		# read from adc channels and print to screen
		print("Channel 1: %02f" % adc.read_voltage(1))
		print("Channel 2: %02f" % adc.read_voltage(2))
		print("Channel 3: %02f" % adc.read_voltage(3))
		print("Channel 4: %02f" % adc.read_voltage(4))
		print("Channel 5: %02f" % adc.read_voltage(5))
		print("Channel 6: %02f" % adc.read_voltage(6))
		print("Channel 7: %02f" % adc.read_voltage(7))

		Left_Sensor=(adc.read_voltage(1)+adc.read_voltage(2)+adc.read_voltage(3)+adc.read_voltage(4))
		Right_Sensor=(adc.read_voltage(4)+adc.read_voltage(5)+adc.read_voltage(6)+adc.read_voltage(7))

		
		Line_pos= scale(Left_Sensor-Right_Sensor,(0,1.5),(-100,100))
		
		MotorA_PWM = scale(Line_pos,(0,-100),(100,-100))
		MotorB_PWM = scale(Line_pos,(0,100),(100,-100))