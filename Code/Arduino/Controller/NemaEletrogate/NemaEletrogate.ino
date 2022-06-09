// Controle de Motor de Passo com Modulo driver A4988
//
// Modulo A4988 / Motor de Passo Bipolar / Arduino Nano / IDE 1.8.5
// Gustavo Murta 29/mar/2018

// Definiçoes das Portas Digitais do Arduino
/*
int RST = 8;              // Porta digital D08 - reset do A4988
int SLP = 9;              // Porta digital D09 - dormir (sleep) A4988
int ENA = 7;              // Porta digital D07 - ativa (enable) A4988
int MS1 = 4;              // Porta digital D04 - MS1 do A4988
int MS2 = 5;              // Porta digital D05 - MS2 do A4988
int MS3 = 6;              // Porta digital D06 - MS3 do A4988
int DIR = 3;              // Porta digital D03 - direção (direction) do A4988
int STP = 2;              // Porta digital D02 - passo(step) do A4988
*/
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

  DDRD = DDRD | B11111100;  // Configura Portas D02 até D07 como saída
  disa_A4988();             // Desativa o chip A4988

  DDRB = 0x0F;              // Configura Portas D08,D09,D10 e D11 como saída
  // digitalWrite(SLP, HIGH);  // Desativa modo sleep do A4988
  rst_A4988();              // Reseta o chip A4988
  ena_A4988();              // Ativa o chip A4988
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

void FREQUENCIA()                    // calcula Pulsos, PPS e RPM
{
  Pulsos = PPR * Voltas;             // Quantidade total de Pulsos (PPR = pulsos por volta)
  PPS = 1000000 / (2 * MeioPeriodo); // Frequencia Pulsos por segundo
  RPM = (PPS * 60) / PPR;            // Calculo do RPM
}

/*

void FULL()
{
  Serial.println(" Passo Completo  PPR = 200 ");
  PPR = 200;                 // PPR = pulsos por volta
  digitalWrite(MS1, LOW);    // Configura modo Passo completo (Full step)
  digitalWrite(MS2, LOW);
  digitalWrite(MS3, LOW);
}

void HALF()
{
  Serial.println(" Meio Passo  PPR = 400 ");
  PPR = 3200;                  // PPR = pulsos por volta
  digitalWrite(MS1, HIGH);    // Configura modo Meio Passo (Half step)
  digitalWrite(MS2, HIGH);
  digitalWrite(MS3, HIGH);
}

void P1_4()
{
  Serial.println(" Micro-passo 1/4  PPR = 800 ");
  PPR = 800;                 // PPR = pulsos por volta
  digitalWrite(MS1, LOW);    // Configura modo Micro Passo 1/4
  digitalWrite(MS2, HIGH);
  digitalWrite(MS3, LOW);
}

void P1_8()
{
  Serial.println(" Micro-passo 1/8  PPR = 1600 ");
  PPR = 1600;                 // PPR = pulsos por volta
  digitalWrite(MS1, HIGH);    // Configura modo Micro Passo 1/8
  digitalWrite(MS2, HIGH);
  digitalWrite(MS3, LOW);
}

void P1_16()
{
  Serial.println(" Micro-passo 1/16  PPR = 3200 ");
  PPR = 3200;                 // PPR = pulsos por volta
  digitalWrite(MS1, HIGH);    // Configura modo Micro Passo 1/16
  digitalWrite(MS2, HIGH);
  digitalWrite(MS3, HIGH);
}
*/
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
  Serial.print(" PPS= ");
  Serial.print(PPS, 2);
  Serial.print(" RPM= ");
  Serial.println(RPM, 2);
}

void loop()
{
  Serial.println();
  // FULL();          // Selecione aqui o modo de passo
  // HALF();        // desmarque o comentario somente da opcao desejada
  //P1_4();
  //P1_8();
  //P1_16();
  Voltas = 1;        // Selecione o numero de Voltas
  TesteMotor();      // Inicia teste do motor
}
