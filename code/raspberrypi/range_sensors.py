from i2c import I2C


class RangeSensor(I2C):
    """Class representing the range sensor module"""

    def __init__(self, adress):
        super(RangeSensor, self).__init__(adress)

    def get_range(self, sensor):
        self.send(sensor)
        r = self.receive()
        return r[0]
