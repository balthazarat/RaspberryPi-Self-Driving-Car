#!/usr/bin/env python

# Import required modules
from re import U
import time
import RPi.GPIO as GPIO

# Declare the GPIO settings
GPIO.setmode(GPIO.BOARD)

TRIG = 16
ECHO = 18
# set up GPIO pins

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

def ultrasonic():
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
  #GPIO.cleanup()

# Wait 5 seconds
time.sleep(5)
ultrasonic()
