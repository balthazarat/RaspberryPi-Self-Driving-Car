# **sees lines and tells direction, sees distance and tells it to stop** #

# Import required modules
from json.tool import main
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import math
from re import U
# **sees lines and tells direction, sees distance and tells it to stop** #
# Declare the GPIO settings
shouldStop = 1
distance1 = 0
direction = "stop"
TRIG = 16
ECHO = 18
MOTOR1 = 37 # LEFT
MOTOR2 = 31 # LEFT
MOTOR3 = 33 # RIGHT
MOTOR4 = 35 # RIGHT
KILLSWITCH = 15
# if distance is greater than 15 cm shouldStop == 0 else shouldStop == 1
# Declare the GPIO settings
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
GPIO.setup(MOTOR1,GPIO.OUT)
GPIO.setup(MOTOR2,GPIO.OUT)
GPIO.setup(MOTOR3,GPIO.OUT)
GPIO.setup(MOTOR4,GPIO.OUT)
GPIO.setup(KILLSWITCH,GPIO.IN)

print("Waiting For Sensor To Settle")
time.sleep(5)

# **sees lines and tells direction, sees distance and tells it to stop** #
def lineDetect():
    theta = 0
    minLineLength = 5
    maxLineGap = 10
    camera = cv2.VideoCapture(0)

    while(True):
        ret, image = camera.read()
        image = cv2.resize(image,(600,600))
        rotate = cv2.rotate(image, cv2.ROTATE_180)
        gray = cv2.cvtColor(rotate, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(rotate, (9, 9), 0)
        edged = cv2.Canny(blurred, 95, 95)
        lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap)
        if(np.any(lines) != None):
            for x in range(0, len(lines)):
                for x1,y1,x2,y2 in lines[x]:
                    cv2.line(rotate,(x1,y1),(x2,y2),(0,255,0),2)
                    theta=theta+math.atan2((y2-y1),(x2-x1))

        threshold=4
        if(theta>threshold):
            direction = "right"
            rightForward()
            leftStop()
        if(abs(theta)<threshold):
            direction = "straight"
            forward()
        if(theta<-threshold):
            direction = "left"
            leftForward()
            rightStop()
        testDistance()
        print(direction)#print(theta)GPIO pins were connected to arduino for servo steering control
        theta = 0
        # cv2.imshow("Edges",edged)
        cv2.imshow("Frame",rotate)
        key = cv2.waitKey(1) & 0xFF
        #image.truncate(0)#print(theta)GPIO pins were connected to arduino for servo steering control
        if key == ord("q"):
            break
# never needs to be called by user
def ultrasonic(): #measures distance using an ultrasonic sensor
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:

        pulse_end = time.time() 

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance
    print ("Distance:",distance,"cm")
# never needs to be called by user
def testDistance():
    distance1 = ultrasonic()
    print(distance1)
    if distance1 <= 15:
        shouldStop = 1
        direction = "stop"
        stop()
    elif distance1 > 15:
        shouldStop = 0
    print(shouldStop)
# drive #
def leftForward():
    GPIO.output(MOTOR1, True)
    GPIO.output(MOTOR2, False)
    print("leftForward")
"""def leftBackward():
    GPIO.output(MOTOR1, False)
    GPIO.output(MOTOR2, True)
    print("leftBackward")"""
def leftStop():
    GPIO.output(MOTOR1, True)
    GPIO.output(MOTOR2, True)
    print("leftStop")
def rightForward():
    GPIO.output(MOTOR3, True)
    GPIO.output(MOTOR4, False)
    print("rightForward")
"""def rightBackward():
    GPIO.output(MOTOR3, False)
    GPIO.output(MOTOR4, True)
    print("rightBackward")"""
def rightStop():
    GPIO.output(MOTOR3, True)
    GPIO.output(MOTOR4, True)
    print("rightStop")
def forward():
    leftForward()
    rightForward()
    print("forward")
"""def backward():
    leftBackward()
    rightBackward()
    print("backward")"""
def stop():
    leftStop()
    rightStop()
    print("stop")

#main#
while GPIO.input(KILLSWITCH) == 1:
    lineDetect()
#forward()
print("kill")
stop()
