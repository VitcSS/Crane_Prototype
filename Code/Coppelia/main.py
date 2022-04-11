from libs.Object import *
from libs.Crane import *
import time
if __name__ == '__main__':
    # Connect to the Crane Model in the Simulation:
    object.sim.startSimulation()
    Model = Crane(XY = '/Spear_joint',
                  Z = '/Tool_joint',
                  Tool = '/Tool',
                  Cam = '/Cam',
                  Alignment='/Ray_Sensor')
    Model.Z.set_velocity(-0.08)
    while Model.Alignment.detect() > 0.1:
        print(Model.Alignment.detect())
        pass
    Model.Z.set_velocity(0)
    object.sim.stopSimulation()