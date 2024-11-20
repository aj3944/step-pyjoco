import cv2 as cv
from motor import motor, device
from commands import *
import time
import serial
import signal
import sys


# Initialize the device
uca = device("/dev/tty.usbserial-14120")

# Initialize the motor (assuming motor ID is 3, adjust as necessary)
# knee_left = motor(3, uca.port(),240)
# knee_left.motor_disarm()
# time.sleep(0.5)
# knee_left.motor_arm()


thigh_left = motor(13, uca.port(),50)
thigh_left.motor_disarm()
time.sleep(0.5)
thigh_left.motor_arm()
target_angle = 180
# thigh_left.move_to(target_angle, max_torque=10, tolerance=1)



# while 1:
	# thigh_left.increment(100)
	# # knee_left.read_single_loop()
	# thigh_left.read_single_loop()
	
	# delta_1 = target_angle - thigh_left.curr_deg
	# # print(knee_left.curr_deg)
	# time.sleep(0.01)
	# if abs(delta_1)<=1:
	# 	#torque_control_move(0)
	# 	break
		
	# #delta = int(thigh_left.HOME - thigh_left.curr_deg);
	# # print(thigh_left.curr_deg)
	# print(delta_1)
	# #thigh_left.increment(delta*100,200)
	# # knee_left.increment(delta*10,200)
	# # knee_left.goto_single_loop_shortest(240,10)

 
speed = 500
location = 0
direction = 0 

thigh_left.motor_disarm()

time.sleep(1)

print("current location: ", thigh_left.read_single_loop())
location = int(input("enter location\n")) 
if (location < 0 or location > 360):
	location = int(input("enter valid location\n"))

thigh_left.motor_arm()

delta = int(thigh_left.curr_deg) - location
location = location * 803

time.sleep(0.1)

# while 1: 
#     thigh_left.read_single_loop()
#     print(thigh_left.curr_deg)

print(delta)
if delta>0:
    direction = 1
else:
    direction = 0
    
thigh_left.goto_single_loop(location,direction,speed)
time.sleep(5)
thigh_left.motor_disarm()




# knee_left.increment(5,200)
# knee_left.move_degrees_abs(290)
# knee_left.move_to(290,10)