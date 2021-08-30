'''
Created on 30.08.2021

@author: stephan
'''

import MasterProgram
import Clock
import RasperryPi

clock = Clock.DummyClock()
button1 = RasperryPi.DummyButton();

MasterProgram.main(clock, button1)