from libs.Object import *
from libs import zmqRemoteApi

class Crane:
    sim = object.sim
    def __init__(self,XY,Z,Tool,Cam,Alignment):
        self.XY = revolute(XY,20,-20)
        self.Z = prismatic(Z,0.07,-0.07)
        self.Tool = self.sim.getObject(Tool)
        self.Cam = vision(Cam)
        self.Alignment = proximity(Alignment)
    