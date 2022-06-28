"""Arquivo onde será inicializado o software."""
# Importações de pacotes externos
import time

# Importações de pacotes internos
from view import Controller
import globalData as globalData

from controllers.Strategy import Context
from controllers.Arduino import Arduino
from controllers.Copelia import Copelia

interface = Context(Arduino())

gui = Controller.TkThread()

if __name__ == "__main__":   
    stateFsm = 1
    while 1:
        # escolhe o tipo de guindaste
        if stateFsm == 1:
            globalData.tela_selecionada = "GUI001"
            globalData.eventos.wait()
            globalData.eventos.clear()    

            stateFsm = 3
            if globalData.dataInput == 'copelia':
                stateFsm = 2
            
            globalData.dataInput = None
        
        # controla com copelia
        if stateFsm == 2:
            globalData.tela_selecionada = "GUI002"
            while 1:
                time.sleep(0.00001)
        
        # controla com arduino
        if stateFsm == 3:
            globalData.tela_selecionada = "GUI002"
            while 1:
                time.sleep(0.00001)

                
