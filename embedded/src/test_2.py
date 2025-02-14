from motor2 import device, motor
import serial
import time


# Initialize the device
uca = device("/dev/tty.usbserial-130")

test_motor = motor(1, uca.port()) 

test_motor.torque_control(100)

time.sleep(5) 

test_motor.stop_motor() 
time.sleep(1)