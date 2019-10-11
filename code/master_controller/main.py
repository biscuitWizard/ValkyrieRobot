import serial


class MyClass(object):
    def __init__(self):
        self.ser = None

    def start(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600)

    def loop(self):
        print self.ser.readline()
