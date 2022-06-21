# Python program for Detection of a
# specific color(blue here) using OpenCV with Python
from ast import Try
import cv2
import numpy as np

# VideoCapture (0) is used to capture the frames using a camera
cap = cv2.VideoCapture(0)

# This drives the program into an infinite loop.
while cap.isOpened():		
	# Captures the live stream frame-by-frame
	_, frame = cap.read()
	# Converts images from BGR to HSV
	hsv = cv2.cvtColor(cv2.GaussianBlur(frame,(5,5),0), cv2.COLOR_BGR2HSV)
	lower_blue = np.array([101,50,38])
	upper_blue = np.array([110,255,255])

	# Here we are defining range of bluecolor in HSV
	# This creates a mask of blue coloured
	# objects found in the frame.
	mask = cv2.inRange(hsv, lower_blue, upper_blue)

	contours,hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
	# The bitwise and of the frame and mask is done so
	# that only the blue coloured objects are highlighted
	# and stored in res
	res = cv2.bitwise_and(frame,frame, mask= mask)


	if len(contours) > 0:
		try:
			c = max(contours, key=cv2.contourArea)
			M = cv2.moments(c)

			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])

			cv2.line(frame,(cx,0),(cx,720),(255,0,0),1)
			cv2.line(frame,(0,cy),(1280,cy),(0,0,255),1)

			cv2.drawContours(frame, contours, -1, (0,255,0), 1)
		except:
			None
	cv2.imshow('frame',frame)
	cv2.imshow('mask',mask)
	cv2.imshow('res',res)
	# This displays the frame, mask
	# and res which we created in 3 separate windows.
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

# Destroys all of the HighGUI windows.
cv2.destroyAllWindows()

# release the captured frame
cap.release()
