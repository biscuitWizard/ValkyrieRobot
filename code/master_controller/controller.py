from enums import Channel
from enums import Output
import math


class Controller(object):
    def __init__(self, config, radio, mcu):
        self.config = config
        self.radio = radio
        self.mcu = mcu
        self.channel_assignments = {}

    def get_channel_value(self, channel):
        channel_number = self.channel_assignments[channel]
        return self.radio.channels[channel_number]

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
        throttle_modifier = self.get_channel_value(Channel.THROTTLE_MIX) / 100  # 0 - 1 range
        lateral_throttle = self.get_channel_value(Channel.CHASSIS_LATERAL)      # -100 to 100 range
        yaw_throttle = self.get_channel_value(Channel.CHASSIS_YAW)              # -100 to 100 range

        thrust = steering(lateral_throttle, yaw_throttle) * throttle_modifier
        self.mcu.set_motor_value(Output.DRIVE_LEFT, thrust[0])
        self.mcu.set_motor_value(Output.DRIVE_RIGHT, thrust[1])


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

