import gpiozero
from gpiozero import PhaseEnableMotor
from time import sleep
from gpiozero import Button
from signal import pause

def say_hello():
    print("Hello!")

button = Button(4)

button.when_pressed = say_hello

pause()
# LeftFrontMotor = gpiozero.PhaseEnableMotor("BOARD16", "BOARD12", pwm=True)
# LeftBackMotor = gpiozero.PhaseEnableMotor("BOARD18", "BOARD11", pwm=True)



# LeftFrontMotor = gpiozero.PhaseEnableMotor(7, 11, pwm=True)
# RightFrontMotor = gpiozero.PhaseEnableMotor(25,9, pwm=True)

# #otorA = gpiozero.PhaseEnableMotor("BOARD12", "BOARD16", pwm=True)
# #MotorB = gpiozero.PhaseEnableMotor("BOARD11", "BOARD18", pwm=True)

# RightFrontMotor.forward(0.6)
# RightFrontMotor.forward(0.6)


# sleep(1)import os
# import sys
# import subprocess

# #input: null 
# #output: null
# #function: clears the buffer manually and then executes the program
# def Restart():
# 	sys.stdout.flush() #flushing the buffer
# 	subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:]) #re running the current file