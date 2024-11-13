import cv2 as cv
from motor import motor, device
import time
import serial
import signal
import sys


uca = device("/dev/ttyUSB0")

def find_motor_id(device, max_attempts=32):
    """
    Scans possible motor IDs and returns the detected motor IDs.
    
    Parameters:
        device (object): The serial device object to communicate with the motor.
        max_attempts (int): The maximum range for motor IDs to try (default is 32).
        
    Returns:
        list: List of detected motor IDs.
    """
    found_ids = []

    for motor_id in range(1, max_attempts + 1):
        # Send a read command to check if this ID is valid
        frame = read_motor_state_1(motor_id)
        device.write(frame)
        time.sleep(0.01)

        # Read response from the device
        response = device.read(device.in_waiting)

        # Check if a valid response is received
        if response and response[0] == 0xAA and response[4] == 0x9A:
            print(f"Motor ID {motor_id} detected.")
            found_ids.append(motor_id)

    if not found_ids:
        print("No motor detected.")
    else:
        print("Detected motor IDs:", found_ids)
    
    return found_ids
