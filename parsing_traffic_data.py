import json
import csv

# Load JSON data from file
with open('Delhi Traffic Data/Delhi_Traffic_Data_-_Oct_2022.json', 'r') as file:
    # Read the entire file as a single string
    json_str = file.read()

# Parse JSON data
data = json.loads(json_str)

network_data = data['network']
segment_results = network_data['segmentResults']

with open('traffic_data.csv', 'w', newline='') as csvfile:
    # Define CSV writer
    fieldnames = ['segmentId', 'streetName', 'shape', 'probeCount', 'timeSet', 'dateRange']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write CSV header
    writer.writeheader()
    
    # Iterate through each segment result
    for segment_result in segment_results:
        # Extract relevant information
        segment_id = segment_result.get('segmentId')
        street_name = segment_result.get('streetName')
        shape = segment_result.get('shape')
        probe_counts = segment_result.get('segmentProbeCounts')
        
        # Extract latitude and longitude from shape and format as list of tuples
        shape_list = [(coord.get('latitude'), coord.get('longitude')) for coord in shape]
        
        # Write data to CSV file
        if probe_counts:
            for probe_count in probe_counts:
                time_set = probe_count.get('timeSet')
                date_range = probe_count.get('dateRange')
                probe_count_value = probe_count.get('probeCount')
                
                writer.writerow({
                    'segmentId': segment_id,
                    'streetName': street_name,
                    'shape': shape_list,
                    'probeCount': probe_count_value,
                    'timeSet': time_set,
                    'dateRange': date_range
                })
        else:
            writer.writerow({
                'segmentId': segment_id,
                'streetName': street_name,
                'shape': shape_list,
                'probeCount': None,
                'timeSet': None,
                'dateRange': None
            })
