import pandas as pd
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt

file = pd.concat([
    pd.read_csv('June.csv'),
    pd.read_csv('July.csv'),
    pd.read_csv('August.csv')
])

# Assuming 'all_stations' is a DataFrame with both start and end stations' names
all_stations = pd.concat([
    file[['start_station_name', 'start_lat', 'start_lng']],
    file[['end_station_name', 'end_lat', 'end_lng']].rename(columns={
        'end_station_name': 'start_station_name',
        'end_lat': 'start_lat',
        'end_lng': 'start_lng'
    })
])

# Group by station name and aggregate the number of rides
station_counts = all_stations.groupby(['start_station_name', 'start_lat', 'start_lng']).size().reset_index(name='count')

# Convert station counts to a list of lists for HeatMap
heat_data = station_counts[['start_lat', 'start_lng', 'count']].values.tolist()

# Create a map centered around Chicago
chicago_map = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

# Create HeatMap layer for entire map with customizations
HeatMap(heat_data,
        radius=12,  # Adjust the radius of the heatmap points
        gradient={0.2: 'blue', 0.4: 'green', 0.6: 'yellow', 1: 'red'},  # Define a custom gradient for heatmap colors
        blur=10,  # Increase the blur for smoother heatmap transitions
        max_zoom=13,  # Limit the maximum zoom level for better visibility
        min_opacity=0.3  # Set a minimum opacity for the heatmap layer
       ).add_to(chicago_map)

# Display the map
chicago_map

# Find the 10 stations with the lowest count
lowest_count_stations = station_counts.nsmallest(10, 'count')

# Find the 10 stations with the highest count
highest_count_stations = station_counts.nlargest(10, 'count')

# Display the top 10 stations with the lowest count in a visual table
print("Top 10 Stations with Lowest Count:")
display(lowest_count_stations.style.hide_index())

# Display the top 10 stations with the highest count in a visual table
print("\nTop 10 Stations with Highest Count:")
display(highest_count_stations.style.hide_index())
