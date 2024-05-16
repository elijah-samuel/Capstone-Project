import pandas as pd
import matplotlib.pyplot as plt

# Read the original node network
subsection_nodes_df = pd.read_csv("subsection_nodes.csv")

# Read the best solution from CSV file
best_solution_df = pd.read_csv("best_solution.csv")

# Extract indices from the best solution
best_solution_indices = list(zip(best_solution_df['latitude'], best_solution_df['longitude']))

# Map the indices to actual latitude and longitude
best_solution_coords = []
for row, col in best_solution_indices:
    node = subsection_nodes_df[(subsection_nodes_df['Grid Row'] == row) & (subsection_nodes_df['Grid Column'] == col)]
    if not node.empty:
        lat = node.iloc[0]['latitude']
        lon = node.iloc[0]['longitude']
        best_solution_coords.append((lat, lon))

# Split the coordinates into separate latitude and longitude lists
best_lats, best_lons = zip(*best_solution_coords)

# Get the latitude and longitude columns from the original DataFrame
lats = subsection_nodes_df['latitude']
lons = subsection_nodes_df['longitude']

# Plot the original node network
plt.figure(figsize=(10, 8))
plt.scatter(lats, lons, c='blue', label='Nodes')

# Plot the best solution path
plt.plot(best_lats, best_lons, c='red', marker='o', label='Best Solution Path')

# Mark the start and end nodes
plt.scatter(best_lats[0], best_lons[0], c='green', s=100, label='Start Node', zorder=5)
plt.scatter(best_lats[-1], best_lons[-1], c='purple', s=100, label='End Node', zorder=5)

# Add titles and labels
plt.title('Best Solution Path on Original Node Network')
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.legend()
plt.grid(True)
plt.show()
