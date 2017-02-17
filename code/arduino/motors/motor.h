#ifndef MOTOR_H
#define MOTOR_H

#include <Arduino.h>

class Motor
{
    public:
        Motor(int pwm_pin, int dir_pin);
        void setup();
        void stop();
        void move_forward(int speed);
        void move_backward(int speed);
        void encoder_pulse(int pulse);
        long get_encoder_impulsion();
        long get_encoder_distance();

    private:
        const int WHEEL_RADIUS = 4.02;
        const float WHEEL_PERIMETER = WHEEL_RADIUS * 2 * PI;
        // The encoder has a 1024 pulses/revolution.
        // The DEO nano reduces per 5 the impulsion and we take the pulse
        // when high and low.
        // The final calculus is 1024*2/5 = 409.6
        const float IMP_PER_REVOLUTION = 409.6;
        const float IMP_DISTANCE = WHEEL_PERIMETER / IMP_PER_REVOLUTION;

        int pwm_pin;
        int dir_pin;
        long encoder_pulse;
}

#endif
