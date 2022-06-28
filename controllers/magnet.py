from controllers.object import object
from controllers.sensors import proximity

class Magnet(object):
    def __init__(self, fantasy_name : str = '/Link',Field : str = '/Field',sim=None):
        self.Field = proximity(Field)
        super().__init__(fantasy_name, sim)
    
    def disturbance(self):
        try :
            _,src = self.Field.detect()
            return src
        except :
            return None
    
    def is_full(self):
        if self.sim.getObjectChild(self.handle,0) != -1:
            return True
        else :
            return False
    
    def on(self):
        target = self.disturbance()
        if (target != None) and (self.is_full() == False):
            print(self.sim.getObjectAlias(target))
            self.sim.setObjectParent(target, self.handle, True)
    
    def off(self):
        if self.is_full():
             self.sim.setObjectParent(self.sim.getObjectChild(self.handle,0),-1,True)
