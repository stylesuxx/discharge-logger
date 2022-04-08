"""
Log load output in CSV format.

Connect to a given serial port and log the output of the load in CSV format.
"""

import sys
import datetime
import serial
import signal

if(len(sys.argv) < 2):
    print("Usage: %s SERIAL_PORT" % sys.argv[0])
    sys.exit()

port = sys.argv[1]
baudrate = 115200
running = True
ser = serial.Serial(port, baudrate)


def signal_handler(sig, frame):
    """Shut down cleanly."""
    global running
    global ser

    ser.close()
    running = False


signal.signal(signal.SIGINT, signal_handler)

if not ser.isOpen():
    ser.open()

index = 0
hexArray = []
while running:
    try:
        byte = ser.read()
        hex = byte.hex()
        hexArray.append(hex)

        if len(hexArray) >= 3:
            if(hexArray[2] == '01'):
                now = datetime.datetime.now().isoformat()
                print("%s, %s.%s" % (now, hexArray[0], hexArray[1]))
                hexArray = hexArray[3:]
            else:
                """
                Remove first item since the bytes are not yet aligned
                correctly
                """
                hexArray.pop()

    except serial.serialutil.SerialException:
        """Read has been aborted."""
        pass

sys.exit()
