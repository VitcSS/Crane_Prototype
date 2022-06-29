#include <ArduinoJson.h>
#include <Stepper.h>
#include <Ultrasonic.h>

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
int distanceTool = 0;
// Indica a posição da torre
int towerPosition = 0;
#define MAX_POS_TOWER 360
// Indica se o eletroima esta ativo ou não
int electromagnet = 0;

// Indica a posição da ferramenta
int toolPosition = 27;

#define RST 11              // Porta digital D08 - reset do A4988
#define ENA 12              // Porta digital D07 - ativa (enable) A4988
#define DIR 9              // Porta digital D03 - direção (direction) do A4988
#define STP 10              // Porta digital D02 - passo(step) do A4988

int MeioPeriodo = 1000;   // MeioPeriodo do pulso STEP em microsegundos F= 1/T = 1/2000 uS = 500 Hz
float PPS = 0;            // Pulsos por segundo
boolean sentido = true;   // Variavel de sentido
long PPR = 3200;           // Número de passos por volta
long Pulsos;              // Pulsos para o driver do motor
float RPM;                // Rotacoes por minuto

// Inicia variáveis de tempo
unsigned long telemetria = millis();

int RELE = 8;

#define stepsPerRevolution 64

//Inicializa a biblioteca utilizando as portas de 8 a 11 para
#define IN_1 2
#define IN_2 3
#define IN_3 4
#define IN_4 5
Stepper motorVertical(stepsPerRevolution, IN_1, IN_3, IN_2, IN_4);

//Define os pinos para o trigger e echo
#define pino_trigger 7
#define pino_echo 6

//Inicializa o sensor nos pinos definidos acima
Ultrasonic ultrasonic(pino_trigger, pino_echo);

//--- Variáveis para armazenamento dos dicionamos de leitura e escrita de dados para comunicação com o supervisorio ---
StaticJsonDocument<128> messageToSend;
StaticJsonDocument<96> receivedMessage;

void sendMessage();
void readExecuteCommand();
void readSensors();
void rst_A4988();
void disa_A4988();
void ena_A4988();
void HOR();
void AHR();
void PASSO();
int giraMotorTorre(int graus);
int giraMotorFerrementa(int centimetros);
void ativaRele();
void desativaRele();

void setup()
{
  // Serial
  Serial.begin(9600);

  // Motor de passo nema
  pinMode(RST, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(STP, OUTPUT);
  disa_A4988();             // Desativa o chip A4988
  rst_A4988();              // Reseta o chip A4988
  
  // Rela que ativa eletroima
  pinMode(RELE, OUTPUT);
  desativaRele();
  
  // Motor passo fraco
  motorVertical.setSpeed(512);
}

void loop()
{
  // put your main code here, to run repeatedly:
  if (Serial.available()){  //Tratemento da interrupção Serial
    readExecuteCommand();
  }
}

int giraMotorFerrementa(int centimetros)
{
  if (centimetros >= -30 && centimetros <= 30 && centimetros != 0) {
    /*
    * 2048 - 13,823
    * x    - 1
    * x = 585,14
    */
    int uma_volta_steps = 2048;
    float uma_volta_cm = 13.823;
    int steps_um_cm = uma_volta_steps/uma_volta_cm;       
    int contador = 0;
    for (int i = 0; i<abs(centimetros); i++) {
      if (centimetros > 0)
      {
        motorVertical.step(steps_um_cm);
        toolPosition = toolPosition - contador;
        contador = i+1;
        toolPosition = toolPosition + contador;
      }
      else 
      {
        motorVertical.step(-1*steps_um_cm);
        toolPosition = toolPosition + contador;
        contador = i+1;
        toolPosition = toolPosition - contador;
      }
      readSensors ();
      sendMessage();
    }
    return centimetros;
  } else {
    return 0; 
  }
}

void ativaRele() 
{
  digitalWrite(RELE, LOW);
}

void desativaRele() 
{
  digitalWrite(RELE, HIGH);
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

int giraMotorTorre(int graus)
{
  if (graus>360 || graus <-360 || graus == 0) return 0;
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

  // Serial.print(" pulsos= ");
  // Serial.print(pulsos_f);
  // Serial.print(" Passos= ");
  // Serial.print(int(pulsos_f));
  ena_A4988();                            // Ativa o chip A4988  
  int contador = 0;
  for (int i = 0; i <= int(pulsos_f); i++)       // Incrementa o Contador
  {
    PASSO();                              // Avança um passo no Motor

    // Verifica se já passou 1000 milisegundos
    if((millis() - telemetria) > 1000){
      if (graus > 0)
      {
        towerPosition = towerPosition - contador;
        contador = int(i/(8.888888888888888888*5));
        towerPosition = towerPosition + contador;
      }
      else 
      {
        towerPosition = towerPosition + contador;
        contador = int(i/(8.888888888888888888*5));
        towerPosition = towerPosition - contador;
      }
      readSensors ();
      sendMessage();
      telemetria = millis();
    }
  }
  disa_A4988();                           // Desativa o chip A4988
  delay (100) ;                          // Atraso de 1 segundo

  if (graus > 0)
  {
    towerPosition = towerPosition - contador;
    towerPosition = towerPosition + int(pulsos_f/(8.888888888888888888*5));
  }
  else 
  {
    towerPosition = towerPosition + contador;
    towerPosition = towerPosition - int(pulsos_f/(8.888888888888888888*5));
  }
  
  if (graus > 0) return int(pulsos_f/(8.888888888888888888*5));
  else return -int(pulsos_f/(8.888888888888888888*5));
}

void readSensors ()
{
  long microsec;
  microsec = ultrasonic.timing();
  distanceTool = ultrasonic.convert(microsec, Ultrasonic::CM);
  /*
  delay(50);
  microsec = ultrasonic.timing();
  cmMsec2 = ultrasonic.convert(microsec, Ultrasonic::CM);
  delay(50);
  microsec = ultrasonic.timing();
  cmMsec3 = ultrasonic.convert(microsec, Ultrasonic::CM);
  distanceTool = (int(cmMsec1) + int(cmMsec2) + int(cmMsec3))/3;
  // cmMsec1 >>  ou cmMsec1 <<
  if ((cmMsec1 > (cmMsec2-1) && cmMsec1 > (cmMsec3-1)) || (cmMsec1 < (cmMsec2+1) && cmMsec1 < (cmMsec3+1))) distanceTool = (int(cmMsec2) + int(cmMsec3)) / 2;
  // cmMsec2 >>  ou cmMsec2 <<
  if ((cmMsec2 > (cmMsec1-1) && cmMsec2 > (cmMsec3-1)) || (cmMsec2 < (cmMsec1+1) && cmMsec2 < (cmMsec3+1))) distanceTool = (int(cmMsec1) + int(cmMsec3)) / 2;
  // cmMsec3 >>  ou cmMsec3 <<
  if ((cmMsec3 > (cmMsec1-1) && cmMsec3 > (cmMsec2-1)) || (cmMsec3 < (cmMsec1+1) && cmMsec3 < (cmMsec2+1))) distanceTool = (int(cmMsec1) + int(cmMsec2)) / 2;
  */
}

void sendMessage ()
{ 
  messageToSend["executeCommand"]            = executeCommand;
  messageToSend["distanceTool"]              = distanceTool;
  messageToSend["towerPosition"]             = towerPosition;
  messageToSend["electromagnet"]             = electromagnet;
  messageToSend["toolPosition"]              = toolPosition;
    
  serializeJson(messageToSend, Serial);
  Serial.print('\n');
}

void readExecuteCommand ()
{
  //tenta ler a mensagem via serial
  DeserializationError err = deserializeJson(receivedMessage, Serial.readStringUntil('\n'));
  
  //Se ocorreu leitura, interpreta o que foi enviado
  if(err.code() == DeserializationError::Ok){
    command = receivedMessage["command"].as<String>();
    if (command.equals(ROTACIONAR)) {
      executeCommand = 1;
      int value = receivedMessage["value"].as<int>();
      if ((value + towerPosition) > MAX_POS_TOWER || (value + towerPosition) < -MAX_POS_TOWER) {
        executeCommand = -1;
        sendMessage();
      } else {
        sendMessage();
        telemetria = millis();
        int grausGirado = giraMotorTorre(value);
      }
    } else if (command.equals(SUBIR_DESCER)) {
      executeCommand = 1;
      int value = receivedMessage["value"].as<int>();
      /*if ((toolPosition + value) < 0 || (toolPosition + value) > 30) {
        executeCommand = -1;
        sendMessage();
      } else { */
        giraMotorFerrementa(value);
        sendMessage();
      // }
    } else if (command.equals(ZERAR)) {
      executeCommand = 1;
      distanceTool = 0;
      towerPosition = 0;
      electromagnet = 0;
      sendMessage();
    } else if (command.equals(IMA)) {
      executeCommand = 1;
      sendMessage();
      int value = receivedMessage["value"].as<int>();
      if (value == 1) {
        ativaRele();
      } else {
        desativaRele();
      }
    } else if (command.equals(SENSORES)) {
      executeCommand = 0;
      readSensors ();
      sendMessage();
    } else{
      executeCommand = -1;
      sendMessage();      
    }
  }
}
