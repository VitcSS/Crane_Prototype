from sqlalchemy import false
from libs.Object import *
from libs.Crane import *
import time
if __name__ == '__main__':
    # Connect to the Crane Model in the Simulation:
    Coin = object.sim.getObject('/Coin')
    object.sim.startSimulation()
    Model = Crane(XY = '/Spear_joint',
                  Z = '/Tool_joint',
                  Tool = '/Magnet',
                  Cam = '/Cam',
                  Alignment='/Ray_Sensor')
    Model.Z.set_velocity(-0.08)
    while Model.Alignment.detect() > 0.03: pass
    object.sim.setObjectParent(Coin,object.sim.getObject('/Atatcher'),True)
    Model.Z.set_velocity(0.08)
    while Model.Alignment.detect() < 0.55: pass
    Model.Z.set_velocity(0)
    Model.XY.set_velocity(8)
    while Model.XY.get_position > 180: print(Model.XY.get_position)
    Model.XY.set_velocity(0)
    Model.Z.set_velocity(-0.08)
    while Model.Alignment.detect() > 0.03: pass
    object.sim.setObjectParent(Coin,-1,False)
    Model.Z.set_velocity(0.08)
    while Model.Alignment.detect() < 0.55-0.21: pass
    Model.Z.set_velocity(0)
    time.sleep(3)
    object.sim.stopSimulation()