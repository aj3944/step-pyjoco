from commands import motor_off,motor_on,single_loop_angle_control,read_encoder,torque_speed_control
import time
import random
import serial

from commands import multi_loop_angle_speed_control,read_motor_state_1

CANUSB_TTY_BAUD_RATE_DEFAULT = 2000000
# uca_serial_device = serial.Serial("/dev/ttyUSB1", baudrate=CANUSB_TTY_BAUD_RATE_DEFAULT, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, timeout=0.000001)

class device():
	uca = None
	def __init__(self, port):
		self.uca = serial.Serial(port, baudrate=CANUSB_TTY_BAUD_RATE_DEFAULT, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, timeout=0.000001)
	def port(self):
		return self.uca

def parse_encoder(frame):
	# print(len(frame))
	if not len(frame) == 13 or not frame[4] == 0x90 :
		return
	# print("ID:", frame[2] - 0x40, end = '\t')
	# print("Function:", hex(frame[4]), end = '\t')
	# print("Next:", hex(frame[5]), end = '\t')
	encoder_val = int.from_bytes(frame[6:7],byteorder='little', signed=False)
	# print("Encoder:", encoder_val, end = '\t')
	# print("Encoder Raw:", int.from_bytes(frame[8:9],byteorder='little', signed=False), end = '\t')
	# print("Encoder Offset:", int.from_bytes(frame[10:11],byteorder='little', signed=False), end = '\n')
	return encoder_val


def parse_state(frame):
	if not len(frame) == 13 or not frame[4] == 0x9a :
		return
	# print("ID:", frame[2] - 0x40, end = '\t')
	# print("Function:", hex(frame[4]), end = '\t')
	print("Temprature:", frame[5], end = '\t')
	# encoder_val = int.from_bytes(frame[6:7],byteorder='little', signed=False)
	# print("Encoder:", encoder_val, end = '\t')
	# print("Encoder Raw:", int.from_bytes(frame[8:9],byteorder='little', signed=False), end = '\t')
	# print("Encoder Offset:", int.from_bytes(frame[10:11],byteorder='little', signed=False), end = '\n')
	return frame[5]


class motor():
	motor_id = -1
	curr_pos = 0
	goal_pos = 0
	curr_vel = 0
	goal_vel = 0
	armed = False
	device = None
	response_frames = []
	curr_temp = 0

	def __init__(self, id_, uca):
		self.motor_id = id_
		self.curr_pos = 0
		self.goal_pos = 0
		self.device = uca
	def motor_arm(self):
		self.armed = True
		self.device.write(motor_on(self.motor_id))
	def motor_disarm(self):
		self.armed = False
		self.device.write(motor_off(self.motor_id))
	def move_degrees_abs(self,value):
		self.goal_pos += value
		self.device.write(single_loop_angle_control(self.motor_id,value))
	def read_motor_encoder(self):
		# self.curr_pos
		self.device.write(read_encoder(self.motor_id))
		time.sleep(0.01)
		byte_list = self.device.read(self.device.in_waiting)
		# print(byte_list)
		frame = []
		for byte in byte_list:
			if byte == 0xaa:
				self.response_frames.append(frame)
				frame = []
				frame.append(byte)
			else:
				frame.append(byte)
		self.response_frames.append(frame)
		for frame in self.response_frames:
			# print(frame)
			parse_encoder(frame)
	def goto(self,angle):
		delta = angle - self.goal_pos;
		self.device.write(increment_angle(self.motor_id,delta))
		self.goal_pos = angle
	def goto(self,angle,speed):
		delta = angle - self.goal_pos;
		self.device.write(multi_loop_angle_speed_control(self.motor_id,delta,speed))
		self.goal_pos = angle
	def read(self):
		self.device.write(read_encoder(self.motor_id))
		time.sleep(0.01)
		byte_list = self.device.read(self.device.in_waiting)
		frame = []
		for byte in byte_list:
			if byte == 0xaa:
				self.response_frames.append(frame)
				frame = []
				frame.append(byte)
			else:
				frame.append(byte)
		self.response_frames.append(frame)
		for frame in self.response_frames:
			# print(frame)
			curr_pos = parse_encoder(frame)	
			if not curr_pos == None:
				self.curr_pos = curr_pos
				print(self.curr_pos)
	def read_state(self):
		self.device.write(read_motor_state_1(self.motor_id))
		time.sleep(0.01)
		byte_list = self.device.read(self.device.in_waiting)
		frame = []
		for byte in byte_list:
			if byte == 0xaa:
				self.response_frames.append(frame)
				frame = []
				frame.append(byte)
			else:
				frame.append(byte)
		self.response_frames.append(frame)
		print(self.response_frames)
		for frame in self.response_frames:
			# print(frame)
			curr_temp = parse_state(frame)	
			if not curr_temp == None:
				self.curr_temp = curr_temp
				print(self.curr_temp)