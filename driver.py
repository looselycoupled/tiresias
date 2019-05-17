
# imports
import argparse
from tiresias.sensors.imu import IMUSensor
from tiresias.sensors.distance import UltrasonicRangingSensor
from tiresias.managers import Manager, FlaskManager
from tiresias.consumers.serializers import JSONConsumer
from tiresias.consumers.web import FlaskConsumer

# legacy function for our multiprocessing version of the codebase.
def main():
    sensors = [IMUSensor(), UltrasonicRangingSensor()]
    consumers = [JSONConsumer(), FlaskConsumer()]
    manager = Manager(sensors, consumers)
    manager.start()

# single process, multi-threaded codebase for data collection and visualization
# through a Flask based website.
def single_process_main():
    sensors = [IMUSensor(), UltrasonicRangingSensor()]
    consumers = [JSONConsumer()]
    manager = FlaskManager(sensors, consumers)
    manager.start()


if __name__ == "__main__":
    single_process_main()
