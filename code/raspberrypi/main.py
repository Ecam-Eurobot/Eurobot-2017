from range_sensors import RangeSensor
from arduino_servo import ArduinoServo
import time

# Testing code to see if it works
sensors = RangeSensor(4)
servo = ArduinoServo(1)
time.sleep(0.1)

while True:
    servo.up_clamp()
    time.sleep(4)
    servo.down_clamp()
    time.sleep(2)
    print("Sensor 1: " + str(sensors.get_range(0)))
    print("Sensor 2: " + str(sensors.get_range(1)))
    time.sleep(1)
