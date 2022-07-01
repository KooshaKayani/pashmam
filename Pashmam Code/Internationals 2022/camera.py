import cv2
import numpy as np
import os
cap = cv2.VideoCapture(0)
# We need to check if camera
# is opened previously or not
if (cap.isOpened() == False): 
    print("Error reading video file")
    cap.release()

# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

size = (frame_width, frame_height)

# Below VideoWriter object will create
# a frame of above defined The output 
# is stored in 'filename.avi' file.
#result = cv2.VideoWriter('final.avi',cv2.VideoWriter_fourcc(*'MJPG'),10, size)

while (True):
    # clear the console
    #os.system('clear')
    ret, frame = cap.read()
    if ret == True:
        try:
            #applying blur and gray filter
            blared = cv2.GaussianBlur(frame,(21,21),0)
        except:
            break
        #adjusting the picture
        alpha =1.6
        beta = 50
        frame = cv2. addWeighted(blared, alpha, np.zeros(frame.shape, frame.dtype), gamma=1.2, beta=beta)
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # apply binary thresholding
        ret, thresh = cv2.threshold(img_gray, 140, 255, cv2.THRESH_BINARY)
        cv2.imshow('thresh',thresh)
        DetectedObjects =[]
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
        (contours, hierarchy) = zip(*sorted(zip(contours, hierarchy),key=lambda b:b[1][1], reverse=False))
        i=0
    # For each contour, find the bounding rectangle and draw the parent and childe at the bottom
        for component in zip(contours, hierarchy):
            try:
                M = cv2.moments(component[0])
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                currentContour = component[0]
                currentHierarchy = component[1]
                x,y,w,h = cv2.boundingRect(currentContour)
 
                if currentHierarchy[2] < 0 and y > cordinatesList[-1] and w*h > 2000:
                    i+=1
                    # these are the innermost child components
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),3)
                    cv2.putText(frame, "#{}".format(i), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,1.0, (255, 255, 255), 2)
                    DetectedObjects.append([cY,cY])

                elif currentHierarchy[3] < 0 and y == cordinatesList[-1]:
                    # these are the outermost parent components
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)   

                elif currentHierarchy[1] < 0 and y > cordinatesList[-1] and w*h>2000:
                    i+=1
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,225),3) 
                    cv2.putText(frame, "#{}".format(i), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,1.0, (255, 255, 255), 2)
                    DetectedObjects.append([cY,cY])
            except:
                None


            # draw contours on the original image
            cv2.drawContours(image=frame, contours=contours, contourIdx=-1, color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)
            
        # Display the resulting frame
        cv2.imshow('Frame',frame)
        print(DetectedObjects)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
        else: 
            None
                    
    # save the results
    #result.write(frame)




# When everything done, release 
# the video capture and video 
# write objects
cap.release()

# Closes all the frames
cv2.destroyAllWindows()

    

