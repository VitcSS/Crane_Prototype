from controllers.object import object
from numbers import Number
from numpy import Inf, deg2rad, rad2deg

class joint(object):
    def __init__(self, fantasy_name, sim=None, min_ : Number = 0, max_ : Number = Inf):
        self.__max__ = max_
        self.__min__ = min_
        super().__init__(fantasy_name, sim)
    
    def set_Position(self, value): 
        if value > self.__max__:
            self.sim.setJointTargetPosition(self.handle, self.__max__)
        elif value < self.__min__:
            self.sim.setJointTargetPosition(self.handle, self.__max__)
        else :
            self.sim.setJointTargetPosition(self.handle, value)
    
    def getPosition(self):
        return self.sim.getJointPosition(self.handle)

class revolute_joint(joint):
    def __init__(self, fantasy_name, sim=None, min_: Number = 0, max_: Number = Inf):
        max_ = deg2rad(max_)
        min_ = deg2rad(min_)
        super().__init__(fantasy_name, sim, min_, max_)
    
    def set_Position(self, value):
        value = deg2rad(value)
        return super().set_Position(value)
    
    def getPosition(self):
        return rad2deg(super().getPosition())

