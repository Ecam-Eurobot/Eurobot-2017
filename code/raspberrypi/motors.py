import time

from enum import IntEnum
from i2c import I2C


class Command(IntEnum):
    Forward = 1
    Backward = 2
    TurnLeft = 3
    TurnRight = 4
    SetSpeed = 5
    Stop = 6
    GetDistanceDone = 7
    IsDone = 8
    IsStopped = 9
    Restart = 10


class Motors(I2C):
    ANGLE_CORRECTION = 107.5 / 360

    def __init__(self, address):
        super(Motors, self).__init__(address)

    def move_with_instructions(self, path, move_callback, done_callback):
        for action in path:
            val = action['value']
            if action['action'] == 'move':
                if val > 0:
                    self.forward(val)
                else:
                    self.backward(val)
            elif action['action'] == 'turn':
                if val > 0:
                    self.turn_right(val)
                else:
                    self.turn_left(val)

            # Wait before action is done.
            while not self.is_done(done_callback):
                if move_callback() == 'obstacle':
                    done_callback(self.get_distance_travelled(), 'obstacle')
                    return
                time.sleep(0.1)

        done_callback(self.get_distance_travelled())

    def forward(self, distance):
        self.send([Command.Forward, distance])

    def backward(self, distance):
        self.send([Command.Backward, distance])

    def turn_left(self, angle):
        self.send([Command.TurnLeft, angle])

    def turn_right(self, angle):
        self.send([Command.TurnRight, angle])

    def set_speed(self, speed):
        self.send([Command.SetSpeed, speed])

    def stop(self):
        self.send(Command.Stop)

    def get_distance_travelled(self):
        self.send(Command.DistanceTravelled)
        r = self.receive(2)
        return {
            "left": r[0],
            "right": r[1]
        }

    def is_done(self, callback=None):
        self.send(Command.IsDone)
        is_done = self.receive()
        if is_done and callback is not None:
            callback(self.get_distance_travelled())
        return is_done

    def is_stopped(self):
        self.send(Command.IsStopped)
        return self.receive()

    def restart(self):
        self.send(Command.Restart)
