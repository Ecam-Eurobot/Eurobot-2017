#ifndef REGULATION_H
#define REGULATION_H

#include "motor.h"

class Regulation {
    public:
        Regulation(Motor *left, Motor *right);
        void tune();
        void set_setpoint(int setpoint);
        void set_max_speed(int maxspeed);

    protected:
        int setpoint;

        virtual float get_rotation_error();
        virtual float get_lead_error();

    private:
        const float KP_LEAD = 0.4;
        const float KP_ROT = 0.5;
        const float KI_LEAD = 0.0057;
        const float KI_ROT = 0.005;
        const int INTEGRAL_SATURATION = 60;
        const int PROGRESSIVE_COMMAND = 3;
        const int COMMAND_DELTA = 4;
        const int MAX_SPEED_BOOST = 20;

        Motor *motor_left, *motor_right;
        int maxspeed = 50;
        float sum_errors_lead, sum_errors_rot;
        bool finished;

        void reset_regulation();
        void update_sum_errors(float lead, float rot);
        float get_lead_regulation(float error);
        float get_rotation_regulation(float error);
        float saturate_integral_regulation(float value);
        float set_command_limit(Motor *motor, float command);
        void send_command(float cmd_left, float cmd_right,
                bool forward_left, bool forward_right);
};

class LeadRegulation : public Regulation {
    private:
        float get_lead_error();
};

class RotationRegulation : public Regulation {
    private:
        float get_rotation_error();
};

#endif
