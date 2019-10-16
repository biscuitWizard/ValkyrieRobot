from enums import Output, OutputType


class MotorMapping:
    def __init__(self, pin, output, output_type):
        self.output = output
        self.output_type = output_type
        self.value = 0
        self.pin = pin

    def set_motor_value(self, value):
        if self.output_type == OutputType.CONTINUOUS_MOTOR:
            return
        elif self.output_type == OutputType.SERVO_MOTOR:
            return
        elif self.output_type == OutputType.SWITCH:
            return
        else:
            print("Incorrect output type selected for motor")


class MotorController(object):
    def __init__(self, config):
        self.output_mappings = {}
        self.config = config

    def start(self):
        for output in [e.value for e in Output]:
            config = self.config[str(output)]
            # Guard statement. Ignore invalid inputs.
            if config is None or config.get('OutputType') is None:
                continue
            mapping = MotorMapping(
                config.getint('Pin'),
                output,
                OutputType[config.get('OutputType')]
            )

            self.output_mappings.append(mapping)
        return

    def loop(self):
        return

    def set_motor_value(self, output, value):
        return

    #  Stops defined output, or if none defined -- all of them
    def stop(self, output):
        return

    def calibrate(self, output):
        return

    def arm(self, output):
        return
