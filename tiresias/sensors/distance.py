import time
import RPi.GPIO as GPIO
from tiresias.sensors.base import SensorBase

# BOARD NUMBERING
# PIN_TRIGGER = 7
# PIN_ECHO = 11

# BCM NUMBERING
PIN_TRIGGER = 4
PIN_ECHO = 17

class UltrasonicRangingSensor(SensorBase):

    def setup(self):
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

    def read(self, fmt="raw"):
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
                    "cm": distance,
                    "inches": distance_inches,
                }

            raise ValueError("invalid fmt argument ({})".format(fmt))

        except Exception:
            self.shutdown()
            raise

    def shutdown(self):
        self.logger.info("UltrasonicRangingSensor: cleaning up GPIO")
        GPIO.cleanup()