from controllers.Strategy import Strategy
from libs.SerialCommunication import SerialCommunication
import globalData

import threading
import time

class Arduino(Strategy):

    def __init__(self) -> None:
        self.serialArduino = None
        self.pauseThread = False
        self.threadTryReceive = False
        self._closeThread = False
        # self.inicializa_serial()

    def __del__(self):
        self._closeThread = True
        del self.serialArduino

    def inicializa_serial(self):
        existsThread = next((thread for thread in threading.enumerate() if thread.name == 'thread_atualiza_telemetria'), False)
        if existsThread == False:
            radioThread = threading.Thread(target = self.thread_atualiza_telemetria, daemon=True, name="thread_atualiza_telemetria")
            radioThread.start()
        
        existsThread = next((thread for thread in threading.enumerate() if thread.name == 'thread_solicita_atualiza_telemetria'), False)
        if existsThread == False:
            radioThread = threading.Thread(target = self.thread_solicita_atualiza_telemetria, daemon=True, name="thread_solicita_atualiza_telemetria")
            radioThread.start()

        if self.serialArduino is None:
            self.serialArduino = SerialCommunication(port='COM11', timeoutUart=0.3)
            self.serialArduino.startCommunication()
    
    def thread_atualiza_telemetria(self):
        self.inicializa_serial()

        while 1:
            if not self.pauseThread:
                self.threadTryReceive = True
                mensagem_recebida = self.serialArduino.receiveMessage()
                if 'distanceTool' in mensagem_recebida and 'towerPosition' in mensagem_recebida and 'electromagnet' in mensagem_recebida and 'toolPosition' in mensagem_recebida:
                    print("Recebi coisas: ", mensagem_recebida)
                    globalData.distanceTool = int(mensagem_recebida['distanceTool'])
                    globalData.towerPosition = int(mensagem_recebida['towerPosition'])
                    globalData.electromagnet = int(mensagem_recebida['electromagnet'])
                    globalData.toolPosition = int(mensagem_recebida['toolPosition'])
                self.threadTryReceive = False
            time.sleep(0.0001)
    
    def thread_solicita_atualiza_telemetria(self):
        self.inicializa_serial()
        while 1:
            if not self.pauseThread:
                self.valor_sensores()
                time.sleep(3)
            time.sleep(0.0001)

    def rotacionar_torre(self, graus: int) -> bool:
        self.inicializa_serial()
        if graus < -720 or graus > 720 or graus == 0: return False
        
        messageToSend = {'command':'rotacionar', 'value': graus}
        self.pauseThread = True
        while self.threadTryReceive:
            time.sleep(0.0001)
        command = self.serialArduino.communication(messageToSend)
        self.pauseThread = False
        print(messageToSend, '\n -> ', command)

        if 'executeCommand' in command and command['executeCommand'] == 1: return True
        return False
    
    def mover_ferramenta(self, centimentros: int) -> bool:
        self.inicializa_serial()
        if centimentros < -30 or centimentros > 30 or centimentros == 0: return False
        messageToSend = {'command':'subir_descer', 'value': centimentros}
        self.pauseThread = True
        while self.threadTryReceive:
            time.sleep(0.0001)
        command = self.serialArduino.communication(messageToSend)
        self.pauseThread = False
        print(messageToSend, '\n -> ', command)

        if 'executeCommand' in command and command['executeCommand'] == 1: return True
        return False

    def valor_sensores(self) -> dict:
        self.inicializa_serial()
        messageToSend = {'command':'sensores', 'value': -1}
        self.pauseThread = True
        while self.threadTryReceive:
            time.sleep(0.0001)
        command = self.serialArduino.communication(messageToSend)
        self.pauseThread = False
        print(messageToSend, '\n -> ', command)
        if 'distanceTool' in command and 'towerPosition' in command and 'electromagnet' in command  and 'toolPosition' in command: return command
        return {}

    def atuar_ferramenta(self, status: bool) -> bool:
        self.inicializa_serial()
        if status is not True and status is not False: return False
        ima = -1
        if status: ima = 1
        messageToSend = {'command':'ima', 'value': ima}
        self.pauseThread = True
        while self.threadTryReceive:
            time.sleep(0.0001)
        command = self.serialArduino.communication(messageToSend)
        self.pauseThread = False
        print(messageToSend, '\n -> ', command)

        if 'executeCommand' in command and command['executeCommand'] == 1: return True
        return False
