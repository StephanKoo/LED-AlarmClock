#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# RollingClock by joe703 / https://www.youtube.com/channel/UChMi8gAr52_jZXIpr9WXYQQ
# Inspired by luma.led_matrix/examples/silly_clock.py by ttsiodras
# https://github.com/rm-hull/luma.led_matrix/blob/master/examples/silly_clock.py

import Clock

import threading
import time
import random
from datetime import datetime

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message # da werden wohl Funktionen importiert
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT

class BaseClock(threading.Thread, Clock.Clock):

    def __DrawNumber(self, draw, StringOld, StringNew, PosOld, PosNew, Iterator):
        # Draws and animates Number - Iterator has to be increased from 0 (old String) to 8 (NewString)
        if Iterator > 8:
            Iterator = 8
        if Iterator < 8:
            text(draw, (PosOld, 1 - Iterator), StringOld, fill="white", font=proportional(CP437_FONT))
        if Iterator > 0:
            text(draw, (PosNew, 9 - Iterator), StringNew, fill="white", font=proportional(CP437_FONT))
            
    def __DrawColon(self, draw, StringOld, StringNew, Iterator):
        # Draws and animates colon - Iterator has to be increased from 0 (old String) to 8 (NewString)
        if StringOld == ":":
            text(draw, (15, 1 - Iterator), ":", fill="white", font=proportional(TINY_FONT))
        if StringNew == ":":
            text(draw, (15, 9 - Iterator), ":", fill="white", font=proportional(TINY_FONT))
            
    def __GetHourPos(self, hours):
        # Returns position for hours with CP437_FONT
        # Das Pixel, bei dem die Uhr anfängt
        if hours == 0 or hours == 4:
            return 7
        elif hours < 10:
            return 8
        elif hours == 10 or hours == 14 or hours == 20:
            return 0
        else:
            return 1
            
    def __init__(self):  # __init__ ist der Konstruktor
        # Init Own Thread for Clock
        threading.Thread.__init__(self)  # sich selber im Thread starten
        # Init LED Matrix
        serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(serial, cascaded=4, block_orientation=-90, blocks_arranged_in_reverse_order=False) # 7219 ist der Chip der Steuerung; cascade: Anzahl der 8x8-Kacheln
        self.device.contrast(1)  # niedrigste Helligkeitsstufe
    
    def run(self):
        # Clock is running
        self.__RunClock = True
        self.__ShowClock = True
        self.__DisplayText=""

        # Toggle the second indicator every second
        toggle = False  

        while self.__RunClock:
            # Init Time
            CurrentTime = datetime.now()
            MinutesStr = CurrentTime.strftime('%M')
            MinutesStrOld = MinutesStr
            HoursStr = CurrentTime.strftime('%-H')
            HoursStrOld = HoursStr
            HoursPos = self.__GetHourPos(CurrentTime.hour)
            HoursPosOld = HoursPos
            
            # Scroll in Clock
            for i in range(0,9):
                with canvas(self.device) as draw:
                    self.__DrawNumber(draw, "", HoursStr, HoursPos, HoursPos, i)
                    self.__DrawColon(draw, "", ":", i)
                    self.__DrawNumber(draw, "", MinutesStr, 17, 17, i)
                time.sleep(0.1)

            while (self.__ShowClock==True and self.__DisplayText==""):
                # Get New Time
                CurrentTime = datetime.now()
                MinutesStr = CurrentTime.strftime('%M')
                HoursStr = CurrentTime.strftime('%-H')
                HoursPos = self.__GetHourPos(CurrentTime.hour)
                
                # Handle special cases for right alignemnt of hours in CP437_FONT
                HoursPos = self.__GetHourPos(CurrentTime.hour)
                if (MinutesStr != MinutesStrOld or HoursStr != HoursStrOld):
                    # Time changed
                    for i in range(0,9):
                        if i == 5:
                            # toggle colon
                            toggle = not toggle
                        if HoursStr != HoursStrOld:
                            # Animate Hours and Minutes
                            with canvas(self.device) as draw:
                                self.__DrawNumber(draw, HoursStrOld, HoursStr, HoursPosOld, HoursPos, i)
                                self.__DrawColon(draw, ":" if toggle else " ", " ", 0)
                                self.__DrawNumber(draw, MinutesStrOld, MinutesStr, 17, 17, i)
                        elif MinutesStr[0] != MinutesStrOld[0]:
                            # Animate 2 digit Minute Update
                            with canvas(self.device) as draw:
                                self.__DrawNumber(draw, HoursStrOld, HoursStr, HoursPos, HoursPos, 0)
                                self.__DrawColon(draw, ":" if toggle else " ", " ", 0)
                                self.__DrawNumber(draw, MinutesStrOld, MinutesStr, 17, 17, i)
                        else:
                            # Animate 1 digit Minute Update
                            with canvas(self.device) as draw:
                                self.__DrawNumber(draw, HoursStrOld, HoursStr, HoursPos, HoursPos, 0)
                                self.__DrawColon(draw, ":" if toggle else " ", " ", 0)
                                self.__DrawNumber(draw, MinutesStr[0],
                                                  MinutesStr[0], 17, 17, 0)
                                # If we don't draw digit 1 we need to check it for the position
                                if MinutesStr[0] == "0" or MinutesStr[0] == "4":
                                    self.__DrawNumber(draw, MinutesStrOld[1], MinutesStr[1], 25, 25, i)
                                else:
                                    self.__DrawNumber(draw, MinutesStrOld[1], MinutesStr[1], 24, 24, i)
                        time.sleep(0.1)
                else:
                    # Redraw Time to toggle colon
                    with canvas(self.device) as draw:
                        self.__DrawNumber(draw, HoursStr, HoursStr, HoursPos, HoursPos, 0)
                        self.__DrawColon(draw, ":" if toggle else " ", " ", 0)
                        self.__DrawNumber(draw, MinutesStr, MinutesStr, 17, 17, 0)
                    time.sleep(0.5)

                # Store Time
                MinutesStrOld = MinutesStr
                HoursStrOld = HoursStr
                HoursPosOld = HoursPos

                # toggle colon
                toggle = not toggle

            # Scroll out Clock
            for i in range(0,9):
                with canvas(self.device) as draw:
                    self.__DrawNumber(draw, HoursStr, "", HoursPos, HoursPos, i)
                    self.__DrawColon(draw, ":", "", i)
                    self.__DrawNumber(draw, MinutesStr, "", 17, 17, i)
                time.sleep(0.1)
                
            # Wait and show text
            while self.__RunClock and ((self.__ShowClock==False) or (self.__DisplayText!="")):
                if self.__DisplayText!="":
                    show_message(self.device, self.__DisplayText, fill="white", font=proportional(CP437_FONT))
                    self.__DisplayText=""
                time.sleep(0.5)

    def Show(self):
        self.__ShowClock = True   # __ShowClock: Clock ist nicht allgemein genug hier

    def Hide(self):
        self.__ShowClock = False

    # Lauftext
    def ShowText(self, text):
        # Replace special characters, whch are not available in font
        chars = {'ö':'oe','ä':'ae','ü':'ue','Ö':'Oe','Ä':'Ae','Ü':'ue','ß':'ss'}
        for char in chars:
            text = text.replace(char,chars[char])
        # Check if text can be displayed and request output if not busy
        if self.__DisplayText=="":
            self.__DisplayText = text
            print("Textausgabe angefordert: "+text)
            return True
        else:
            print("Textausgabe nicht moeglich: "+text)
            return False
            
    def close(self):
        self.__ShowClock = False
        self.__RunClock = False
    
    # Step by 16 
    def changeContrast(self, value):
        self.device.contrast(value)
    
    # Clock.DemoBrightness()
    def DemoBrightness(self):
        tempContrast : int = random.randrange(0,255,1)
        print("TempContrast:=" + str(tempContrast))
        self.changeContrast(tempContrast)

    # UHr blinkt, um Mensch aus dem Bett zu schmeißen
    #flashDuration: min 2 / max 59
    #minBrightness: 1
    #maxBrightness: 255 #Step 16
    #Wecker klingelt ohne Snozze: Idee FlashBrightness(2, 1, 255)
    def FlashBrightness(self, flashDuration, minBrightness, maxBrightness):
        CurSecond = datetime.now().strftime('%S')
        if int(CurSecond) % flashDuration == 0:
            self.changeContrast(maxBrightness)
        else:
            self.changeContrast(minBrightness)
    
if __name__ == "__main__":
    Wochentag=["Sonntag ", "Montag ", "Dienstag ", "Mittwoch ", "Donnerstag ", "Freitag ", "Samstag "]

    # LedAlarmClock for Test
    Uhr = BaseClock() 
    Uhr.start()
    
    print("Uhr gestartet")
    print("Press Ctrl-C to quit.")
    try:
        while True:
            datum = datetime.now().strftime('%d.%m.%Y')
            tag = datetime.now().strftime('%w')
            sekunden = datetime.now().strftime('%S')

            if sekunden=="05":
                # show Date
                Uhr.ShowText(Wochentag[int(tag)] + datum)
                
            time.sleep(1)
    except KeyboardInterrupt:
        pass # = NOP, da hier ja irgendein Befehl stehen muss
    Uhr.close()
    print("Stop der Uhr angefordert")
    Uhr.join()
    print("Uhr gestoppt")
