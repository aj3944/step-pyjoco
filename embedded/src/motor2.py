from commands2 import *
import time
import random
import serial

import can
from can import BusState
 
# can.rc['interface'] = 'serial'
# can.rc['channel'] = "/dev/tty.usbserial-120"
# can.rc['baudrate'] = 1000000
# from can.interface import Bus

# bus = Bus()

CANUSB_TTY_BAUD_RATE_DEFAULT = 2000000

class device():
	uca = None
	def __init__(self, port):
		self.uca = serial.Serial(port, baudrate=CANUSB_TTY_BAUD_RATE_DEFAULT, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, timeout=0.000001)
	def port(self):
		return self.uca

class motor():
	motor_id = -1	
	device = None 

	def __init__ (self, id, uca): 
		self.motor_id = id   
		self.device = uca

	def stop_motor(self):
		self.device.write(motor_stop(self.motor_id))

	def single_turn_position_control(self):
		self.device.write(motor_single_turn_position_control(self.motor_id, 0x00))

	def torque_control(self, torque): 
		# self.device.write(motor_torque_control(self.motor_id))
		# with can.Bus(interface='serial', channel="/dev/tty.usbserial-120", bitrate=1000000) as bus: 
		# 	msg = can.Message(
		# 		arbitration_id=0x141, 
		# 		# data = [0xA1, 0x00, 0x00, 0x00, 0xAA, 0xAA, 0x00, 0x00],
		# 		data = [161, 0, 0, 0, 170, 170, 0, 0],
		# 		is_extended_id=False
		# 	)
		# 	try: 
		# 		bus.send(msg, timeout=2)
		# 		print(f"Message sent on {bus.channel_info}")
		# 		print(f"{msg.arbitration_id:X}: {msg.data}")
				
		# 	except can.CanError:
				# print("Message NOT sent")
		self.device.write(motor_torque_control(self.motor_id, torque))

def receive(): 
	with can.Bus(interface='serial', channel="/dev/tty.usbserial-120", bitrate=2000000) as bus: 
		try: 
			  bus.state = BusState.PASSIVE
		except NotImplementedError:
			pass

		try:
			while True:
				msg = bus.recv(1)
				if msg is not None:
					print(msg)

		except KeyboardInterrupt:
			pass  # exit normally

if __name__ == '__main__':
	torque_control()
	