#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#use "python3 MasterProgram.py" without " to start on LX Terminal

import time
from datetime import datetime

import BaseClock
import gpiozero as gz
import RPi.GPIO as GPIO

import Util

# UHr blinkt, um Mensch aus dem Bett zu schmeißen
#flashDuration: min 2 / max 59
#minBrightness: 1
#maxBrightness: 255 #Step 16
#Wecker klingelt ohne Snozze: Idee FlashBrightness(2, 1, 255)
def FlashBrightness(flashDuration, minBrightness, maxBrightness):
    CurSecond = datetime.now().strftime('%S')
    if int(CurSecond) % flashDuration == 0:
        Clock.changeContrast(maxBrightness)
    else:
        Clock.changeContrast(minBrightness)
    
if __name__ == "__main__": # d.h. Hauptprogramm
    #set default values
    WeekdayLong=["Sonntag ", "Montag ", "Dienstag ", "Mittwoch ", "Donnerstag ", "Freitag ", "Samstag "]
    WeekdayShort=["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"]
    prevTempData = ""
    curTempData = "" 
    lastHour = 0
    latitude = "52.526630" #Berlin Spandau
    longitude = "13.148786" #Berlin Spandau
    #latitude = "53.613147" # Hamburg Großborstel
    #longitude = "9.976744" # Hamburg Großborstel
    sunrise = Util.getSunData(latitude, longitude, "rise")
    sunset =  Util.getSunData(latitude, longitude, "set")
    contrastDay = 100
    contrastNight = 1
    selftest = False
   
    # Taster definieren
    # GPIO Setup
    # Pin Definitons:
    touchSwitch = 17 # GPIO 17 = Pin 11 for mode BCM
    # Pin Setup:GeneratorExit
    GPIO.setmode(GPIO.BCM) # BCM pin-numbering scheme / Board-Mode
    GPIO.setup(touchSwitch, GPIO.OUT) # Button pin set as input w/ pull-up # OUT = Die Daten kommen AUS dem Schalter
    setSwitch1 = False
    setSwitch1Old = setSwitch1

    # Main for Test
    Clock = BaseClock.BaseClock() 
    Clock.start()
    print("Uhr gestartet")
    print("Press Ctrl-C to quit.")

    try:
        while True:
            date = datetime.now().strftime('%d.%m.') #old '%d.%m.%Y'
            day = datetime.now().strftime('%w')
            hour = datetime.now().strftime('%h')
            secondS = datetime.now().strftime('%S')
            second  = int(secondS)
            
            microsecond = datetime.now().microsecond
            #print(str(microsecond)[0:1])
            
            if GPIO.input(touchSwitch): # button is released
                setSwitch1 = True
                print(str(setSwitch1))

            # Clock.changeContrast((int(second) % 2) * 100)
               
            if int(str(str(microsecond).zfill(6)[0:1])) == 0: # zfill: 1/10-Sekunde == 0
                
                if setSwitch1 == True:
                    if setSwitch1Old == False:
                        Clock.changeContrast(255)
                        setSwitch1Old = setSwitch1
                        setSwitch1 = False
                    else: #setSwitch1Old == True
                        Clock.changeContrast(16)
                        setSwitch1Old = False
                        setSwitch1 = False
                        
                # Day / Night Mode
                #if isDayTime(sunrise, sunset) == True:
                #    Clock.changeContrast(contrastDay)
                #else:
                #    Clock.changeContrast(contrastNight)
                
                # set sunrise and sunset to new time
                if hour == "0" and second == 23:
                    sunrise = Util.getSunData(latitude, longitude, "rise")
                    sunset =  Util.getSunData(latitude, longitude, "set")
                
                # 
                if (second == 5) :# and isDayTime(sunrise, sunset):
                    # update Tempratures and show Tempratures at day time  
                    if hour != lastHour or curTempData == "":
                        lastHour = hour
                        curTempData = Util.ReadYrTemp(latitude, longitude)
                    Clock.ShowText(curTempData)
                
                if (second == 20) :
                    ipInfo = Util.getIpInfo();
                    Clock.ShowText(ipInfo)
                
                if second == 45 and Util.isDayTime(sunrise, sunset):
                    Clock.ShowText("CPU temp: " + str(Util.CPUTemp()) + " C") # Lauftext ausgeben; Uhrzeit ausgeben ist in er baseClock drin
                    
                
                # show date at daytime
                if second == 30 and Util.isDayTime(sunrise, sunset): #
                    # show Date
                    Clock.ShowText(WeekdayShort[int(day)] + " " + date)
                
                time.sleep(0.1)
                setSwitch1 = False
            
            
    except KeyboardInterrupt:
        pass
    GPIO.cleanup() # cleanup all GPIO
    Clock.close()
    print("Stop der Uhr angefordert")
    Clock.join()
    print("Uhr gestoppt")
