#include <Stepper.h>

const int stepsPerRevolution = 64;

//Inicializa a biblioteca utilizando as portas de 8 a 11 para
//ligacao ao motor
Stepper myStepper(stepsPerRevolution, 2, 4, 3, 5);

void setup()
{
  Serial.begin(9600);

  //Determina a velocidade inicial do motor
  myStepper.setSpeed(512);
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
    } else if (data.startsWith("cm:")) {
      int cm = data.substring(3).toInt();
      Serial.print("cm: ");
      Serial.println(cm);
      if (cm >= -30 && cm <= 30 && cm != 0) {
        /*
         * 2048 - 13,823
         * x    - 1
         * x = 585,14
         */
         int uma_volta_steps = 2048;
         float uma_volta_cm = 13.823;
         int steps_um_cm = uma_volta_steps/uma_volta_cm;         
         myStepper.step(cm*steps_um_cm);
      } else {
        Serial.println("Valor invalido");
      }
      
      delay(2);
    }
  }
}
