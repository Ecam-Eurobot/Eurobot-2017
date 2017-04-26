#ifndef MOTOR_H
#define MOTOR_H

#include <Arduino.h>

class Motor {
    public:
        Motor(int pwm_pin, int dir_pin);
        void setup();
        void stop();
        void reset();
        void move_forward(int speed);
        void move_backward(int speed);
        int get_speed() const;
        void count_encoder_pulse(int pulse);
        void reset_encoder_counter();
        long get_encoder_counter() const;
        int get_encoder_distance() const;

        static long convert_cm_to_imp(int cm);
        static int convert_imp_to_cm(long imp);
        static long convert_angle_to_imp(int angle);

    private:
        static const int WHEEL_RADIUS = 4.02;
        static constexpr float WHEEL_PERIMETER = WHEEL_RADIUS * 2 * PI;
        // The encoder has a 1024 pulses/revolution.
        // The DEO nano reduces per 5 the impulsion and we take the pulse
        // when high and low.
        // The final calculus is 1024*2/5 = 409.6
        static constexpr float IMP_PER_REVOLUTION = 409.6;
        static constexpr float IMP_DISTANCE = WHEEL_PERIMETER / IMP_PER_REVOLUTION;
        static constexpr float ANGLE_CORRECTION = 107.5 / 360;

        int pwm_pin, dir_pin;
        long encoder_counter;
        int speed;
};

#endif
