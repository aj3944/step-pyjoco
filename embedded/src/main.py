import time
import random
import serial
from math import sin , pi
import struct
from commands import motor_off,motor_on,increment_angle,torque_control,read_pid,read_encoder,clear_motor_state,single_loop_angle_control,single_loop_angle_read

CANUSB_TTY_BAUD_RATE_DEFAULT = 2000000
uca_serial_device = serial.Serial("/dev/ttyUSB0", baudrate=CANUSB_TTY_BAUD_RATE_DEFAULT, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, timeout=0.000001)


uca_serial_device.write(motor_on(1))
# uca_serial_device.write(motor_on(2))
uca_serial_device.write(motor_on(3))
# uca_serial_device.write(motor_off(1))
# uca_serial_device.write(motor_off(2))
# uca_serial_device.write(motor_off(3))
# uca_serial_device.write(torque_control(3, 35))
# uca_serial_device.write(torque_control(3, 40))
# uca_serial_device.write(torque_control(3, 40))
# uca_serial_device.write(torque_control(3, 40))

# uca_serial_device.write(increment_angle(3,40000))
def combine_uint8_to_int(byte1, byte2):
    # Combine the two uint8 into a single 16-bit number (little-endian order)
    combined = (byte2 << 8) | byte1
    # Convert to signed 16-bit integer
    if combined >= 0x8000:  # If the highest bit is set, it's a negative number
        combined -= 0x10000
    return combined

def parse_frame(frame):
    if not len(frame) == 13:
        return
    # print([hex(x) for x in frame])
    # count = -1
    # for byte,index in zip(frame,range(len(frame))):
    #     count += 1
    #     if count == 2:
    #         print("ID:", int(byte, 16) - 0x40, end = '\t')
    #     if count == 4:
    #         print("Function:", byte, end = '\t')
    #     if count == 5:
    #         print("Temp:", int(byte, 16), end = '\t\n')
    #     if count == 5:
    #         print("Temp:", int(byte, 16), end = '\t\n')
    # print("ID:", int(frame[2], 16) - 0x40, end = '\t')
    print("ID:", frame[2] - 0x40, end = '\t')
    print("Function:", hex(frame[4]), end = '\t')

    if frame[4] == 0x94: 
        print("Encoder:", int.from_bytes(frame[8:11],byteorder='little', signed=True), end = '\t')
    else:
        print("Temp:", frame[5], end = '\t')
        print("Torque:", int.from_bytes(frame[6:7],byteorder='little', signed=True), end = '\t')
        print("Speed:", combine_uint8_to_int(frame[8],frame[9]), end = '\t')
        print("Position:", combine_uint8_to_int(frame[10],frame[11]), end = '\t')
    # print(int.from_bytes(frame[7], "little"))
    # print("Torque:", struct.unpack("<h",frame[6] + frame[7]), end = '\t')

    # print("Speed:", frame[4], end = '\t')
    # print("Position:", frame[4], end = '\t')
    print()

curr_frame = 0
response_frames = []
frame = [] 
for i in range(10):
    # x = int(-100*sin(i/200*pi))
    # x = 36000
    x = int(36000*sin(0.5*pi*i/10))
    # print(x)
    # single_loop_angle_read
    uca_serial_device.write(single_loop_angle_read(3))
    time.sleep(0.001)
    uca_serial_device.write(single_loop_angle_control(3,x))
    # uca_serial_device.write(increment_angle(2,x))
    # uca_serial_device.write(increment_angle(3,x))
    byte_list = uca_serial_device.read(uca_serial_device.in_waiting)
    # print(byte_list)
    # print(len(byte_list))
    for byte in byte_list:
        # print(byte == 0xaa)
        if byte == 0xaa:
            response_frames.append(frame)
            parse_frame(frame)
            frame = []
            frame.append(byte)
        else:
            frame.append(byte)
        # print()
    time.sleep(1)

# for f in response_frames:
#     parse_frame(f)
# print(response_frames)
# # off = motor_off(3)
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
