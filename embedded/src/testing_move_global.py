import cv2 as cv
from motor import motor, device
import time
import serial
import signal
import sys


# Initialize the device
uca = device("/dev/tty.usbserial-14140")

# Initialize the motor (assuming motor ID is 3, adjust as necessary)
shin_left = motor(3, uca.port())

# Disarm the motor to make sure it starts in a safe state
shin_left.motor_arm()

# Arm the motor for operation
time.sleep(1)
# shin_left.motor_arm()
# Define maximum speed based on protocol: 36000 corresponds to 360 dps
max_speed = 1800 # Maximum speed
testing_angle=120 #testing angle

# Perform pre-warning movement: move 10 degrees left, then right, and return to initial position
def pre_warning_movement():
    print("Pre-warning movement: moving 10 degrees left and right.")
    print("go to 20 degrees")
    shin_left.goto_single_loop(20*803, 0, max_speed // 2)  # Slow move left 10 degrees (5 dps)
    time.sleep(2)
    print("go to -20 degrees")
    shin_left.goto_single_loop(340*803, 1, max_speed // 2)  # Slow move right 10 degrees
    time.sleep(2)
    print("go to 0 degree")
    shin_left.goto_single_loop(0, 0, max_speed // 2)    # Return to initial position
    time.sleep(2)

# Perform fast movement to 60 degrees and return slowly

def fast_move_and_return(target_angle, active_Warning):
    Not_Reach_Target_1 = True
    Not_Reach_Target_2 = True
    tolerance=1
    if active_Warning:
        pre_warning_movement()
    
    print(f"Fast movement to {target_angle} degrees.")
    shin_left.goto_single_loop(target_angle * 803, 0, max_speed)  # Fast move to target_angle (max speed)
    
    while Not_Reach_Target_1:
        shin_left.read_single_loop()
        if abs(shin_left.curr_deg-target_angle)<tolerance:
            Not_Reach_Target_1 = False

    print("Returning to initial position.")
    shin_left.goto_single_loop(0, 1, max_speed // 1)  # Slowly return to the initial position
    
    
    while Not_Reach_Target_2:
        shin_left.read_single_loop()
        if abs(shin_left.curr_deg-0)<tolerance:
            Not_Reach_Target_2 = False

    
        
    
    

# Function triggered by the trackbar
def callback(x):
    global target
    print("Target angle: ", x)
    if x >= shin_left.curr_deg:
        shin_left.goto_single_loop(x, 1, max_speed)  # Move motor to the target position (max speed)
    else:
        shin_left.goto_single_loop(x, 0, max_speed)  # Move motor to the target position in the opposite direction

# Create OpenCV control window with a trackbar to adjust angle in real-time
cv.namedWindow('controls')
cv.createTrackbar('R', 'controls', 0, 360, callback)

# Get current trackbar position
r = cv.getTrackbarPos('R', 'controls')

# Perform the sequence
#pre_warning_movement()  # Step 2: pre-warning movement
#print(f"Iteration {i + 1}:")


for i in range(10):
    print(f"Iteration {i+1}")
    fast_move_and_return(testing_angle,False)  # Step 3 & 4: fast move to 60 degrees and slow return



time.sleep(2)
shin_left.goto_single_loop(0, 0, max_speed // 2)    # Return to initial position

# Wait for the trackbar input indefinitely
#cv.waitKey(0)

# Disarm the motor after the test
shin_left.motor_disarm()

print("Test complete.")
