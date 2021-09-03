'''
Created on 30.08.2021

@author: stephan
'''

import MasterProgram
import BaseClock
import RasperryPiImpl
import signal
import sys
import time

print ("LedAlarmClock.py gestartet um "+time.strftime("%d.%m.%Y %H:%M:%S"))

def signal_term_handler(sig, frame):
    MasterProgram.closeFast()
    sys.exit(0)

MasterProgram.clock = BaseClock.BaseClock()
MasterProgram.button1 = RasperryPiImpl.RaspyButton();

signal.signal(signal.SIGTERM, signal_term_handler)

print ("signal handler registered, will now start MasterProgram")

MasterProgram.run()

print ("MasterProgram finished")
