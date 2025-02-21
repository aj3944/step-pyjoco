def read_multi_turn_encoder_original_position(motor_id=1):
    """7. Read multi-turn encoder original position data command (0x61)"""
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x61)
    [frame.append(0x00) for i in range(7)]
    frame.append(0x55)
    return bytes(frame)

def write_encoder_zero_to_rom(motor_id=1, offset=0x0000):
    """9. Write encoder multi-turn value to ROM as motor zero command (0x63)"""
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x63)
    [frame.append(0x00) for i in range(3)]
    [frame.append(x) for x in offset.to_bytes(4, 'little', signed=True)]
    frame.append(0x55)
    return bytes(frame)

def read_single_turn_encoder(motor_id=1):
    """11. Read single-turn encoder command (0x90)"""
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x90)
    [frame.append(0x00) for _ in range(7)]
    frame.append(0x55)
    return bytes(frame)

def read_single_turn_angle(motor_id=1):
    """13. Read single-turn angle command (0x94)"""
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x94)
    [frame.append(0x00) for _ in range(7)]
    frame.append(0x55)
    return bytes(frame)

def read_motor_status_2(motor_id=1):
    """15. Read Motor Status 2 Command (0x9C)"""
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x9C)
    [frame.append(0x00) for _ in range(7)]
    frame.append(0x55)
    return bytes(frame)

def motor_shutdown(motor_id=1):
    """17. Motor shutdown command (0x80)"""
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x80)
    [frame.append(0x00) for _ in range(7)]
    frame.append(0x55)
    return bytes(frame)

def torque_closed_loop_control(motor_id=1, torque=0x03):
    """19. Torque closed-loop control command (0xA1)"""
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0xa1)
    [frame.append(0x00) for _ in range(3)]
    [frame.append(x) for x in torque.to_bytes(2, 'little', signed=True)]
    [frame.append(0x00) for _ in range(2)]

    frame.append(0x55)
    return bytes(frame)

def absolute_position_closed_loop_control(motor_id=1, angleControl=0x00000000, maxSpeed=0x0000):
    """21. Absolute position closed-loop control command (0xA4)"""
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0xa4)
    frame.append(0x00)
    [frame.append(x) for x in maxSpeed.to_bytes(2,'little', signed=True)]
    [frame.append(x) for x in angleControl.to_bytes(4, 'little', signed=True)]
    frame.append(0x55)
    return bytes(frame)

def incremental_position_closed_loop_control(motor_id=1, maxSpeed=0x0000, angleControl=0x00000000):
    """23. Incremental position closed-loop control command (0xA8)"""
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0xa8)
    frame.append(0x00)
    [frame.append(x) for x in maxSpeed.to_bytes(2,'little', signed=True)]
    [frame.append(x) for x in angleControl.to_bytes(4, 'little', signed=True)]
    [frame.append(0x00) for _ in range(5)]
    frame.append(0x55)
    return bytes(frame)

def motor_power_acquisition(motor_id=1):
    """25. Motor power acquisition (0x71)"""
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0x71)
    [frame.append(0x00) for _ in range(7)]
    frame.append(0x55)
    return bytes(frame)

def system_runtime_read(motor_id=1):
    """29. System runtime read command (0xB1)"""
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x40 + motor_id)
    frame.append(0x01)
    frame.append(0xB1)
    [frame.append(0x00) for _ in range(7)]
    frame.append(0x55)
    return bytes(frame)