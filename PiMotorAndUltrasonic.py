#!/usr/bin/env python

# Import required modules
import time
import RPi.GPIO as GPIO

# Declare the GPIO settings
GPIO.setmode(GPIO.BOARD)

TRIG = 16
ECHO = 18
# set up GPIO pins

GPIO.setup(7, GPIO.OUT) # Connected to PWMA
GPIO.setup(11, GPIO.OUT) # Connected to AIN2
GPIO.setup(12, GPIO.OUT) # Connected to AIN1
GPIO.setup(13, GPIO.OUT) # Connected to STBY

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


GPIO.output(TRIG, False)
print("Waiting For Sensor To Settle")
time.sleep(2)

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
print ("Distance:",distance,"cm")
GPIO.cleanup()

# Wait 5 seconds
time.sleep(5)

# Drive the motor clockwise
GPIO.output(12, GPIO.HIGH) # Set AIN1
GPIO.output(11, GPIO.LOW) # Set AIN2

# Set the motor speed
GPIO.output(7, GPIO.HIGH) # Set PWMA

# Disable STBY (standby)
GPIO.output(13, GPIO.HIGH)

# Wait 5 seconds
time.sleep(5)

# Drive the motor counterclockwise
GPIO.output(12, GPIO.LOW) # Set AIN1
GPIO.output(11, GPIO.HIGH) # Set AIN2

# Set the motor speed
GPIO.output(7, GPIO.HIGH) # Set PWMA

# Disable STBY (standby)
GPIO.output(13, GPIO.HIGH)

# Wait 5 seconds
time.sleep(5)

# Reset all the GPIO pins by setting them to LOW
GPIO.output(12, GPIO.LOW) # Set AIN1
GPIO.output(11, GPIO.LOW) # Set AIN2
GPIO.output(7, GPIO.LOW) # Set PWMA
GPIO.output(13, GPIO.LOW) # Set STBY
