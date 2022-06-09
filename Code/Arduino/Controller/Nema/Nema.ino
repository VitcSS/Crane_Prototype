const int stepPin = 9;
const int dirPin = 8;
int speedTime = 500;

void setup()
{
  Serial.begin(9600);
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

void loop()
{
  if (Serial.available()) {
    String data = Serial.readString();
    if (data.startsWith("speed:")) {
      int newSpeed = data.substring(6).toInt();

      if (newSpeed < 500 || newSpeed > 1000) {
        Serial.println("Could not set speed up to 1000 ou menor que 500!");
      } else {
        speedTime = newSpeed;
        Serial.print("Speed setted to: ");
        Serial.println(newSpeed);
      }
    } else if (data.startsWith("steps:")) {
      int steps = data.substring(6).toInt();
      if (steps > 0){
        digitalWrite(dirPin, HIGH);
        for(int x = 0; x<steps; x++) {
          digitalWrite(stepPin, HIGH);
          delayMicroseconds(speedTime);
          digitalWrite(stepPin, LOW);
          delayMicroseconds(speedTime);
        }
      } else {
        digitalWrite(dirPin, LOW);
        for(int x = 0; x<steps; x++) {
          digitalWrite(stepPin, HIGH);
          delayMicroseconds(speedTime);
          digitalWrite(stepPin, LOW);
          delayMicroseconds(speedTime);
        }
      }
    }
  }
}
