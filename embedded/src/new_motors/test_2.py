from motor2 import device, motor
import serial
import time


import can 

# Initialize the device
# uca = device("/dev/tty.usbserial-130")
uca = device("/dev/ttyUSB0")

test_motor = motor(1, uca.port()) 

# bus = can.interface.Bus(interface='serial', channel='/dev/ttyUSB0', bitrate=2000000) #Replace '/dev/ttyUSB0' with the actual serial port


# msg = can.Message(
#     arbitration_id=0x0141, data=[0xa1, 0, 0, 0, 0, 1, 0, 0], is_extended_id=False
# )

# # print(msg)
# # print(dir(msg))


# try:
#     bus.send(msg)
#     print(f"Message sent: {msg}")
# except can.CanError as e:
#      print(f"Error sending message: {e}")


# bus.shutdown()
# # for i in range(10):
# # 	test_motor.single_turn_position_control()
# for i in range(10):
test_motor.torque_control_move(120)

time.sleep(1) 

test_motor.motor_stop()

# test_motor.stop_motor() 