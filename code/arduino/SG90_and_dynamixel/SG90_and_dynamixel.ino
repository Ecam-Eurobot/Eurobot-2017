#include <Servo.h> 
#include <Wire.h>
#include <DynamixelSerial.h>

//Dynamixel const 
const int DYNAMIXEL_ADDRESS = 4;
const int DYNAMIXEL_CTRL_PIN = 2; 
const int ANGLE_DYNAMIXEL_HORIZONTAL = 508;
const int ANGLE_DYNAMIXEL_VERTICAL = 810;
//const int ANGLE_VERTICAL = 205; Depend on the dynamixel's position 

//I2C slave adresses
const byte SLAVE_ADDRESS = 0x06; //ToDefine 

//Clamp servo const 
const int SERVO_PIN = 9; 
const int CLAMP_OPEN_ANGLE = 0;
const int CLAMP_CLOSE_ANGLE = 180; 
Servo servo_clamp;

int servo;
int action;

//TODO Define other servos and positions 

void setup() {
   Wire.begin(SLAVE_ADDRESS);
   Wire.onReceive(receive_data);
   //Wire.onRequest(sendData);

   //Set the actual baudrate et ctrl pin (input) for the dynamixel
   pinMode(DYNAMIXEL_CTRL_PIN, INPUT); 
   Dynamixel.begin(1000000, DYNAMIXEL_CTRL_PIN);

  //Attache the clamp servo on the DYNAMIXEL_PIN (PWM);
  servo_clamp.attach(SERVO_PIN);

}

void loop() {
process_action(servo, action);
}

void receive_data(int byte_count) {
   bool command_processed = true;
  
  while(Wire.available()){
    if (command_processed == true) {
      byte dataReceived = Wire.read();
     
      servo = dataReceived >> 4;
      action = dataReceived & 0x0F;
      command_processed = false;

    } 
    else {
      Wire.read();
    }
  }
  
}

void process_action(byte servo, byte action) {
  switch (servo) {
    case 0 : 
      if (action == 0) {
        change_servo_angle(&servo_clamp, CLAMP_OPEN_ANGLE);
      } 
      else if (action == 1) {
        change_servo_angle(&servo_clamp, CLAMP_CLOSE_ANGLE);
      }
      break;
    case 1 : 
      if (action == 0) {
        move_dynamixel_angle(ANGLE_DYNAMIXEL_HORIZONTAL);
      }
      else if (action == 1) {
        move_dynamixel_angle(ANGLE_DYNAMIXEL_VERTICAL); 
      }
      break;  
   //Ohter cases ...  
   default : 
     break; //TODO : do something when value is not right?   
  } 
}


//Use a specifique servo and give it an angle
void change_servo_angle(Servo *servo, int angle) {
  servo->write(angle);  
}

void move_dynamixel_angle(int angle) {
  Dynamixel.ledStatus(DYNAMIXEL_ADDRESS,ON);
  Dynamixel.move(DYNAMIXEL_ADDRESS, angle); 
  Dynamixel.ledStatus(DYNAMIXEL_ADDRESS,OFF);
}


