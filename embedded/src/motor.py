from commands import motor_off,motor_on,single_loop_angle_control,read_encoder
import time
import random
import serial


CANUSB_TTY_BAUD_RATE_DEFAULT = 2000000
uca_serial_device = serial.Serial("/dev/ttyUSB0", baudrate=CANUSB_TTY_BAUD_RATE_DEFAULT, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, timeout=0.000001)


def parse_encoder(frame):
	print(len(frame))
	if not len(frame) == 13 :
		return
	print("ID:", frame[2] - 0x40, end = '\t')
	print("Function:", hex(frame[4]), end = '\t')
	print("Next:", hex(frame[5]), end = '\t')
	print("Encoder:", int.from_bytes(frame[6:7],byteorder='little', signed=False), end = '\t')
	print("Encoder Raw:", int.from_bytes(frame[8:9],byteorder='little', signed=False), end = '\t')
	print("Encoder Offset:", int.from_bytes(frame[10:11],byteorder='little', signed=False), end = '\t')



class motor():
	motor_id = -1
	curr_pos = 0
	goal_pos = 0
	curr_vel = 0
	goal_vel = 0
	armed = False
	device = None
	response_frames = []
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

shin_left = motor(3,uca_serial_device)

# shin_left.motor_arm()

print(shin_left.goal_pos)

shin_left.read_motor_encoder()
shin_left.move_degrees_abs(10000)

time.sleep(1)
shin_left.read_motor_encoder()

print(shin_left.goal_pos)