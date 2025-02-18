# 2.1 send data: Create request frame for the Read PID parameter command
# returns a frame that requests the parameters of current, speed, position loop KP and KI
def motor_read_pid_command(motor_id = 1):
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

# 2.1 read data: Parse returned frame for the Read PID parameter command
# returns a tuple: (CurrKP, CurrKI, SpdKP, SpdKI, PosKP, PosKI)
def motor_read_pid_parse(frame):
	dataStartIndex = 0
	CurrKP = int.from_bytes(frame[dataStartIndex + 2], byteorder='little', signed=False)
	CurrKI = int.from_bytes(frame[dataStartIndex + 3], byteorder='little', signed=False)
	SpdKP = int.from_bytes(frame[dataStartIndex + 4], byteorder='little', signed=False)
	SpdKI = int.from_bytes(frame[dataStartIndex + 5], byteorder='little', signed=False)
	PosKP = int.from_bytes(frame[dataStartIndex + 6], byteorder='little', signed=False)
	PosKI = int.from_bytes(frame[dataStartIndex + 7], byteorder='little', signed=False)

	return (CurrKP, CurrKI, SpdKP, SpdKI, PosKP, PosKI)
	

# 2.3 Write PID parameters to ROM command
# write the parameters of current, speed, position loop KP and KI to RAM
# stay in 8 bit range, 0-255
def motor_write_pid_rom(motor_id = 1, CurrKP = 0x00, CurrKI = 0x00, SpdKP = 0x00, 
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
def motor_write_accel(motor_id = 1, function_index = 0x00, acceleration = 0x64):
	frame = bytearray()
	# header 
	frame.append(0xaa)
	frame.append(0xc8)
	# id 
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	# command_name
	frame.append(0x43)
	# data_packet
	frame.append(function_index)
	frame.append(0x00) 
	frame.append(0x00) 
	[frame.append(x) for x in acceleration.to_bytes(4, 'little', signed=False)]
	# eof 
	frame.append(0x55)
	return bytes(frame)

# 2.7 send data: Create request frame for multi-turn encoder original position data command 
# returns a frame that requests for the multi-turn encoder home position
def motor_read_multi_encoder_original_position_command(motor_id = 1):
	frame = bytearray()
	# header 
	frame.append(0xaa)
	frame.append(0xc8)
	# id 
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	# command_name
	frame.append(0x61)
	# data_packet
	[ frame.append(0x00) for i in range(7) ]
	# eof 
	frame.append(0x55)
	return bytes(frame)

# 2.7 read data: Parse returned frame for the read multi-turn encoder original position data command 
# returns the multi-turn encoder home position
def motor_read_multi_encoder_original_position_parse(frame):
	dataStartIndex = 0
	origPos = int.from_bytes(frame[dataStartIndex + 4: dataStartIndex + 8], byteorder='little', signed=True)
	return origPos

# 2.9 Write encoder multi-turn value to ROM as motor zero command
# set the zero offset (initial position) of the multi turn encoder
def motor_write_encoder_multi_value_rom_as_zero(motor_id = 1, new_zero = 0x00):
	frame = bytearray()
	# header 
	frame.append(0xaa)
	frame.append(0xc8)
	# id 
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	# command_name
	frame.append(0x63)
	# data_packet
	[ frame.append(0x00) for i in range(3) ]
	[ frame.append(x) for x in new_zero.to_bytes(4, 'little', signed=True) ]
	# eof 
	frame.append(0x55)
	return bytes(frame)

# 2.11 send data: Create request frame for the read single-turn encoder command
# returns a frame that rquests the current position of the single turn encoder
def motor_read_single_turn_encoder_command(motor_id = 1):
	frame = bytearray()
	# header 
	frame.append(0xaa)
	frame.append(0xc8)
	# id 
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	# command_name
	frame.append(0x90)
	# data_packet
	[ frame.append(0x00) for i in range(7) ]
	# eof 
	frame.append(0x55)
	return bytes(frame)

# 2.11 read data: Parse returned frame for the read single-turn encoder command
# returns tuple: (position with zero offset, original position, zero offset)
def motor_read_single_turn_encoder_parse(frame):
	dataStartIndex = 0
	position = int.from_bytes(frame[dataStartIndex + 2: dataStartIndex + 4], byteorder='little', signed=False)
	origPosition = int.from_bytes(frame[dataStartIndex + 4: dataStartIndex + 6], byteorder='little', signed=False)
	zeroOffset = int.from_bytes(frame[dataStartIndex + 6: dataStartIndex + 8], byteorder='little', signed=False)
	return (position, origPosition, zeroOffset)


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

#2.25 Motor Power Acquisition
def motor_power_acq(motor_id=1):
	frame = bytearray()
	frame.append(0xaa) #header
	frame.append(0xc8) #header
	frame.append(0x40 + motor_id) #id
	frame.append(0x01) #id
	frame.append(0x71) #command name
	for i in range(7): #datapacket gets all the data[1]-[7]
		frame.append(0x00)
	frame.append(0x55) #end of frame
	return bytes(frame)