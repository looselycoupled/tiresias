from tiresias.sensors.imu import IMUSensor



ss = IMUSensor()
ss.setup()
print(ss.status())

