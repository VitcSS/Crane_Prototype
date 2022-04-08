from libs import zmqRemoteApi
import numpy as np
import cv2

class object:
    try : 
        sim = zmqRemoteApi.RemoteAPIClient().getObject('sim')
        print("Connected to simulation")
    except :
        print("Could not connect to the simulation.")

    def __init__(self, path : str, sim = None):
        if sim != None:
            self.sim = sim
        self.path = path
        self.handle = self.sim.getObject(self.path)

class BaxterCup(object):
    def __init__(self, path: str, sim=None):
        super().__init__(path, sim)
        self.signal = self.path[1:]+'_active'
        print(self.signal)

    def set_on(self):
        if self.state != 1 :
            self.sim.setInt32Signal(self.signal,1)
        else :
            print('Baxter Cup Already ON')

    def set_off(self):
        if self.state != 0 :
            self.sim.setInt32Signal(self.signal,0)
        else :
            print('Baxter Cup Already OFF')
            
    @property
    def state(self):
        return self.sim.getInt32Signal(self.signal)

class joint(object):
    def __init__(self, path: str,upper = np.inf,lower = -np.inf,sim=None):
        super().__init__(path, self.sim)
        self.upper = upper
        self.lower = lower
    
    def set_velocity(self, vel):
        if vel > self.upper :
            print('Invalid input value, velocity set to max')
            self.sim.setJointTargetVelocity(self.handle,self.upper)
        elif vel < self.lower:
            print('Invalid input value, velocity set to min')
            self.sim.setJointTargetVelocity(self.handle,self.lower)
        else :
            self.sim.setJointTargetVelocity(self.handle,vel)

    @property
    def get_position(self):
        return self.sim.getJointPosition(self.handle)
    

class prismatic(joint):
    def __init__(self, path: str, upper=np.inf, lower=-np.inf, sim=None):
        super().__init__(path, upper, lower, sim)

class revolute(joint):
    def __init__(self, path: str, upper=360, lower=-360, sim=None):
        rad_upper = np.deg2rad(upper)
        rad_lower = np.deg2rad(lower)
        super().__init__(path, rad_upper, rad_lower, sim)

    def set_velocity(self, vel):
        rad_vel = np.deg2rad(vel)
        return super().set_velocity(rad_vel)

class sensor(object):
    def __init__(self, path: str, sim=None):
        super().__init__(path, sim)

class vision(sensor):
    def __init__(self, path: str, sim=None):
        super().__init__(path, sim)
    
    def get_image(self):
        pass
    
class proximity(sensor):
    def __init__(self, path: str, sim=None):
        super().__init__(path, sim)
    
    def get_read(self):
        pass



