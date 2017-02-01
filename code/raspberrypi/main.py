from range_sensors import RangeSensor

import time

sensors = RangeSensor(4)
time.sleep(0.1)

while True:
    print("Sensor 1: " + str(sensors.get_range(0)))
    print("Sensor 2: " + str(sensors.get_range(1)))
    time.sleep(1)
