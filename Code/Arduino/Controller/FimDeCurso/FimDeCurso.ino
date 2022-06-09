
void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT); //DEFINE O PINO COMO ENTRADA / "_PULLUP" É PARA ATIVAR O RESISTOR INTERNO
}
void loop(){
  if(digitalRead(A0) == LOW){ //SE A LEITURA DO PINO FOR IGUAL A LOW, FAZ
      Serial.println("DESATIVADA");
  }else{ //SENÃO, FAZ
    Serial.println("ATIVADO");
  }
  delay(500);
}
