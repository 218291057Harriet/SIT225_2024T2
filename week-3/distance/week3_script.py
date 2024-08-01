"""
    Requirement: arduino_iot_cloud
    Install: pip install arduino-iot-cloud

    @Ahsan Habib
    School of IT, Deakin University, Australia.
"""

import sys
import traceback
import random
from arduino_iot_cloud import ArduinoCloudClient
import asyncio
from datetime import datetime


DEVICE_ID = "adf79794-391f-454d-9ef3-c5f785a9962e"
SECRET_KEY = "BL1QmOyuJxJJ7E0ZU3emP8PJq"

# Create CSV
csv_file = open('demo.csv', mode='a', newline = '')
csv_file.write("Time, Distance\n")


# Callback function on distance change event.
#
def on_distance_changed(client, value):
    print(f"New distance: {value}")

    timestamp = datetime.now().isoformat()
    csv_string = (timestamp) + ", " + str(value) + "\n"
    csv_file.write(csv_string)
    csv_file.flush()


def main():
    print("main() function")

    # Instantiate Arduino cloud client
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
    )

    # Register with 'distance' cloud variable
    # and listen on its value changes in 'on_distance_changed'
    # callback function.
    client.register(
        "distance", value=None, 
        on_write=on_distance_changed)

    # start cloud client
    client.start()


if __name__ == "__main__":
    try:
        main()  # main function which runs in an internal infinite loop
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)
    finally:
        # Close the CSV file
        csv_file.close()