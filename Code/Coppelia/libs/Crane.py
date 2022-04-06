from libs.Object import *
from libs import zmqRemoteApi

class Crane:
    sim = object.sim
    Dof_keys = ['Rot', 'XY','Z']
    def __init__(self,Rot,XY,Z,Actuator,img_source):
        self.DoFs = {key:None for key in self.Dof_keys}
        self.set_DoFs(Rot,XY,Z)
        self.POV = vision(img_source)
        self.Magnet = sucky(Actuator)

    def set_render_collection(self):
        for render in self.render_list:
            self.render_collection.addObject(self.sim.getObject(render))

    def set_DoFs(self,Rot=None,XY=None,Z=None):
        if Rot != None:
            self.DoFs['Rot'] = revolute(Rot,20,-20)
        if XY != None:
            self.DoFs['XY'] = prismatic(XY,0.12,-0.12)
        if Z != None:
            self.DoFs['Z'] = prismatic(Z,0.20,-0.20)
        for Dof in self.DoFs.values():
            Dof.set_velocity(0)
    
    def DoF_test(self):
        init_time = self.sim.getSimulationTime()
        while self.sim.getSimulationTime() < 4+init_time:
            self.DoFs['Rot'].set_velocity(18)
        self.DoFs['Rot'].set_velocity(0)
        init_time = self.sim.getSimulationTime()
        while self.sim.getSimulationTime() < 4+init_time:
            self.DoFs['XY'].set_velocity(0.010)
        self.DoFs['XY'].set_velocity(0)
        init_time = self.sim.getSimulationTime()
        while self.sim.getSimulationTime() < 4+init_time:
            self.DoFs['Z'].set_velocity(0.006)
        self.DoFs['Z'].set_velocity(0)
