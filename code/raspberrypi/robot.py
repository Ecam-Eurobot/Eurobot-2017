from arduino_servo import ArduinoServo
from motors import Motors
from i2c import I2C
import time

class Robot():
    i=0
    def __init__(self, arg):
        self._arduinoservo = ArduinoServo(1)
        self._motors = Motors(5)
        self._DELAY_OC_CLAMP = 0.7
        self._DELAY_UD_CLAMP = 2.5
        self._DELAY_SR_BLOCK = 2
        self._DELAY_IO_BLOCK = 3


    def take_modules(self, number=1, distance=0):
        for i in range(number):
            self._arduinoservo.release_block()
            self._arduinoservo.down_clamp()
            time.sleep(DELAY_UD_CLAMP)
            self._motors.forward(distance)
            while not self._motors.is_done():
                time.sleep(0.5)
            self._arduinoservo.close_clamp()
            time.sleep(DELAY_OC_CLAMP)
            self._motors.backward(distance)
            while not self._motors.is_done():
                time.sleep(0.5)
            self._arduinoservo.up_clamp()
            time.sleep(DELAY_UD_CLAMP)
            self._arduinoservo.open_clamp()

    def eject_modules(self, number=1):
        for i in range(number):
            self._arduinoservo.stack_block()
            time.sleep(DELAY_SR_BLOCK)
            self._arduinoservo.push_out()
            time.sleep(DELAY_IO_BLOCK)
            self._arduinoservo.push_back()
            time.sleep(DELAY_IO_BLOCK)
            self._arduinoservo.release_block
            time.sleep(DELAY_SR_BLOCK)
