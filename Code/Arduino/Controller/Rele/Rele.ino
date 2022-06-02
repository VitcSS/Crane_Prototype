#define AcionaRelay 7

int Estado = HIGH;

void setup(){
  Serial.begin(9600);
  pinMode(AcionaRelay, OUTPUT);
  delay(100);
}

void loop(){
  digitalWrite(AcionaRelay, Estado);
  Estado = !Estado;
  Serial.print("Estado: ");
  Serial.println(Estado);
  delay(2000);
}
