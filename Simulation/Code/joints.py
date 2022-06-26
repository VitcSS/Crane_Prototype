from object import object
from numbers import Number
import numpy as np

class joint(object):
    def __init__(self, fantasy_name, sim=None):
        super().__init__(fantasy_name, sim)
    
    def set_Position(self, value): 
        self.sim.setJointTargetPosition(self.handle, value)
    
    def getPosition(self):
        return self.sim.getJointPosition(self.handle)

