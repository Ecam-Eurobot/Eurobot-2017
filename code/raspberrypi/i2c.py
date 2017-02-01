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
        data = []
        for _ in range(num_bytes):
            data.append(self.bus.read_byte(self.adress))

        return data
