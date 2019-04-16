import time
import multiprocessing as mp
import RPi.GPIO as GPIO

from tiresias.sensors.imu import IMUSensor
from tiresias.sensors.distance import UltrasonicRangingSensor


def basic_test():
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


def mp_test():
    imu = IMUSensor()
    imu.setup()
    ranger = UltrasonicRangingSensor()
    ranger.setup()

    command = [mp.Queue(), mp.Queue()]
    output = mp.Queue()

    procs = [
        mp.Process(name="tilt", target=imu.monitor, args=(command[0], output)),
        mp.Process(name="distance", target=ranger.monitor, args=(command[1], output)),

    ]
    [p.start() for p in procs]

    for _ in range(20):
        start = time.time()
        data = {"time": { "start": int(start * 1e6), "scale": "microsecond"}}
        for q in command:
            q.put(True)

        for _ in procs:
            data.update(output.get())

        data["time"].update({"duration": time.time() - start})
        print(data)
        time.sleep(.01)

    for q in command: q.put(None)
    [p.join() for p in procs]
    print("exiting")



if __name__ == "__main__":
    mp_test()