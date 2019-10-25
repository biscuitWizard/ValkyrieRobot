from enums import Channel
from enums import Output
import math


class Controller(object):
    def __init__(self, config, radio, mcu):
        self.config = config
        self.radio = radio
        self.mcu = mcu
        self.channel_assignments = {}

        self.throttle_modifier = 0
        self.lateral_throttle = 0;
        self.yaw_throttle = 0;

    def get_channel_value(self, channel):
        channel_number = self.channel_assignments[channel]
        if channel_number in self.radio.channels.keys():
            return self.radio.channels[channel_number]
        return 0

    def start(self):
        # Parse all the channel assignments in config to assign numbers to channels
        # to give the radio context.
        i = 1
        while i <= 8:
            channel_value = self.config["CHANNELS"].get("CHANNEL_" + str(i))
            self.channel_assignments[Channel[channel_value]] = i
            i += 1

    def loop(self):
        # Calculate what duty load to give the chassis ESCs.
        self.throttle_modifier = self.get_channel_value(Channel.THROTTLE_MIX) / 100  # 0 - 1 range
        self.lateral_throttle = self.get_channel_value(Channel.CHASSIS_LATERAL)      # -100 to 100 range
        self.yaw_throttle = self.get_channel_value(Channel.CHASSIS_YAW)              # -100 to 100 range

        thrust = steering(self.lateral_throttle, self.yaw_throttle)
        self.mcu.set_motor_value(Output.DRIVE_LEFT, thrust[0] * self.throttle_modifier)
        self.mcu.set_motor_value(Output.DRIVE_RIGHT, thrust[1] * self.throttle_modifier)


def steering(x, y):
    # convert to polar
    r = math.hypot(x, y)
    t = math.atan2(y, x)

    # rotate by 45 degrees
    t += math.pi / 4

    # back to cartesian
    left = r * math.cos(t)
    right = r * math.sin(t)

    # rescale the new coords
    left = left * math.sqrt(2)
    right = right * math.sqrt(2)

    # clamp to -1/+1
    left = max(-1, min(left, 1))
    right = max(-1, min(right, 1))

    return [left, right]

