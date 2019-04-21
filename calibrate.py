# calibrate
# Calibration testing for IMU data
#
# This file is provided as a means to save and load calibration data for
# the BNO055 IMU.  HOWEVER, due to localized electromagnetic interference
# the magnetometer calibration should not be trusted and a calibration
# should be performed upon every use.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Sun Apr 21 13:17:41 2019 -0400
#
# Copyright (C) 2019 Allen Leis
# For license information, see LICENSE
#
# ID: calibrate.py [] allen.leis@gmail.com $

"""
Calibration testing for IMU data
"""

##########################################################################
# Imports
##########################################################################

import argparse
import time
import pickle

from tiresias.sensors.imu import IMUSensor

FILENAME = "imu.calibration"

##########################################################################
# Helpers
##########################################################################

def take_readings(imu, num=20, status=False):
    print("\ntaking {} readings:".format(num))
    for _ in range(num):
        print(imu.read())

        if status:
            print(imu.status())

        time.sleep(1)


def save_calibration(imu):
    data = imu.bno.get_calibration()
    with open(FILENAME, "wb") as f:
        pickle.dump(data, f)
    print("calibration data saved to `{}`".format(FILENAME))


##########################################################################
# Primary Functions
##########################################################################

def calibrate(options):
    imu = IMUSensor()
    imu.setup()
    while True:
        readings = imu.read()
        status = imu.status()
        print(readings)
        print(status)
        cal = status['imu_calibration']
        if cal['system'] == 3 and cal['magnetometer'] == 3 and cal['accelerometer'] == 3:
            print("System calibration reached")
            save_calibration(imu)
            break
        time.sleep(1)


def load(pre_test=True, post_test=True):
    imu = IMUSensor()
    imu.setup()
    print(imu.status())

    if pre_test:
        take_readings(imu)

    with open(FILENAME, "rb") as f:
        data = pickle.load(f)

    print("setting calibration data")
    imu.bno.set_calibration(data)
    time.sleep(1)
    print(imu.status())

    if post_test:
        take_readings(imu, 50, True)


def test():
    imu = IMUSensor()
    imu.setup()

    try:
        while True:
            print(imu.status())
            print(imu.read())
            print("")
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    imu.shutdown()


##########################################################################
# Execution
##########################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Short sample app')
    parser.add_argument('--load','-l', action="store_true", default=False, help="load saved calibration data to IMU")
    parser.add_argument('--save','-s', action="store_true", default=False, help="calibrate data IMU and save to disk")
    parser.add_argument('--test','-t', action="store_true", default=False, help="test IMU by continiously taking readings")
    options = parser.parse_args()
    print(options)

    if options.save:
        calibrate(options)

    if options.load:
        load()

    if options.test:
        test()