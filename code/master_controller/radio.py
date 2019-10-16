import serial


class RadioReader(object):
    def __init__(self):
        self.ser = None
        self.channels = {}
        self.timeout = 1

    def start(self):
        self.ser = serial.Serial('/dev/ttyACM0', 19200)
        self.ser.timeout = self.timeout

    def loop(self):
        data = self.ser.readline()

        # Ignore serial lines starting with //
        if len(data) >= 2 \
                and data[0] == 0x2F \
                and data[1] == 0x2F:
            return

        channel = 1
        in_channel = False
        i = 0
        while i < len(data):
            if data[i] == 255:
                # We are done reading this serial. 0xFF is the manual bail code.
                break

            if in_channel:
                # Unpack the value of channel into a number we can use.
                channel_value = data[i]

                # Assign the value of the channel.
                self.channels[channel] = channel_value

                in_channel = False
            else:
                # Set the channel based on the first read of the bit.
                channel = data[i]
                in_channel = True
            i += 1

