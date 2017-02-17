#include "motor.h"

Motor::Motor(int pwm_pin, int dir_pin):
    pwm_pin(pwm_pin), dir_pin(dir_pin), encoder_counter(0), speed(0) {

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
    this->speed = speed;
}

void Motor::move_backward(int speed) {
    digitalWrite(dir_pin, HIGH);
    analogWrite(pwm_pin, speed);
    this->speed = speed;
}

int Motor::get_speed() {
    return speed;
}

void Motor::count_encoder_pulse(int pulse) {
    encoder_counter += pulse;
}

void Motor::reset_encoder_counter() {
    encoder_counter = 0;
}

long Motor::get_encoder_counter() {
    return encoder_counter;
}

long Motor::get_encoder_distance() {
    return encoder_counter * IMP_DISTANCE;
}
