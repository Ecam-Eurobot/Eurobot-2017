#include "lidar.h"

Lidar lidar();

void setup() {
    Serial.begin(9600);
}

void loop() {
    analogRead(lidar.get_pin());
    lidar.get_distance_cm(measured_value);
    delay(60)
}
