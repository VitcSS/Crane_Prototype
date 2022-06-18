from controllers.Strategy import Context
from controllers.Arduino import Arduino
from controllers.Copelia import Copelia

import threading
import time

interface = Context(Arduino())

if __name__ == "__main__":
    
    existsThread = next((thread for thread in threading.enumerate() if thread.name == 'thread_atualiza_telemetria'), False)
    if existsThread == False:
        print("cria thread radio")
        radioThread = threading.Thread(target = interface.thread_atualiza_telemetria, daemon=True, name="thread_atualiza_telemetria")
        radioThread.start()

    while 1:
        print("Escolha uma opção:")
        print("1 - rotacionar_torre")
        print("2 - mover_ferramenta")
        print("3 - zerar_posicao")
        print("4 - valor_sensores")
        print("5 - atuar_ferramenta")
        inp = int(input("> "))
        value = 0
        if (inp == 1 or inp == 2 or inp == 5):
            value = int(input("Insira o valor\n> "))
        
        if inp == 1:
            print("Valor: ", value)
            interface.rotacionar_torre(value)
            interface.valor_sensores()
        if inp == 2:
            interface.mover_ferramenta(value)
        if inp == 3:
            interface.zerar_posicao()
        if inp == 4:
            interface.valor_sensores()
        if inp == 5:
            ima = False
            if value == 1: ima = True
            interface.atuar_ferramenta(ima)
        
        print("\n")