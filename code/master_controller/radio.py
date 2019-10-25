import serial


class RadioReader(object):
    def __init__(self, serial_device):
        self.ser = None
        self.channels = {}
        self.timeout = 1
        self.serial_device = serial_device

    def start(self):
        self.ser = serial.Serial(self.serial_device, 19200)
        self.ser.timeout = self.timeout

    def loop(self):
        raw_data = self.ser.readline()

        if len(raw_data) < 4:
            return

        data = raw_data.decode("utf-8")

        raw_channels = data.split('|')
        for raw_channel in raw_channels:
            if len(raw_channel) < 3:
                # Possible for there to be empty channels. Ignore them.
                continue

            tokens = raw_channel.split(':')
            if len(tokens) < 2:
                # There was an error parsing. Skip this channel.
                continue

            channel = tokens[0]
            value = tokens[1]

            self.channels[channel] = value

