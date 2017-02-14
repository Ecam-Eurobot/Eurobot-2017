from enum import IntEnum
from i2c import I2C


class Command(IntEnum):
    Forward = 1
    Backward = 2
    TurnLeft = 3
    TurnRight = 4
    Stop = 5
    SetSpeed = 6
    DistanceTravelled = 7
    IsDone = 8


class Motors(I2C):
    def __init__(self, address):
        super(Motors, self).__init__(address)

    def forward(self, distance):
        self.send([Command.Forward, distance])

    def backward(self, distance):
        self.send([Command.Backward, distance])

    def turn_left(self, angle):
        self.send([Command.TurnLeft, angle])

    def turn_right(self, angle):
        self.send([Command.TurnRight, angle])

    def stop(self):
        self.send(Command.Stop)

    def set_speed(self, speed):
        self.send([Command.SetSpeed, speed])

    def distance_travelled(self):
        self.send(Command.DistanceTravelled)
        r = self.receive(2)
        return {
            "left": r[0],
            "right": r[1]
        }

    def is_done(self):
        self.send(Command.IsDone)
        return self.receive()
