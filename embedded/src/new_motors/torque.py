from motor2 import device, motor
import serial
import time
import random

low, high, count = 1,100,12  

# Initialize the device
uca = device("/dev/tty.usbserial-130")
# uca = device("/dev/ttyUSB0")

test_motor = motor(1, uca.port()) 

# test_motor.incr_position_clc(1000, 18000)
# test_motor.goto_position_control(18000, 0x00, 1000)

test_motor.motor_stop()

def process_torque_inputs(inputs, low, high):
    """
    Process 12 outputs and send commands to the motor
    """
    if len(inputs) != count:
        raise ValueError("Exactly", count, "input values are required.")

    torque_values = []
        
    for value in inputs:
        torque_value = int((value - low) / (high - low) * 65535 - 32768)
        torque_values.append(torque_value)
        # torque_control_move(torque_value) 
        
    return torque_values   

# Generate 12 random input values
inputs = [random.randint(low, high) for i in range(count)]

print("Random inputs:", inputs)

# Process torque inputs and retrieve torque values
torque_values = process_torque_inputs(inputs,low, high)
print("Processed torque values:", torque_values)

for i in torque_values:
    test_motor.torque_control_move(i)

# time.sleep(1) 

test_motor.motor_stop()