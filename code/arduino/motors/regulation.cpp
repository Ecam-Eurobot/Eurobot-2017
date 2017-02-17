#include "regulation.h"

Regulation::Regulation(Motor *left, Motor *right):
        motor_left(left), motor_right(right) {
    reset_regulation();
}

void Regulation::tune() {
    float lead_error = get_lead_error();
    float rot_error = get_rotation_error();

    update_sum_errors(lead_error, rot_error);

    float lead_regul = get_lead_regulation(lead_error);
    float rot_regul = get_rotation_regulation(rot_error);

    float cmd_left = get_command_motor(motor_left, lead_regul + rot_regul);
    float cmd_right = get_command_motor(motor_right, lead_regul - rot_regul);

    send_command(cmd_left, cmd_right, cmd_left > 0, cmd_right > 0);
}

void Regulation::set_order(int order) {
    reset_regulation();
    finished = false;
    this->order = order;
    tune();
}

void Regulation::set_max_speed(int maxspeed) {
    this->maxspeed = maxspeed;
}

void Regulation::reset_regulation() {
    sum_errors_lead = 0;
    sum_errors_rot = 0;
    order = 0;
    finished = true;

    motor_left->reset_encoder_counter();
    motor_right->reset_encoder_counter();
}

void Regulation::update_sum_errors(float lead, float rot) {
    // TODO: check if we update them everytimes...
    sum_errors_lead += lead;
    sum_errors_rot += rot;
}

float Regulation::get_lead_regulation(float error) {
    float integral = saturate_integral_regulation(sum_errors_lead * KI_LEAD);
    return KP_LEAD * error + integral;
}

float Regulation::get_rotation_regulation(float error) {
    float integral = saturate_integral_regulation(sum_errors_rot * KI_ROT);
    return KP_ROT * error + integral;
}

float Regulation::saturate_integral_regulation(float value) {
    if (abs(value) > INTEGRAL_SATURATION) {
        return (value > 0) ? INTEGRAL_SATURATION : -INTEGRAL_SATURATION;
    }
    return value;
}

float Regulation::get_command_motor(Motor *motor, float command) {
    int prev_cmd = motor->get_speed();

    if (((int) abs(command) - prev_cmd) > PROGRESSIVE_COMMAND) {
        float new_cmd = prev_cmd + PROGRESSIVE_COMMAND;
        return (command > 0) ? new_cmd : -new_cmd;
    }
    return command;
}

void Regulation::send_command(float cmd_left, float cmd_right,
        bool forward_left, bool forward_right) {
    float maxspeed_right = maxspeed, maxspeed_left = maxspeed;

    if (abs(cmd_left - cmd_right) > COMMAND_DELTA) {
        if (cmd_left > cmd_right) {
            maxspeed_left += 20;
        } else {
            maxspeed_right += 20;
        }
    }

    cmd_left = (cmd_left > maxspeed_left) ? maxspeed_left : cmd_left;
    cmd_right = (cmd_right > maxspeed_right) ? maxspeed_right : cmd_right;

    if (forward_left) {
        motor_left->move_forward(cmd_left);
    } else {
        motor_left->move_backward(cmd_left);
    }
    if (forward_right) {
        motor_right->move_forward(cmd_right);
    } else {
        motor_right->move_backward(cmd_right);
    }
}

float Regulation::get_lead_error() {
    return (motor_left->get_encoder_counter() + motor_right->get_encoder_counter()) / 2;
}

float Regulation::get_rotation_error() {
    return (motor_left->get_encoder_counter() - motor_right->get_encoder_counter()) / 2;
}

float LeadRegulation::get_lead_error() {
    return order + Regulation::get_lead_error();
}

float RotationRegulation::get_rotation_error() {
    return order - Regulation::get_rotation_error();
}
