def motor_stop(motor_id = 1):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0x81)
	[ frame.append(0x00) for i in range(7) ]
	frame.append(0x55)
	return bytes(frame)

def motor_single_turn_position_control(motor_id = 0x1, direction = 0x00): 
	speedLSB = 0x3
	speedMSB = 0x3
	angleCTRLLSB = 0x3
	angleCTRLMSB = 0x3
	frame = bytearray()
	frame.extend(0xaa)
	frame.append(0xc8)
	frame.extend(0x40 + motor_id) 
	frame.extend(0x01) 
	frame.extend(0xA6) 
	frame.extend(direction)
	frame.extend(speedLSB) 
	frame.extend(speedMSB)
	frame.extend(angleCTRLLSB)
	frame.extend(angleCTRLMSB)
	frame.extend(0x00)
	frame.extend(0x00) 
	frame.extend(0x55)

	return bytes(frame)

def motor_torque_control(motor_id = 1, torque = 0x03):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id) 
	frame.append(0x01)
	frame.append(0xa1) 
	[ frame.append(0x00) for i in range(3) ]
	[ frame.append(x) for x in torque.to_bytes(2, 'little', signed=True)]
	[ frame.append(0x00) for i in range(2) ]
	frame.append(0x55)
	return bytes(frame)

