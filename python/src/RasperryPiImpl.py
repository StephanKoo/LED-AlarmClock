'''
Created on 30.08.2021

@author: stephan
'''

import abc
import gpiozero as gz
import RPi.GPIO as GPIO
import RasperryPi

class RaspyButton(RasperryPi.Button):

    # Taster definieren
    # GPIO Setup
    # Pin Definitons:
    touchSwitch = 17 # GPIO 17 = Pin 11 for mode BCM
    # Pin Setup:GeneratorExit
    GPIO.setmode(GPIO.BCM) # BCM pin-numbering scheme / Board-Mode
    GPIO.setup(touchSwitch, GPIO.OUT) # Button pin set as input w/ pull-up # OUT = Die Daten kommen AUS dem Schalter
    setSwitch1 = False
    setSwitch1Old = setSwitch1

    def updateState_1(self):
        if GPIO.input(self.touchSwitch): # button is released
            setSwitch1 = True
            print(str(setSwitch1))

    def updateState_2(self):
        if self.setSwitch1 == True:
            if self.setSwitch1Old == False:
                self.setSwitch1Old = self.setSwitch1
                self.setSwitch1 = False
                return False;
            else: #setSwitch1Old == True
                self.setSwitch1Old = False
                self.setSwitch1 = False
                return True;
        return None;

    def close(self):
        GPIO.cleanup() # cleanup all GPIO
