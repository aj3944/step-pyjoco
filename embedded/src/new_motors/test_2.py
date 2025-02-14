from motor2 import device, motor
import serial
import time


import can 

# Initialize the device
# uca = device("/dev/tty.usbserial-130")
uca = device("/dev/ttyUSB0")

test_motor = motor(1, uca.port()) 


test_motor.torque_control_move(120)

time.sleep(1) 

test_motor.motor_stop()
