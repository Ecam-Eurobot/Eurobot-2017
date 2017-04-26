#include "lidar.h"

Lidar::Lidar(): { }

Lidar::get_distance_cm(float volts) {
    measured_value = (0,008271 + 939,6*volts)/(1 - 3,398*volts + 17,339*volts^2);
    return measured_value;
}

Lidar::get_pin() {
    return analog_pin;
}
