#include <Wire.h>
#include "motor.h"
#include "regulation.h"

/*
 * This code has been created for an Arduino Mega.
 * The left and right are defined from the back of
 * the robot.
 */

// I2C address
const byte SLAVE_ADDRESS = 0x05;

// I2C variables
byte command = 0;
int data = -1;
bool command_received = false;

// I2C commands
enum Commands {
    Forward = 1,
    Backward,
    TurnLeft,
    TurnRight,
    SetSpeed,
    Stop,
    GetDistanceDone,
    IsDone,
    IsStopped,
    Resume
};

// Encoder wheel pins
// IMP_ENCODER_{LEFT,RIGHT}_PIN should be interrupt pins.
const int IMP_ENCODER_LEFT_PIN = 2;
const int IMP_ENCODER_RIGHT_PIN = 3;
const int DIRECTION_LEFT_PIN = 4;
const int DIRECTION_RIGHT_PIN = 5;

// Motor pins.
const int PWM_MOTOR_LEFT = 9;
const int PWM_MOTOR_RIGHT = 10;
const int DIR_MOTOR_LEFT = 12;
const int DIR_MOTOR_RIGHT = 13;


Motor motor_left(PWM_MOTOR_LEFT, DIR_MOTOR_LEFT);
Motor motor_right(PWM_MOTOR_RIGHT, DIR_MOTOR_RIGHT);

Regulation *regulation = 0;

int motor_speed = 0;

// Distance already done during the regulation.
// Could be useful if we need the position when we
// encounter an obstacle.
int distance_already_done[] = { 0, 0 };

void setup() {
    Serial.begin(9600);

    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receive_i2c_data);
    Wire.onRequest(send_i2c_data);

    // Generate interrupt number from pins.
    int int_right = digitalPinToInterrupt(IMP_ENCODER_RIGHT_PIN);
    int int_left = digitalPinToInterrupt(IMP_ENCODER_LEFT_PIN);

    attachInterrupt(int_left, encoder_pulse_left, CHANGE);
    attachInterrupt(int_right, encoder_pulse_right, CHANGE);
    motor_left.setup();
    motor_right.setup();

    // Increase the PWM clock speed.
    TCCR1B = TCCR1B & 0b11111000 | 0x01;
}


void loop() {
    if (regulation) {
        // Tune the motors speed.
        regulation->tune();
    }
    delay(10);
}

// Receive data from I2C communication
void receive_i2c_data(int byteCount) {
    while (Wire.available()) {

        byte dataReceived = Wire.read();
        if (dataReceived == 0) continue;

        if (! command_received) {
            command = dataReceived;
            command_received = true;
        } else {
            data = dataReceived;
        }
    }
    if ((data != -1) || !has_command_data(command)) {
        execute_action();
    }
}

bool has_command_data(int command) {
    switch (command) {
        case Forward:
        case Backward:
        case TurnLeft:
        case TurnRight:
        case SetSpeed:
            return true;
    }
    return false;
}

void execute_action() {
    // Cleanup regulation object and initialize a new one if we
    // order a new regulation.
    switch(command) {
        case Forward:
        case Backward:
            delete regulation;
            regulation = new LeadRegulation(&motor_left, &motor_right);
            if (motor_speed) {
                regulation->set_max_speed(motor_speed);
            }
            reset_distance_already_done();
            break;

        case TurnLeft:
        case TurnRight:
            delete regulation;
            regulation = new RotationRegulation(&motor_left, &motor_right);
            if (motor_speed) {
                regulation->set_max_speed(motor_speed);
            }
            reset_distance_already_done();
            break;
    }

    // Execute the command.
    switch(command) {
        case Forward:
            regulation->set_setpoint(Motor::convert_cm_to_imp(data));
            break;

        case Backward:
            regulation->set_setpoint(-Motor::convert_cm_to_imp(data));
            break;

        case TurnRight:
            regulation->set_setpoint(Motor::convert_angle_to_imp(data));
            break;

        case TurnLeft:
            regulation->set_setpoint(-Motor::convert_angle_to_imp(data));
            break;

        case SetSpeed:
            regulation->set_max_speed(data);
            motor_speed = data;
            break;

        case Stop:
            regulation->stop();
            break;

        case Resume:
            regulation->resume();
            break;
    }

    // Reset I2C data.
    data = -1;
    command_received = false;
}

void send_i2c_data() {
    switch (command) {
        case GetDistanceDone:
        // Required to define a new variable in a switch-case.
        // http://stackoverflow.com/a/2392693
        {
            byte buf[2]= { (byte) motor_left.get_encoder_distance(),
                (byte) motor_right.get_encoder_distance() };

            for (int i = 0; i < 2; i++) {
                buf[i] = buf[i] - distance_already_done[i];
                distance_already_done[i] = distance_already_done[i] + buf[i];
            }

            Wire.write(buf, 2);
            break;
        }

        case IsDone:
            // Is Done
            Wire.write(regulation->is_finished());
            break;

        case IsStopped:
            // Is stopped
            Wire.write(regulation->is_stopped());
            break;
    }
}

// Interrupt routine called when a pulse is detected from the
// wheel encoder pins.The direction left is the opposite of the right
// direction because the 2 wheels encoders are in mirrors.

void encoder_pulse_right() {
    int direction = digitalRead(DIRECTION_RIGHT_PIN);
    motor_right.count_encoder_pulse((direction == 1) ? 1 : -1);
}

void encoder_pulse_left() {
    int direction = digitalRead(DIRECTION_LEFT_PIN);
    motor_left.count_encoder_pulse((direction == 0) ? 1 : -1);
}

void reset_distance_already_done() {
    for (int i = 0; i < 2; i++) {
        distance_already_done[i] = 0;
    }
}
