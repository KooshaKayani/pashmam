from curses import raw
import cv2 
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _ , raw_image = cap.read()
    raw_image = cv2.rotate(raw_image, cv2.ROTATE_90_CLOCKWISE)
    try:
        #blared = cv2.GaussianBlur(raw_image,(21,21),0)
            #adjusting the picture
        alpha =1.6
        beta = 50
        frame = cv2. addWeighted(raw_image, alpha, np.zeros(raw_image.shape, raw_image.dtype), gamma=1.2, beta=beta)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.medianBlur(gray, 13)
        cv2.imshow("gray",gray)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=30, maxRadius=90)
        detected_circles = np.round(circles[0,:]).astype("int")
        detected_circles = sorted(detected_circles , key = lambda v: [v[1], v[1]],reverse=True)
        print(detected_circles)
        i = 0
        for (x, y ,r) in detected_circles:
            i+=1
            #print(y)
            cv2.circle(raw_image, (x, y), r, (0, 0, 0), 3)
            cv2.putText(raw_image, "#{}".format(i), (x , y), cv2.FONT_HERSHEY_SIMPLEX,1.0, (255, 255, 255), 2)

    except Exception as e:
        print("what the hell", e)

    cv2.imshow('output',raw_image)
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()