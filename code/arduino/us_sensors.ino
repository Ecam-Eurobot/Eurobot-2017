#include <Wire.h>

const byte SLAVE_ADDRESS = 0x04;
const byte N_SENSORS = 2;
const byte N_MEASURES = 5;

int measures[N_SENSORS][N_MEASURES];
byte measure_index = 0;
unsigned long last_measure = 0;

// I2C variables
byte command = 0;
byte sensor = 0;
bool command_processed = true;


void setup() {
    // I2C
    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    // Setup trig pins
    for(byte i = 2; i < N_SENSORS + 2; i++) {
        pinMode(i, OUTPUT);
        digitalWrite(i, LOW);
    }

    // Setup echo pins
    for(byte i = 8; i < 8+N_SENSORS; i++) {
        pinMode(i, INPUT);
    }
}

void loop() {
    if (millis() - last_measure > 100) {
        for(byte i = 0; i < N_SENSORS; i++) {
            measures[i][measure_index] = measure(i + 2, 8 + i);
        }

        last_measure = millis();

        if (measure_index < N_MEASURES - 1) {
            measure_index++;
        } else {
            measure_index = 0;
        }
    }
}

int measure(byte trig, byte echo) {
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);
    int t = pulseIn(echo, HIGH);

    // Vitesse du son: 343 m/s
    // 343 * 100 / 10^6 [cm/µs] / 2 (aller-retour) = 58.3
    int distance = t / 58.3;
    return distance;
}


// I2C

void receiveData(int byteCount){
    while(Wire.available()){
        // The way I2C works is that we write and read from specific registers
        // but here we interpret the bytes received as a command, when the command
        // has been send the Pi will send a register from which it wants to read
        // but we don't use that register, we send arbitrary data back
        // So once the command has been extracted, the next byte(s) received
        // can be ignored until the response has been send (command has been processed)
        if (command_processed == true) {
            byte dataReceived = Wire.read();

            // Extract the command and the sensor index
            // from the 8 bits received
            command = dataReceived >> 4;
            sensor = dataReceived & 0xF;
            command_processed = false;
        }
        else {
            // Discard the byte we receive, which is supposed to represent the register to read
            Wire.read();
        }

    }
}

void sendData(){
    int avg_value = 0;
    byte avg_split[2];


    switch(command){

        // Return the measurement of one specific sensor
        case 1:
            // Handle if the sensor does not exist
            if (sensor > N_SENSORS - 1) {
                Wire.write(0);
                Wire.write(0);
                return;
            }
            avg_value = avg(measures[sensor]);
            avg_split[0] = avg_value & 0xFF;
            avg_split[1] = avg_value >> 8;
            Wire.write(avg_split, 2);
            break;

        // Return measurements of all sensors
        case 2:
            for(byte i = 0; i < N_SENSORS; i++) {
                avg_value = avg(measures[sensor]);
                avg_split[0] = avg_value & 0xFF;
                avg_split[1] = avg_value >> 8;
                Wire.write(avg_split, 2);
            }
            break;

        // Enumerate all the sensors
        case 3:
            for(byte i = 0; i < N_SENSORS; i++) {
                Wire.write( i );
            }
            break;

        case 4:
            Wire.write( N_SENSORS );
            break;

        default:
            Wire.write(0);
            return;
    }

    command_processed = true;
}

int avg(int values[N_MEASURES]) {
    int sum = 0;
    for (byte i = 0; i < N_MEASURES; i++) {
        sum += values[i];
    }

    return sum / N_MEASURES;
}
