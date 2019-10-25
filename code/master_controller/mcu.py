from enums import Output, OutputType
from adafruit_servokit import ServoKit
import time


class MotorMapping:
    def __init__(self, pin, output, output_type):
        self.output = output
        self.output_type = output_type
        self.value = 0
        self.pin = pin

    def set_motor_value(self, value):
        if self.output_type == OutputType.CONTINUOUS_MOTOR:
            self.value = value
            self.kit.continuous_servo[self.pin].throttle = min(1.0, max(-1.0, value))
            return
        elif self.output_type == OutputType.SERVO_MOTOR:
            self.value = value
            return
        elif self.output_type == OutputType.SWITCH:
            self.value = value
            return
        else:
            print("Incorrect output type selected for motor")

    def calibrate(self):
        if self.output_type == OutputType.CONTINUOUS_MOTOR:
            self.kit.continuous_servo[self.pin].set_pulse_width_range(700, 2000)
            print("Calibrating ESC for %s..." % self.output)
            self.kit.continuous_servo[self.pin].throttle = 0
            time.sleep(2.5)
            self.kit.continuous_servo[self.pin].throttle = 1
            time.sleep(2.5)
            self.kit.continuous_servo[self.pin].throttle = 0
            time.sleep(2.5)
            print("Calibration for %s complete!" % self.output)

    def arm(self):
        if self.output_type == OutputType.CONTINUOUS_MOTOR:
            print("Arming ESC for %s now..." % self.output)
            self.kit.continuous_servo[self.pin].throttle = 0
            time.sleep(1)
            self.kit.continuous_servo[self.pin].throttle = 1
            time.sleep(1)
            self.kit.continuous_servo[self.pin].throttle = 0
            time.sleep(1)
            print("ESC for %s armed!" % self.output)


class MotorController(object):
    def __init__(self, config):
        self.output_mappings = {}
        self.config = config
        self.kit = ServoKit(channels=16)

    def start(self):
        for output in [e.name for e in Output]:
            print("Setting up " + str(output) + "...");
            config = self.config[str(output)]
            # Guard statement. Ignore invalid inputs.
            if config is None or config.get('OutputType') is None:
                print("Unable to find config or OutputType. Skipping.")
                continue

            mapping = MotorMapping(
                config.getint('Pin'),
                output,
                OutputType[config.get('OutputType')]
            )

            # Assign any extra variables.
            mapping.kit = self.kit

            # Setup the servo.
            mapping.calibrate()
            mapping.arm()

            self.output_mappings[output] = mapping
            print(str(output) + " setup complete!")
        return

    def loop(self):
        return

    def set_motor_value(self, output, value):
        mapping = self.output_mappings[output.name]
        if mapping is None:
            return
        mapping.set_motor_value(value)

    #  Stops defined output, or if none defined -- all of them
    def stop(self, output):
        return
