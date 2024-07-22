"""
    Harriet Rawson
    s218291057
"""

import serial
import random
import time
from datetime import datetime

baud_rate = 9600

s = serial.Serial('COM3', baud_rate, timeout=None)

while True:  # infinite loop, keep running

    #  Send random number between 1 and 10.
    data_send = random.randint(1, 10)

    # Write to serial port, set data encoding. 
    d = s.write(bytes(str(data_send), 'utf-8'))
    print(f"{datetime.now()}: Send >>> {data_send} ({d} bytes)")

    s.flush()

    # Read from serial port. 
    d = s.readline().decode("utf-8").strip()
    print(f"{datetime.now()}: Recv <<< {d}")

    # Sleep for time received, print date and time.
    try:
        sleepy_time = int(float(d))
        print(f"{datetime.now()}: Sleeping for {sleepy_time} seconds")
        time.sleep(sleepy_time)
        print(f"{datetime.now()}: Awake now!")
    except ValueError:
        # Retry if the integer d is invalid
        print(f"{datetime.now()}: Error: Invalid integer '{d}' received from Arduino. Naughty Arduino")

