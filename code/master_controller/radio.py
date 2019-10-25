import serial


class RadioReader(object):
    def __init__(self, serial_device):
        self.ser = None
        self.channels = {}
        self.timeout = 1
        self.serial_device = serial_device
        self.last_input = None

    def start(self):
        self.ser = serial.Serial(self.serial_device, 115200)
        self.ser.timeout = self.timeout

    def loop(self):
        # We don't need stale data.
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.ser.readline(); # Clear out the last line, as it was probably wiped mid-line.

        # Get fresh data.
        raw_data = self.ser.readline()

        if len(raw_data) < 4:
            return

        try:
            data = raw_data.decode("ascii")

            self.last_input = data

            raw_channels = data.split('|')
            for raw_channel in raw_channels:
                if len(raw_channel) < 3:
                    # Possible for there to be empty channels. Ignore them.
                    continue

                tokens = raw_channel.split(':')
                if len(tokens) < 2:
                    # There was an error parsing. Skip this channel.
                    continue

                try:
                    channel = int(tokens[0])
                    value = int(tokens[1])

                    self.channels[channel] = value
                except:
                    continue
        except UnicodeDecodeError as err:
            return
