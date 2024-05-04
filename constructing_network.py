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

# Add nodes and edges with weights based on scaled probe counts
for _, row in merged_data.iterrows():
    coords = row['geometry'].coords  # Extract coordinates from LineString geometry
    for i in range(len(coords)-1):
        start_node = coords[i]  # Start node of the edge
        end_node = coords[i+1]  # End node of the edge
        weight = row['scaledProbeCount']  # Weight of the edge
        G.add_edge(start_node, end_node, weight=weight)
        
nx.write_graphml(G, 'metro_network.graphml')

# # Visualize network subset
# plt.figure(figsize=(10, 10))
# pos = nx.spring_layout(G)  # Define layout for nodes
# nx.draw(G, pos, with_labels=False, node_size=5, node_color='skyblue', edge_color='grey', width=0.5)  # Draw nodes and edges without labels
# plt.title('Metro Line Network with Weights from Traffic Data (Top 5000 Segments)')
# plt.show()

end_time = time.time()

# Calculate and print execution time
execution_time = end_time - start_time
print("Execution time: {:.2f} seconds".format(execution_time))