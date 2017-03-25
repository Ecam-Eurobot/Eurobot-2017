#include "motor.h"

Motor::Motor(int pwm_pin, int dir_pin):
    pwm_pin(pwm_pin), dir_pin(dir_pin), encoder_counter(0), speed(0) { }

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

int Motor::get_speed() const {
    return speed;
}

void Motor::count_encoder_pulse(int pulse) {
    encoder_counter += pulse;
}

void Motor::reset_encoder_counter() {
    encoder_counter = 0;
}

// Get the number of pulse from the wheel encoder.
long Motor::get_encoder_counter() const {
    return encoder_counter;
}

int Motor::get_encoder_distance() const {
    return convert_imp_to_cm(encoder_counter);
}

static long Motor::convert_cm_to_imp(int cm) {
    return cm / IMP_DISTANCE;
}

static int Motor::convert_imp_to_cm(long imp) {
    return imp * IMP_DISTANCE;
}

static long Motor::convert_angle_to_imp(int angle) {
    return angle * ANGLE_CORRECTION / IMP_DISTANCE;
}
