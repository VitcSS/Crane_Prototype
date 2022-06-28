import time
from sensors import *
from joints import *
from magnet import Magnet

class Crane_Lite:
    def __init__(self, XY = '/XY', Z = '/Z', Sonar = '/Sonar', ESP = '/ESP_CAM' ):
        self.XY = revolute_joint(XY)
        self.Z = joint(Z)
        self.Sonar = proximity(Sonar)
        self.ESP32 = vision(ESP)
        self.actuator = Magnet()

    @staticmethod
    def start():
        object.sim.startSimulation()
    
    @staticmethod
    def stop():
        object.sim.stopSimulation()