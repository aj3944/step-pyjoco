import argparse
import signal
import sys
import threading
import time

from commands import motor_off, motor_on, speed_closed_loop
from motor import device

stop_event = threading.Event()


def request_stop(signum=None, frame=None):
    """
    Signal handler that flips the stop flag so the main loop can exit cleanly.
    """
    if not stop_event.is_set():
        print("\nStop requested, shutting motor down...")
        stop_event.set()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Spin a motor at a constant speed until interrupted."
    )
    parser.add_argument(
        "--port",
        default="/dev/tty.usbserial-120",
        help="Serial port connected to the CAN-USB adapter.",
    )
    parser.add_argument(
        "--motor-id",
        type=int,
        default=1,
        help="CAN motor ID to control.",
    )
    parser.add_argument(
        "--speed-dps",
        type=float,
        default=1080.0,
        help="Desired constant speed in degrees per second.",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=0.1,
        help="Loop sleep interval while monitoring for stop requests (seconds).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)

    serial_adapter = device(args.port)
    serial_port = serial_adapter.port()

    def cleanup():
        try:
            serial_port.write(speed_closed_loop(args.motor_id, 0))
        except Exception as exc:
            print(f"Warning: could not send stop command: {exc}", file=sys.stderr)
        try:
            serial_port.write(motor_off(args.motor_id))
        except Exception as exc:
            print(f"Warning: failed to disarm motor: {exc}", file=sys.stderr)
        try:
            serial_port.close()
        except Exception as exc:
            print(f"Warning: failed to close serial port: {exc}", file=sys.stderr)

    try:
        serial_port.write(motor_off(args.motor_id))
        time.sleep(0.2)
        serial_port.write(motor_on(args.motor_id))
        time.sleep(0.2)

        speed_command = int(args.speed_dps * 100)  # convert to 0.01 dps units
        serial_port.write(speed_closed_loop(args.motor_id, speed_command))
        print(
            f"Motor {args.motor_id} running at {args.speed_dps} dps. "
            "Press Ctrl+C to stop."
        )

        while not stop_event.is_set():
            time.sleep(args.poll_interval)
    except KeyboardInterrupt:
        request_stop()
    finally:
        cleanup()
        print("Motor stopped and serial port closed.")


if __name__ == "__main__":
    main()