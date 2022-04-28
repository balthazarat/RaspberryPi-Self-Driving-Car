import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import math

theta=0
minLineLength = 5
maxLineGap = 10
camera = cv2.VideoCapture(0)

time.sleep(10)
while(True):
    ret, image = camera.read()
    image = cv2.resize(image,(600,600))
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 85, 85)
    lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap)
    if(np.any(lines) != None):
        for x in range(0, len(lines)):
            for x1,y1,x2,y2 in lines[x]:
                cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
                theta=theta+math.atan2((y2-y1),(x2-x1))
#print(theta)GPIO pins were connected to arduino for servo steering control
    threshold=6
    if(theta>threshold):
        print("left")
    if(abs(theta)<threshold):
        print("straight")
    if(theta<-threshold):
        print("right")
    
    theta=0
    cv2.imshow("Edges",edged)
    cv2.imshow("Frame",image)
    key = cv2.waitKey(1) & 0xFF
    #image.truncate(0)
    if key == ord("q"):
        break
