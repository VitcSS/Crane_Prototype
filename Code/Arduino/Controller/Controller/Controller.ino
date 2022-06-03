#include <ArduinoJson.h>

String ROTACIONAR = "rotacionar";
String SUBIR_DESCER = "subir_descer";
String ZERAR = "zerar";
String SENSORES = "sensores";
String IMA = "ima";

// Indica se recebeu comando do supervisorio
String command = "";
// Indica se executou o comando solicitado pelo supervisorio
int executeCommand = 0;
// Indica a distancia da ferramenta
float distanceTool = 0;
// Indica a posição da torre
float towerPosition = 0;
// Indica se o eletroima esta ativo ou não
float electromagnet = 0;

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
  distanceTool = 1;
  towerPosition = 1;
  electromagnet = 1;
}

void sendMessage (){ 
  // readSensors ();
  messageToSend["executeCommand"]            = executeCommand;
  messageToSend["distanceTool"]              = distanceTool;
  messageToSend["towerPosition"]             = towerPosition;
  messageToSend["electromagnet"]             = electromagnet;
    
  serializeJson(messageToSend, Serial);
  Serial.print('\n');
}

void readCommand (){
  //tenta ler a mensagem via serial
  DeserializationError err = deserializeJson(receivedMessage, Serial.readStringUntil('\n'));
  
  //Se ocorreu leitura, interpreta o que foi enviado
  if(err.code() == DeserializationError::Ok){
    command = receivedMessage["command"].as<String>();
    if (command.equals(ROTACIONAR)) {
      executeCommand = 1;
      distanceTool = 1;
      towerPosition = 360;
      electromagnet = 1;
      sendMessage();
    } else if (command.equals(SUBIR_DESCER)) {
      executeCommand = 1;
      distanceTool = 30;
      towerPosition = 1;
      electromagnet = 1;
      sendMessage();
    } else if (command.equals(ZERAR)) {
      executeCommand = 1;
      distanceTool = 0;
      towerPosition = 0;
      electromagnet = 0;
      sendMessage();
    } else if (command.equals(IMA)) {
      executeCommand = 1;
      distanceTool = 0;
      towerPosition = 0;
      electromagnet = 1;
      sendMessage();
    } else if (command.equals(SENSORES)) {
      executeCommand = 0;
      readSensors ();
      sendMessage();
    } else{
      executeCommand = -1;
      messageToSend["teste"] = command;
      sendMessage();      
    }
  }
}
