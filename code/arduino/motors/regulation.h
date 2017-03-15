#ifndef REGULATION_H
#define REGULATION_H

#include "motor.h"

// Abstract class. Should not be instantiated.
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

        virtual int get_maxspeed();
        virtual float get_rotation_error();
        virtual float get_lead_error();

    private:
        // Regulation gain.
        static constexpr float KP_LEAD = 0.6;
        static constexpr float KP_ROT = 0.6;
        static constexpr float KI_LEAD = 0.006;
        static constexpr float KI_ROT = 0.01;

        static const int SUM_ERRORS_LIMIT = 300;
        static const int INTEGRAL_SATURATION = 60;
        // Limit the speed command to the last command + PROGRESSIVE_COMMAND
        // to avoid demanding too much to the motors and the alim.
        static const int PROGRESSIVE_COMMAND = 10;
        // Difference of commands to decide if we need to increase the max
        // speed of a motor.
        static const int COMMAND_DELTA = 3;
        static const int MAX_SPEED_BOOST = 5;

        static const int REGULATION_PRECISION = 2;

        static const int MAXSPEED = 50;

        Motor *motor_left, *motor_right;
        int maxspeed;
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
        static const int MAXSPEED = 80;

        float get_lead_error();
        int get_maxspeed();
};

class RotationRegulation : public Regulation {
    public:
        RotationRegulation(Motor *left, Motor *right);

    private:
        float get_rotation_error();
};

#endif
