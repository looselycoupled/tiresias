import time
import RPi.GPIO as GPIO
from tiresias.sensors.base import SensorBase

# BOARD NUMBERING (cannot be be used in conjuction with BNO055)
# PIN_TRIGGER = 7
# PIN_ECHO = 11

# BCM NUMBERING
PIN_TRIGGER = 4
PIN_ECHO = 17

class UltrasonicRangingSensor(SensorBase):

    def setup(self):
        """
        Performs one-time hardware setup and configuration nescessary before
        reading data from the sensor.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        self.logger.info("UltrasonicRangingSensor: waiting for sensor to settle")
        time.sleep(2)

        super(UltrasonicRangingSensor, self).setup()


    def _signal(self):
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)

    def read(self, fmt="dict"):
        """
        Returns distance sensor data in a raw tuple or dict format.

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
        try:
            self._signal()

            while GPIO.input(PIN_ECHO)==0:
                pulse_start_time = time.time()

            while GPIO.input(PIN_ECHO)==1:
                pulse_end_time = time.time()

            duration = pulse_end_time - pulse_start_time
            distance = round(duration * 17150, 2)
            distance_inches = round(duration * (13504 / 2), 2)

            if fmt == "raw":
                return distance, distance_inches

            if fmt == "dict":
                return {
                    "distance": {
                        "cm": distance,
                        "inches": distance_inches,
                    }
                }

            raise ValueError("invalid fmt argument ({})".format(fmt))

        except Exception:
            self.shutdown()
            raise


    def shutdown(self):
        """
        Performs hardware shutdown/cleanup operations to ensure tidy/safe
        operation.
        """
        self.logger.info("UltrasonicRangingSensor: cleaning up GPIO")
        GPIO.cleanup()
        super(UltrasonicRangingSensor, self).shutdown()


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
                    self.logger.info("UltrasonicRangingSensor: exiting monitor")
                    break
                data = self.read()
                output.put(data)
        except KeyboardInterrupt:
            pass

        self.shutdown()
