from controllers.Strategy import Strategy
from controllers.Crane_lite import Crane_Lite
from numpy import power
import globalData
import threading
import time

class Copelia(Strategy):
    Model = None
    
    def __init__(self):
        self.Model = Crane_Lite()
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
        if self.Model.actuator.is_full():
            self.Model.actuator.off()
        else :
            self.Model.actuator.on()