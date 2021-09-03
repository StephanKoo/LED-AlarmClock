'''
Created on 30.08.2021

@author: stephan
'''

import MasterProgram
import Clock
import RasperryPi
import signal
import sys
import time

print ("OnNonRaspi.py gestartet")
print ("OnNonRaspi.py gestartet um "+time.strftime("%d.%m.%Y %H:%M:%S"))

def signal_term_handler(sig, frame):
    MasterProgram.close()
    sys.exit(0)

MasterProgram.clock = Clock.DummyClock()
MasterProgram.button1 = RasperryPi.DummyButton();

signal.signal(signal.SIGTERM, signal_term_handler)

print ("signal handler registered, will now start MasterProgram")

MasterProgram.run()

print ("MasterProgram finished")
