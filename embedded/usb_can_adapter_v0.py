import time
import random
import serial
import argparse
import signal
import sys

import traceback
from typing import Dict, Union


class UsbCanAdapter:
    # Constants
    CANUSB_INJECT_SLEEP_GAP_DEFAULT = 200  # ms
    CANUSB_TTY_BAUD_RATE_DEFAULT = 2000000
    DATA_START_INDEX = 6
    FRAME_ID_SLICE = slice(2, 6)
    PGN_SLICE = slice(3, 5)


    # Enumerations
    CANUSB_SPEED = {
        'CANUSB_SPEED_1000000': 0x01,
        'CANUSB_SPEED_800000': 0x02,
        'CANUSB_SPEED_500000': 0x03,
        'CANUSB_SPEED_400000': 0x04,
        'CANUSB_SPEED_250000': 0x05,
        'CANUSB_SPEED_200000': 0x06,
        'CANUSB_SPEED_125000': 0x07,
        'CANUSB_SPEED_100000': 0x08,
        'CANUSB_SPEED_50000': 0x09,
        'CANUSB_SPEED_20000': 0x0a,
        'CANUSB_SPEED_10000': 0x0b,
        'CANUSB_SPEED_5000': 0x0c
    }

    CANUSB_MODE = {
        'NORMAL': 0x00,
        'LOOPBACK': 0x01,
        'SILENT': 0x02,
        'LOOPBACK_SILENT': 0x03
    }

    CANUSB_FRAME = {
        'STANDARD': 0x01,
        'EXTENDED': 0x02
    }

    CANUSB_PAYLOAD_MODE = {
        'CANUSB_INJECT_PAYLOAD_MODE_RANDOM': 0,
        'CANUSB_INJECT_PAYLOAD_MODE_INCREMENTAL': 1,
        'CANUSB_INJECT_PAYLOAD_MODE_FIXED': 2
    }

    def __init__(self):
        self.device_port = None
        self.speed = None
        self.baudrate = self.CANUSB_TTY_BAUD_RATE_DEFAULT
        self.terminate_after = 0
        self.program_running = True
        self.inject_payload_mode = self.CANUSB_PAYLOAD_MODE['CANUSB_INJECT_PAYLOAD_MODE_FIXED']
        self.inject_sleep_gap = self.CANUSB_INJECT_SLEEP_GAP_DEFAULT
        self.print_traffic = False
        self.frame = bytearray()
        self.serial_device = None
        self.data_dict = {}



    @staticmethod
    def canusb_int_to_speed(speed):
        speed_dict = {
            1000000: UsbCanAdapter.CANUSB_SPEED['CANUSB_SPEED_1000000'],
            800000: UsbCanAdapter.CANUSB_SPEED['CANUSB_SPEED_800000'],
            500000: UsbCanAdapter.CANUSB_SPEED['CANUSB_SPEED_500000'],
            400000: UsbCanAdapter.CANUSB_SPEED['CANUSB_SPEED_400000'],
            250000: UsbCanAdapter.CANUSB_SPEED['CANUSB_SPEED_250000'],
            200000: UsbCanAdapter.CANUSB_SPEED['CANUSB_SPEED_200000'],
            125000: UsbCanAdapter.CANUSB_SPEED['CANUSB_SPEED_125000'],
            100000: UsbCanAdapter.CANUSB_SPEED['CANUSB_SPEED_100000'],
            50000: UsbCanAdapter.CANUSB_SPEED['CANUSB_SPEED_50000'],
            20000: UsbCanAdapter.CANUSB_SPEED['CANUSB_SPEED_20000'],
            10000: UsbCanAdapter.CANUSB_SPEED['CANUSB_SPEED_10000'],
            5000: UsbCanAdapter.CANUSB_SPEED['CANUSB_SPEED_5000']
        }
        return speed_dict.get(speed, 0)

    @staticmethod
    def generate_checksum(data):
        checksum = sum(data)
        return checksum & 0xff

    def frame_send(self, frame):
        if not self.serial_device.is_open:
            print("Error: Serial port is not open.")
            return -1

        frame_len = len(frame)

        if self.print_traffic:
            print(">>> ", end="")
            print(" ".join(f"{byte:02x}" for byte in frame), end="")
            if isinstance(self.print_traffic, int) and self.print_traffic > 1:
                print("    '", end="")
                print("".join(chr(byte) if chr(byte).isalnum() else '.' for byte in frame[4:frame_len-1]), end="")
                print("'", end="")
            print()

        try:
            result = self.serial_device.write(bytes(frame))
        except serial.SerialException as e:
            print(f"write() failed: {e}")
            return -1

        return frame_len


    def frame_recv(self, frame_len_max = 20):

        if not self.serial_device.is_open:
            print("Error: Serial port is not open.")
            return -1

        self.frame = bytearray()
        frame_len = 0
        started = False

        if self.print_traffic:
            print("<<< ", end="")

        while self.program_running and frame_len < frame_len_max:
            try:
                byte = self.serial_device.read(1)
            except serial.SerialException as e:
                print(f"Error reading from serial port: {e}")
                return -1

            if self.print_traffic:
                print(f"{byte[0]:02x} ", end="")

            if byte[0] == 0x55 and started:
                self.frame.append(byte[0])
                frame_len += 1
                break

            if byte[0] == 0xaa:
                started = True

            if started:
                self.frame.append(byte[0])
                frame_len += 1

            if frame_len >= 32:
                break

        if self.print_traffic:
            print('')
        return frame_len

    def command_settings(self, speed = None, mode = CANUSB_MODE["NORMAL"], frame= CANUSB_FRAME["STANDARD"]):
        if speed != None:
            self.speed = speed
        self.frame = frame

        cmd_frame = bytearray()

        cmd_frame.append(0xaa)
        cmd_frame.append(0x55)
        cmd_frame.append(0x12)
        cmd_frame.append(self.speed)
        cmd_frame.append(self.frame)
        cmd_frame.extend([0] * 8)  # Fill with zeros for Filter ID and Mask ID (not handled)
        cmd_frame.append(mode)
        cmd_frame.extend([0x01, 0, 0, 0, 0])
        cmd_frame.append(self.generate_checksum(cmd_frame[2:19]))

        if self.frame_send(cmd_frame) < 0:
            return -1

        return 0

    def extract_data(self, frame: bytearray) -> Dict[str, Union[bytearray, str]]:
        """
        Extracts the frame ID, PGN, node, and data bytes from a CAN frame.

        Args:
            frame (bytearray): A bytearray containing the CAN frame data.

        Returns:
            dict: A dictionary containing the following keys:
                * frame_id: The frame ID (4 bytes) as a string.
                * pgn: The parameter group number (2 bytes) as a string.
                * node: The node ID (1 byte) as a string.
                * data: A bytearray containing the data bytes.
        """
        try:
            frame_id_bytes = frame[self.FRAME_ID_SLICE][::-1]
            pgn_bytes = frame[self.PGN_SLICE][::-1]
            node_byte = frame[2]

            frame_id = frame_id_bytes.hex()
            pgn = pgn_bytes.hex()
            node = f"{node_byte:02x}"

            # Use slicing to extract data bytes and reverse the order of every adjacent pair of bytes
            data_bytes = bytearray()
            for i in range(self.DATA_START_INDEX, len(frame), 2):
                data_bytes.extend(frame[i+1:i-1:-1])

        except IndexError as e:
            error_message = (f"Error in CAN data frame\nException: {e}\nTraceback:\n{traceback.format_exc()}")
            print(error_message)

        return {"frame_id": frame_id, "pgn": pgn, "node": node, "data": data_bytes}


    def dump_data_frames(self, print_flag):
        while self.program_running:
            frame_len = self.frame_recv(20)

            if not self.program_running:
                break

            if frame_len == -1:
                print("Frame receive error!")
            else:
                self.data_dict = self.extract_data(self.frame)

            if print_flag:
                try:
                    print(f"{self.data_dict}")
                except KeyError:
                    pass
        return 0



    def adapter_init(self, device_port=None, baudrate=None):
        if device_port != None:
            self.device_port = device_port
        if baudrate != None:
            self.baudrate = baudrate
        try:
            self.serial_device = serial.Serial(self.device_port, baudrate=self.baudrate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, timeout=None)
            return self.serial_device
        except serial.SerialException as e:
            print("Error opening serial port {}: {}".format(device_port, e))
            return None

    def adapter_close(self):
        """Closes the serial port.

        Args:
            ser: A serial port object.
        """
        try:
            if self.serial_device is not None and hasattr(self.serial_device, 'close'):
                self.serial_device.close()
        except serial.SerialException as e:
            print("Error closing serial port".format(e))
            return None

    @staticmethod
    def hex_value(c):
        if '0' <= c <= '9':
            return ord(c) - ord('0')
        elif 'A' <= c <= 'F':
            return ord(c) - ord('A') + 10
        elif 'a' <= c <= 'f':
            return ord(c) - ord('a') + 10
        else:
            return -1


    def convert_from_hex(self, hex_string):
        bin_string = bytearray()
        high = None

        for c in hex_string:
            value = self.hex_value(c)
            if value >= 0:
                if high is None:
                    high = value
                else:
                    bin_string.append(high * 16 + value)
                    high = None

        if len(bin_string) > len(hex_string) // 2:
            print(f"hex string truncated to {len(bin_string)} bytes")

        return bin_string

    def inject_data_frame(self, hex_id, hex_data):
        binary_data = bytearray(8)
        binary_id_lsb = 0
        binary_id_msb = 0
        gap_ts = self.inject_sleep_gap / 1000  # Convert milliseconds to seconds for Python's sleep()

        # Seed random with current time
        random.seed(time.time())

        data_len = len(self.convert_from_hex(hex_data))
        if data_len == 0:
            print("Unable to convert data from hex to binary!")
            return -1

        if len(hex_id) == 1:
            binary_id_lsb = self.hex_value(hex_id[0])
        elif len(hex_id) == 2:
            binary_id_lsb = (self.hex_value(hex_id[0]) * 16) + self.hex_value(hex_id[1])
        elif len(hex_id) == 3:
            binary_id_msb = self.hex_value(hex_id[0])
            binary_id_lsb = (self.hex_value(hex_id[1]) * 16) + self.hex_value(hex_id[2])
        else:
            print("Unable to convert ID from hex to binary!")
            return -1

        error = 0
        # program_running = 1
        while self.program_running and not error:
            if gap_ts:
                time.sleep(gap_ts)

            if self.terminate_after:
                self.terminate_after -= 1
                if self.terminate_after == 0:
                    self.program_running = 0

            if self.inject_payload_mode == UsbCanAdapter.CANUSB_PAYLOAD_MODE['CANUSB_INJECT_PAYLOAD_MODE_RANDOM']:
                for i in range(data_len):
                    binary_data[i] = random.randint(0, 255)
            elif self.inject_payload_mode == UsbCanAdapter.CANUSB_PAYLOAD_MODE['CANUSB_INJECT_PAYLOAD_MODE_INCREMENTAL']:
                for i in range(data_len):
                    binary_data[i] += 1
                    binary_data[i] %= 256  # Ensure value stays within byte range

        return error

    @staticmethod
    def display_help():
        print(f"Usage: {sys.argv[0]} <options>")
        print("Options:")
        print("  -h          Display this help and exit.")
        print("  -t          Print TTY/serial traffic debugging info.")
        print(f"  -d DEVICE   Use TTY DEVICE.")
        print("  -s SPEED    Set CAN SPEED in bps.")
        print(f"  -b BAUDRATE Set TTY/serial BAUDRATE (default: {UsbCanAdapter.CANUSB_TTY_BAUD_RATE_DEFAULT}).")
        print("  -i ID       Inject using ID (specified as hex string).")
        print("  -j DATA     CAN DATA to inject (specified as hex string).")
        print(f"  -n COUNT    Terminate after COUNT frames (default: infinite).")
        print(f"  -g MS       Inject sleep gap in MS milliseconds (default: {UsbCanAdapter.CANUSB_INJECT_SLEEP_GAP_DEFAULT} ms).")
        print(f"  -m MODE     Inject payload MODE ({UsbCanAdapter.CANUSB_PAYLOAD_MODE['CANUSB_INJECT_PAYLOAD_MODE_RANDOM']} = random, {UsbCanAdapter.CANUSB_PAYLOAD_MODE['CANUSB_INJECT_PAYLOAD_MODE_INCREMENTAL']} = incremental, {UsbCanAdapter.CANUSB_PAYLOAD_MODE['CANUSB_INJECT_PAYLOAD_MODE_FIXED']} = fixed).")
        print()

    def sigterm(self, signo, frame):
        self.program_running = 0

    def main(self):

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("-h", "--help", action="store_true")
        parser.add_argument("-t", action="store_true")
        parser.add_argument("-d")
        parser.add_argument("-s", type=int)
        parser.add_argument("-b", type=int, default=self.CANUSB_TTY_BAUD_RATE_DEFAULT)
        parser.add_argument("-i")
        parser.add_argument("-j")
        parser.add_argument("-n", type=int)
        parser.add_argument("-g", type=float)
        parser.add_argument("-m", type=int)
        args = parser.parse_args()

        if args.help:
            self.display_help()
            sys.exit(0)

        if args.t:
            self.print_traffic = True

        tty_device = args.d
        speed = self.canusb_int_to_speed(args.s) if args.s else 0
        baudrate = args.b
        inject_id = args.i
        inject_data = args.j

        if args.n:
            terminate_after = args.n

        if args.g:
            inject_sleep_gap = args.g

        if args.m:
            inject_payload_mode = args.m

        signal.signal(signal.SIGTERM, self.sigterm)
        #signal.signal(signal.SIGHUP, self.sigterm)
        signal.signal(signal.SIGINT, self.sigterm)

        if not tty_device:
            print("Please specify a TTY!")
            self.display_help()
            sys.exit(1)

        if speed == 0:
            print("Please specify a valid speed!")
            self.display_help()
            sys.exit(1)

        self.adapter_init(tty_device, baudrate)
        if self.serial_device is None:
            sys.exit(1)

        self.command_settings(speed, self.CANUSB_MODE["NORMAL"], self.CANUSB_FRAME["STANDARD"])

        if inject_data is None:
            # Dumping mode (default).
            self.dump_data_frames(print_flag =True)
        else:
            # Inject mode.
            if inject_id is None:
                print("Please specify a ID for injection!")
                self.display_help()
                sys.exit(1)
            if self.inject_data_frame(inject_id, inject_data) == -1:
                sys.exit(1)
            else:
                sys.exit(0)

        sys.exit(0)

    def set_can_baudrate(self, baudrate):
        self.speed = self.canusb_int_to_speed(baudrate)

    def set_port(self, port):
        self.device_port = port


if __name__ == "__main__":
    uca = UsbCanAdapter()
    uca.main()



