#ifndef REGULATION_H
#define REGULATION_H

#include "motor.h"

class Regulation {
    public:
        Regulation(Motor *left, Motor *right);
        void set_setpoint(int setpoint);
        void tune();
        void set_max_speed(int maxspeed);
        void resume();
        void stop();
        bool is_stopped() const;
        bool is_finished() const;

    protected:
        int setpoint;

        virtual float get_rotation_error();
        virtual float get_lead_error();

    private:
        // Regulation gain.
        const float KP_LEAD = 0.4;
        const float KP_ROT = 0.5;
        const float KI_LEAD = 0.0057;
        const float KI_ROT = 0.005;

        const int SUM_ERRORS_LIMIT = 300;
        const int INTEGRAL_SATURATION = 60;
        // Limit the speed command to the last command + PROGRESSIVE_COMMAND
        // to avoid demanding too much to the motors and the alim.
        const int PROGRESSIVE_COMMAND = 3;
        // Difference of commands to decide if we need to increase the max
        // speed of a motor.
        const int COMMAND_DELTA = 4;
        const int MAX_SPEED_BOOST = 20;

        const int REGULATION_PRECISION = 15;

        Motor *motor_left, *motor_right;
        int maxspeed = 50;
        float sum_errors_lead, sum_errors_rot;
        bool finished, stopped;

        void reset();
        bool is_finished(float lead_err, float rot_err);
        void update_sum_errors(float lead, float rot);
        float get_lead_regulation(float error);
        float get_rotation_regulation(float error);
        float saturate_integral_regulation(float value);
        float set_command_limit(Motor *motor, float command);
        void send_command(float cmd_left, float cmd_right);
};

class LeadRegulation : public Regulation {
    public:
        LeadRegulation(Motor *left, Motor *right);

    private:
        float get_lead_error();
};

class RotationRegulation : public Regulation {
    public:
        RotationRegulation(Motor *left, Motor *right);

    private:
        float get_rotation_error();
};

#endif
