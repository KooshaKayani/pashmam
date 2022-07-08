from threading import Thread
import cv2
import numpy as np

class BlueCheck:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, raw=None):
        self.result = [False,0,0]
        self.raw = raw
        self.frame = cv2.rotate(self.raw, cv2.ROTATE_90_CLOCKWISE)
        self.stopped = False

    def start(self):
        Thread(target=self.Search, args=()).start()
        return self

    def Search(self):
        while not self.stopped:
            
            self.frame = cv2.rotate(self.raw  , cv2.ROTATE_90_CLOCKWISE)
            # Converts images from BGR to HSV
            self.blared = cv2.GaussianBlur(self.frame,(21,21),0)
            self.hsv = cv2.cvtColor(self.blared, cv2.COLOR_BGR2HSV)
            self.lower_blue = np.array([85,120,90])
            self.upper_blue = np.array([125,225,255])

            # Here we are defining range of bluecolor in HSV
            # This creates a mask of blue coloured
            # objects found in the frame.
            self.mask = cv2.inRange(self.hsv, self.lower_blue, self.upper_blue)
            self.contours, self.hierarchy = cv2.findContours(image=self.mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)


            
            if len(self.contours) > 0:
                try:
                    self.c = max(self.contours, key=cv2.contourArea)
                    self.M = cv2.moments(self.c)
                    self.cX = int(self.M["m10"] / self.M["m00"])
                    self.cY = int(self.M["m01"] / self.M["m00"])
                    self.x,self.y,self.w,self.h = cv2.boundingRect(self.c)

                    
                    cv2.rectangle(self.frame,(self.x,self.y),(self.x+self.w,self.y+self.h),(0,255,0),3)   
                    print([self.w,self.cY])
                    
                    if self.cY > 370:
                        self.result =  [True,self.cX,self.cY]
                    

                except Exception as e:
                    print("problme in analyzing ",e)
                    self.result = [False,0,0]
                
            cv2.imshow('Rescue kit', self.frame)
        

    def stop(self):
        self.stopped = True