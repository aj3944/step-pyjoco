import cv2 as cv
from motor import motor,device
import time

uca = device("/dev/ttyUSB2")


shin_left = motor(3,uca.port())

shin_left.motor_arm()

# print(shin_left.goal_pos)

shin_left.read_motor_encoder()
shin_left.move_degrees_abs(1000)
shin_left.read_motor_encoder()

time.sleep(1)
shin_left.read_motor_encoder()



mult = 1;
speed = 1000;



def callback(x):
	print("x\t",x)
	# shin_left.goto(int(x*803/mult),speed)
	# shin_left.goto(int(x),speed)
	shin_left.read_state()
	# shin_left.read()

cv.namedWindow('controls')
cv.createTrackbar('R','controls',0,360*mult,callback)

r = cv.getTrackbarPos('R','controls')

k = cv.waitKey(0)

# print(shin_left.goal_pos)