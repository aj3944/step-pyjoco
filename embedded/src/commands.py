# 1
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

# 2
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

# 3
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

# 6
# SpeedControl value is int32_t, corresponding actual speed is 0.01dps/LSB.
def speed_closed_loop(motor_id = 1,speedControl=0): 
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0xa2)
	[ frame.append(0x00) for i in range(3) ]
	[ frame.append(x) for x in speedControl.to_bytes(4, 'little', signed=True) ]
	frame.append(0x55)
	return bytes(frame)

# 7
# anglecontrol is int32_t, corresponding actual position is 0.01degree/LSB, i.e 36000 corresponding to 360°,
# motor spin direction is determined by the difference between the target position and the current position.
def multi_loop_angle_control(motor_id = 1,angleControl=0):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0xa3)
	[ frame.append(0x00) for i in range(3) ]
	[ frame.append(x) for x in angleControl.to_bytes(4, 'little', signed=True) ]	
	frame.append(0x55)
	return bytes(frame)

# 8
# 1. angleControl is int32_t,corresponding actual position is 0.01degree/LSB, i.e 36000 corresponding to 360°,
# motor spin direction is determined by the difference between the target
# position and the current position.
# 2. maxSpeed limit the max speed, it is uint16_t, corresponding actual speed is 1dps/LSB, i.e 360
# corresponding to 360dps.
def multi_loop_angle_speed_control(motor_id=1,angleControl=0,speedControl=0):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0xa4)
	frame.append(0x00)
	[ frame.append(x) for x in speedControl.to_bytes(2, 'little', signed=True) ]
	[ frame.append(x) for x in angleControl.to_bytes(4, 'little', signed=True) ]
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
 
# 10
def single_loop_angle_speed_control(motor_id=1,angleAbsolute=0,direction=0x00,speedControl=0):
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0xa6)
	frame.append(direction)
	[ frame.append(x) for x in speedControl.to_bytes(2, 'little', signed=True)]
	[ frame.append(x) for x in angleAbsolute.to_bytes(4, 'little', signed=True)]
	frame.append(0x55)
	return bytes(frame)

# 12
def increment_angle_speed(motor_id=1, speed=0, speedControl=0): 
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01)
	frame.append(0xa8)
	frame.append(0x00)
	[ frame.append(x) for x in speedControl.to_bytes(2,'little',signed=True) ]
	[ frame.append(x) for x in speed.to_bytes(4,'little',signed=True) ]
	frame.append(0x55)
	return bytes(frame)	
# def increment_angle2(motor_id = 1,angleIncrement = 0, max_speed = 0):
# 	frame = bytearray()
# 	frame.append(0xaa)
# 	frame.append(0xc8)
# 	frame.append(0x40 + motor_id)
# 	frame.append(0x01)
# 	frame.append(0xa8)
# 	frame.append(0x00)
# 	[ frame.append(x) for x in max_speed.to_bytes(2,'little', signed=True)]
# 	[ frame.append(x) for x in angleIncrement.to_bytes(4,'little', signed=True)]
# 	frame.append(0x55)
# 	return bytes(frame)	

# 22
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


# 11
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

# 5
# Host send commands to control the torque current output, iqControl value is int16_t, range is -2048~
# 2048, corresponding MF motor actual torque current range is -16.5A~16.5A, corresponding MG motor
# actual torque current range is -33A~33A.
#torque closed loop control command
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

# 13
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

# 14
# write pid commands to ram
def write_pid_to_RAM(motor_id = 1, anglePidKp=0, anglePidKi=0, speedPidKp=0, speedPidKi=0, iqPidKp=0, iqPidKi=0): 
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01) 
	frame.append(0x31)
	frame.append(0x00)
	frame.append(anglePidKp.to_bytes(1, 'little', signed=True))
	frame.append(anglePidKi.to_bytes(1, 'little', signed=True))
	frame.append(speedPidKp.to_bytes(1, 'little', signed=True))
	frame.append(speedPidKi.to_bytes(1, 'little', signed=True))
	frame.append(iqPidKp.to_bytes(1, 'little', signed=True))
	frame.append(iqPidKi.to_bytes(1, 'little', signed=True))
	frame.append(0x55)
	return bytes(frame)

# 16 
def read_acceleration(motor_id): 
	frame = bytearray()
	frame.append(0xaa)
	frame.append(0xc8)
	frame.append(0x40 + motor_id)
	frame.append(0x01) 
	frame.append(0x33)
	[ frame.append(0x00) for i in range(7) ]
	frame.append(0x55) 
	return bytes(frame)

# 17
#Host send commands to write acceleration to RAM.Parameter are invalid when power off. DataAccel is int32_t,unit is 1dps/s
def write_acceleration_to_ram(motor_id=1, accel=0):
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x34)
    [ frame.append(0x00) for i in range(3) ]
    [ frame.append(x) for x in accel.to_bytes(4,'little', signed=True)]
    frame.append(0x55)
    return bytes(frame)

# 18
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

# 25
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

# 19 
#Host send this command to set encoder offset. EncoderOffset is uint16_t,14bit encoder range is 0~16383.
def write_encoder_value_to_rom_as_zero(motor_id = 1, encoder_offset = 0):
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x91)
    [frame.append(0x00) for i in range(5)]
    [ frame.append(x) for x in encoder_offset.to_bytes(2,'little', signed=False)]
    frame.append(0x55)
    return bytes(frame)
    
    
# 20
#Write motor encoder current position to ROM as the initial position. Remark:
#1. The command will be valid only after reset power.
#2. This command will write the zero point to the driver's ROM, multiple writes will affect the
#chip life, and frequent use is not recommended.
def write_current_position_to_rom_as_zero(motor_id=1):
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x19)
    [frame.append(0x00) for i in range(7)]
    frame.append(0x55)
    return bytes(frame)

# 21 
#Host send this command to read current motor multi angle absolute value.
def read_multi_angle_loop(motor_id=1):
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x92)
    [frame.append(0x00) for i in range(7)]
    frame.append(0x55)
    return bytes(frame)

# 25
#This command is to clear motor current error state.
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

# 23
#This command clear motor multi turn and single turn data and set current position as motor zero point. It’s invalid when power off.
def clear_motor_angle_loop(motor_id=1):
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x95)
    [frame.append(0x00) for i in range(7)]
    frame.append(0x55)
    return bytes(frame)

# 24
#This command read current motor temperature, voltage and error state.
def read_motor_state_1(motor_id=1):
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x9a)
    [frame.append(0x00) for i in range(7)]
    frame.append(0x55)
    return bytes(frame)

# 26 
#This command read current temperature,voltage,speed and encoder position.
def read_motor_state_2(motor_id=1):
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x9c)
    [frame.append(0x00) for i in range(7)]
    frame.append(0x55)
    return bytes(frame)

 # 27
#This command read current motor temperature and phase current data.
def read_motor_state_3(motor_id = 1):
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x9d)
    [ frame.append(0x00) for i in range(7) ]
    frame.append(0x55)
    return bytes(frame)