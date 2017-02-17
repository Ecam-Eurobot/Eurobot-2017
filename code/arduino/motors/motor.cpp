#include "motor.h"

Motor::Motor(int pwm_pin, int dir_pin):
    pwm_pin(pwm_pin), dir_pin(dir_pin), encoder_pulse(0) {

}

void Motor::setup() {
    pinMode(pwm_pin, OUTPUT);
    pinMode(dir_pin, OUTPUT);
}

void Motor::stop() {
    analogWrite(pwm_pin, 0);
}

void Motor::move_forward(int speed) {
    digitalWrite(dir_pin, LOW);
    analogWrite(pwm_pin, speed);
}

void Motor::move_backward(int speed) {
    digitalWrite(dir_pin, HIGH);
    analogWrite(pwm_pin, speed);
}

void Motor::encoder_pulse(int pulse) {
    encoder_pulse += pulse;
}

long Motor::get_encoder_impulsion() {
    return encoder_pulse;
}

int Motor::get_encoder_distance() {
    return encoder_pulse * IMP_DISTANCE;
}
