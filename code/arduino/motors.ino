#include <Wire.h>

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

// TODO: verify this value!
const int WHEEL_RADIUS = 4.02;
const float WHEEL_PERIMETER = WHEEL_RADIUS * 2 * PI;
// The encoder has a 1024 pulses/revolution.
// The DEO nano reduces per 5 the impulsion and we take the pulse
// when high and low.
// The final calculus is 1024*2/5 = 409.6
const float IMP_PER_REVOLUTION = 409.6;
const float IMP_DISTANCE = WHEEL_PERIMETER / IMP_PER_REVOLUTION;

const int PWM_MOTOR_LEFT = 10;
const int PWM_MOTOR_RIGHT = 11;

const int DIR_MOTOR_LEFT = 52;
const int DIR_MOTOR_RIGHT = 53;

long counter_left = 0;
long counter_right = 0;


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

    pinMode(PWM_MOTOR_LEFT, OUTPUT);
    pinMode(PWM_MOTOR_RIGHT, OUTPUT);

    pinMode(DIR_MOTOR_LEFT, OUTPUT);
    pinMode(DIR_MOTOR_RIGHT, OUTPUT);

    // TODO: check which one we need.
    TCCR1B = TCCR1B & B11111000 | B00000001;
    TCCR2B = TCCR2B & B11111000 | B00000001;
    TCCR3B = TCCR3B & B11111000 | B00000001;
}

void loop() {
    digitalWrite(DIR_MOTOR_LEFT, LOW);
    digitalWrite(DIR_MOTOR_RIGHT, LOW);

    analogWrite(PWM_MOTOR_LEFT, 50);
    analogWrite(PWM_MOTOR_RIGHT, 50);
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
          stop_motors();
          break;

      case 6:
          // Set speed
          speed_order = data;
          break;

      case 7:
          // Distance
          byte buf[] = { convert_imp_to_cm(counter_left),
            convert_imp_to_cm(counter_right) };
          Wire.write(buf, 2);
          break;

      case 8:
          // Is Done
          Wire.write(is_movement_command_done ? 1 : 0);
          break;
    }
}

void stop_motors() {
    analogWrite(PWM_MOTOR_LEFT, 0);
    analogWrite(PWM_MOTOR_RIGHT, 0);
}

// Interrupt callbacks

void encoder_pulse_left() {
    int direction = digitalRead(DIRECTION_LEFT_PIN);
    counter_left += (direction == 1) ? 1 : -1;
}

void encoder_pulse_right() {
    int direction = digitalRead(DIRECTION_RIGHT_PIN);
    counter_right += (direction == 0) ? 1 : -1;
}

// Helper to convert impulsion to centimèter and vise-versa.

float convert_imp_to_cm(long imp) {
    return imp * IMP_DISTANCE;
}

float convert_cm_to_imp(long cm) {
    return cm / IMP_DISTANCE;
}
