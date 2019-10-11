import main as m


def main():
    mc = m.MyClass()

    mc.start()

    while True:
        mc.loop()


if __name__ == "__main__":
    main()
