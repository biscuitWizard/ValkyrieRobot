from enum import Enum


class Channel(Enum):
    CHASSIS_LATERAL = 1
    CHASSIS_YAW = 2
    TURRET_PITCH = 3
    TURRET_YAW = 4
    TURRET_PRIME = 5
    TURRET_FIRE = 6
    THROTTLE_MIX = 7
    ACCESSORY = 8


class Output(Enum):
    DRIVE_LEFT = 1
    DRIVE_RIGHT = 2
    TURRET_PITCH = 3
    TURRET_YAW = 4
    TURRET_PRIME = 5
    TURRET_FIRE = 6
    SWITCH_1 = 7


class OutputType(Enum):
    CONTINUOUS_MOTOR = 1
    SERVO_MOTOR = 2
    SWITCH = 3
