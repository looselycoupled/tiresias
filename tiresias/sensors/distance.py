
from tiresias.sensors.base import SensorBase


class DistanceBase(SensorBase):
    """base class for distance sensors"""
    pass


class UltrasonicRangingSensor(DistanceBase):

    def read(self):
        return 42.0

