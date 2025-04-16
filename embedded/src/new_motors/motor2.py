from commands2 import *
from blueteam import *
import time
import random
import serial

CANUSB_TTY_BAUD_RATE_DEFAULT = 2000000


from parsing import *


class device():
	uca = None
	def __init__(self, port):
		self.uca = serial.Serial(port, baudrate=CANUSB_TTY_BAUD_RATE_DEFAULT, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, timeout=0.0001)
	def port(self):
		return self.uca

class motor():
	motor_id = -1	
	device = None 

	def __init__ (self, id, uca, offset): 
		self.motor_id = id   
		self.device = uca
		self.offset = offset 
		self.speed = 100


	def home(self):
		self.abs_position_clc(self.speed, self.offset)
	# 2.1
	def read_pid_param(self):
		self.device.write(read_pid(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

	#2.2
	def write_pid_to_RAM(self, currentPidKp, currentPidKi, speedPidKp, speedPidKi, positionPidKp, positionPidKi):
		self.device.write(write_pid_to_RAM(self.motor_id, currentPidKp, currentPidKi, speedPidKp, speedPidKi, positionPidKp, positionPidKi))

	#2.3
	def write_pid_to_ROM(self, currentPidKp, currentPidKi, speedPidKp, speedPidKi, positionPidKp, positionPidKi):
		self.device.write(write_pid_rom(self.motor_id, currentPidKp, currentPidKi, speedPidKp, speedPidKi, positionPidKp, positionPidKi))

	#2.4
	def read_acceleration(self):
		self.device.write(read_acceleration(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

	#2.5
	def write_accel_ROM_RAM(self, func_index, accel):
		self.device.write(write_accel(self.motor_id, func_index, accel))

	#2.6
	def read_encoder(self):
		self.device.write(read_encoder(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

	# 2.7
	def read_multi_encoder_orig_pos(self):
		self.device.write(read_multi_encoder_original_position(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

	# 2.8
	def read_encoderZero_offset_data(self):
		self.device.write(read_encoder_zero_offset_data(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

	# 2.9
	def write_multiturn_encoder_zero_rom(self, new_zero):
		self.device.write(write_encoder_multi_value_rom_as_zero(self.motor_id, new_zero))

	#2.10 
	def write_encoder_value_to_rom_as_zero(self):
		self.device.write(write_encoder_value_to_rom_as_zero(self.motor_id))


	# 2.11
	def read_single_turn_encoder(self):
		self.device.write(read_single_turn_encoder(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		# for b in byte_list:
		# 	print(hex(b))
		parse_angle(byte_list)
	#2.12
	def read_multiturn_angle(self):
		self.device.write(read_multi_turn_angle(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

	# 2.13
	def read_singleTurn_angle(self):
		self.device.write(read_single_turn_angle(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		# for b in byte_list:
		# 	print(hex(b))
		parse_angle(byte_list)

	#2.14
	def read_motor_stats_one_and_error_flag(self):
		self.device.write(read_motor_stats_one_and_error_flag(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

	# 2.15
	def read_motor_status2(self):
		self.device.write(read_motor_status_2(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

	#2.16
	def read_motor_stats_three(self):
		self.device.write(read_motor_stats_three(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

	# 2.17
	def motor_shut_down(self):
		self.device.write(motor_shutdown(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))
		

	# 2.18
	def motor_stop(self):
		self.device.write(motor_stop(self.motor_id))

	# 2.19
	def torque_control_move(self,torque):
		self.device.write(motor_torque_control(self.motor_id,torque))

	# 2.20
	def speed_control_move(self, speed):
		self.device.write(motor_speed_control(self.motor_id, speed))

	# 2.21
	def abs_position_clc(self, maxSpeed, angle):
		self.device.write(abs_position_closedloop_control(self.motor_id, maxSpeed, angle))

    # 2.22
	def goto_position_control(self,angle,direction,speed):
		self.device.write(single_turn_position_control(self.motor_id, angle, direction, speed))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

	# 2.23
	def incr_position_clc(self, maxSpeed, angle): 
		self.device.write(incremental_position_closedloop_control(self.motor_id, maxSpeed, angle))
	
	# 2.24
	def sys_op_mode(self):
		self.device.write(sys_op_mode(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

	# 2.25
	def Motor_Power_Acquisition(self):
		self.device.write(motor_power_acq(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

	# 2.26
	def reset_mode(self):
			self.device.write(sys_reset_command(self.motor_id))

	# 2.27
	def Motor_brake_release(self):
		self.device.write(motor_brake_release(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))			
	
	# 2.28
	def brake_lock(self):
		self.device.write(sys_brake_lock(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

	# 2.29
	def sys_run_read(self):
		self.device.write(sys_runtime_read(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

	#2.30
	def read_version(self):
		self.device.write(sys_software_date(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))

		# print(int.from_bytes(byte_list[8:1], 'little', signed=False))

	# 2.31
	def communication_interruption_time_set(self, time):
		self.device.write(set_comm_interupt_protection_time(self.motor_id, time))

	# 2.32
	def set_com_baud(self, baudrate):
		self.device.write(com_baud_setting(self.motor_id, baudrate))

	# 2.33
	def motor_model(self):
		self.device.write(read_motor_model(self.motor_id))
		time.sleep(0.1)
		byte_list = self.device.read(self.device.in_waiting)
		for b in byte_list:
			print(hex(b))
	
	# 2.34
	def reply_active(self, command,reply,interval_time):
		self.device.write(active_reply(self.motor_id, command, reply, interval_time))

	# 2.35
	def func_control_command(self, func_index, val):
		self.device.write(function_control(self.motor_id, func_index, val))
	
	# 4
	def canID_control(self, wr, newID): 
		self.device.write(canID_command(self.motor_id, wr, newID))



	
