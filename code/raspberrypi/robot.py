from arduino_servo import ArduinoServo
from motors import Motors
from i2c import I2C
import time

class Robot():
    def __init__(self, arg):
        self._kinematic = ArduinoServo(1)
        self._motors = Motors(5)
        self._DELAY_OPEN_ClOSE_CLAMP = 0.7
        self._DELAY_UP_DOWN_CLAMP = 2.5
        self._DELAY_IN_OUT_BLOCK = 3


    def take_modules(self, number=1, distance=0):
        for i in range(number):
            self._kinematic.release_block()
            self._kinematic.down_clamp()
            time.sleep(self._DELAY_UP_DOWN_CLAMP)
            self._motors.forward(distance)
            while not self._motors.is_done():
                time.sleep(0.5)
            self._kinematic.close_clamp()
            time.sleep(self._DELAY_OPEN_CLOSE_CLAMP)
            self._motors.backward(distance)
            while not self._motors.is_done():
                time.sleep(0.5)
            self._kinematic.up_clamp()
            time.sleep(self._DELAY_UP_DOWN_CLAMP)
            self._kinematic.open_clamp()

    def eject_modules(self, number=1):
        for i in range(number):
            self._kinematic.push_out()
            time.sleep(self._DELAY_IN_OUT_BLOCK)
            self._kinematic.push_back()
            time.sleep(DELAY_IN_OUT_BLOCK)
