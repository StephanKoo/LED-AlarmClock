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
    def start(self):
        pass

    @abc.abstractclassmethod
    def ShowText(self, text):
        pass
    
    @abc.abstractclassmethod
    def close(self):
        pass

    @abc.abstractclassmethod
    def join(self):
        pass

class DummyClock(Clock):
    
    def start(self):
        pass

    def ShowText(self, text):
        print(text)
    
    def close(self):
        pass

    def join(self):
        pass
