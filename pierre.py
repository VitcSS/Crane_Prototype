# Importações de pacotes externos
import time

from libs.SerialCommunication import SerialCommunication

if __name__ == "__main__":
    serialCommunication = SerialCommunication(port='COM11')
    serialCommunication.startCommunication()

    messageToSend = {'command':'rotacionar', 'value': 90}
    print(messageToSend, '\n -> ', serialCommunication.communication(messageToSend))
    
    # messageToSend = {'command':'subir_descer', 'value': 10}
    # print(messageToSend, '\n -> ', serialCommunication.communication(messageToSend))
    
    # messageToSend = {'command':'zerar', 'value': -1}
    # print(messageToSend, '\n -> ', serialCommunication.communication(messageToSend))
    
    # messageToSend = {'command':'ima', 'value': 1}
    # print(messageToSend, '\n -> ', serialCommunication.communication(messageToSend))

    # time.sleep(5)

    # messageToSend = {'command':'ima', 'value': -1}
    # print(messageToSend, '\n -> ', serialCommunication.communication(messageToSend))
    
    # for i in range(5):
    #     messageToSend = {'command':'sensores', 'value': -1}
    #     print(messageToSend, '\n -> ', serialCommunication.communication(messageToSend))    
    #     time.sleep(1)