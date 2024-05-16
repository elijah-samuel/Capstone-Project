import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import json
import pandas as pd

# Extract probe counts from segmentProbeCounts column
def extract_probe_count(segment_probe_counts):
    if segment_probe_counts is not None:
        segment_probe_counts = json.loads(segment_probe_counts)
        if segment_probe_counts:
            return segment_probe_counts[0]['probeCount']
    return None

traffic_data = pd.read_csv('traffic_data.csv')

# Read GeoJSON data into a GeoDataFrame
gdf = gpd.read_file('Delhi Traffic Data/geojson_Delhi_Traffic_Data_-_Oct_2022.geojson')
gdf['probeCount'] = gdf['segmentProbeCounts'].apply(extract_probe_count)

scaler = MinMaxScaler()
gdf['scaledProbeCount'] = scaler.fit_transform(gdf[['probeCount']])
traffic_data['scaledProbeCount'] = scaler.fit_transform(traffic_data[['probeCount']])

# Plot LineString geometries with color encoding based on probe counts
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, column='scaledProbeCount', cmap='Reds', linewidth=2, legend=True)
ax.set_title('Traffic Flow Heatmap with Scaled Probe Counts')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.show()
fig.savefig('traffic_flow_heatmap.png', dpi=300, bbox_inches='tight')


# traffic_data.to_csv('traffic_data.csv', index=False)
# gdf.to_file("geojson_Delhi_Traffic_Data_-_Oct_2022_scaled.geojson", driver='GeoJSON')
