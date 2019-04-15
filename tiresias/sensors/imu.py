import logging
import sys
import time

from Adafruit_BNO055 import BNO055

from tiresias.sensors.base import SensorBase

MAX_STARTUP_ERRORS = 2

class IMUSensor(SensorBase):

    def setup(self):
        self.bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

        error_count = 0
        while True:
            try:
                status = self.bno.begin()
                break
            except RuntimeError as e:
                error_count += 1
                if error_count > MAX_STARTUP_ERRORS:
                    raise RuntimeError("cannot startup BNO055 sensor")
                time.sleep(1)

        status, self_test, error = self.bno.get_system_status()
        self.logger.info("status: {}, self_test: {}, error: {}".format(status, self_test, error))
        super().setup()

    def read(self):
        return 42.0

    def status(self):
        sys, gyro, accel, mag = self.bno.get_calibration_status()
        return {
            "calibration": {
                "system": sys,
                "gyroscope": gyro,
                "acceleromater": accel,
                "magnetometer": mag,
            }
        }
