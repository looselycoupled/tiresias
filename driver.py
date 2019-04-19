import argparse

from tiresias.sensors.imu import IMUSensor
from tiresias.sensors.distance import UltrasonicRangingSensor
from tiresias.manager import Manager
from tiresias.consumers.serializers import JSONConsumer
from tiresias.consumers.web import FlaskConsumer


def main():
    sensors = [IMUSensor(), UltrasonicRangingSensor()]
    consumers = [JSONConsumer(), FlaskConsumer()]
    manager = Manager(sensors, consumers)
    manager.start()

if __name__ == "__main__":
    main()