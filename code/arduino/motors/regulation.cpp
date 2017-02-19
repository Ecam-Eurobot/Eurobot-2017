#include "regulation.h"

Regulation::Regulation(Motor *left, Motor *right):
        motor_left(left), motor_right(right) {
    reset();
}

// Add a new setpoint that will be executed by the regulation process.
// The setpoint is in impulsion. We can have 2 differents kind of setpoints
// defined by which child class is used:
//      - A lead
//      - A rotation
void Regulation::set_setpoint(int setpoint) {
    reset();
    finished = false;
    stopped = false;
    this->setpoint = setpoint;

    // Begin the regulation.
    tune();
}

// Tune the regulation according to the wheel encoder value.
void Regulation::tune() {
    if (stopped) return;

    // Calculate the error coming from the wheel encoder.
    float lead_error = get_lead_error();
    float rot_error = get_rotation_error();

    if (is_finished(lead_error, rot_error)) return;

    // Update the sums of errors used for the integral of the PID.
    update_sum_errors(lead_error, rot_error);

    // Calculate the output of the PID.
    float lead_regul = get_lead_regulation(lead_error);
    float rot_regul = get_rotation_regulation(rot_error);

    // Restrict the speed compared to the last speed to avoid big jumps
    // of speed.
    float cmd_left = set_command_limit(motor_left, lead_regul + rot_regul);
    float cmd_right = set_command_limit(motor_right, lead_regul - rot_regul);

    // Actually send command to the motors (with speed limiting).
    send_command(cmd_left, cmd_right);
}

void Regulation::set_max_speed(int maxspeed) {
    this->maxspeed = maxspeed;
}

void Regulation::resume() {
    stopped = false;
}

void Regulation::stop() {
    motor_left->stop();
    motor_right->stop();

    stopped = true;
}

bool Regulation::is_stopped() const {
    return stopped;
}

bool Regulation::is_finished() const {
    return finished;
}

// Reset all the parameters needed for a regulation and stop the motors.
void Regulation::reset() {
    stop();

    sum_errors_lead = 0;
    sum_errors_rot = 0;
    setpoint = 0;
    finished = true;

    motor_left->reset_encoder_counter();
    motor_right->reset_encoder_counter();
}

bool Regulation::is_finished(float lead_err, float rot_err) {
    if (finished) return true;

    if (abs(lead_err) <= REGULATION_PRECISION &&
            abs(rot_err) <= REGULATION_PRECISION) {
        finished = true;
        stop();
    }
    return finished;
}

// Increase the sum of errors with the current error.
// The sum of errors will be used for the integral of the PID.
// We don't modify the sum of errors if the error is small
// because it means we are nearly to the setpoint.
// Because the integral parts of PID can give a big overshoot,
// we limit the overshoot when we are near the setpoint.
void Regulation::update_sum_errors(float lead, float rot) {
    if (lead < SUM_ERRORS_LIMIT) {
        sum_errors_lead += lead;
    }
    if (rot < SUM_ERRORS_LIMIT) {
        sum_errors_rot += rot;
    }
}

// Calculate the lead and the rotation of PID output with the specifics Kp and Ki.

float Regulation::get_lead_regulation(float error) {
    float integral = saturate_integral_regulation(sum_errors_lead * KI_LEAD);
    return KP_LEAD * error + integral;
}

float Regulation::get_rotation_regulation(float error) {
    float integral = saturate_integral_regulation(sum_errors_rot * KI_ROT);
    return KP_ROT * error + integral;
}

// Saturate the integral gain to avoid having a too big overshoot (i.e. exceed
// the setpoint).
float Regulation::saturate_integral_regulation(float value) {
    if (abs(value) > INTEGRAL_SATURATION) {
        return (value > 0) ? INTEGRAL_SATURATION : -INTEGRAL_SATURATION;
    }
    return value;
}

// Limit the command to avoid demanding too much power to the motors and
// soften the startup of the robot.
float Regulation::set_command_limit(Motor *motor, float command) {
    int prev_cmd = motor->get_speed();

    if (((int) abs(command) - prev_cmd) > PROGRESSIVE_COMMAND) {
        float new_cmd = prev_cmd + PROGRESSIVE_COMMAND;
        return (command > 0) ? new_cmd : -new_cmd;
    }
    return command;
}

// Send the speed control to the motors.
void Regulation::send_command(float cmd_left, float cmd_right) {
    float maxspeed_right = maxspeed, maxspeed_left = maxspeed;

    bool forward_left = cmd_left > 0;
    bool forward_right = cmd_right > 0;
    cmd_left = abs(cmd_left);
    cmd_right = abs(cmd_right);

    // If a motor is too behind, we can increase the max speed to
    // reach the stability faster.
    if (abs(cmd_left - cmd_right) > COMMAND_DELTA) {
        if (cmd_left > cmd_right) {
            maxspeed_left += MAX_SPEED_BOOST;
        } else {
            maxspeed_right += MAX_SPEED_BOOST;
        }
    }

    // Limit the speed to the maximum speed defined.
    cmd_left = (cmd_left > maxspeed_left) ? maxspeed_left : cmd_left;
    cmd_right = (cmd_right > maxspeed_right) ? maxspeed_right : cmd_right;

    // Send the command to the motors.
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

// Calculate the error in rotation and lead. This is the only thing changing from LeadRegulation and
// RotationRegulation because the setpoint is used in differents places.

float Regulation::get_lead_error() {
    return (motor_left->get_encoder_counter() + motor_right->get_encoder_counter()) / 2;
}

float Regulation::get_rotation_error() {
    return (motor_left->get_encoder_counter() - motor_right->get_encoder_counter()) / 2;
}

LeadRegulation::LeadRegulation(Motor *left, Motor *right): Regulation(left, right) { }

float LeadRegulation::get_lead_error() {
    return setpoint + Regulation::get_lead_error();
}

RotationRegulation::RotationRegulation(Motor *left, Motor *right): Regulation(left, right) { }

float RotationRegulation::get_rotation_error() {
    return setpoint - Regulation::get_rotation_error();
}
