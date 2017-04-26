#ifndef LIDAR_H
#define LIDAR_H

#include <Arduino.h>

class Lidar {
    public:
        Lidar();
        static float get_distance_cm(float volts);

    private:
        static const int analog_pin = 0;
};

#endif
