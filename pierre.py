# Importações de pacotes externos
import time

from libs.SerialCommunication import SerialCommunication

if __name__ == "__main__":
    serialCommunication = SerialCommunication(port='COM11')
    serialCommunication.startCommunication()
    
    messageToSend = {'commandFlag':1}
    print(messageToSend, '\n -> ', serialCommunication.communication(messageToSend))
    messageToSend = {'commandFlag':2}
    print(messageToSend, '\n -> ', serialCommunication.communication(messageToSend))

