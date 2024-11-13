import cv2 as cv
from motor import motor, device
import time
import serial
import signal
import sys

# Initialize the device
uca = device("/dev/ttyUSB0")

# Initialize the motor (assuming motor ID is 3, adjust as necessary)
knee_left = motor(3, uca.port(),290)

knee_left.motor_disarm()

while 1:
	knee_left.read_single_loop()
	print(knee_left.curr_deg)
	time.sleep(0.1)