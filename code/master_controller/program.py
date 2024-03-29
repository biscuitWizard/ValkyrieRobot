import time
from colorama import Fore, Style
import configparser
from radio import RadioReader
from controller import Controller
from mcu import MotorController

from os import system


def main():
    system('clear')

    print("Starting Master Controller...")

    # Boot up first by loading the configuration file.
    print("Loading Configuration...")
    config = configparser.ConfigParser()
    # Read the default file.
    config.read('config.ini')

    # Initialize our modules.
    print("Loading Modules...")
    radio = RadioReader(config["DEFAULT"].get("RadioSubprocessor"))
    mc = MotorController(config)
    controller = Controller(config, radio, mc)

    # Apply configuration to relevant modules.
    framerateMs = (1 / config["DEFAULT"].getint("Framerate", 30)) * 1000
    radioTimeout = config["DEFAULT"].getfloat("RadioChannelTimeout", 1)

    radio.timeout = radioTimeout

    print("Loading a frame every " + str(framerateMs) + "ms.")
    print("Radio Channel Timeout: " + str(radioTimeout) + "ms.")
    # Start the modules.
    radio.start()
    mc.start()
    controller.start()

    last_debug_update = 0

    print("Master Controller successfully started.")
    # Engage the main program loop.
    while True:
        # Log starting time.
        start = time.time()

        # Loop through all modules.
        radio.loop()
        controller.loop()
        mc.loop()

        # Update if necessary.
        if time.time() - last_debug_update > 2:
            system('clear')

            # Write out our channel values.
            print("\r\n[Radio Channel Values]")
            print("\tRAW: " + str(radio.last_input))
            for channel in radio.channels.keys():
                print("\tChannel " + str(channel) + ": " + str(radio.channels[channel]))

            print("\r\n[Motor Outputs]")
            for output in mc.output_mappings.keys():
                mapping = mc.output_mappings[output]
                print("\t" + str(output) + ": " + str(mapping.value))

            print("\r\n[Controller Status]")
            print("\tThrottle Modifier: " + str(controller.throttle_modifier))
            print("\tLateral Throttle: " + str(controller.lateral_throttle))
            print("\tYaw Throttle: " + str(controller.yaw_throttle))

            # Update the time since we've last updated.
            last_debug_update = time.time()

        # Log ending time.
        durationMs = (time.time() - start) * 1000

        # Sleep.
        time.sleep(max(0, (framerateMs - durationMs) / 1000))


if __name__ == "__main__":
    main()
