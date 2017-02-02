from i2c import I2C


class RangeSensor(I2C):
    """Class representing the range sensor module"""

    def __init__(self, adress):
        super(RangeSensor, self).__init__(adress)
        self.n = self.get_number_of_sensors()

    def get_range(self, sensor):
        cmd = I2C.pack8(1, sensor)
        self.send(cmd)
        r1 = self.receive()
        r2 = self.receive()
        return I2C.pack16(r1, r2)

    def get_ranges(self):
        cmd = I2C.pack8(2, 0)
        self.send(cmd)
        return self.receive(2 * self.n)

    def enumerate_sensors(self):
        cmd = I2C.pack8(3, 0)
        self.send(cmd)
        return self.receive(self.n)

    def get_number_of_sensors(self):
        cmd = I2C.pack8(4, 0)
        self.send(cmd)
        return self.receive()
