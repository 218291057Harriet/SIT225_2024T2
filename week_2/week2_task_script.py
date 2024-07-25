"""
    Harriet Rawson
    s218291057
"""

import serial
import random
import csv
from datetime import datetime

# Baud rate set at same as Arduino sketch.
baud_rate = 9600

# Serial port set
s = serial.Serial('COM3', baud_rate, timeout=60)

# Create CSV
csv_file = open('week2.csv', 'w', newline = '')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Timestamp', 'Humidity', 'Temperature'])

# Data collection
print(f"Data collection started. Writing to {csv_file}") # Just for debugging, so I can ensure that the CSV has been created
try:
    while True:  # Infinite loop to keep running
            
        data = s.readline().decode('utf-8').strip()
        hum, temp = data.split(',') # Split variables with a comma.
        # Write to CSV        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        csv_writer.writerow([timestamp, hum, temp])
        csv_file.flush()  
except KeyboardInterrupt: # Escape route
    pass                

s.close()
csv_file.close()