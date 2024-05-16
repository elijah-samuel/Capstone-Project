import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geopandas as gpd

nodes_df = pd.read_csv("subsection_nodes.csv")
gdf = gpd.read_file('Delhi Traffic Data/geojson_Delhi_Traffic_Data_-_Oct_2022.geojson')

# Extract latitude, longitude, and average traffic probe count from the DataFrame
latitude = nodes_df['latitude']
longitude = nodes_df['longitude']
avg_traffic_probe_count = nodes_df['avg_traffic_probe_count']

# Define the minimum value for the color scale (excluding zeros)
min_value = np.min(avg_traffic_probe_count[avg_traffic_probe_count > 0])

# Create a scatter plot with the average traffic probe count as the color intensity
plt.figure(figsize=(10, 8))
plt.scatter(longitude, latitude, c=avg_traffic_probe_count, cmap='Reds', s=10, vmin=min_value)
plt.colorbar(label='Average Traffic Probe Count')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Traffic Node Map overlay on Road Network')
plt.show()
