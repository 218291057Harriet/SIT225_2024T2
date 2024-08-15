import firebase_admin
from firebase_admin import credentials, db
import csv

# Firebase setup
databaseURL = 'https://sit225-week-5-45da4-default-rtdb.firebaseio.com/'
cred_obj = credentials.Certificate('H:/HUni/SIT225/week5/sit225-week-5-45da4-firebase-adminsdk-osv5d-29868a29b4.json')

# Initialize Firebase app if it hasn't been initialized yet. I needed help with this because I ran out of time to keep getting ERRORS.
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred_obj, {
        'databaseURL': databaseURL
    })

#Query Firebase
ref = db.reference('/')
data = ref.get()

csv_file = 'gyroscope1.csv'

with open(csv_file, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Timestamp', 'X', 'Y', 'Z'])
    
    #I needed help with this bit too, I couldn't work out how to define a (for each ... print a row).
    for sensor_key, sensor_data in data.items():

        timestamp = sensor_data.get('timestamp', 'N/A')
        x = sensor_data.get('x', 'N/A')
        y = sensor_data.get('y', 'N/A')
        z = sensor_data.get('z', 'N/A')
        csv_writer.writerow([timestamp, x, y, z])


