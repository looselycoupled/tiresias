import time

from Adafruit_BNO055 import BNO055

from tiresias.sensors.base import SensorBase

MAX_STARTUP_ERRORS = 5
SELF_TEST_GOOD = 15
STATUS_GOOD = 5

class IMUSensor(SensorBase):

    def setup(self, serial_port='/dev/serial0', rst=18):
        """
        Performs one-time hardware setup and configuration nescessary before
        reading data from the sensor.
        """
        self.bno = BNO055.BNO055(serial_port=serial_port, rst=rst)

        # allow multiple attempts to establish hardware connection
        error_count = 0
        while True:
            try:
                status = self.bno.begin()
                break
            except RuntimeError as e:
                self.logger.warn("IMUSensor: RuntimeError encountered during setup")
                error_count += 1
                if error_count >= MAX_STARTUP_ERRORS:
                    raise RuntimeError("cannot startup BNO055 sensor")
                time.sleep(2)

        # verify/report system status
        status, self_test, error = self.bno.get_system_status()
        status = "good" if status == STATUS_GOOD else "bad"
        self_test = "good" if self_test == SELF_TEST_GOOD else "bad"
        self.logger.info("IMUSensor: status: {}, self_test: {}, error: {}".format(status, self_test, error))

        if status == "good" and self_test == "good" and error == 0:
            self.logger.info("IMUSensor: ready")
        else:
            raise RuntimeError("IMUSensor: something is wrong")

        super(IMUSensor, self).setup()


    def read(self, fmt="dict"):
        """
        Returns IMU sensor data in a raw tuple or dict format.

        Parameters
        ----------
        fmt: str
            Controls the output format for this method.  Valid values include
            `dict` and `raw`.

        Returns
        -------
        tuple or dict
            A tuple or dictionary containing current sensor values
        """
        heading, roll, pitch = self.bno.read_euler()
        x,y,z = self.bno.read_linear_acceleration()

        if fmt == "raw":
            return heading, roll, pitch, x, y, z

        if fmt == "dict":
            return {
                "euler_angles": {
                    "heading": heading,
                    "roll": roll,
                    "pitch": pitch,
                },
                "linear_acceleration": {
                    "x": x,
                    "y": y,
                    "z": z,
                }
            }

        raise ValueError("invalid fmt argument ({})".format(fmt))


    def status(self):
        """
        Returns a dict containing relevant status information for the actual
        sensor hardware.

        Returns
        ----------
        dict: a dictionary object containing calibration and status information
        """
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


    def monitor(self, command, output):
        """
        A control loop in which this object will await new commands from a
        command queue and then add sensor data to the output queue as
        requested

        Parameters
        ----------
        command: multiprocessing.Queue
            A multiprocessing safe queue object that contains commands to perform

        output: multiprocessing.Queue
            A multiprocessing safe queue object to put data into that is eventually
            consumed by another process thread.
        """

        try:
            while True:
                cmd = command.get()
                if cmd is None:
                    self.logger.info("IMUSensor: exiting monitor")
                    break
                data = self.read()
                output.put(data)
        except KeyboardInterrupt:
            pass

        self.shutdown()