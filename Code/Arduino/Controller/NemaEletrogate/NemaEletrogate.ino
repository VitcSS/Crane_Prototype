// Controle de Motor de Passo com Modulo driver A4988
//
// Modulo A4988 / Motor de Passo Bipolar / Arduino Nano / IDE 1.8.5
// Gustavo Murta 29/mar/2018

// Definiçoes das Portas Digitais do Arduino

int RST = 11;              // Porta digital D08 - reset do A4988
int ENA = 12;              // Porta digital D07 - ativa (enable) A4988
int DIR = 9;              // Porta digital D03 - direção (direction) do A4988
int STP = 10;              // Porta digital D02 - passo(step) do A4988

int MeioPeriodo = 1000;   // MeioPeriodo do pulso STEP em microsegundos F= 1/T = 1/2000 uS = 500 Hz
float PPS = 0;            // Pulsos por segundo
boolean sentido = true;   // Variavel de sentido
long PPR = 3200;           // Número de passos por volta
long Pulsos;              // Pulsos para o driver do motor
int Voltas;               // voltas do motor
float RPM;                // Rotacoes por minuto

void setup()
{
  Serial.begin(9600);
  pinMode(RST, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(STP, OUTPUT);
  disa_A4988();             // Desativa o chip A4988
  rst_A4988();              // Reseta o chip A4988
  // ena_A4988();              // Ativa o chip A4988
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

void FREQUENCIA(int graus = 0)                    // calcula Pulsos, PPS e RPM
{
  /*
  PPR = 360/g_p = 3200
  g_p = 360/3200
  g_p = 0,1125 graus
  Para girar a torre 360 x5
  g_p = 0,5625 graus
  */
  if (graus != 0){
    Pulsos = graus * 0,5625;
  } else {
    Pulsos = PPR * Voltas;             // Quantidade total de Pulsos (PPR = pulsos por volta)    
  }

  PPS = 1000000 / (2 * MeioPeriodo); // Frequencia Pulsos por segundo
  RPM = (PPS * 60) / PPR;            // Calculo do RPM
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

void TesteMotor()
{
  Print_RPM ();                           // Print Voltas, PPS e  RPM

  HOR();                                  // Gira sentido Horario
  for (int i = 0; i <= Pulsos; i++)       // Incrementa o Contador
  {
    PASSO();                              // Avança um passo no Motor
  }
  disa_A4988();                           // Desativa o chip A4988
  delay (1000) ;                          // Atraso de 1 segundo
  ena_A4988();                            // Ativa o chip A4988

  AHR();                                  // Gira sentido anti-Horario
  for (int i = 0; i <= Pulsos; i++)       // Incrementa o Contador
  {
    PASSO();                              // Avança um passo no Motor
  }
  disa_A4988();                           // Desativa o chip A4988
  delay (1000) ;                          // Atraso de 1 segundo
  ena_A4988();                            // Ativa o chip A4988
}

void Print_RPM ()
{
  FREQUENCIA();                           // calcula Pulsos, PPS e RPM
  Serial.print(" Voltas= ");
  Serial.print(Voltas);
  Serial.print(" Pulsos= ");
  Serial.print(Pulsos);
  Serial.print(" Pulsos= ");
  Serial.print(int(Pulsos));
  Serial.print(" PPS= ");
  Serial.print(PPS, 2);
  Serial.print(" RPM= ");
  Serial.println(RPM, 2);
}

void loop()
{
  Serial.println();
  Voltas = 5;        // Selecione o numero de Voltas
  // TesteMotor();      // Inicia teste do motor
  giraMotor(90);
  delay(2000);
  giraMotor(-90);
  delay(2000);
}
