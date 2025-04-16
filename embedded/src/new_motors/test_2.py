from motor2 import device, motor
import serial
import time


# import can 

# Initialize the device
uca = device("/dev/tty.usbserial-1140")
# uca = device("/dev/ttyUSB0")

test_motor = motor(1, uca.port(), 2000 ) 
test_motor.canID_control(wr = 0, newID = 4)
# test_motor.home()

# test_motor.incr_position_clc(1000, 18000)
# test_motor.goto_position_control(18000, 0x00, 1000)

# test_motor.read_singleTurn_angle()
# test_motor.read_single_turn_encoder()

# test_motor.abs_position_clc(100,-3500)
# test_motor.abs_position_clc(100,9000)
time.sleep(2) 

test_motor.motor_stop()




# [ 1 , 1000]
# [ 11, 1000]

# [2, -500]
# [12 , -500]

# [3, 2500 ]
# [13, -2500]


#  [4 , ???]
#  [4, 2000]
#  [14, -1000] 

# [ 5, 1000 ]
# [ 15, 0]