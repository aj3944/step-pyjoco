import cv2 as cv
from motor import motor, device
import time
import serial
import signal
import sys

# Initialize the device
uca = device("/dev/ttyUSB0")

# Initialize the motor (assuming motor ID is 3, adjust as necessary)
# knee_left = motor(3, uca.port(),240)
# knee_left.motor_disarm()
# time.sleep(0.5)
# knee_left.motor_arm()


thigh_left = motor(1, uca.port(),50)
thigh_left.motor_disarm()
time.sleep(0.5)
thigh_left.motor_arm()


while 1:
	# knee_left.read_single_loop()
	thigh_left.read_single_loop()
	# print(knee_left.curr_deg)
	time.sleep(0.01)
	delta = int(thigh_left.HOME - thigh_left.curr_deg);
	print(thigh_left.curr_deg)
	thigh_left.increment(delta*100,200)
	# knee_left.increment(delta*10,200)
	# knee_left.goto_single_loop_shortest(240,10)


# knee_left.increment(5,200)
# knee_left.move_degrees_abs(290)
# knee_left.move_to(290,10)