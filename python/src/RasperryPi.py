'''
Created on 30.08.2021

@author: stephan
'''

import abc

class RasperryPi(abc.ABC):
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

class DummyRasperryPi(RasperryPi):
    def ShowText(self, text):
        print(text)


class Button(abc.ABC):

    @abc.abstractclassmethod
    def updateState_1(self):
        pass

    @abc.abstractclassmethod
    def updateState_2(self):
        pass

    @abc.abstractclassmethod
    def close(self):
        pass

class DummyButton(Button):

    def updateState_1(self):
        pass

    def updateState_2(self):
        pass

    def close(self):
        pass
