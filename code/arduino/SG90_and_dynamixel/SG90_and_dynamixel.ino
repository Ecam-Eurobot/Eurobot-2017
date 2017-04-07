#include <Servo.h> 
#include <Wire.h>
#include <DynamixelSerial.h>

//Dynamixel const 
const int DYNAMIXEL_ADDRESS = 6;
const int DYNAMIXEL_CTRL_PIN = 2; 
//RIGHT VALUE FOR DYNAMIXEL
const int ANGLE_DYNAMIXEL_HORIZONTAL = 508;
const int ANGLE_DYNAMIXEL_VERTICAL = 830;
//const int ANGLE_VERTICAL = 205; Depend on the dynamixel's position 

//I2C slave adresses
const byte SLAVE_ADDRESS = 0x06; //ToDefine 

//Clamp servo const 
const int SERVO_CLAMP_PIN = 9; 
const int SERVO_PUSH_PIN = 10;
const int PUSH_BACK = 60;
const int PUSH_OUT = 20; 
const int CLAMP_OPEN_ANGLE = 70;
const int CLAMP_CLOSE_ANGLE = 180; 
Servo servo_clamp;
Servo servo_push;
 
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

  //Attache the servo on the PWM pin;
  servo_clamp.attach(SERVO_CLAMP_PIN);
  servo_push.attach(SERVO_PUSH_PIN);
  //servo_stack.attach(SERVO_STACK_PIN);
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
    case 2: 
      if (action == 0) {
        change_servo_angle(&servo_push, PUSH_BACK);
      } 
      else if (action == 1) {
        change_servo_angle(&servo_push, PUSH_OUT);
      }
      break;   
   default : 
     break; //do something when value is not right?   
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


