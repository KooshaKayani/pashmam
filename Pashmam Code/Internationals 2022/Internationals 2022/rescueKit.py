# Python program for Detection of a
# specific color(blue here) using OpenCV with Python
import cv2
import numpy as np

# Webcamera no 0 is used to capture the framessudo su

cap = cv2.VideoCapture(0)

# This drives the program into an infinite loop.
while cap.isOpened():		
    # Captures the live stream frame-by-frame
    _, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    # Converts images from BGR to HSV
    blared = cv2.GaussianBlur(frame,(21,21),0)
    hsv = cv2.cvtColor(blared, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([85,120,90])
    upper_blue = np.array([125,225,255])

    # Here we are defining range of bluecolor in HSV
    # This creates a mask of blue coloured
    # objects found in the frame.
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
 
    cv2.drawContours(image=frame, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    # The bitwise and of the frame and mask is done so
    # that only the blue coloured objects are highlighted
    # and stored in res
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    if len(contours) > 0:
        try:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            x,y,w,h = cv2.boundingRect(c)
            print(cY)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)   
     

        except Exception as e:
            print("problme in analyzing ",e)

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


