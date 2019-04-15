import time
import RPi.GPIO as GPIO

from tiresias.sensors.imu import IMUSensor
from tiresias.sensors.distance import UltrasonicRangingSensor



imu = IMUSensor()
imu.setup()
print(imu.status())

print("\nIMU DATA:")
for ii in range(20):
    print(imu.read())
    time.sleep(.1)



ranger = UltrasonicRangingSensor()
ranger.setup()

print("\nRANGING DATA:")
for ii in range(20):
    print(ranger.read())
    time.sleep(.1)

ranger.shutdown()