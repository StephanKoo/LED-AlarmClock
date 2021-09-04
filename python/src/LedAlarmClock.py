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

def signal_term_handler(sig, frame):
    MasterProgram.closeFast()
    time.sleep(1)
    sys.exit(0)

MasterProgram.clock = BaseClock.BaseClock()
MasterProgram.button1 = RasperryPiImpl.RaspyButton();

signal.signal(signal.SIGTERM, signal_term_handler)

MasterProgram.run()
