#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#use "python3 MasterProgram.py" without " to start on LX Terminal
import requests
import json
from requests.structures import CaseInsensitiveDict
import time
from datetime import datetime
import BaseClock
import gpiozero as gz
import RPi.GPIO as GPIO

def ReadYrTemp(lat, lon):
    #with open("/home/pi/Python/YrData.txt", "r") as yrdata:
    #    yrd = yrdata.read()
    #jdata = json.loads(yrd)
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["User-agent"] = "My User Agent 1.0"

    url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat="+lat+"&lon="+lon+""
    resp = requests.get(url, headers=headers)
    #print(resp.text)
    jdata = json.loads(resp.text)
    
    maxTemp = -100
    minTemp = 100

    for i in range(0, 18):
        thisTemp = jdata['properties']['timeseries'][i]['data']['instant']['details']['air_temperature']
        
        if i == 0:
            curTemp = thisTemp
            
        if thisTemp > maxTemp:
            maxTemp = thisTemp
        
        if thisTemp < minTemp:
            minTemp = thisTemp
    retTemp = "Temp min/max " + str(minTemp) + "/" + str(maxTemp) + " C"
    print("retTemp: " + retTemp)
    return retTemp

#lat = 0.000000
#lng = 9.999999
#type = rise or set
def getSunData(lat, lng, type):
    url = "https://api.sunrise-sunset.org/json?lat="+str(lat)+"&lng="+str(lng)+"&date=today&formatted=0"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["User-agent"] = "My User Agent 1.0"
    resp = requests.get(url, headers=headers)
    jdata = json.loads(resp.text)
    res = ""
    
    if type == "rise" :
        res = jdata['results']['sunrise']
        res = res[0:19]
    elif type == "set":
        res = jdata['results']['sunset']
        res = res[0:19]
    #print(res)
    
    if res == "":
        return ""
    else:
        return datetime_from_utc_to_local(res)

def datetime_from_utc_to_local(utc_datetime):
    utc_datetime = datetime.strptime(utc_datetime, "%Y-%m-%dT%H:%M:%S")
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

def isDayTime(sunrise, sunset):
    hour = datetime.now().strftime('%h')
    
    if hour <= sunrise.strftime('%h') or hour >= sunset.strftime('%h'):
        return False
    else:
        return True

def CPUTemp():
    cpu_temp = gz.CPUTemperature().temperature
    return str(round(cpu_temp, 1))

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
    #latitude = "52.526630" #Berlin Spandau
    #longitude = "13.148786" #Berlin Spandau
    latitude = "53.613147" # Hamburg Großborstel
    longitude = "9.976744" # Hamburg Großborstel
    sunrise = getSunData(latitude, longitude, "rise")
    sunset =  getSunData(latitude, longitude, "set")
    contrastDay = 100
    contrastNight = 1
    selftest = False
   
    # Taster definieren
    # GPIO Setup
    # Pin Definitons:
    touchSwitch = 17 # BCM pin 17 
    # Pin Setup:GeneratorExit
    GPIO.setmode(GPIO.BCM) # BCM pin-numbering scheme
    GPIO.setup(touchSwitch, GPIO.OUT) # Button pin set as input w/ pull-up
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
            second = datetime.now().strftime('%S')
            
            microsecond = datetime.now().microsecond
            #print(str(microsecond)[0:1])
            
            if GPIO.input(touchSwitch): # button is released
                setSwitch1 = True
                print(str(setSwitch1))
                
               
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
                if hour == "0" and second == "23":
                    sunrise = getSunData(latitude, longitude, "rise")
                    sunset =  getSunData(latitude, longitude, "set")
                
                # 
                if int(second) == 5 and isDayTime(sunrise, sunset): #
                    # update Tempratures and show Tempratures at day time  
                    if hour != lastHour or curTempData == "":
                        lastHour = hour
                        curTempData = ReadYrTemp(latitude, longitude)
                        
                    elif isDayTime(sunrise, sunset) == True:
                        Clock.ShowText(curTempData)
                    
                
                if int(second) == 45 and isDayTime(sunrise, sunset):
                    Clock.ShowText("CPU temp: " + str(CPUTemp()) + " C") # Lauftext ausgeben; Uhrzeit ausgeben ist in er baseClock drin
                    
                
                # show date at daytime
                if int(second)== 30 and isDayTime(sunrise, sunset): #
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
