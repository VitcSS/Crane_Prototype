from controllers.Strategy import Strategy
from libs.SerialCommunication import SerialCommunication
import globalData

import time

class Arduino(Strategy):

    def __init__(self) -> None:
        self.serialArduino = None
        self.inicializa_serial()

    def __del__(self):
        del self.serialArduino

    def inicializa_serial(self):
        if self.serialArduino is None:
            self.serialArduino = SerialCommunication(port='COM11')
            self.serialArduino.startCommunication()
    
    def thread_atualiza_telemetria(self):

        while 1:
            if not globalData.pauseThread:
                mensagem_recebida = self.serialArduino.receiveMessage()
                if 'distanceTool' in mensagem_recebida and 'towerPosition' in mensagem_recebida and 'electromagnet' in mensagem_recebida:
                    print("Recebi coisas: ", mensagem_recebida)
                    globalData.distanceTool = int(mensagem_recebida['distanceTool'])
                    globalData.towerPosition = int(mensagem_recebida['towerPosition'])
                    globalData.electromagnet = int(mensagem_recebida['electromagnet'])
            time.sleep(2)

    def rotacionar_torre(self, graus: int) -> bool:
        if graus < -720 or graus > 720 or graus == 0: return False
        
        messageToSend = {'command':'rotacionar', 'value': graus}
        command = self.serialArduino.communication(messageToSend)
        print(messageToSend, '\n -> ', command)

        if command['executeCommand'] == 1: return True
        return False
    
    def mover_ferramenta(self, centimentros: int) -> bool:
        return True
    
    def zerar_posicao(self) -> bool:
        return True

    def valor_sensores(self) -> dict:
        return {}

    def atuar_ferramenta(self, status: bool) -> bool:
        return True