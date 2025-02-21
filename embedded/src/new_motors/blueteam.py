# 2 CHECK BEFORE FINALIZE: Write PID to RAM Command
def write_pid_to_RAM(motor_id=1, currentPidKp=0, currentPidKi=0,
                     speedPidKp=0, speedPidKi=0, positionPidKp=0, positionPidKi=0):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0x31)
    frame.append(0x00)
    frame.append(currentPidKp)
    frame.append(currentPidKi)
    frame.append(speedPidKp)
    frame.append(speedPidKi)
    frame.append(positionPidKp)
    frame.append(positionPidKi)
    # EOF
    frame.append(0x55)
    return bytes(frame)


# 4 Read Acceleration Command
def read_acceleration(motor_id, functionIndex=0):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0x42)
    frame.append(functionIndex)
    # Data packets
    [frame.append(0x00) for i in range(6)]
    # EOF
    frame.append(0x55)
    return bytes(frame)


# 6 Read Encoder Command
def read_encoder(motor_id=1):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0x60)
    # Data packets
    [frame.append(0x00) for i in range(7)]
    # EOF
    frame.append(0x55)
    return bytes(frame)


# 8 Read Multi-turn Encoder Zero Offset Data Command
def read_encoder_zero_offset_data(motor_id):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0x62)
    # Data packets
    [frame.append(0x00) for i in range(7)]
    # EOF
    frame.append(0x55)
    return bytes(frame)


# 10 Write Encoder Value to ROM as Zero Command
def write_encoder_value_to_rom_as_zero(motor_id=1):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0x64)
    # Data packets
    [frame.append(0x00) for i in range(7)]
    # EOF
    frame.append(0x55)
    return bytes(frame)


# 12 Read Multi-turn Angle Command
def read_multi_turn_angle(motor_id=1):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0x92)
    # Data packets
    [frame.append(0x00) for i in range(7)]
    # EOF
    frame.append(0x55)
    return bytes(frame)


# 14 Read Motor Stats and Error Flag Command
def read_motor_stats_one_and_error_flag(motor_id=1):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0x9A)
    # Data packets
    [frame.append(0x00) for i in range(7)]
    # EOF
    frame.append(0x55)
    return bytes(frame)


# 16 Read Motor Status 3 Command
def read_motor_stats_three(motor_id=1):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0x9D)
    # Data packets
    [frame.append(0x00) for i in range(7)]
    # EOF
    frame.append(0x55)
    return bytes(frame)

# 18 Motor Stop Command
def motor_stop(motor_id=1):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0x81)
    # Data packets
    [frame.append(0x00) for i in range(7)]
    # EOF
    frame.append(0x55)
    return bytes(frame)

# 2.20 Speed Closed-loop Control Command
def motor_speed_control(motor_id=1, speed=0):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0xa2)
    # Data packets
    frame.append(0x00)
    frame.append(0x00)
    frame.append(0x00)
    [frame.append(x) for x in speed.to_bytes(4, 'little', signed=False)]
    # EOF
    frame.append(0x55)
    return bytes(frame)


# 2.22 Single Turn Position Control Command
def single_turn_position_control(motor_id=1, angleAbsolute=0, direction=0x01, speedControl=0):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0xa6)
    # Data packets
    frame.append(direction)
    [frame.append(x) for x in speedControl.to_bytes(2, 'little', signed=True)]
    [frame.append(x) for x in angleAbsolute.to_bytes(2, 'little', signed=True)]
    [frame.append(0x00) for i in range(2)]
    # EOF
    frame.append(0x55)
    return bytes(frame)


# 2.26 System Reset Command
def sys_reset_command(motor_id=1):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0x76)
    # Data packets
    [frame.append(0x00) for i in range(7)]
    # EOF
    frame.append(0x55)
    return bytes(frame)


# 2.28 System Brake Lock Command
def sys_brake_lock(motor_id=1):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0x78)
    # Data packets
    [frame.append(0x00) for i in range(7)]
    # EOF
    frame.append(0x55)
    return bytes(frame)


# 2.30 System Software Version Date Read
def sys_software_date(motor_id=1):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0xB2)
    # Data packets
    [frame.append(0x00) for i in range(7)]
    # EOF
    frame.append(0x55)
    return bytes(frame)


# 2.32 Communication Baud Rate Setting
def com_baud_setting(motor_id=1, baudrate=0):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0xB4)
    # Data packets
    [frame.append(0x00) for i in range(6)]
    frame.append(baudrate)
    # EOF
    frame.append(0x55)
    return bytes(frame)


# 2.34 Active Reply Function Command
def active_reply(motor_id=1, command=0, reply=1, interval_time=0):
    frame = bytearray()
    # Header
    frame.append(0xaa)
    frame.append(0xc8)
    # ID
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    # Command name
    frame.append(0xB6)
    frame.append(command)
    frame.append(reply)
    [frame.append(x) for x in interval_time.to_bytes(2, 'little', signed=False)]
    frame.append(0x00)
    frame.append(0x00)
    frame.append(0x00)
    # EOF
    frame.append(0x55)
    return bytes(frame)
