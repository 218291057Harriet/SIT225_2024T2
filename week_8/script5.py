from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from arduino_iot_cloud import ArduinoCloudClient
import sys
import traceback


DEVICE_ID = "3b8a947c-d0fb-4de2-b01b-8ce95296752a"
SECRET_KEY = "JnGB7wh#Xc6QhxglNetvDPOBA"

# Create CSV
csv_file = open('GyrData.csv', mode='a', newline='')
csv_file.write("Time, X, Y, Z\n")
df = pd.read_csv('GyrData.csv')

data_list = []
kept_data_list = []
data_set = {'py_x': None, 'py_y': None, 'py_z': None}

app = Dash()

app.layout = html.Div([
    html.H1('Accelerometer Data'),
    dcc.Graph(id='updating-graph'),
    dcc.Interval(
        id='interval',
        interval=5000,  
        n_intervals=0
    )
])

@app.callback(
    Output('updating-graph', 'figure'),
    [Input('interval', 'n_intervals')]
)
def update_graph(n_intervals):
    try:
        df = pd.read_csv(csv_file)
        if df.empty:
            return go.Figure()  # Return an empty figure if no data
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Time'], y=df['X'], mode='lines', name='X', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=df['Time'], y=df['Y'], mode='lines', name='Y', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=df['Time'], y=df['Z'], mode='lines', name='Z', line=dict(color='blue')))
        fig.update_layout(title='Accelerometer Data', xaxis_title='Time', yaxis_title='Value')
        return fig
    except Exception as e:
        print(f"Error updating graph: {e}")
        return go.Figure()  # Return an empty figure if there's an error


def write_full_set():
    global data_list, kept_data_list
    if all(value is not None for value in data_set.values()):
        timestamp = datetime.now().isoformat()
        csv_string = f"{timestamp}, {data_set['py_x']}, {data_set['py_y']}, {data_set['py_z']}\n"
        csv_file.write(csv_string)
        csv_file.flush()
        print(f"Data written to CSV: {csv_string}")
        data_list.append({'timestamp': timestamp, 'X': data_set['py_x'], 'Y': data_set['py_y'], 'Z': data_set['py_z']})
        data_set['py_x'] = None
        data_set['py_y'] = None
        data_set['py_z'] = None
        print(f"Data stored: {data_list[-1]}")
        
        if len(data_list) >= 1000:
            kept_data_list.extend(data_list) 
            data_list.clear()  
            print(f"List Restarted")

def on_accelerometer_X_changed(client, value):
    data_set['py_x'] = value
    write_full_set()

def on_accelerometer_Y_changed(client, value):
    data_set['py_y'] = value
    write_full_set()

def on_accelerometer_Z_changed(client, value):
    data_set['py_z'] = value
    write_full_set()

def main():
    print("main() function")
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
    )
    client.register("py_x", value=None, on_write=on_accelerometer_X_changed)
    client.register("py_y", value=None, on_write=on_accelerometer_Y_changed)
    client.register("py_z", value=None, on_write=on_accelerometer_Z_changed)
    client.start()

if __name__ == "__main__":
    try:
        main()
        app.run_server(debug=True, jupyter_mode="tab")
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)
