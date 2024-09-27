from usb_can_adapter_v1 import UsbCanAdapter
# from imu_f99xB20 import IMUIf99xB20nterpreter
from can import Message
import can 
import can.interfaces.serial.serial_can
# bus = 

if __name__ == "__main__":
    uca = UsbCanAdapter()
    # # imu = IMUIf99xB20nterpreter()


    uca.set_port("/dev/ttyUSB0")
    uca.adapter_init()
    uca.command_settings(speed=1000000)

    # id_ = 0x143;


    # # frame.append(0xFF)
    # # frame.append(0x43)
    # frame.append(0x88)
    # frame.append(0x00)
    # frame.append(0x00)
    # frame.append(0x00)
    # frame.append(0x00)
    # frame.append(0x00)
    # frame.append(0x00)
    # frame.append(0x00)

    # data = [0x80,0,0,0,0,0,0,0]
    # test = Message(is_extended_id=True, arbitration_id=id_,data = data)
    # data2 = ['8','0'] + ['0']*14
    # print(test)
    # print((can.interfaces.BACKENDS['serial']))
    # with can.interfaces.serial.serial_can.SerialBus('/dev/ttyUSB0', baudrate=1000000, timeout=0.25) as  bus:
    #     for msg in bus:
    #         print(msg.data)
        # for i in range(10):
        #     test = Message(is_extended_id=False, arbitration_id=id_,data = data)
        #     try:
        #         bus.send(test)
        #         print(f"Message sent on {bus.channel_info}")
        #     except can.CanError:
        #         print("Message NOT sent")        
    # print(test)
    # frame_byte = bytearray.fromhex("aa c8 43 01 a1 00 00 00 07 f0 00 00 55")
    # frame_byte = bytearray.fromhex("aa c8 43 01 88 00 00 00 00 00 00 00 55") # motor start
    # frame_byte = bytearray.fromhex("aa c8 43 01 80 00 00 00 00 00 00 00 55") # motor stop
    # frame_byte = bytearray.fromhex("aa c8 43 01 a1 00 00 00 e8 03 00 00 55") # torque control move
    # frame_byte = bytearray.fromhex("aa c8 43 01 a2 00 00 00 e8 03 00 00 55") # speed control move
    frame_byte = bytearray.fromhex("aa c8 43 01 a5 00 00 00 00 cc 00 00 55") # position control move
    frame = bytearray()
    frame.append(0xaa)
    frame.append(0xc8)
    frame.append(0x43)
    frame.append(0x01)
    frame.append(0xa5)
    frame.append(0x00)
    frame.append(0x00)
    frame.append(0x00)
    frame.append(0x00)
    frame.append(0xaa)
    frame.append(0x00)
    frame.append(0x00)
    frame.append(0x55)

    uca.serial_device.write(bytes(frame))
    # uca.frame_send(frame)
    # while 1:
    # started = True;
    # while started:
    #     byte = uca.serial_device.read(1)
    #     print(byte.hex())
    #     # print(byte.hex() == '55')
    #     if byte.hex() == '55':
    #         started = False
    #         print()
    # uca.dump_data_frames(0)
    # uca.frame_send(test)
    # print(uca.convert_from_hex(data2))
    # print(dir(test))
    # print(test.channel)
    # print(test.data)
    # uca.frame_send(test)
    # while True:
    #     frame_len = uca.frame_receive()
    #     print(frame_len)
    #     if frame_len == -1:
    #         print("Frame receive error!")
    #         break
    #     else:
    #         frame = uca.extract_data(uca.frame)
    #         print(frame)
            # data = imu.interpret_frame(uca.extract_data(uca.frame))

    #     # try:
    #     #     roll, pitch, yaw = data["Roll"], data["Pitch"], data["Yaw"]
    #     #     print(f"Roll: {roll} Pitch: {pitch} Yaw: {yaw}")
    #     # except KeyError as e:
    #     #     pass # Sometimes the frame does not have data