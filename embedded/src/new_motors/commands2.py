# 2.1 Read PID parameter command
# read the parameters of current, speed, position loop KP and KI
def motor_read_pid(motor_id = 1):
	frame = bytearray()
	# header 
	frame.append(0xaa)
	frame.append(0xc8)
	# id 
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	# command_name
	frame.append(0x30)
	# data_packet
	[ frame.append(0x00) for i in range(7) ]
	# eof 
	frame.append(0x55)
	return bytes(frame)

# 2.3 Write PID parameters to ROM command
# write the parameters of current, speed, position loop KP and KI to RAM
# stay in 8 bit range, 0-255
def motor_write_accel(motor_id = 1, CurrKP = 0x00, CurrKI = 0x00, SpdKP = 0x00, 
						SpdKI = 0x00, PosKP = 0x00, PosKI = 0x00):
	frame = bytearray()
	# header 
	frame.append(0xaa)
	frame.append(0xc8)
	# id 
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	# command_name
	frame.append(0x32)
	# data_packet
	frame.append(0x00) 
	frame.append(CurrKP) 
	frame.append(CurrKI) 
	frame.append(SpdKP) 
	frame.append(SpdKI) 
	frame.append(PosKP)
	frame.append(PosKI)  
	# eof 
	frame.append(0x55)
	return bytes(frame)

# 2.5 Write acceleration to RAM and ROM command
# write the acceleration to RAM and ROM (units are degrees per second^2)
def motor_write_pid_rom(motor_id = 1, function_index = 0x00, acceleration = 0x64):
	frame = bytearray()
	# header 
	frame.append(0xaa)
	frame.append(0xc8)
	# id 
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	# command_name
	frame.append(0x32)
	# data_packet
	frame.append(function_index)
	frame.append(0x00) 
	frame.append(0x00) 
	[frame.append(x) for x in acceleration.to_bytes(4, 'little', signed=False)]
	# eof 
	frame.append(0x55)
	return bytes(frame)


# 2.18 Motor stop command
def motor_stop(motor_id = 1):
	frame = bytearray()
	# header 
	frame.append(0xaa)
	frame.append(0xc8)
	# id 
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	# command_name
	frame.append(0x81)
	# data_packet
	[ frame.append(0x00) for i in range(7) ]
	# eof 
	frame.append(0x55)
	return bytes(frame)

# 2.19 Torque closed-loop control command
def motor_torque_control(motor_id = 1, torque = 0x03):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0xa1)
	frame.append(0x00)
	frame.append(0x00)
	frame.append(0x00)
	[ frame.append(x) for x in torque.to_bytes(2, 'little', signed=True) ]
	frame.append(0x00)
	frame.append(0x00)
	# [ frame.append(x) for x in angleControl.to_bytes(4, 'little', signed=True) ]
	frame.append(0x55)
	return bytes(frame)


# 2.24 System operating mode acquisition 
# reads the current motor running mode
def sys_op_mode(motor_id = 1):
	frame = bytearray()
	# header 
	frame.append(0xaa)
	frame.append(0xc8)
	# id 
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	# command_name
	frame.append(0x70)
	# data packets
	[ frame.append(0x00) for i in range(7) ]
	# eof 
	frame.append(0x55)	
	return bytes(frame)
