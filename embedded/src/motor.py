from commands import motor_off,motor_on,single_loop_angle_control,read_encoder,increment_angle_speed
import time
import random
import serial

from commands import multi_loop_angle_speed_control,read_motor_state_1,torque_control,single_loop_angle_read,single_loop_angle_speed_control,read_motor_state_3,read_motor_state_2

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
	encoder_val = int.from_bytes(frame[6:8],byteorder='little', signed=False)
	# print("Encoder:", encoder_val, end = '\t')
	# print("Encoder Raw:", int.from_bytes(frame[8:10],byteorder='little', signed=False), end = '\t')
	# print("Encoder Offset:", int.from_bytes(frame[10:12],byteorder='little', signed=False), end = '\n')
	return encoder_val

def parse_single_loop(frame):
	# print(len(frame))
	if not len(frame) == 13 or not frame[4] == 0x94 :
		return
	# print("ID:", frame[2] - 0x40, end = '\t')
	# print("Function:", hex(frame[4]), end = '\t')
	# print("Next:", hex(frame[5]), end = '\t')
	single_loop_val = int.from_bytes(frame[8:12],byteorder='little', signed=False)
	# print("Single Loop:", single_loop_val, end = '\t')
	return single_loop_val


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

def parse_torque_current(frame): 
	if not len(frame) == 13 or not frame[4] == 0x9c:
		return
	#print("ID:", frame[2] - 0x40, end = '\t')
	#print("Function:", hex(frame[4]), end = '\t')
	#print("Temprature:", frame[5], end = '\t')
	torque_current = int.from_bytes(frame[6:8],byteorder='little', signed=True)
	#print("torque current:", torque_current, end = '\t')
	#motor_speed = int.from_bytes(frame[8:10],byteorder='little', signed=True),
	#print("motor speed:", motor_speed,  end = '\t')
	#encoder_position = int.from_bytes(frame[10:12],byteorder='little', signed=True),
	#print("encoder_position:", encoder_position, end = '\n')
	return torque_current

def parse_phase_current(frame): 
	if not len(frame) == 13 or not frame[4] == 0x9d :
		return
	#print("ID:", frame[2] - 0x40, end = '\t')
	#print("Function:", hex(frame[4]), end = '\t')
	#print("Temprature:", frame[5], end = '\t')
	A_phase = int.from_bytes(frame[6:8],byteorder='little', signed=True)
	print("A phase current:", A_phase, end = '\t')
	B_phase = int.from_bytes(frame[8:10],byteorder='little', signed=True),
	print("B phase current:", B_phase[0],  end = '\t')
	C_phase = int.from_bytes(frame[10:12],byteorder='little', signed=True),
	print("C phase current:", C_phase[0], end = '\n')
	return A_phase, B_phase[0], C_phase[0]



class motor():
	motor_id = -1
	curr_pos = 0
	curr_deg = 0
	goal_pos = 0
	curr_vel = 0
	goal_vel = 0
	armed = False
	device = None
	response_frames = []
	curr_temp = 0
	curr_encod1 = 0
	curr_i = 0
	cf_factor = 1.251281695;

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
			encoder_1 = parse_encoder(frame)
			if not encoder_1 == None:
				self.curr_encod1 = encoder_1
	def increment(self,angle):
		self.device.write(increment_angle(self.motor_id,angle))
	def increment(self,angle,speed):
		self.device.write(increment_angle_speed(self.motor_id,angle,speed))
	def goto_single_loop(self,angle,direction,speed):
		self.device.write(single_loop_angle_speed_control(self.motor_id,angle,direction,speed))
	def read(self):
		self.device.write(read_encoder(self.motor_id))
		time.sleep(0.001)
		byte_list = self.device.read(self.device.in_waiting)
		frame = []
		for byte in byte_list:
			if byte == 0xaa:
				self.response_frames.append(frame)
				frame = []
				frame.append(byte)
			else:
				frame.append(byte)
		# self.response_frames.append(frame)
		# for frame in self.response_frames:
		# 	# print(frame)
		if not frame == []: 
			curr_pos = parse_encoder(frame)	
			if not curr_pos == None:
				self.curr_pos = curr_pos
				# print(self.curr_pos)
	def read_single_loop(self):
		self.device.write(single_loop_angle_read(self.motor_id))
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
		# self.response_frames.append(frame)
		# for frame in self.response_frames:
		# print(frame)
		if not frame == []: 
			curr_sl = parse_single_loop(frame)	
			if not curr_sl == None:
				self.curr_deg = self.cf_factor*curr_sl*0.001
				# print(self.curr_deg)
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
	def torque_control_move(self,q_val):
		self.device.write(torque_control(self.motor_id,q_val))
	def stop_when_reached(self,max_torque,tolerance):
		self.read_single_loop()
		error = self.goal_pos - self.curr_deg;
		while abs(error) > tolerance: 
			self.torque_control_move(0)
			print("error\t",error,"tolerance\t",tolerance)
			self.read_single_loop()
			error = self.goal_pos - self.curr_deg;
			tolerance *= 1.01
			self.torque_control_move(max_torque)

		self.torque_control_move(0)
	def start_move(self,max_torque,tolerance):
		error = self.goal_pos - self.curr_deg;
		if abs(error) > tolerance:
			pass
		direction = self.goal_pos - self.curr_deg + 0.0000001
		d = -abs(direction)/direction
		if d < 0:
			d = 0
		else:
			d = 1
		if d:
			self.torque_control_move(max_torque)
		else:
			self.torque_control_move(-1*max_torque)
		self.stop_when_reached(max_torque,tolerance)
	def move_to(self,deg,max_torque = 10,tolerance = 1):
		if deg < 0 or deg > 360:
			return 0
		else:
			self.goal_pos = deg;
			self.start_move(max_torque,tolerance)
			# delta = deg - self.curr_deg;
			# if abs(delta) > tolerance:
			# 	if deg > self.curr_deg:
			# 		self.torque_control_move(max_torque)
			# 		self.read_single_loop()
			# 	elif deg < self.curr_deg:
			# 		self.torque_control_move(-1*max_torque)
			# 		self.read_single_loop()
			# 	delta = deg - self.curr_deg;

	def read_state3(self):
		self.device.write(read_motor_state_3(self.motor_id))
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
		# print(self.response_frames)
		for frame in self.response_frames:
			#print(frame)
			curr_phases = parse_phase_current(frame)	
			if not curr_phases == None:
				self.curr_i = curr_phases
				# print(self.curr_phases)

	def read_state2(self): 
		self.device.write(read_motor_state_2(self.motor_id))
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
		# print(self.response_frames)
		for frame in self.response_frames:
			#print(frame)
			torque_curr = parse_torque_current(frame)	
			if not torque_curr == None:
				self.curr_i = torque_curr
				#print(torque_curr)
				