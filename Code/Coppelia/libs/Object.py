from libs import zmqRemoteApi
import numpy as np
import cv2

class object:
    try : 
        sim = zmqRemoteApi.RemoteAPIClient().getObject('sim')
        print("Connected to simulation")
    except :
        print("Could not connect to the simulation.")

    def __init__(self, handle : str):
        self.channel = self.sim.getObject(handle)

class joint(object):
    def __init__(self, handle: str, upper = np.inf,lower = -np.inf):
        super().__init__(handle)
        self.upper = upper
        self.lower = lower
    
    def set_velocity(self, value):
        if value > self.upper :
            print('Warning : Velocity value out of Range, defined as max')
        elif value < self.lower :
            print('Warning : Velocity value out of Range, defined as minimum')
        else:
            self.sim.setJointTargetVelocity(self.channel,value)

class revolute(joint):
    def __init__(self, handle: str, upper=np.deg2rad(360), lower=-np.deg2rad(360)):
        super().__init__(handle, upper, lower)
    
    def set_velocity(self, value):
        return super().set_velocity(np.deg2rad(value))
    
class prismatic(joint):
    def __init__(self, handle: str, upper=np.inf, lower=-np.inf):
        super().__init__(handle, upper, lower)
    

class vision(object):
    def __init__(self, handle: str):
        super().__init__(handle)
        self.to_render = self.sim.createCollection(0)
        self.render_list = list()
    
    def add_to_render(self, channel):
        self.render_list.append(channel)
        self.sim.addItemToCollection(self.to_render,self.sim.handle_single,channel,0)
    
    def get_image(self):
        img, resX, resY = self.sim.getVisionSensorCharImage(self.channel)
        img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
        img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
        return img

    def set_to_render(self):
        self.sim.setObjectInt32Param(self.channel,self.sim.visionintparam_entity_to_render,-1)
        # self.sim.setObjectInt32Param(self.channel,self.sim.visionintparam_entity_to_render,self.to_render)

class sucky(object):
    def __init__(self, handle: str):
        super().__init__(handle)
    
    def set_on():
        pass

    def set_off():
        pass
