#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 10:34:53 2025

@author: ennisk
"""

import pickle
import numpy as np  
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr

file_path = '/Path/to/file/graphcast.pickle'
with open(file_path, 'rb') as file:
    data = pickle.load(file)
    
ds = data['predictions'] 
temp_data = ds['2m_temperature'] - 273.15
    
# Define grid points for case studies 
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

# Extract averaged daily temperature for each location
location_temps = {}
for name, coords in locations.items():
    temp_at_loc = temp_data.sel(lon=coords['lon'], lat=coords['lat'], method='nearest')
    location_temps[name] = temp_at_loc.values.item()

# Create dataset with grid point temps for plotting later
location_ds = xr.Dataset(
    {"2m_temperature": ("location", list(location_temps.values()))},
    coords={"location": list(location_temps.keys())}
)

# Save to a NetCDF file
output_path = '/Path/to/output/filepath/gridpoint_temperature.nc'
location_ds.to_netcdf(output_path)
