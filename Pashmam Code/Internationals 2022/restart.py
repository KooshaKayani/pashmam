import os
import sys
import subprocess

#input: null 
#output: null
#function: clears the buffer manually and then executes the program
def Restart():
	sys.stdout.flush() #flushing the buffer
	subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:]) #re running the current file