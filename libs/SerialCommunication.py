import serial
# from ast import literal_eval
from clrprint import *
import json
from libs.Singleton import Singleton

class SerialCommunication(metaclass=Singleton):
    def __init__(self, port: str, baudrate: int = 9600, timeoutUart: int = 0.1, MAXIMUM_TRY_SEND_RECEIVE_MICROCONTROLLER_SERIAL: int = 1, \
        MAXIMUM_TRY_RECEIVE_MICROCONTROLLER_SERIAL: int = 10, DEBUG_MODE: bool = False):
        self.__microcontrollerConnectionSerial = None
        self.__port = port
        self.__baudrate = baudrate
        self.__timeout = timeoutUart
        self.__DEBUG_MODE = DEBUG_MODE
        self.__messageToSend = ''
        self.__messageReceived = {}
        self.__MAXIMUM_TRY_SEND_RECEIVE_MICROCONTROLLER_SERIAL = MAXIMUM_TRY_SEND_RECEIVE_MICROCONTROLLER_SERIAL
        self.__MAXIMUM_TRY_RECEIVE_MICROCONTROLLER_SERIAL = MAXIMUM_TRY_RECEIVE_MICROCONTROLLER_SERIAL
        """
        dict = {"ICD":1,"commandFlag":0,"stateSbc":1} > len  = 38
        Apenas para testes locais
        """

    def startCommunication(self):
        try:
            self.__microcontrollerConnectionSerial = serial.Serial(self.__port, self.__baudrate, timeout=self.__timeout)
            self.__messageToSend = ''
            self.__messageReceived = {}
            self.__microcontrollerConnectionSerial.flushInput()
            self.__microcontrollerConnectionSerial.flushOutput()
        except:
            self.__microcontrollerConnectionSerial = None
        return self.__microcontrollerConnectionSerial

    def __closeCommunication(self):
        if self.__microcontrollerConnectionSerial is not None:
            try:
                self.__microcontrollerConnectionSerial.close()
            except:
                self.__microcontrollerConnectionSerial = None

    def sendMessage(self, messageToSend: str = ''):
        if self.__microcontrollerConnectionSerial is not None:
            try:
                if messageToSend != '':
                    self.__messageToSend = str(messageToSend)+"\n"
                self.__microcontrollerConnectionSerial.write(self.__messageToSend.encode('utf-8'))
            except:
                pass

    def receiveMessage(self):
        self.__messageReceived = {}
        if self.__microcontrollerConnectionSerial is not False:
            try:
                self.__messageReceived = self.__microcontrollerConnectionSerial.readline().decode('utf-8').rstrip()
                if len(self.__messageReceived)>0:
                    try:
                        self.__messageReceived = json.loads(self.__messageReceived)
                        if type(self.__messageReceived) is dict:
                            pass
                        else:
                            self.__messageReceived = {}
                    except:
                        self.__messageReceived = {}
                else:
                    self.__messageReceived = {}
            except:
                pass
        return self.__messageReceived

    def __del__(self):
        self.__closeCommunication()

    def communication(self, messageToSend: str, MAXIMUM_TRY_SEND_RECEIVE_MICROCONTROLLER_SERIAL: int = 0, MAXIMUM_TRY_RECEIVE_MICROCONTROLLER_SERIAL: int = 0)-> dict:
        """Send and receive message in communication."""
        if MAXIMUM_TRY_SEND_RECEIVE_MICROCONTROLLER_SERIAL != 0:
            self.__MAXIMUM_TRY_SEND_RECEIVE_MICROCONTROLLER_SERIAL = MAXIMUM_TRY_SEND_RECEIVE_MICROCONTROLLER_SERIAL
        if MAXIMUM_TRY_RECEIVE_MICROCONTROLLER_SERIAL != 0:
            self.__MAXIMUM_TRY_RECEIVE_MICROCONTROLLER_SERIAL = MAXIMUM_TRY_RECEIVE_MICROCONTROLLER_SERIAL
        self.__messageToSend = json.dumps(messageToSend)+"\n"
        self.__messageReceived = {}

        if self.__microcontrollerConnectionSerial is None:
            return self.__messageReceived
        
        for COUNT_TRY_SEND_RECEIVE_MICROCONTROLLER_SERIAL in range(self.__MAXIMUM_TRY_SEND_RECEIVE_MICROCONTROLLER_SERIAL):
            clrprint('-----------SERIAL-----------\n'+ 'mensagem enviada: ', clr='p', debug=self.__DEBUG_MODE)
            clrprint(self.__messageToSend, clr='p', debug=self.__DEBUG_MODE)
            self.sendMessage()

            for COUNT_TRY_RECEIVE_MICROCONTROLLER_SERIAL in range(self.__MAXIMUM_TRY_RECEIVE_MICROCONTROLLER_SERIAL):
                self.receiveMessage()
                if len(self.__messageReceived)>0:
                    break
                else:
                    self.__messageReceived = {}
                # if len(self.__messageReceived)>0:
                #     try:
                #         self.__messageReceived = json.loads(self.__messageReceived)
                #         if type(self.__messageReceived) is dict:
                #             break
                #         else:
                #             self.__messageReceived = {}
                #     except:
                #         self.__messageReceived = {}
                # else:
                #     self.__messageReceived = {}
            if self.__messageReceived != {}:
                break

        clrprint('-----------SERIAL-----------\n'+ 'mensagem recebida: ', clr='y', debug=self.__DEBUG_MODE)
        clrprint(self.__messageReceived, clr='y', debug=self.__DEBUG_MODE)
        return self.__messageReceived