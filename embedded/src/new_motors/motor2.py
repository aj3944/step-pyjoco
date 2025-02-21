from commands2 import *
import time
import random
import serial

CANUSB_TTY_BAUD_RATE_DEFAULT = 2000000

class device():
	uca = None
	def __init__(self, port):
		self.uca = serial.Serial(port, baudrate=CANUSB_TTY_BAUD_RATE_DEFAULT, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, timeout=0.0001)
	def port(self):
		return self.uca

class motor():
	motor_id = -1	
	device = None 

	def __init__ (self, id, uca): 
		self.motor_id = id   
		self.device = uca
		
	def torque_control_move(self,torque):
		self.device.write(motor_torque_control(self.motor_id,torque))

	def motor_stop(self):
		self.device.write(motor_stop(self.motor_id))

	def read_mode(self):
		self.device.write(sys_op_mode(self.motor_id))

	# 2.20
    	def speed_control_move(self, speed):
        	self.device.write(motor_speed_control(self.motor_id, speed))

    	# 2.22
    	def goto_position_control(self,angle,direction,speed):
        	self.device.write(single_turn_position_control(self.motor_id,angle,direction,speed)

	def motor_stop(self):
		self.device.write(motor_stop(self.motor_id))

    	#2.24
	def read_mode(self):
		self.device.write(sys_op_mode(self.motor_id))

    	# 2.26
    	def reset_mode(self):
        	self.device.write(sys_reset_command(self.motor_id))
		
