from cassandra.cluster import Cluster
import pandas as pd
import folium
from dash import Dash, html
from dash.dependencies import Input, Output

# Connect to Cassandra
# cluster = Cluster(['cassandra'])
cluster = Cluster(['192.168.1.111'],9042)
session = cluster.connect('my_keyspace')

# Fetch data from Cassandra
rows = session.execute('SELECT * FROM iss_data')
data = pd.DataFrame(list(rows))

# Create a map centered at a specific location
map = folium.Map(location=[0, 0], zoom_start=2)

# Add markers for each data point
# for _, row in data.iterrows():
#     folium.Marker([float(row['latitude']), float(row['longitude'])]).add_to(map)

for _, row in data.iterrows():
    folium.CircleMarker(
        location=[float(row['latitude']), float(row['longitude'])],
        radius=2, 
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(map)

# Save the map to an HTML file
map.save('map.html')

# Create a Dash application
app = Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1('ISS Location Dashboard'),
    html.Iframe(id='map', srcDoc=open('map.html', 'r').read(), width='100%', height='600')
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)