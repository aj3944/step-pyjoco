from motor2 import device, motor
import serial
import time


# import can 

# Initialize the device
uca = device("/dev/tty.usbserial-130")
# uca = device("/dev/ttyUSB0")

test_motor = motor(1, uca.port()) 

# test_motor.incr_position_clc(1000, 18000)
# test_motor.goto_position_control(18000, 0x00, 1000)

test_motor.read_version()

# time.sleep(1) 

test_motor.motor_stop()
