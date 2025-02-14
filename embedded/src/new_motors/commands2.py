
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
