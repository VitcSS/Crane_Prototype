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


"""DADOS DE TELEMETRIA"""
distanceTool = 0
"""Distancia da ferramenta com algo abaixo mais proximo, em centimetros"""
towerPosition = 0
"""Posicao da torre em graus."""
electromagnet = 0
"""Indica se o eletroima esta ligado ou nao."""

"""PAUSA THREAD DE LEITURA DA SERIAL"""
pauseThread = 0
"""Quando for enviar algum comando, essa flag eh responsavel por bloquear a thread."""