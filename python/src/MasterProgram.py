#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#use "python3 MasterProgram.py" without " to start on LX Terminal

import time
from datetime import datetime

import Clock
import BaseClock
import RasperryPi
import RasperryPiImpl

import Util

import sys
from sys import argv
    
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
    
    if (len(argv) == 0):
        button1 = RasperryPiImpl.RaspyButton();
        clock = BaseClock.BaseClock()
    elif (argv[0] == "--no-led"):
        button1 = RasperryPi.DummyButton();
        clock = Clock.DummyClock()
    else:
        print ("Parameter "+argv[0] +" nicht unterstützt. Entweder kein Parameter übergeben, oder --no-led")

    clock.start()
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
    
            button1.updateState_1()         

            # clock.changeContrast((int(second) % 2) * 100)
               
            if int(str(str(microsecond).zfill(6)[0:1])) == 0: # zfill: 1/10-Sekunde == 0
                
                c = button1.updateState_2()
                if c == True:
                    clock.changeContrast(255)
                elif c == False:
                    clock.changeContrast(16)
                               
                # Day / Night Mode
                #if isDayTime(sunrise, sunset) == True:
                #    clock.changeContrast(contrastDay)
                #else:
                #    clock.changeContrast(contrastNight)
                
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
                    clock.ShowText(curTempData)
                
                if (second == 20) :
                    ipInfo = Util.getIpInfo();
                    clock.ShowText(ipInfo)
                
                if second == 45 and Util.isDayTime(sunrise, sunset):
                    clock.ShowText("CPU temp: " + str(Util.CPUTemp()) + " C") # Lauftext ausgeben; Uhrzeit ausgeben ist in er baseClock drin
                    
                
                # show date at daytime
                if second == 30 and Util.isDayTime(sunrise, sunset): #
                    # show Date
                    clock.ShowText(WeekdayShort[int(day)] + " " + date)
                
                time.sleep(0.1)
                setSwitch1 = False
            
            
    except KeyboardInterrupt:
        pass
    button1.close()
    clock.close()
    print("Stop der Uhr angefordert")
    clock.join()
    print("Uhr gestoppt")
