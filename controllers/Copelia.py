from controllers.Strategy import Strategy
from controllers.Crane_lite import Crane_Lite
from numpy import power
class Copelia(Strategy):
    Model = None
    
    def Copelia(self):
        self.Model = Crane_Lite()
        
    def rotacionar_torre(self, graus: int) -> bool:
        self.Model.XY.set_Position(self.Model.XY.getPosition()+graus)

    def mover_ferramenta(self, centimentros: int) -> bool:
        aux = self.Model.Z.getPosition() - centimentros*(10**-2)
        self.Model.Z.set_Position(aux)

    def valor_sensores(self) -> dict:
        try :
            dist,_ = self.Model.Sonar.detect()
        except :
            dist = self.Model.Sonar.detect()
        
        return {'distanceTool' : dist*power(10,2),
                'towerPosition' : self.Model.XY.getPosition, 
                'electromagnet' : self.Model.actuator.is_full(), 
                'toolPosition' : self.Model.Z.getPosition()*power(10,2) }

    def atuar_ferramenta(self, status: bool) -> bool:
        if self.Model.actuator.is_full:
            self.Model.actuator.off()
        else :
            self.Model.actuator.on()