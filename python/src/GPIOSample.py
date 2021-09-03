#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# External module imports
import RPi.GPIO as GPIO
import time
from datetime import datetime

# Pin Definitons:
touchSwitch = 17 # Broadcom pin 17 (P1 pin 11)

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(touchSwitch, GPIO.OUT) # Button pin set as input w/ pull-up

# Initial state for LEDs:

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        if GPIO.input(touchSwitch): # button is released
            print("Taster: an")
            time.sleep(0.1)
        else: # button is pressed:
            print("Taster: aus")
            time.sleep(0.1)
            microsecond = datetime.now().microsecond
            print("microsecond: " + str(str(microsecond).zfill(6)[0:1]))
            print("microsecond: " + str(microsecond))
            
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    
    GPIO.cleanup() # cleanup all GPIO
