#include <Stepper.h>

const int stepsPerRevolution = 64;

//Inicializa a biblioteca utilizando as portas de 8 a 11 para
//ligacao ao motor
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

void setup()
{
  Serial.begin(9600);

  //Determina a velocidade inicial do motor
  myStepper.setSpeed(300);
}

void loop()
{
  if (Serial.available()) {
    String data = Serial.readString();
    
    if (data.startsWith("speed:")) {
      int newSpeed = data.substring(6).toInt();

      if (newSpeed > 500) {
        Serial.println("Could not set speed up to 500!");
      } else {
        myStepper.setSpeed(newSpeed);
        Serial.print("Speed setted to: ");
        Serial.println(newSpeed);
      }
    } else if (data.startsWith("steps:")) {
      int steps = data.substring(6).toInt();
      Serial.print("Steps: ");
      Serial.println(steps);
      myStepper.step(steps);
      delay(2);
    }
  }
}
