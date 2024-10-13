import cv2 as cv
from motor import motor,device
import time

uca = device("/dev/ttyUSB1")


shin_left = motor(3,uca.port())

shin_left.motor_disarm()

# print(shin_left.goal_pos)

# shin_left.read_motor_encoder()
# shin_left.move_degrees_abs(1000)
# shin_left.read_motor_encoder()

time.sleep(1)
# shin_left.read_motor_encoder()
shin_left.motor_arm()



mult = 1;
speed = 500000;


target = 0

def callback(x):
	global target
	print("x\t",x)
	# shin_left.goto(int(x*803/mult),speed)
	# shin_left.goto(int(x),speed)
	# shin_left.read_state()
	# shin_left.move_to(x,20,1)
	# deg = x*800;


	# direction = deg - target + 0.0000001

	# target = deg
	# d = -abs(direction)/direction
	# if d < 0:
	# 	d = 0
	# else:
	# 	d = 1
	# print(deg)
	# shin_left.goto_single_loop(deg,d,10000)
	# shin_left.read_single_loop()
	# shin_left.move_to(x,20);
	for i in range(100):
		shin_left.read_single_loop()
		print(shin_left.curr_deg)
	# shin_left.goto_single_loop(deg,d,10000)

	tolerance = 10;
	E_this, E_prev = 100,100
	E_acc = 0
	while abs(E_this) < tolerance:
		E_this = shin_left.curr_deg - x
		print(E_this)
		E_acc += E_this
		E_diff = E_this - E_prev
		P = 15
		I = 1
		D = 1
		ctrl = P*E_this + I*E_acc + D*E_diff
		shin_left.torque_control_move(int(ctrl))
		E_prev = E_this
		shin_left.read_single_loop()
		time.sleep(0.1)
	shin_left.torque_control_move(0)


cv.namedWindow('controls')
cv.createTrackbar('R','controls',0,360*mult,callback)

r = cv.getTrackbarPos('R','controls')

k = cv.waitKey(0)

#  484389  = 1.251281695;


# for i in range(100000):
# 	shin_left.read_single_loop()
# 	print(shin_left.curr_deg)
# 	# shin_left.read()

# print(shin_left.goal_pos)