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
result = cv2.VideoWriter('final.avi',cv2.VideoWriter_fourcc(*'MJPG'),30, size)

while (True):
	ret, frame = cap.read()
	try:
		#applying blur and gray filter
		blared = cv2.GaussianBlur(frame,(17,17),3)
		img_gray = cv2.cvtColor(blared, cv2.COLOR_BGR2GRAY)
	except:
		break
	# apply binary thresholding
	ret, thresh = cv2.threshold(img_gray, 125, 255, cv2.THRESH_BINARY)

	# detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
	contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
	hierarchy = hierarchy[0] # get the actual inner list of hierarchy descriptions

	#find the bigest y value 
	cordinatesList=[]
	for component in zip(contours, hierarchy):
		currentContour = component[0]
		currentHierarchy = component[1]

		x,y,w,h = cv2.boundingRect(currentContour)

		if currentHierarchy[3] < 0 and w*h > 1000:
			cordinatesList.append(y)

	cordinatesList.sort()
	(contours, hierarchy) = zip(*sorted(zip(contours, hierarchy),key=lambda b:b[1][1], reverse=True))
	i=0
	for component in zip(contours, hierarchy):
		

		currentContour = component[0]
		currentHierarchy = component[1]
		x,y,w,h = cv2.boundingRect(currentContour)
			# draw the countour number on the image

		if currentHierarchy[2] < 0 and y > cordinatesList[-1] and w*h > 1000:
			# these are the innermost child components
			M = cv2.moments(component[0])
			try:
				i+=1
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				cv2.putText(frame, "#{}".format(i), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,1.0, (255, 255, 255), 2)
			except:
				None

			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),3)


		elif currentHierarchy[3] < 0 and y == cordinatesList[-1]:
			# these are the outermost parent components
			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)   


		elif currentHierarchy[1] < 0 and y > cordinatesList[-1]and w*h > 1000:
			M = cv2.moments(component[0])
			try:
				i+=1
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				cv2.putText(frame, "#{}".format(i), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,1.0, (255, 255, 255), 2)
			except:
				None
			
			
			cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,225),3)

		# draw contours on the original image
		cv2.drawContours(image=frame, contours=contours, contourIdx=-1, color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)
				
	# save the results
	result.write(frame)




# When everything done, release 
# the video capture and video 
# write objects
cap.release()
result.release()

	