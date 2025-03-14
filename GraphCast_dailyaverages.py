#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 10:28:33 2025

@author: ennisk
"""

import pickle
import numpy as np  
import xarray as xr

##This script was used to obtain daily averages for GraphCast

file_path = '/Path/to/Graphcast/file/graphcast_heatwave.pickle'
with open(file_path, 'rb') as file:
    data = pickle.load(file)

ds = data['predictions'] 
temp_data = ds['2m_temperature'] - 273.15

# Calculate the 6hr average over the available time indexes 
# (every 4th, representing 6-hour intervals) this is because graphcast is in time index form not date
average_temp = temp_data.isel(time=slice(0, 80)).mean(dim='time')

# Make a netcdf  to store  the averaged data
avg_ds = xr.Dataset(
    {
        "2m_temperature": average_temp
    },
    coords={
        "lat": ds.coords['lat'],
        "lon": ds.coords['lon'],
    }
)

output_path = '/Path/to/output/file/output_graphcast.nc'
avg_ds.to_netcdf(output_path)

