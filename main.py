import networkx as nx
import matplotlib.pyplot as plt
import folium
import pandas as pd

# Load data
stops = pd.read_csv('Metro_DMRC_GTFS/stops.csv')
trips = pd.read_csv('Metro_DMRC_GTFS/trips.csv')
stop_times = pd.read_csv('Metro_DMRC_GTFS/stop_times.csv')

# Create a transportation network graph
G = nx.Graph()

# Add stations as nodes to the graph
for index, row in stops.iterrows():
    G.add_node(row['stop_id'], pos=(row['stop_lon'], row['stop_lat']))

# Add connections between stations as edges
for index, row in trips.iterrows():
    trip_stops = stop_times[stop_times['trip_id'] == row['trip_id']]
    stop_ids = trip_stops['stop_id'].tolist()
    for i in range(len(stop_ids) - 1):
        G.add_edge(stop_ids[i], stop_ids[i + 1])

# Create a Folium map centered around Delhi
delhi_coordinates = (28.6139, 77.2090)  # Coordinates of Delhi
mymap = folium.Map(location=delhi_coordinates, zoom_start=11)

# Plot the transportation network on the map
for edge in G.edges():
    start = stops.loc[stops['stop_id'] == edge[0], ['stop_lat', 'stop_lon']].values.tolist()[0]
    end = stops.loc[stops['stop_id'] == edge[1], ['stop_lat', 'stop_lon']].values.tolist()[0]
    folium.PolyLine(locations=[start, end], color='blue', weight=2.5, opacity=0.7).add_to(mymap)

# Add markers for each station
for node, attrs in G.nodes(data=True):
    folium.CircleMarker(location=attrs['pos'], radius=2, color='black', fill=True, fill_color='black').add_to(mymap)

# Save the map as an HTML file
mymap.save("metro_network_with_stations.html")
