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

	def write_pid_to_rom(self, CurrKP = 0x00, CurrKI = 0x00, SpdKP = 0x00, 
						SpdKI = 0x00, PosKP = 0x00, PosKI = 0x00):
		self.device.write(write_pid_rom(self.motor_id, CurrKP, CurrKI, SpdKP,
								  		 SpdKI, PosKP, PosKI))
		
	def write_acceleration(self, function_index, acceleration):
		self.device.write(write_accel(self.motor_id, function_index, acceleration))

	def read_multi_encoder_orig_pos(self):
		self.device.write(read_multi_encoder_original_position(self.motor_id))

	def write_multiturn_encoder_zero_rom(self, new_zero):
		self.device.write(write_encoder_multi_value_rom_as_zero(self.motor_id, new_zero))

	def read_single_turn_encoder(self):
		self.device.write(read_single_turn_encoder(self.motor_id))
	
	def read_pid_param(self):
		self.device.write(read_pid(self.motor_id))
		
	def torque_control_move(self,torque):
		self.device.write(motor_torque_control(self.motor_id,torque))

	def motor_stop(self):
		self.device.write(motor_stop(self.motor_id))

	def read_mode(self):
		self.device.write(sys_op_mode(self.motor_id))
	#2.2
	def write_pid_to_RAM(self, currentPidKp, currentPidKi, speedPidKp, speedPidKi, positionPidKp, positionPidKi):
		self.device.write(write_pid_to_RAM(self.motor_id, currentPidKp, currentPidKi, speedPidKp, speedPidKi, positionPidKp, positionPidKi))

	#2.4
	def read_acceleration(self):
		self.device.write(read_encoder(self.motor_id))
	
	#2.6
	def read_encoder(self):
		self.device.write(read_encoder(self.motor_id))

	#2.8
	def read_encoderZero_offset_data(self):
		self.device.write(read_encoderZero_offset_data(self.motor.id))

	#2.10 
	def write_encoder_value_to_rom_as_zero(self):
		self.device.write(write_encoder_value_to_rom_as_zero(self.motor.id))

	#2.12
	def read_multi_turn_angle(self):
		self.device.write(read_multi_turn_angle(self.motor.id))

	#2.14
	def read_motor_stats_one_and_error_flag(self):
		self.device.write(read_motor_stats_one_and_error_flag(self.motor.id))

	#2.16
	def read_motor_stats_three(self):
		self.device.write(read_motor_stats_three(self.motor.id))
		
	#2.18
	def motor_stop(self):
		self.device.write(motor_stop(self.motor_id))

	# 2.20
    	def speed_control_move(self, speed):
        	self.device.write(motor_speed_control(self.motor_id, speed))

    	# 2.22
	def reset_mode(self):
        	self.device.write(sys_reset_command(self.motor_id))
	# 2.24
	def sys_op_mode(self):
        	self.device.write(sys_op_mode(self.motor_id))

	# 2.26
	def goto_position_control(self,angle,direction,speed):
		self.device.write(single_turn_position_control(self.motor_id, angle, direction, speed))
				
	# 2.28
	def brake_lock(self):
		self.device.write(sys_brake_lock(self.motor_id))

	#2.30
	def read_version(self):
		self.device.write(sys_software_date(self.motor_id))

	#2.32
	def set_com_baud(self, baudrate):
		self.device.write(com_baud_setting(self.motor_id, baudrate))
	#2.34
	def reply_active(self, command,reply,interval_time):
		self.device.write(active_reply(self.motor_id, command, reply, interval_time))
	
		
	def abs_position_clc(self, maxSpeed, angle):
		self.device.write(abs_position_closedloop_control(self.motor_id, maxSpeed, angle))

	def incr_position_clc(self, maxSpeed, angle): 
		self.device.write(incremental_position_closedloop_control(self.motor_id, maxSpeed, angle))
  
  	def Motor_Power_Acquisition(self):
       self.device.write(motor_power_acq(self.motor_id))

