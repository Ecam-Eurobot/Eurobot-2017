// This code is made for an Arduino Mega and test if 
// the wheel encoder are working properly.

// Encoder wheel pins
const int IMP_ENCODER_LEFT_PIN = 2;
const int IMP_ENCODER_RIGHT_PIN = 3;
const int DIRECTION_LEFT_PIN = 4;
const int DIRECTION_RIGHT_PIN = 5;

// TODO: verify this value!
const int WHEEL_RADIUS = 4.02;
const float WHEEL_PERIMETER = WHEEL_RADIUS * 2 * PI;
// The encoder has a 1024 pulses/revolution.
// The DEO nano reduces per 5 the impulsion and we take the pulse
// when high and low.
// The final calculus is 1024*2/5 = 409.6
const float IMP_PER_REVOLUTION = 409.6;
const float IMP_DISTANCE = WHEEL_PERIMETER / IMP_PER_REVOLUTION;

const int PWM_MOTOR_LEFT = 6;
const int PWM_MOTOR_RIGHT = 7;

const int DIR_MOTOR_LEFT = 8;
const int DIR_MOTOR_RIGHT = 9;

long counter_left = 0;
long counter_right = 0;

void setup() {
    Serial.begin(9600);
    
    // Generate interrupt number from pins.
    int int_left = digitalPinToInterrupt(IMP_ENCODER_LEFT_PIN);
    int int_right = digitalPinToInterrupt(IMP_ENCODER_RIGHT_PIN);
    
    attachInterrupt(int_left, encoder_pulse_left, CHANGE);
    attachInterrupt(int_right, encoder_pulse_right, CHANGE);

    pinMode(PWM_MOTOR_LEFT, OUTPUT);
    pinMode(PWM_MOTOR_RIGHT, OUTPUT);

    pinMode(DIR_MOTOR_LEFT, OUTPUT);
    pinMode(DIR_MOTOR_RIGHT, OUTPUT);
}

void loop() {
    digitalWrite(DIR_MOTOR_LEFT, OUTPUT);
    digitalWrite(DIR_MOTOR_RIGHT, OUTPUT);

    analogWrite(PWM_MOTOR_LEFT, 1);
    analogWrite(PWM_MOTOR_RIGHT, 1);

    Serial.print("Left distance: ");
    Serial.println(convert_imp_to_cm(counter_left));
    Serial.print("Right distance: ");
    Serial.println(convert_imp_to_cm(counter_right));

    delay(1000);
}

// Interrupt callbacks

void encoder_pulse_left() {
    //Serial.println("encoder left pulse");
    
    int direction = digitalRead(DIRECTION_LEFT_PIN);
    counter_left += (direction == 1) ? 1 : -1;
}

void encoder_pulse_right() {
    //Serial.println("encoder right pulse");
    
    int direction = digitalRead(DIRECTION_RIGHT_PIN);
    counter_right += (direction == 0) ? 1 : -1;
}

// Helper to convert impulsion to centimèter and vise-versa.

float convert_imp_to_cm(long imp) {
    return imp * IMP_DISTANCE;
}

float convert_cm_to_imp(long cm) {
    return cm / IMP_DISTANCE;
}
