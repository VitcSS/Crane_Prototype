from controllers.Strategy import Strategy
from controllers.Crane_lite import Crane_Lite
from numpy import power
import threading
import globalData
import time

Model = Crane_Lite()
class Copelia(Strategy):
    def __init__(self) -> None:
        existsThread = next((thread for thread in threading.enumerate() if thread.name == 'thread_atualiza_telemetria_copelia'), False)
        if existsThread == False:
            updateTelemetriaThread = threading.Thread(target = self.thread_atualiza_telemetria, daemon=True, name="thread_atualiza_telemetria_copelia")
            updateTelemetriaThread.start()

    def thread_atualiza_telemetria(self):
        valores = self.valor_sensores()
        globalData.distanceTool = int(valores['distanceTool'])
        globalData.towerPosition = int(valores['towerPosition'])
        globalData.electromagnet = int(valores['electromagnet'])
        globalData.toolPosition = int(valores['toolPosition'])
        time.sleep(1)

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