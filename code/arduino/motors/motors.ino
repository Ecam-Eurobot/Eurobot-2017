#include <Wire.h>
#include "motor.h"

// This code is made for an Arduino Mega and test if
// the wheel encoder are working properly.

// I2C address
const byte SLAVE_ADDRESS = 0x05;

// I2C variables
byte command = 0;
byte data = 0;

byte movement_command = 0;
byte movement_data = 0;
byte speed_order = 0;
bool is_movement_command_done = true;

// Encoder wheel pins
const int IMP_ENCODER_LEFT_PIN = 2;
const int IMP_ENCODER_RIGHT_PIN = 3;
const int DIRECTION_LEFT_PIN = 4;
const int DIRECTION_RIGHT_PIN = 5;

// Motor pins.
const int PWM_MOTOR_LEFT = 10;
const int PWM_MOTOR_RIGHT = 11;
const int DIR_MOTOR_LEFT = 52;
const int DIR_MOTOR_RIGHT = 53;

Motor motor_left(PWM_MOTOR_LEFT, DIR_MOTOR_LEFT);
Motor motor_right(PWM_MOTOR_RIGHT, DIR_MOTOR_RIGHT);

void setup() {
    Serial.begin(9600);

    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    // Generate interrupt number from pins.
    int int_left = digitalPinToInterrupt(IMP_ENCODER_LEFT_PIN);
    int int_right = digitalPinToInterrupt(IMP_ENCODER_RIGHT_PIN);

    attachInterrupt(int_left, encoder_pulse_left, CHANGE);
    attachInterrupt(int_right, encoder_pulse_right, CHANGE);

    motor_left.setup();
    motor_right.setup();

    // TODO: check which one we need.
    // Increase the PWM clock speed.
    TCCR1B = TCCR1B & B11111000 | B00000001;
    TCCR2B = TCCR2B & B11111000 | B00000001;
    TCCR3B = TCCR3B & B11111000 | B00000001;
}

void loop() {
    motor_left.move_forward(40);
    motor_right.move_forward(40);
}

// Receive data from I2C communication
void receiveData(int byteCount){
    while (Wire.available()) {
        byte dataReceived = Wire.read();
        if (dataReceived == 0) { continue; }

        if (command == 0) {
            command = dataReceived;
        }
        else {
            data = dataReceived;
        }
    }
}

void sendData(){
    switch (command) {
      case 1:
          // Forward
          movement_command = command;
          movement_data = data;
          is_movement_command_done = false;
          break;

      case 2:
          // Backward
          movement_command = command;
          movement_data = data;
          is_movement_command_done = false;
          break;

      case 3:
          // Turn left
          movement_command = command;
          movement_data = data;
          is_movement_command_done = false;
          break;

      case 4:
          // Turn Rigth
          movement_command = command;
          movement_data = data;
          is_movement_command_done = false;
          break;

      case 5:
          // Stop
          motor_left.stop();
          motor_right.stop();
          break;

      case 6:
          // Set speed
          speed_order = data;
          break;

      case 7:
      // Required to define a new variable in a switch-case.
      // http://stackoverflow.com/a/2392693
      {
          // Distance
          byte buf[2]= { (byte) motor_left.get_encoder_distance(),
                (byte) motor_right.get_encoder_distance() };
          Wire.write(buf, 2);
          break;
      }

      case 8:
          // Is Done
          Wire.write(is_movement_command_done ? 1 : 0);
          break;
    }
}

// Interrupt callbacks

void encoder_pulse_left() {
    int direction = digitalRead(DIRECTION_LEFT_PIN);
    motor_left.add_encoder_pulse((direction == 1) ? 1 : -1);
}

void encoder_pulse_right() {
    int direction = digitalRead(DIRECTION_RIGHT_PIN);
    motor_right.add_encoder_pulse((direction == 0) ? 1 : -1);
}
