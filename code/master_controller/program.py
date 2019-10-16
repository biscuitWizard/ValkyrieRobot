import time
import configparser
from radio import RadioReader
from controller import Controller
from mcu import MotorController


def main():
    print("Starting Master Controller...")

    # Boot up first by loading the configuration file.
    print("Loading Configuration...")
    config = configparser.ConfigParser()
    # Read the default file.
    config.read('config.ini')

    # Initialize our modules.
    print("Loading Modules...")
    radio = RadioReader()
    mc = MotorController(config)
    controller = Controller(config["DEFAULT"], radio, mc)

    # Apply configuration to relevant modules.
    framerateMs = (1 / config["DEFAULT"].getint("Framerate", 30)) * 1000
    radioTimeout = config["DEFAULT"].getfloat("RadioChannelTimeout", 1)

    radio.timeout = radioTimeout

    print("Loading a frame every " + str(framerateMs) + "ms.")
    print("Radio Channel Timeout: " + str(radioTimeout) + "ms.")
    # Start the modules.
    radio.start()
    controller.start()

    print("Master Controller successfully started.")
    # Engage the main program loop.
    while True:
        # Log starting time.
        start = time.time()

        # Loop through all modules.
        radio.loop()
        controller.loop()

        # Log ending time.
        durationMs = (time.time() - start) * 1000

        # Sleep.
        if durationMs >= framerateMs:
            print("System running late. Allocated " + str(framerateMs) + "ms, took " + str(durationMs) + "ms.")
        time.sleep(max(0, (framerateMs - durationMs) / 1000))


if __name__ == "__main__":
    main()
