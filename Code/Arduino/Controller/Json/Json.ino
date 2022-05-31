#include <ArduinoJson.h>

// Indica se recebeu comando do supervisorio
int command = 0;
// Indica se executou o comando solicitado pelo supervisorio
int executeCommand = 0;
// Indica a distancia da ferramenta
float distanceTool = 0;

//--- Variáveis para armazenamento dos dicionamos de leitura e escrita de dados para comunicação com o supervisorio ---
StaticJsonDocument<128> messageToSend;
StaticJsonDocument<96> receivedMessage;

void sendMessage();
void readCommand();
void readSensors();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()){  //Tratemento da interrupção Serial
    readCommand();
  }
}

void readSensors (){
  
}

void sendMessage (){ 
  readSensors ();
  messageToSend["executeCommand"]            = executeCommand;
  messageToSend["distanceTool"]              = distanceTool;
    
  serializeJson(messageToSend, Serial);
  Serial.print('\n');
}

void readCommand (){
  //tenta ler a mensagem via serial
  DeserializationError err = deserializeJson(receivedMessage, Serial.readStringUntil('\n'));
  
  //Se ocorreu leitura, interpreta o que foi enviado
  if(err.code() == DeserializationError::Ok){
    
    command = receivedMessage["commandFlag"];

    if (command == 1) // flag de comando
    {
      executeCommand = 1;
      sendMessage();
    }else if(command == 2){ //flag de leitura 
      executeCommand = 0;
      distanceTool = 10.0;
      sendMessage();
    }
  }
}
