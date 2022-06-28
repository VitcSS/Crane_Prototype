"""Arquivo onde será inicializado o software."""
# Importações de pacotes externos
import time

# Importações de pacotes internos
from view import Controller
import globalData as globalData

gui = Controller.TkThread()

if __name__ == "__main__":   
    globalData.tela_selecionada = "GUI001"
