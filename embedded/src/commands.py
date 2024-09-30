
def motor_off(motor_id = 1):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0x80)
	[ frame.append(0x00) for i in range(7) ]
	frame.append(0x55)
	return bytes(frame)


def motor_on(motor_id = 1):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0x88)
	[ frame.append(0x00) for i in range(7) ]
	frame.append(0x55)
	return bytes(frame)

def single_loop_angle_read(motor_id = 1):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0x94)
	[ frame.append(0x00) for i in range(7) ]
	frame.append(0x55)
	return bytes(frame)

# angleIncrement is int32_t, corresponding actual position is 0.01degree/LSB, i.e 36000
# corresponding to 360°,motor spin direction is determined by the symbol of parameter.
def increment_angle(motor_id = 1,angleIncrement = 0):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0xa7)
	frame.append(0x00)
	frame.append(0x00)
	frame.append(0x00)
	[ frame.append(x) for x in angleIncrement.to_bytes(4,'little', signed=True)]
	frame.append(0x55)
	return bytes(frame)	

def single_loop_angle_control(motor_id = 1,angleAbsolute = 0,direction = 0x00):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0xa5)
	frame.append(direction)
	frame.append(0x00)
	frame.append(0x00)
	[ frame.append(x) for x in angleAbsolute.to_bytes(4,'little', signed=True)]
	frame.append(0x55)
	return bytes(frame)	


# Host send commands to control the torque current output, iqControl value is int16_t, range is -2048~
# 2048, corresponding MF motor actual torque current range is -16.5A~16.5A, corresponding MG motor
# actual torque current range is -33A~33A.
def torque_control(motor_id = 1,iqControl = 0):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0xa1)
	frame.append(0x00)
	frame.append(0x00)
	frame.append(0x00)
	[ frame.append(x) for x in iqControl.to_bytes(2,'little', signed=True)]
	frame.append(0x00)
	frame.append(0x00)
	frame.append(0x55)
	return bytes(frame)		

def read_pid(motor_id = 1):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0x30)
	[ frame.append(0x00) for i in range(7) ]
	frame.append(0x55)
	return bytes(frame)
def read_encoder(motor_id = 1):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0x90)
	[ frame.append(0x00) for i in range(7) ]
	frame.append(0x55)
	return bytes(frame)
def clear_motor_state(motor_id = 1):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0x9b)
	[ frame.append(0x00) for i in range(7) ]
	frame.append(0x55)
	return bytes(frame)