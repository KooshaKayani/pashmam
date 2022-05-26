# import the necessary packages
from inspect import stack
import numpy as np
import argparse
import imutils
import cv2
def sort_contours(cnts):
	# initialize the reverse flag and sort index
	reverse = True
	i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]

	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),

		key=lambda b:b[1][i], reverse=reverse))

	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)


def draw_contour(image, c, i):
	# compute the center of the contour area and draw a circle
	# representing the center
	M = cv2.moments(c)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	# draw the countour number on the image
	cv2.putText(image, "#{}".format(i + 1), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
		1.0, (255, 255, 255), 2)
	# return the image with the contour number drawn on it
	return image

# load the image and initialize the accumulated edge image
image = cv2.imread("blob.jpg")


blured = cv2.GaussianBlur(image,(17,17),0)
img_gray = cv2.cvtColor(blured, cv2.COLOR_BGR2GRAY)

# apply binary thresholding
ret, thresh = cv2.threshold(img_gray, 120, 255, cv2.THRESH_BINARY)

contoursa, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
									
# find contours in the accumulated image, keeping only the largest
# ones
cnts = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
orig = image.copy()


# sort the contours according to the provided method
(cnts, boundingBoxes) = sort_contours(cnts)
# loop over the (now sorted) contours and draw them
for (i, c) in enumerate(cnts):
	draw_contour(image, c, i)

cv2.drawContours(image=image, contours=cnts, contourIdx=-1, color=(0, 255, 0), thickness=4, lineType=cv2.LINE_AA)
cv2.drawContours(image=image, contours=contoursa, contourIdx=-1, color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)

# show the output image
cv2.imshow("Sorted", image)
cv2.waitKey(0)