from object import object
from numpy import Inf, frombuffer, uint8
import cv2

class proximity(object):
    def detect(self):
        self.sim.checkProximitySensor(self.handle, self.sim.handle_all)
        result = None
        try :
            result,distance,_,handle,_ = self.sim.readProximitySensor(self.handle)
        except :
            result = self.sim.readProximitySensor(self.handle)
        if result == 1:
            return distance, handle
        else:
            return Inf

class vision(object):
    
    def get_image(self):
        img, resX, resY = self.sim.getVisionSensorCharImage(self.handle)
        img = frombuffer(img, dtype= uint8).reshape(resY, resX, 3)
        img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
        return img
    