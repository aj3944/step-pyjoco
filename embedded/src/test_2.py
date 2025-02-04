from motor2 import device, motor
import serial
import time
 
# Initialize the device
uca = device("/dev/tty.usbserial-130")

test_motor = motor(1, uca.port()) 

test_motor.single_turn_position_control()

time.wait(5) 

test_motor.stop_motor() 