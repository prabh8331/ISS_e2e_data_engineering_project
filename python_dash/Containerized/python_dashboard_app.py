from cassandra.cluster import Cluster
import pandas as pd
import folium
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
from dash.exceptions import PreventUpdate


# Connect to Cassandra
cluster = Cluster(['192.168.1.111'], 9042)
# cluster = Cluster(['cassandra'])
session = cluster.connect('my_keyspace')

# Function to fetch data from Cassandra based on date filter
def fetch_data(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    query = f"SELECT * FROM iss_data WHERE timestamp >= '{start_date}' AND timestamp < '{end_date}' ALLOW FILTERING"
    rows = session.execute(query)
    return pd.DataFrame(list(rows))

# Create a Dash application
app = Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1('ISS Location Dashboard'),
    html.Div([
        html.Label('Select Date Range:'),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date='2024-03-28',
            end_date='2024-03-28',
            display_format='YYYY-MM-DD'
        ),
        html.Button('Apply Filter', id='apply-filter-btn'),
    ]),
    html.Iframe(id='map', srcDoc='', width='100%', height='600')
])

# Callback to update the map based on date filter
@app.callback(
    Output('map', 'srcDoc'),
    Input('apply-filter-btn', 'n_clicks'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_map(n_clicks, start_date, end_date):
    if n_clicks is None:
        raise PreventUpdate
    data = fetch_data(start_date, end_date)
    map = folium.Map(location=[0, 0], zoom_start=2)
    for _, row in data.iterrows():
        folium.CircleMarker(
            location=[float(row['latitude']), float(row['longitude'])],
            radius=2, 
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(map)
    return map._repr_html_()

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8051, debug=True)
