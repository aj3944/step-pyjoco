# import cv2 as cv
from motor import motor, device
from commands import *
import time
import serial
import signal
import sys


# Initialize the device
uca = device("/dev/tty.usbserial-130")

# Initialize the motor (assuming motor ID is 3, adjust as necessary)
# knee_left = motor(3, uca.port(),240)
# knee_left.motor_disarm()
# time.sleep(0.5)
# knee_left.motor_arm()


# thigh_left = motor(13, uca.port(),150, 135, 175)
# hip_left = motor(12, uca.port(), 210 , 180, 240) #180 -> 240, 210 home 
# upper_left = motor(11, uca.port(), 240, 223,255) # home 240, 223->260 
# upper_right = motor(1, uca.port(), 170, 160, 195) #home: 170 min: 160 max: 195 
# thigh_right = motor(2, uca.port(), 0, 0, 0) #home:15 min: max:30 !!!!!!!!!!! FIX THE LOCATION, TRY TO SET HOME AS CLOSE TO 180
shin_right = motor(3, uca.port(), 250,230 ,265) #home; 250 max: 270 min: 230
# hip_left.motor_disarm()
# thigh_left.motor_disarm()
# upper_left.motor_disarm()
# upper_right.motor_disarm()
# thigh_right.motor_disarm()
shin_right.motor_disarm()

time.sleep(0.5)
# thigh_left.motor_arm()
# hip_left.motor_arm()
# upper_left.motor_arm()
# upper_right.motor_arm()
shin_right.motor_arm()

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

 
speed = 1000
location = 0
direction = 0 

# thigh_left.motor_disarm()

time.sleep(1)

# print("current location: ", thigh_left.read_single_loop())
# location = int(input("enter location\n")) 
# if (location < 0 or location > 360):
# 	location = int(input("enter valid location\n"))

# thigh_left.motor_arm()

# targetLocation = location
# delta = int(thigh_left.curr_deg) - location
# location = location * 803

# time.sleep(0.1)

#range for thigh: 130-180

#READ ANGLES
# while 1: 
#     shin_right.read_single_loop()
#     print(shin_right.curr_deg)

# print(delta)
# if delta>0:
#     direction = 1
# else:
#     direction = 0

    
# thigh_left.goto_single_loop_shortest(135,speed)
# time.sleep(1)
# thigh_left.goto_single_loop_shortest(150,speed)
# time.sleep(1)
# thigh_left.goto_single_loop_shortest(135,speed)
# hip_left.goto_single_loop_shortest(210, speed)
# time.sleep(1)
# hip_left.goto_single_loop_shortest(200, speed)
# time.sleep(1)
# hip_left.goto_single_loop_shortest(220, speed)
# time.sleep(1)
# upper_left.goto_single_loop_shortest(240, speed)
# time.sleep(1)
# upper_left.goto_single_loop_shortest(230, speed)
# time.sleep(1)
# upper_left.goto_single_loop_shortest(250, speed)
# time.sleep(1)
# upper_right.goto_single_loop_shortest(170, speed)
# time.sleep(1)
# upper_right.goto_single_loop_shortest(160, speed)
# time.sleep(1)
# upper_right.goto_single_loop_shortest(190, speed) 
# time.sleep(1) 
shin_right.goto_single_loop_shortest(250, speed)
time.sleep(1)
shin_right.goto_single_loop_shortest(235, speed)
time.sleep(1)
shin_right.goto_single_loop_shortest(260, speed)
time.sleep(1)

shin_right.motor_disarm()


# while 1: 
#      thigh_left.read_single_loop() 
#      time.sleep(0.001) 
#      if thigh_left.curr_deg == targetLocation: 
#           break
# thigh_left.motor_disarm()




# knee_left.increment(5,200)
# knee_left.move_degrees_abs(290)
# knee_left.move_to(290,10)