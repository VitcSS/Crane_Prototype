"""Arquivo onde será inicializado o software."""

# Importações de pacotes externos
import time

# Importações de pacotes internos
from view import Controller
import globalData as globalData

gui = Controller.TkThread()

if __name__ == "__main__":
    globalData.setCurrentScreen = "POR01001"

    while True:
        print("Main loop")
        globalData.setCurrentScreen = "GUI001"
        time.sleep(1)
        globalData.setCurrentScreen = "GUI002"
        time.sleep(1)