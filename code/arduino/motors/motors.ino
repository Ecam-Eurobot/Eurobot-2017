#include <Wire.h>
#include "motor.h"
#include "regulation.h"

// I2C address
const byte SLAVE_ADDRESS = 0x05;

// I2C variables
byte command = 0;
byte data = 0;

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

Regulation *regulation = 0;

void setup() {
    Serial.begin(9600);

    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receive_i2c_data);
    Wire.onRequest(send_i2c_data);

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
    if (regulation) {
        regulation->tune();
    }
    delay(10);
}

// Receive data from I2C communication
void receive_i2c_data(int byteCount) {
    bool command_received = false;

    while (Wire.available()) {
        byte dataReceived = Wire.read();
        if (dataReceived == 0) continue;

        if (! command_received) {
            command = dataReceived;
            command_received = true;

            // Some commands don't need data.
            // TODO: find if this one is required.
            // Could be cool if we don't needed... Feels like a big hack
            // to me.
            if (command > 5) {
                break;
            }
        } else {
            data = dataReceived;
        }
    }
    execute_action();
}

void execute_action() {
    // Cleanup regulation object and initialize a new one.
    switch(command) {
        case Forward:
        case Backward:
            delete regulation;
            regulation = new LeadRegulation(&motor_left, &motor_right);
            break;

        case TurnLeft:
        case TurnRight:
            delete regulation;
            regulation = new RotationRegulation(&motor_left, &motor_right);
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
            break;

        case Stop:
            regulation->stop();
            break;

        case Resume:
            regulation->resume();
            break;
    }
}

void send_i2c_data() {
    switch (command) {
        case GetDistanceDone:
        // Required to define a new variable in a switch-case.
        // http://stackoverflow.com/a/2392693
        {
            byte buf[2]= { (byte) motor_left.get_encoder_distance(),
                (byte) motor_right.get_encoder_distance() };
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

void encoder_pulse_left() {
    int direction = digitalRead(DIRECTION_LEFT_PIN);
    motor_left.count_encoder_pulse((direction == 1) ? 1 : -1);
}

void encoder_pulse_right() {
    int direction = digitalRead(DIRECTION_RIGHT_PIN);
    motor_right.count_encoder_pulse((direction == 0) ? 1 : -1);
}
