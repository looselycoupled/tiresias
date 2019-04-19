import argparse

from tiresias.sensors.imu import IMUSensor
from tiresias.sensors.distance import UltrasonicRangingSensor
from tiresias.manager import Manager
from tiresias.consumers.serializers import JSONConsumer

def main():
    sensors = [IMUSensor(), UltrasonicRangingSensor()]
    consumers = [JSONConsumer()]
    manager = Manager(sensors, consumers)
    manager.start()

if __name__ == "__main__":
    main()