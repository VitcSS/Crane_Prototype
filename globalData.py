"""ARQUIVO COM DADOS GLOBAIS PARA O SISTEMA"""

import threading

global tela_selecionada
tela_selecionada = 'POR01001'
"""Choice current screen for system."""

"""EVENTO PARA GERENCIAR INPUT DE DADOS"""
eventos = threading.Event()

"""VARIAVEIS GLOBAIS DE FLUXO DE DADOS COM INTERFACE"""
global dataInput, dataOutput
dataInput = None
"""interface for data flow."""
dataInput2 = None
"""interface for data flow."""
dataInput3 = None
"""interface for data flow."""
dataOutput = None
"""interface for data flow."""
