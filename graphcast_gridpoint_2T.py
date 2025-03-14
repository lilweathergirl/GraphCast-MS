#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:22:30 2024

@author: ennisk
"""

#This code provides the framework for what was used to get the grid point temperatures for the Case
# studies in Part One of this study. Both PCNW and SE were investigated and their grid points are as shown.

import pickle
import numpy as np  
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr

#Load in your graphcast file 
file_path = '/Path/to/your/Graphcast/file.pickle'
with open(file_path, 'rb') as file:
    data = pickle.load(file)
    
#Opening up the dataset called 'predictions' in my case. 
ds = data['predictions'] 
    
# Define grid points/locations
locations = {
    'Little Rock, AR': {'lon': 267.72, 'lat': 34.74},
    'New Orleans, LA': {'lon': 269.93, 'lat': 29.95},
    'Asheville, NC': {'lon': 277.45, 'lat': 35.59},
}
locations = {
    'Boise, ID': {'lon': 243.80, 'lat': 43.61},
    'Seattle, WA': {'lon': 237.67, 'lat': 47.60},
    'Bend, OR': {'lon': 238.69, 'lat': 44.05},
}

AR_coords = {'longitude': 267.72, 'latitude': 34.74}  # Little Rock, AR
LA_coords = {'longitude': 269.93, 'latitude': 29.95}  # New Orleans, LA
NC_coords = {'longitude': 277.45, 'latitude': 35.59}  # Asheville, NC

ID_coords = {'longitude': 243.80, 'latitude': 43.61}  # Boise, ID
SEA_coords = {'longitude': 237.67, 'latitude': 47.60}  # Seattle, WA
OR_coords = {'longitude': 238.69, 'latitude': 44.05}  # Bend, OR

# Get the temperatures at each grid point. 
def gridpoint_temp(ds, locations, time_indexes=None):
    temp_data = ds['2m_temperature']
    temp_c = temp_data - 273.15  # Convert to Celsius
    
    #These time indexes refer to the 6-h daily averages over NAm for LTs 1-20. Each time index is one value
    #that was already previously averaged for each lead time. I can manually pick the lead time and look
    #at the temp easier this way, rather averaging over every grid point and then print averages for 
    #specific grid points in one script. 
    if time_indexes is None:
        time_indexes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] #Lt's 1-20 in file

    for time_index in time_indexes:
        temp_c_at_time = temp_c.isel(time=time_index)
        print(f"Temperatures at grid points for time index {time_index}:")
        
        for location_name, coords in locations.items():
            temp = temp_c_at_time.sel(lon=coords['lon'], lat=coords['lat'], method='nearest')
            temp_value = temp.values.item()  # Extract scalar value
            print(f"  {location_name}: {temp_value:.2f} °C")

# This part prints it nicer than part one of this script. This came way later when doubling checking my 
# values to ensure they were correct. 
gridpoint_temp(ds, locations, time_indexes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])


# Starting a plotting section, but will do in another script because this is script is for analyzing
# temp prediction on a deeper level and preparing to make line plots for temperature trends/error later
def plot_temp(ds, time_indexes=None):
    temp_data = ds['2m_temperature']
    temp_c = temp_data - 273.15  
    temp_c_at_time = temp_c.isel(time=time_indexes)
    

    # Extract temperatures at the six coordinates for each case study. (each case study requires a different
    # file however.)
    temp_AR = temp_c_at_time.sel(lon=AR_coords['longitude'], lat=AR_coords['latitude'], method='nearest')
    temp_LA = temp_c_at_time.sel(lon=LA_coords['longitude'], lat=LA_coords['latitude'], method='nearest')
    temp_NC = temp_c_at_time.sel(lon=NC_coords['longitude'], lat=NC_coords['latitude'], method='nearest')
    
    temp_ID = temp_c_at_time.sel(lon=ID_coords['longitude'], lat=ID_coords['latitude'], method='nearest')
    temp_SEA = temp_c_at_time.sel(lon=SEA_coords['longitude'], lat=SEA_coords['latitude'], method='nearest')
    temp_OR = temp_c_at_time.sel(lon=OR_coords['longitude'], lat=OR_coords['latitude'], method='nearest')
    

    # Print the temperatures for each location in an easy to read manner
    print(f"Temperature at Little Rock, AR: {temp_AR.item():.2f} °C")
    print(f"Temperature at New Orleans, LA: {temp_LA.item():.2f} °C")
    print(f"Temperature at Asheville, NC: {temp_NC.item():.2f} °C")
    
    print(f"Temperature at Boise, ID: {temp_ID.item():.2f} °C")
    print(f"Temperature at Seattle, WA: {temp_SEA.item():.2f} °C")
    print(f"Temperature at Bend, OR: {temp_OR.item():.2f} °C")

##Plot later after understanding the data first##