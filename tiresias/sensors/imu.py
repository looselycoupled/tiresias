import time

from Adafruit_BNO055 import BNO055

from tiresias.sensors.base import SensorBase

MAX_STARTUP_ERRORS = 2
SELF_TEST_GOOD = 15
STATUS_GOOD = 5

class IMUSensor(SensorBase):

    def setup(self):
        self.bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

        error_count = 0
        while True:
            try:
                status = self.bno.begin()
                break
            except RuntimeError as e:
                self.logger.warn("IMUSensor: RuntimeError encountered during setup")
                error_count += 1
                if error_count > MAX_STARTUP_ERRORS:
                    raise RuntimeError("cannot startup BNO055 sensor")
                time.sleep(1)

        status, self_test, error = self.bno.get_system_status()
        status = "good" if status == STATUS_GOOD else "bad"
        self_test = "good" if self_test == SELF_TEST_GOOD else "bad"
        self.logger.info("IMUSensor: status: {}, self_test: {}, error: {}".format(status, self_test, error))

        super(IMUSensor, self).setup()

    def read(self, fmt="raw"):
        heading, roll, pitch = self.bno.read_euler()
        if fmt == "raw":
            return heading, roll, pitch

        if fmt == "dict":
            return {
                "heading": heading,
                "roll": roll,
                "pitch": pitch,
            }

        raise ValueError("invalid fmt argument ({})".format(fmt))


    def status(self):
        sys, gyro, accel, mag = self.bno.get_calibration_status()
        self.logger.info("IMUSensor: calibration: sys: {}, gyro: {}, accel: {}, mag: {}".format(sys, gyro, accel, mag))
        return {
            "calibration": {
                "system": sys,
                "gyroscope": gyro,
                "acceleromater": accel,
                "magnetometer": mag,
            }
        }
