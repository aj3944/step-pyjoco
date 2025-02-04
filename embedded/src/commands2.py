def motor_stop(motor_id = 1):
	frame = bytearray()
	frame.append(0x140 + motor_id)
	frame.append(0x81)
	[ frame.append(0x00) for i in range(7) ]
	# frame.append(0x55)
	return bytes(frame)

def motor_single_turn_position_control(motor_id = 1, direction = 0x00): 
    speedLSB = 0x3
    speedMSB = 0x3
    angleCTRLLSB = 0x3
    angleCTRLMSB = 0x3
    frame = bytearray()
    frame.append(0x140 + motor_id) 
    frame.append(0xA6) 
    frame.append(direction)
    frame.append(speedLSB) 
    frame.append(speedLSB >> 8)
    frame.append(angleCTRLLSB)
    frame.append(angleCTRLLSB >> 8)
    frame.append(0x00)
    frame.append(0x00) 

def motor_torque_control(motor_id = 1, torque = 0x3):
    frame = bytearray()
    frame.append(0x140 + motor_id) 
    frame.append(0xA1) 
    [ frame.append(0x00) for i in range(3) ]
    frame.append(torque)
    frame.append(torque >> 8) 
    [ frame.append(0x00) for i in range(2) ]

