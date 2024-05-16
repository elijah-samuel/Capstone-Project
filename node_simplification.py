import pandas as pd

# Load the CSV file containing all nodes
nodes_df = pd.read_csv("final_nodes_with_average.csv")  # Replace "nodes.csv" with the actual filename

# Define the boundaries of the smaller square
min_lat = 28.60096
max_lat = 28.73082
min_lon = 77.13236
max_lon = 77.27214

# Filter nodes within the boundaries to create a new grid
new_grid = nodes_df[(nodes_df['latitude'] >= min_lat) & (nodes_df['latitude'] <= max_lat) &
                    (nodes_df['longitude'] >= min_lon) & (nodes_df['longitude'] <= max_lon)]

# Adjust the Grid Row and Grid Column to start from 0
new_grid['Grid Row'] = new_grid['Grid Row'] - new_grid['Grid Row'].min()
new_grid['Grid Column'] = new_grid['Grid Column'] - new_grid['Grid Column'].min()

# Save the adjusted DataFrame to a new CSV file without the index
new_grid.to_csv("subsection_nodes.csv", index=False)

