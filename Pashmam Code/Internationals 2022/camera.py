import cv2
import numpy as np
# record from the raspberry camera
cap = cv2.VideoCapture(0)

# We need to check if camera
# is opened previously or not
if (cap.isOpened() == False): 
    print("Error reading video file")

# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
size = (frame_width, frame_height)


def filter(frame):
    blared = cv2.GaussianBlur(frame,(21,21),0)
        #adjusting the picture
    alpha =1.6
    beta = 50
    frame = cv2. addWeighted(blared, alpha, np.zeros(frame.shape, frame.dtype), gamma=1.2, beta=beta)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # apply binary thresholding
    ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    return ret, thresh


def analyzing(image):
    # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    hierarchy = hierarchy[0] # get the actual inner list of hierarchy descriptions
    #find the bigest y value and sorts them n the list in order to later use and filter out for the largest
    #y value
    coordinatesList=[]
    for component in zip(contours, hierarchy):
        currentContour = component[0]
        currentHierarchy = component[1]
        x,y,w,h = cv2.boundingRect(currentContour)
        if currentHierarchy[3] < 0 and w*h > 1000:
            coordinatesList.append(y)
    coordinatesList.sort()
    # For each contour, find the bounding rectangle and draw the parent and childe at the bottom
    for component in zip(contours, hierarchy):
        try:
            M = cv2.moments(component[0])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            currentContour = component[0]
            currentHierarchy = component[1]
            x,y,w,h = cv2.boundingRect(currentContour)
            if currentHierarchy[2] < 0 and y > coordinatesList[-1]:
                # these are the innermost child components
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),3)
                cv2.circle(frame, (cX, cY), 7, (0, 0, 255), -1)
            elif currentHierarchy[3] < 0 and y == coordinatesList[-1]:
                # these are the outermost parent components
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)   
            elif currentHierarchy[1] < 0 and y > coordinatesList[-1]:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,225),3) 
                cv2.circle(frame, (cX, cY), 7, (0, 0, 255), -1)
        except:
            None
        # draw contours on the original image
        cv2.drawContours(image=frame, contours=contours, contourIdx=-1, color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)
        
    # Display the resulting frame
    cv2.imshow('Frame',frame)


#main loop
while (True):
    ret, frame = cap.read()
    if ret == True:
        try:
           ret, thresh = filter(frame)
        except:
            print("Error while applying filter to the frame")
        
        #applying tge contours detection
        analyzing(thresh)


    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break


# When everything done, release 
# the video capture and video 
# write objects
cap.release()

# Closes all the frames
cv2.destroyAllWindows()

    

