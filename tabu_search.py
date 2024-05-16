import numpy as np
import pandas as pd
# Define parameters
num_stations = 10
min_interspacing = 10
max_interspacing = 16
num_random_walks = 100
y = 10000  # Max iterations without improvement for tabu search
mmin = 5
mmax = 10 

source_node = (17, 3)
destination_node = (4, 8)

# Function to generate random walks for initial solutions
def generate_random_walks(source_node, destination_node, num_walks):
    initial_solutions = []  # List to store initial solutions

    # Perform random walks from the source node
    for _ in range(num_walks // 2):
        source_walk = random_walk(source_node)
        initial_solution = source_walk + [destination_node]
        initial_solutions.append(initial_solution)

    # Perform random walks from the destination node
    for _ in range(num_walks // 2):
        destination_walk = random_walk(destination_node)
        initial_solution = [source_node] + destination_walk[1:]
        initial_solutions.append(initial_solution)

    return initial_solutions

# Function to perform random walk from a given node
def random_walk(start_node):
    current_node = start_node
    walk = [current_node]
    while len(walk) < num_stations:
        # Determine the distance to the next station (12 or 13 units)
        station_distance = np.random.choice([12, 13])
        for _ in range(station_distance):
            # Choose next move (up, down, left, right) with equal probability
            next_move = np.random.choice(['up', 'down', 'left', 'right'])
            # Update current node based on next move
            if next_move == 'up':
                current_node = (current_node[0] + 1, current_node[1])
            elif next_move == 'down':
                current_node = (current_node[0] - 1, current_node[1])
            elif next_move == 'left':
                current_node = (current_node[0], current_node[1] - 1)
            elif next_move == 'right':
                current_node = (current_node[0], current_node[1] + 1)
            # Ensure current_node is within bounds
            current_node = (max(0, min(18 - 1, current_node[0])), 
                            max(0, min(15 - 1, current_node[1])))
        # Append current node to walk after station distance is covered
        walk.append(current_node)
    return walk

# Function to calculate traffic coverage for a solution
def calculate_traffic_coverage(solution, grid_dict):
    return sum(grid_dict[node] for node in solution)

# Function to check if solution meets interspacing constraints
def meets_interspacing_constraints(solution):
    n = len(solution)

    for i in range(n):
        for j in range(n):
            if i != j:  # Avoid checking the same station
                distance = abs(solution[i][0] - solution[j][0]) + abs(solution[i][1] - solution[j][1])  # Manhattan distance
                if distance < min_interspacing:
                    return False  # Minimum interspacing violated

    # Check for maximum interspacing between adjacent stations
    for i in range(n - 1):
        distance = abs(solution[i][0] - solution[i+1][0]) + abs(solution[i][1] - solution[i+1][1])  # Manhattan distance
        if distance > max_interspacing:
            return False  # Maximum interspacing violated between adjacent stations

    return True
    
def check_false_starts(initial_solutions):
    feasible_solutions = []
    for solution in initial_solutions:
        start_node = solution[-2]  # Second-to-last node
        end_node = solution[-1]    # Last node
        distance = abs(end_node[0] - start_node[0]) + abs(end_node[1] - start_node[1])
        if min_interspacing <= distance <= max_interspacing:
            feasible_solutions.append(solution)
    return feasible_solutions

# Neighbourhood search: Switch out a station si with an adjacent station sj
def neighbourhood_search(solution, grid_dict):
    best_solution = solution
    best_traffic_coverage = calculate_traffic_coverage(solution, grid_dict)
    
    for i in range(1, len(solution) - 1):  # Don't change source and destination
        current_station = solution[i]
        neighbours = get_neighbours(current_station)
        for neighbour in neighbours:
            new_solution = solution[:i] + [neighbour] + solution[i+1:]
            if meets_interspacing_constraints(new_solution):
                new_traffic_coverage = calculate_traffic_coverage(new_solution, grid_dict)
                if new_traffic_coverage > best_traffic_coverage:
                    best_solution = new_solution
                    best_traffic_coverage = new_traffic_coverage
    return best_solution, best_traffic_coverage

# Get adjacent stations (neighbors) for a given station
def get_neighbours(station):
    x, y = station
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

def shake_up(solution, grid_dict):
    best_solution = solution
    best_traffic_coverage = calculate_traffic_coverage(solution, grid_dict)
    
    for i in range(1, len(solution) - 1):  # Don't change source and destination
        current_station = solution[i]
        neighbours = get_extended_neighbours(current_station)
        for neighbour in neighbours:
            new_solution = solution[:i] + [neighbour] + solution[i+1:]
            if meets_interspacing_constraints(new_solution):
                new_traffic_coverage = calculate_traffic_coverage(new_solution, grid_dict)
                if new_traffic_coverage > best_traffic_coverage:
                    best_solution = new_solution
                    best_traffic_coverage = new_traffic_coverage
    return best_solution, best_traffic_coverage

def get_extended_neighbours(station):
    x, y = station
    neighbours = []
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            if abs(dx) + abs(dy) <= 8:
                neighbours.append((x + dx, y + dy))
    return neighbours

# Tabu Search algorithm
def tabu_search(initial_solution, grid_dict):
    current_solution = initial_solution
    current_traffic_coverage = calculate_traffic_coverage(current_solution, grid_dict)
    
    best_solution = current_solution
    best_traffic_coverage = current_traffic_coverage
    
    tabu_list = []
    no_improvement_count = 0
    
    while no_improvement_count < y:
        new_solution, new_traffic_coverage = neighbourhood_search(current_solution, grid_dict)
        
        if new_traffic_coverage > current_traffic_coverage:
            current_solution = new_solution
            current_traffic_coverage = new_traffic_coverage
            no_improvement_count = 0  # Reset the no improvement count
        else:
            no_improvement_count += 1
        
        if new_traffic_coverage > best_traffic_coverage:
            best_solution = new_solution
            best_traffic_coverage = new_traffic_coverage
        
        # Update tabu list with random length
        tabu_duration = np.random.randint(mmin, mmax + 1)
        tabu_list.append((current_solution, current_traffic_coverage, tabu_duration))
        
        # Remove expired tabu entries
        for i in range(len(tabu_list)):
            tabu_list[i] = (tabu_list[i][0], tabu_list[i][1], tabu_list[i][2] - 1)
        tabu_list = [item for item in tabu_list if item[2] > 0]
        
        # Perform shake-up procedure if necessary
        if no_improvement_count == 0 or no_improvement_count >= y:
            shake_solution, shake_traffic_coverage = shake_up(current_solution, grid_dict)
            if shake_traffic_coverage > best_traffic_coverage:
                best_solution = shake_solution
                best_traffic_coverage = shake_traffic_coverage
                no_improvement_count = 0  # Reset the no improvement count after shake-up
    
    return best_solution, best_traffic_coverage

# Read subsection nodes DataFrame from CSV
subsection_nodes_df = pd.read_csv("subsection_nodes.csv")

# Initialize grid_dict
grid_dict = {}

# Populate grid_dict using subsection_nodes_df
for index, row in subsection_nodes_df.iterrows():
    latitude = row['Grid Row']
    longitude = row['Grid Column']
    traffic_probe_count = row['avg_traffic_probe_count']
    grid_dict[(latitude, longitude)] = traffic_probe_count


# Generate initial solutions
initial_solutions = generate_random_walks(source_node, destination_node, num_random_walks)

# Check which initial solutions meet interspacing constraints
feasible_solutions = check_false_starts(initial_solutions)

# Apply Tabu Search to each feasible solution
best_global_solution = None
best_global_traffic_coverage = -1

for solution in feasible_solutions:
    best_solution, best_traffic_coverage = tabu_search(solution, grid_dict)
    if best_traffic_coverage > best_global_traffic_coverage:
        best_global_solution = best_solution
        best_global_traffic_coverage = best_traffic_coverage

print("Best Global Solution:", best_global_solution)
print("Best Global Traffic Coverage:", best_global_traffic_coverage)

best_solution_df = pd.DataFrame(best_global_solution, columns=['latitude', 'longitude'])

# Save best solution to CSV file
best_solution_df.to_csv('best_solution.csv', index=False)