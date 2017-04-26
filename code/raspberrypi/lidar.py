from i2c import I2C
from enum import IntEnum

class Command(IntEnum):
    Measure = 1
    Start = 2
    Stop = 3

class Lidar(I2C):
    def __init__(self, address):
        super(Lidar, self).__init__(address)

    def measure(self):
        self.send(Command.Measure)
        return self.receive()

    def start(self):
        self.send(Command.Start)

    def stop(self):
        self.send(Command.Stop)
