import zmqRemoteApi

class object:
    # Try to connect to the current simulation open in Coppelia
    try : 
        sim = zmqRemoteApi.RemoteAPIClient().getObject('sim')
        print("Connected to simulation")
    except :
        print("Could not connect to the simulation.")
    
    def __init__(self, fantasy_name, sim = None):
        if sim != None:
            self.sim = sim
        self.fantasy_name = fantasy_name
        self.handle = self.sim.getObject(self.fantasy_name)
    
    
