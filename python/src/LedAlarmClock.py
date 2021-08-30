'''
Created on 30.08.2021

@author: stephan
'''

import MasterProgram
import BaseClock
import RasperryPiImpl

clock = BaseClock.BaseClock()
button1 = RasperryPiImpl.RaspyButton();

MasterProgram.main(clock, button1)