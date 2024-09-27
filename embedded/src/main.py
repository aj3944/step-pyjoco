import time
import random
import serial
from math import sin , pi

from commands import motor_off,motor_on,increment_angle,torque_control,read_pid,read_encoder,clear_motor_state

CANUSB_TTY_BAUD_RATE_DEFAULT = 2000000
uca_serial_device = serial.Serial("/dev/ttyUSB0", baudrate=CANUSB_TTY_BAUD_RATE_DEFAULT, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, timeout=0.000001)


# uca_serial_device.write(motor_on(3))
# uca_serial_device.write(motor_off(3))
# uca_serial_device.write(torque_control(3, 35))
# uca_serial_device.write(torque_control(3, 40))
# uca_serial_device.write(torque_control(3, 40))
# uca_serial_device.write(torque_control(3, 40))

# uca_serial_device.write(increment_angle(3,20000))


for i in range(200):
    x = int(100*sin(i/200*pi))
    uca_serial_device.write(increment_angle(1,x))
    time.sleep(0.001)
# off = motor_off(3)
# on = motor_on(3)

# # uca_serial_device.write(motor_off(3))
# # uca_serial_device.write(clear_motor_state(3))


# # time.sleep(1)

# # pos = 0
# # goal = 0 

# # for i in range(10):
# #     # now = time.time()
# #     # if i % 2 == 0:
#     uca_serial_device.write(torque_control(3, 100))
# #         # uca_serial_device.write(read_pid(3))
#     # uca_serial_device.write(read_encoder(3))
#     # started = True;
#     # for i in range(10): 
#     time.sleep(0.0025)
#     # print()
#     # print(uca_serial_device.out_waiting)
#     byte = uca_serial_device.read(uca_serial_device.in_waiting)
#     print(byte)
#     # print()
#     time.sleep(0.1)

# # while started:
# #     print(byte)
# #     # print(byte.hex() == '55')
# #     # if byte.hex() == '55':
# #     #     started = False
# #     #     print()

# time.sleep(1)

# uca_serial_device.write(motor_off(3))

# while 1:
