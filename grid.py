import numpy as np
import networkx as nx
import xml.etree.ElementTree as ET
import pandas as pd

# Define the grid size
grid_size = 100

# Function to parse GraphML file and extract node data
def parse_graphml_file(graphml_file):
    # Parse the XML tree from the GraphML file
    tree = ET.parse(graphml_file)
    root = tree.getroot()

    # Define namespace
    ns = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}

    # Initialize empty lists to store node data
    node_ids = []
    node_probe_counts = []
    node_latitudes = []
    node_longitudes = []

    # Extract node data from the XML tree
    for node in root.findall('.//graphml:node', ns):
        node_id = node.get('id')
        node_ids.append(node_id)

        # Extract probe count data from the XML tree
        probe_count_elem = node.find('graphml:data[@key="d0"]', ns)
        if probe_count_elem is not None:
            node_probe_counts.append(float(probe_count_elem.text))
        else:
            node_probe_counts.append(0.0)

        # Extract latitude and longitude data from the node id
        coords = node_id.strip('()').split(',')
        node_latitudes.append(float(coords[1]))
        node_longitudes.append(float(coords[0]))

    return node_ids, node_probe_counts, node_latitudes, node_longitudes

# Function to create grid cells and calculate average probe count for each cell
def create_grid_cells(node_latitudes, node_longitudes, node_probe_counts, grid_size):
    # Determine the minimum and maximum latitude and longitude
    min_lat, max_lat = min(node_latitudes), max(node_latitudes)
    min_lon, max_lon = min(node_longitudes), max(node_longitudes)


    # Calculate the size of each grid cell
    lat_step = (max_lat - min_lat) / grid_size
    lon_step = (max_lon - min_lon) / grid_size


    last_cell_lat = max_lat - lat_step
    last_cell_lon = max_lon - lon_step

    # Initialize grid cells dictionary to store average traffic probe count for each cell
    grid_cells = {}

    # Define top-left coordinates for each grid cell
    for lat_index in range(grid_size):
        for lon_index in range(grid_size):
            top_left_lat = min_lat + (lat_index * lat_step)
            top_left_lon = min_lon + (lon_index * lon_step)
            grid_cells[(lat_index, lon_index)] = {'top_left_lat': top_left_lat,
                                                   'top_left_lon': top_left_lon,
                                                   'traffic_probe_count': []}

    # Iterate over each node and add its traffic probe count to the corresponding grid cell
    for lat, lon, probe_count in zip(node_latitudes, node_longitudes, node_probe_counts):
        lat_index = int((lat - min_lat) / lat_step)
        lon_index = int((lon - min_lon) / lon_step)

        lat_index = max(0, min(lat_index, grid_size - 1))
        lon_index = max(0, min(lon_index, grid_size - 1))

        grid_cells[(lat_index, lon_index)]['traffic_probe_count'].append(probe_count)

    # Calculate the average probe count for each grid cell
    for cell, data in grid_cells.items():
        if data['traffic_probe_count']:
            data['avg_traffic_probe_count'] = np.mean(data['traffic_probe_count'])
        else:
            data['avg_traffic_probe_count'] = 0

    return grid_cells

# Function to assign nodes at the center of each cell with the corresponding average probe count
def assign_nodes(grid_cells, min_lat, min_lon, lat_step, lon_step):
    nodes = {}
    for cell, data in grid_cells.items():
        lat_center = min_lat + (cell[0] + 0.5) * lat_step
        lon_center = min_lon + (cell[1] + 0.5) * lon_step
        nodes[cell] = {'latitude': lat_center, 'longitude': lon_center, 'avg_traffic_probe_count': data['avg_traffic_probe_count']}
    return nodes

# Function to create edges between adjacent nodes
def create_edges(nodes):
    G = nx.Graph()

    # Add nodes to the graph
    for node, data in nodes.items():
        G.add_node(node, latitude=data['latitude'], longitude=data['longitude'], avg_traffic_probe_count=data['avg_traffic_probe_count'])

    # Add edges between adjacent nodes
    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) in nodes:
                if (i + 1, j) in nodes:
                    G.add_edge((i, j), (i + 1, j))
                if (i - 1, j) in nodes:
                    G.add_edge((i, j), (i - 1, j))
                if (i, j + 1) in nodes:
                    G.add_edge((i, j), (i, j + 1))
                if (i, j - 1) in nodes:
                    G.add_edge((i, j), (i, j - 1))

    return G

# Main function
def main():
    # Parse GraphML file
    node_ids, node_probe_counts, node_latitudes, node_longitudes = parse_graphml_file('traffic_network_points.graphml')

    # Create grid cells and calculate average probe count
    grid_cells = create_grid_cells(node_latitudes, node_longitudes, node_probe_counts, grid_size)

    # Assign nodes at the center of each cell with the corresponding average probe count
    min_lat, max_lat = min(node_latitudes), max(node_latitudes)
    min_lon, max_lon = min(node_longitudes), max(node_longitudes)
    lat_step = (max_lat - min_lat) / grid_size
    lon_step = (max_lon - min_lon) / grid_size
    nodes = assign_nodes(grid_cells, min_lat, min_lon, lat_step, lon_step)

    # Create edges between adjacent nodes
    G = create_edges(nodes)

    # Convert nodes dictionary to a DataFrame
    nodes_df = pd.DataFrame(nodes).T.reset_index()
    print(nodes_df.head())
    nodes_df.columns = ['Grid Column', 'Grid Row', 'latitude', 'longitude', 'avg_traffic_probe_count']

    # Save final nodes with average traffic probe count to a CSV file
    nodes_df.to_csv('final_nodes_with_average.csv', index=False)

    return G

# Usage
graph = main()
