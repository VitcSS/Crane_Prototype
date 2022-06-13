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

int RST = 11;              // Porta digital D08 - reset do A4988
int ENA = 12;              // Porta digital D07 - ativa (enable) A4988
int DIR = 9;              // Porta digital D03 - direção (direction) do A4988
int STP = 10;              // Porta digital D02 - passo(step) do A4988

int MeioPeriodo = 1000;   // MeioPeriodo do pulso STEP em microsegundos F= 1/T = 1/2000 uS = 500 Hz
float PPS = 0;            // Pulsos por segundo
boolean sentido = true;   // Variavel de sentido
long PPR = 3200;           // Número de passos por volta
long Pulsos;              // Pulsos para o driver do motor
float RPM;                // Rotacoes por minuto

//--- Variáveis para armazenamento dos dicionamos de leitura e escrita de dados para comunicação com o supervisorio ---
StaticJsonDocument<128> messageToSend;
StaticJsonDocument<96> receivedMessage;

void sendMessage();
void readCommand();
void readSensors();
void rst_A4988();
void disa_A4988();
void ena_A4988();
void HOR();
void AHR();
void PASSO();
int giraMotor(int graus);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  Serial.begin(9600);
  pinMode(RST, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(STP, OUTPUT);
  disa_A4988();             // Desativa o chip A4988
  rst_A4988();              // Reseta o chip A4988

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()){  //Tratemento da interrupção Serial
    readCommand();
  }
}

void rst_A4988()
{
  digitalWrite(RST, LOW);     // Realiza o reset do A4988
  delay (10);                 // Atraso de 10 milisegundos
  digitalWrite(RST, HIGH);    // Libera o reset do A4988
  delay (10);                 // Atraso de 10 milisegundos
}

void disa_A4988()
{
  digitalWrite(ENA, HIGH);    // Desativa o chip A4988
  delay (10);                 // Atraso de 10 milisegundos
}

void ena_A4988()
{
  digitalWrite(ENA, LOW);     // Ativa o chip A4988
  delay (10);                 // Atraso de 10 milisegundos
}

void HOR()                      // Configura o sentido de rotação do Motor
{
  Serial.println(" Sentido Horario ");
  digitalWrite(DIR, HIGH);      // Configura o sentido HORÁRIO
}

void AHR()                      // Configura o sentido de rotação do Motor
{
  Serial.println(" Sentido anti-Horario ");
  digitalWrite(DIR, LOW);       // Configura o sentido ANTI-HORÁRIO
}

void PASSO()                         // Pulso do passo do Motor
{
  digitalWrite(STP, LOW);            // Pulso nível baixo
  delayMicroseconds (MeioPeriodo);   // MeioPeriodo de X microsegundos
  digitalWrite(STP, HIGH);           // Pulso nível alto
  delayMicroseconds (MeioPeriodo);   // MeioPeriodo de X microsegundos
}

int giraMotor(int graus) {
  Print_RPM ();                           // Print Voltas, PPS e  RPM
  if (graus>360 || graus <-360 || graus == 0) return 0;
  Print_RPM ();                           // Print Voltas, PPS e  RPM
  int graus_intern = graus;
  if (graus > 0) {
    HOR();
  } else {
    AHR();
    graus_intern = -1 * graus;
  }

  /*
  3200 passos - 360 graus
  x passos    - 1 grau
  x = 3200/360
  x = 8,888888888888888888
  */

  float pulsos_f = graus_intern*8.888888888888888888*5;

  Serial.print(" pulsos= ");
  Serial.print(pulsos_f);
  Serial.print(" Passos= ");
  Serial.print(int(pulsos_f));
  ena_A4988();                            // Ativa o chip A4988  
  for (int i = 0; i <= int(pulsos_f); i++)       // Incrementa o Contador
  {
    PASSO();                              // Avança um passo no Motor
  }
  disa_A4988();                           // Desativa o chip A4988
  delay (1000) ;                          // Atraso de 1 segundo
  
  if (graus > 0) return int(pulsos_f/(8.888888888888888888*5));
  else return -int(pulsos_f/(8.888888888888888888*5));
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
