from controllers.Strategy import Strategy
from controllers.Crane_lite import Crane_Lite
from numpy import power
Model = Crane_Lite()
class Copelia(Strategy):
    def rotacionar_torre(self, graus: int) -> bool:
        Model.XY.set_Position(Model.XY.getPosition()+graus)

    def mover_ferramenta(self, centimentros: int) -> bool:
        aux = Model.Z.getPosition() - centimentros*(10**-2)
        Model.Z.set_Position(aux)

    def valor_sensores(self) -> dict:
        try :
            dist,_ = Model.Sonar.detect()
        except :
            dist = Model.Sonar.detect()
        
        return {'distanceTool' : dist*power(10,2),
                'towerPosition' : Model.XY.getPosition, 
                'electromagnet' : Model.actuator.is_full(), 
                'toolPosition' : Model.Z.getPosition()*power(10,2) }

    def atuar_ferramenta(self, status: bool) -> bool:
        if Model.actuator.is_full:
            Model.actuator.off()
        else :
            Model.actuator.on()