import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import time

start_time = time.time()

# Read GeoJSON data into a GeoDataFrame
gdf = gpd.read_file('Delhi Traffic Data/geojson_Delhi_Traffic_Data_-_Oct_2022.geojson')

# Read traffic data containing probe counts and scaled probe counts
traffic_data = pd.read_csv('traffic_data.csv')

# Merge traffic data with gdf based on a common column (e.g., segment ID)
merged_data = pd.merge(gdf, traffic_data, on='segmentId', how='inner')
merged_data.dropna(subset=['scaledProbeCount'], inplace=True)

# Create empty graph
G = nx.Graph()

# Add nodes without edges based on the first tuple of coords
for _, row in merged_data.iterrows():
    coords = row['geometry'].coords  # Extract coordinates from LineString geometry
    start_node = coords[0]  # Start node of the edge
    scaled_probe_count = row['scaledProbeCount']
    G.add_node(start_node, scaled_probe_count=scaled_probe_count)

# Save the graph
nx.write_graphml(G, 'traffic_network_points.graphml')

# # Draw the network
# plt.figure(figsize=(10, 10))
# pos = nx.spring_layout(G)  # or any other layout algorithm
# nx.draw(G, pos, with_labels=False, node_size=0.5, node_color='skyblue')
# plt.title('Traffic Network (Nodes Only)')
# plt.show()
# plt.savefig('traffic_network_original_points_plot.png')

end_time = time.time()

# Calculate and print execution time
execution_time = end_time - start_time
print("Execution time: {:.2f} seconds".format(execution_time))