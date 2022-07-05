#include <Stepper.h>

const int stepsPerRevolution = 64;

//Inicializa a biblioteca utilizando as portas de 8 a 11 para
//ligacao ao motor
#define IN_1 2
#define IN_2 3
#define IN_3 4
#define IN_4 5
Stepper myStepper(stepsPerRevolution, IN_1, IN_3, IN_2, IN_4);

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
      Serial.print("Sai da função");
      delay(2);
    }
  }
}
