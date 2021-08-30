'''
Created on 30.08.2021

@author: stephan
'''

import abc

class Clock(abc.ABC):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    @abc.abstractclassmethod
    def ShowText(self, text):
        pass

class DummyClock(Clock):
    def ShowText(self, text):
        print(text)
