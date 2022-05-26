
import cv2
import numpy as np
cap = cv2.VideoCapture("vid.mp4",0)
# We need to check if camera
# is opened previously or not
if (cap.isOpened() == False): 
	print("Error reading video file")

# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

size = (frame_width, frame_height)

# Below VideoWriter object will create
# a frame of above defined The output 
# is stored in 'filename.avi' file.
result = cv2.VideoWriter('filename.avi',
						cv2.VideoWriter_fourcc(*'MJPG'),
						30, size)


# Capture frame






while (True):
	ret, frame = cap.read()
	try:
		frame = cv2.GaussianBlur(frame,(5,5),0)
		img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	except:
		break
	# apply binary thresholding
	ret, thresh = cv2.threshold(img_gray, 120, 255, cv2.THRESH_BINARY)
	# visualize the binary image
	#cv2.imshow('Binary image', thresh)
	#cv2.waitKey(0)
	#cv2.imwrite('image_thres1.jpg', thresh)
	#cv2.destroyAllWindows()
	# detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
	contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
	hierarchy = hierarchy[0] # get the actual inner list of hierarchy descriptions

	cordinatesList=[]
	# For each contour, find the bounding rectangle and draw it
	for component in zip(contours, hierarchy):
		currentContour = component[0]
		currentHierarchy = component[1]

		x,y,w,h = cv2.boundingRect(currentContour)
		if currentHierarchy[3] < 0:
			cordinatesList.append(y)

	cordinatesList.sort()

	for component in zip(contours, hierarchy):
		currentContour = component[0]
		currentHierarchy = component[1]
		x,y,w,h = cv2.boundingRect(currentContour)
		if currentHierarchy[2] < 0 and y > cordinatesList[-1]:
			# these are the innermost child components
			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,225),3)
		elif currentHierarchy[3] < 0:
			if y == cordinatesList[-1]:
				# these are the outermost parent components
				cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)                                        
		# draw contours on the original image
		image_copy = frame.copy()
		cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
				
	# see the results
	#cv2.imshow('None approximation', image_copy)
	#cv2.waitKey(0)
	cv2.imwrite('contours_none.jpg', frame)
	result.write(frame)



# When everything done, release 
# the video capture and video 
# write objects
cap.release()
result.release()
	

