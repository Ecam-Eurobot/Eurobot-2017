from i2c import I2C


class RangeSensor(I2C):
    """
    This class is an abstraction around the I2C communication with
    the range-sensor module.

    Details of the "protocol" used:

    The Raspberry Pi sends a byte to the module containing a command
    and eventually a sensor number. Both informations are coded on 4 bits
    totalling 8 bits together. The null byte, 0x00, is used to indicate errors.
    This means that we have 15 possible commands and 15 possible sensors.

    We only use 3 different commands:

    1. MeasureOne (get_range): 0001 xxxx
       This command requests the last measure of the sensor number xxxx
       Sensor indices begin at 1. If the sensor does not exists, the module
       will return a null byte. If the sensor does exists, two bytes will be
       returned making up the 16 bits value together.

    2. MeasureAll (get_ranges): 0010 0000
       This command requests the last measures of all the available sensors.
       The response to this request is a sequence of 2*n bytes where n is the
       number of available sensors.

    3. Count (get_number_of_sensors): 0011 0000
       This command requests the number of available sensors.
       The response is only one byte as there are only 15 possible sensors.

    """

    class Command(Enum):
        MeasureOne = 1,
        MeasureAll = 2,
        Count = 3,

    def __init__(self, address):
        """Constructor takes the adress of the I2C module"""
        super(RangeSensor, self).__init__(address)
        self.n = self.get_number_of_sensors()

    def get_range(self, sensor):
        """Requests the last measurement of a specific sensor"""
        cmd = I2C.pack8(Command.MeasureOne, sensor)
        self.send(cmd)
        r = self.receive(2)
        return I2C.pack16(r[1], r[0])

    def get_ranges(self):
        """Requests the last measurements of all sensors"""
        cmd = I2C.pack8(Command.MeasureAll, 0)
        self.send(cmd)
        return self.receive(2 * self.n)

    def get_number_of_sensors(self):
        """Requests the number of available sensors"""
        cmd = I2C.pack8(Command.Count, 0)
        self.send(cmd)
        return self.receive()
