"""Arquivo onde será inicializado o software."""
# Importações de pacotes externos
import time

# Importações de pacotes internos
from view import Controller
import globalData as globalData

from controllers.Strategy import Context
from controllers.Arduino import Arduino
# from controllers.Copelia import Copelia

interface = Context(Arduino())

gui = Controller.TkThread()
globalData.telaSelecionada = "GUI001"

if __name__ == "__main__":
    stateFsm = 1

    while 1:
        # escolhe o tipo de guindaste
        if stateFsm == 1:
            globalData.telaSelecionada = "GUI001"
            globalData.eventos.wait()
            globalData.eventos.clear()

            stateFsm = 3

            if globalData.dataInput == 'copelia':
                stateFsm = 2

            globalData.dataInput = None

        # controla com copelia
        if stateFsm == 2:
            print("COPELIA")
            # interface.strategy = Copelia()
            globalData.telaSelecionada = "GUI002"
            globalData.guindasteSelecionado = 'copelia'
            while 1:
                if globalData.dataInput == 'rotacionar_torre':
                    print("ROTACIONA")
                if globalData.dataInput == 'mover_ferramenta':
                    print("MOVER FERRAMENTA")
                if globalData.dataInput == 'atuar_ferramenta':
                    print("ATUAR FERRAMENTA")
                if globalData.dataInput == 'voltar_menu':
                    stateFsm = 1
                    break
                time.sleep(0.00001)

        # controla com arduino
        if stateFsm == 3:
            print("ARDUINO")
            globalData.telaSelecionada = "GUI002"
            globalData.guindasteSelecionado = 'arduino'
            interface.rotacionar_torre(0)
            while 1:
                if globalData.dataInput == 'rotacionar_torre':
                    print("ROTACIONA")
                    globalData.dataInput = None
                    interface.rotacionar_torre(globalData.dataInput2)
                    globalData.dataInput2 = None
                    time.sleep(0.5)
                if globalData.dataInput == 'mover_ferramenta':
                    print("MOVER FERRAMENTA")
                    globalData.dataInput = None
                    interface.mover_ferramenta(globalData.dataInput2)
                    globalData.dataInput2 = None
                    time.sleep(0.5)
                if globalData.dataInput == 'atuar_ferramenta':
                    print("ATUAR FERRAMENTA")
                    globalData.dataInput = None
                    interface.atuar_ferramenta(globalData.dataInput2)
                    globalData.dataInput2 = None
                    time.sleep(0.5)
                if globalData.dataInput == 'voltar_menu':
                    stateFsm = 1
                    break
                time.sleep(0.00001)
