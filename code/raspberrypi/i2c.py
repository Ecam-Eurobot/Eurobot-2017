import unittest
import smbus


class I2C:

    def __init__(self, adress):
        self.bus = smbus.SMBus(1)
        self.adress = adress

    def send(self, data):
        if isinstance(data, list):
            for byte in data:
                self.bus.write_byte(self.adress, byte)
        elif isinstance(data, int):
            self.bus.write_byte(self.adress, data)

    def receive(self, num_bytes=1):
        if num_bytes == 1:
            return self.bus.read_byte(self.adress)
        else:
            return self.bus.read_i2c_block_data(self.adress, 0x00, num_bytes)

    def pack8(x, y):
        # Use  bitwise AND to retain only the first 4 bits
        # of x and y, shift the four bits from x to the left
        # and do a bitwise OR with the four bits of y
        # to get a 8 bit value of the form: xxxx yyyy
        return (x & 0b1111) << 4 | (y & 0b1111)

    def pack16(x, y):
        # Use  bitwise AND to retain only the first 8 bits
        # of x and y, shift the 8 bits from x to the left
        # and do a bitwise OR with the 8 bits of y
        # to get a 16 bit value of the form: xxxx xxxx yyyy yyyy
        return (x & 0xFF) << 8 | (y & 0xFF)


class TestPack(unittest.TestCase):

    def test_pack8(self):
        self.assertEqual(I2C.pack8(0b0011, 0b0010), 0b00110010)
        self.assertEqual(I2C.pack8(0b11000011, 0b0010), 0b00110010)
        self.assertEqual(I2C.pack8(0b1111, 0b0000), 0b11110000)

    def test_pack16(self):
        self.assertEqual(I2C.pack16(0xF3, 0xAB), 0xF3AB)
        self.assertEqual(I2C.pack16(0x2, 0xFF), 0x02FF)


if __name__ == '__main__':
    unittest.main()
