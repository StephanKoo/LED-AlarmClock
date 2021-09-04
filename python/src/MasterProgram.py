#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#use "python3 MasterProgram.py" without " to start on LX Terminal

import time
from datetime import datetime

import Clock
from RasperryPi import Button

import Util

clock: Clock
button1: Button

def run():
    # clock und button1 muss vorher gesetzt worden sein

    #set default values
    WeekdayLong=["Sonntag ", "Montag ", "Dienstag ", "Mittwoch ", "Donnerstag ", "Freitag ", "Samstag "]
    WeekdayShort=["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"]
    curTempData = "" 
    lastHour = 0
    latitude = "52.5"  # Berlin Spandau
    longitude = "13.1" # Berlin Spandau
    #latitude = "53.6" # Hamburg Großborstel
    #longitude = "9.9" # Hamburg Großborstel
    
    sunrise = "-no sunrise-"
    sunset = "-no sunset-"
    
    #sunrise = Util.getSunData(latitude, longitude, "rise")
    #sunset =  Util.getSunData(latitude, longitude, "set")

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
                
                # print("second="+secondS);
                
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
                #if hour == "0" and second == 23:
                #    sunrise = Util.getSunData(latitude, longitude, "rise")
                #    sunset =  Util.getSunData(latitude, longitude, "set")
                
                # 
                if (second == 5 or second == 6) :# and isDayTime(sunrise, sunset):
                    # update Tempratures and show Tempratures at day time  
                    if hour != lastHour or curTempData == "":
                        lastHour = hour
                        curTempData = Util.ReadYrTemp(latitude, longitude)
                    clock.ShowText(curTempData)
                
                if (second == 25 or second == 26) :
                    ipInfo = Util.getIpInfo();
                    clock.ShowText(ipInfo)
                
                if (second == 45 or second == 46):# and Util.isDayTime(sunrise, sunset)):
                    clock.ShowText("CPU temp: " + str(Util.CPUTemp()) + " C") # Lauftext ausgeben; Uhrzeit ausgeben ist in er baseClock drin

                # show date at daytime
                #if second == 30 and Util.isDayTime(sunrise, sunset): #
                #    # show Date
                #    clock.ShowText(WeekdayShort[int(day)] + " " + date)
                
                time.sleep(0.1)
            
    except KeyboardInterrupt:
        pass
    close()

def close():
    if button1 != None:
        button1.close()
    if clock != None:
        clock.close()
        print("Stop der Uhr angefordert")
        clock.join()
        print("Uhr gestoppt")

def closeFast():
    if button1 != None:
        button1.close()
    if clock != None:
        clock.closeFast()
        print("Schnell-Stop der Uhr angefordert")
        clock.join()
        print("Uhr gestoppt")

if __name__ == "__main__": # d.h. Hauptprogramm
    print("Bitte LedAlarmClock.py (oder OnNonRaspi.py) starten")
