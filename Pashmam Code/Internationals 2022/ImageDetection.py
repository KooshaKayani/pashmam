import cv2
import numpy as np



#this function will analyze the image and sort the victims in order of their importance
#Returns the center and radiance of each founded victim

class PashmamAI:
	
	def __init__(self):
		None


	def Dis_estimate(self, y):
		return 1 / (((2.6441*(10**-4))*y)-0.012871)


	def Victim_finder(self, raw_image):
		detected_victims = []
		raw_image = cv2.rotate(raw_image, cv2.ROTATE_90_CLOCKWISE) # Adjusting the image 
		try:
			#adjusting the picture by applying filters to improve quality and minimize noise.
			alpha =1.6
			beta = 50
			#frame = cv2. addWeighted(raw_image, alpha, np.zeros(raw_image.shape, raw_image.dtype), gamma=1.2, beta=beta)
			gray = cv2.cvtColor(raw_image, cv2.COLOR_RGB2GRAY)  
			blurred = cv2.medianBlur(gray, 9)
			

			#Detecting circular objects and sorting them from bottom to top 
			circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 20, param1=110, param2=25, minRadius=0, maxRadius=120)
			detected_circles = np.round(circles[0,:]).astype("int")
			detected_circles = sorted(detected_circles , key = lambda v: [v[1], v[1]],reverse=True)
			print("There are ",len(detected_circles)," Circles detected")


			#Only sorting Circles that are within the range of tested data to avoid extrapolation
			i = 0
			for (x, y ,r) in detected_circles:
				if y < 345:
					i+=1
					#print(y)
					cv2.circle(raw_image, (x, y), r, (0, 0, 0), 3)
					cv2.putText(raw_image, "#{}".format(i), (x , y), cv2.FONT_HERSHEY_SIMPLEX,1.0, (255, 255, 255), 2)
					approximate_distance = self.Dis_estimate(y)
					detected_victims.append([x,y,approximate_distance])
			
			
			return detected_victims

		except Exception as e:
			print("The following error happened During Victim_finder function: ", e)

		return []



#This function will filter the frame and by using edge detection it will detect the evacuation zone 
#inputs: the frame from the video_get thread
#output True/False , center values of the evacuation zone , annotated frame
def Evacuation_zone_finder(self,raw_image):
	raw_image = cv2.rotate(raw_image, cv2.ROTATE_90_CLOCKWISE) # Adjusting the image 
	try:
		
		alpha =1.2
		beta = 50
		raw_image = cv2. addWeighted(raw_image, alpha, np.zeros(raw_image.shape, raw_image.dtype), gamma=1.2, beta=beta)
		gray = cv2.cvtColor(raw_image, cv2.COLOR_RGB2GRAY)
		blurred = cv2.medianBlur(gray, 13)
		ret, thresh = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)
		edged = cv2.Canny(blurred, 190, 255)
		contours, hierarchy = cv2.findContours(image=edged, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
		hierarchy = hierarchy[0] 
		Evacuation_zone= []

		for component in zip(contours, hierarchy):
			try:

				M = cv2.moments(component[0])
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				currentContour = component[0]
				currentHierarchy = component[1]
				x,y,w,h = cv2.boundingRect(currentContour)
		


				if currentHierarchy[2] < 0 and w*h > 20000 and cY < 160  :
					
					# these are the innermost child components
					cv2.rectangle(raw_image,(x,y),(x+w,y+h),(0,0,0),3)
					print(x,y,w,h)
					print(self.Dis_estimate(y))
					Evacuation_zone.append([cX,cY])


			except Exception as e:
				print("problme in evacuation zone finder ",e)

			# draw contours on the original image
			cv2.drawContours(image=raw_image, contours=contours, contourIdx=-1, color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)

		cv2.imshow('output',raw_image)

		if len(Evacuation_zone) == 1:
			return True, Evacuation_zone, raw_image

		return False,[]
	except:
		return False,[]