#include <Wire.h>
#include "lidar.h"

const byte SLAVE_ADDRESS = 0x07;

Lidar lidar();

void setup() {
    Serial.begin(9600);

    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receive_i2c_data);
    Wire.onRequest(send_i2c_data);
}

void loop() {
    analogRead(lidar.get_pin());
    lidar.get_distance_cm(measured_value);
    delay(60)
}

void receive_i2c_data(int byteCount) {
}

void send_i2c_data() {
}
