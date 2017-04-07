from i2c import I2C
from enum import IntEnum

class Command(IntEnum) :
    MOVE_UP = 1
    MOVE_DOWN = 0

class Adress(IntEnum) :
    SERVO_CLAMP = 0
    SERVO_DYNAMIXEL = 1
    SERVO_PUSH = 2


class Kinematics(I2C) :
    """
    This class is an abstraction around the I2C communication with
    the servo-arduino module.

    Details of the "protocol" used:

    The Raspberry Pi sends a byte to the module containing a command
    and a servo number. Both informations are coded on 4 bits
    totalling 8 bits together. The 4 first bits are for the servo address,
    and the 4 next is used for the action to do with it.

    """

    def __init__(self, address):
        """Constructor takes the adress of the I2C module"""
        super(Kinematics, self).__init__(address)

    def up_clamp(self) :
        cmd = I2C.pack8(Adress.SERVO_DYNAMIXEL, Command.MOVE_UP)
        self.send(cmd)

    def down_clamp(self) :
        cmd = I2C.pack8(Adress.SERVO_DYNAMIXEL, Command.MOVE_DOWN)
        self.send(cmd)

    def close_clamp(self) :
        cmd = I2C.pack8(Adress.SERVO_CLAMP, Command.MOVE_UP)
        self.send(cmd)

    def open_clamp(self) :
        cmd = I2C.pack8(Adress.SERVO_CLAMP, Command.MOVE_DOWN)
        self.send(cmd)

    def push_out(self) :
        cmd = I2C.pack8(Adress.SERVO_PUSH, Command.MOVE_UP)
        self.send(cmd)

    def push_back(self) :
        cmd = I2C.pack8(Adress.SERVO_PUSH, Command.MOVE_DOWN)
        self.send(cmd)
