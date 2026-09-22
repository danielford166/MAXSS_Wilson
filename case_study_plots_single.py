# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 16:15:53 2026

@author: dw557
"""

import os
import glob
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd

# Base data folder
base_dir = r"D:\MAXSS_working_directory\MAXSS_case_study_data"

# Find all subdirectories inside MAXSS_case_study_data
folders = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

for folder in folders:
    # Search for the MAXSS_RUN and REF_RUN NetCDF files within each cyclone folder
    maxss_files = glob.glob(os.path.join(folder, "*_MAXSS_RUN.nc"))
    ref_files = glob.glob(os.path.join(folder, "*_REF_RUN.nc"))
    
    # Ensure both datasets exist before plotting
    if not maxss_files or not ref_files:
        print(f"Skipping {os.path.basename(folder)}: Missing matching NetCDF files.")
        continue
    
    maxss_path = maxss_files[0]
    ref_path = ref_files[0]
    cyclone_name = os.path.basename(folder)
    
    # Read MAXSS Storm Run
    ds_storm = nc.Dataset(maxss_path, mode='r')
    flux_storm = ds_storm.variables['Hourly_flux'][:]
    raw_time = ds_storm.variables['time'][:]
    ds_storm.close()
    
    # Read Reference Run
    ds_ref = nc.Dataset(ref_path, mode='r')
    flux_ref = ds_ref.variables['Hourly_flux'][:]
    ds_ref.close()
    
    # Convert epoch timestamps
    dates = pd.to_datetime(raw_time, unit='s')
    
    # Create individual figure for each tropical cyclone
    plt.figure(figsize=(12, 6))
    
    # Plot Storm Run vs Reference Run using colorblind-safe Okabe-Ito colors
    plt.plot(dates, flux_storm, color='#0072B2', linewidth=1.8, label='MAXSS Run')
    plt.plot(dates, flux_ref, color='#E69F00', linewidth=1.8, linestyle='--', label='Reference Run')
    
    # Zero baseline
    plt.axhline(0, color='#000000', linestyle=':', linewidth=1, alpha=0.5, label='Zero Flux')
    
    # Labels & Formatting
    plt.title(f'Hourly Air-Sea Flux: {cyclone_name}', fontsize=14, fontweight='bold')
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Hourly Flux', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper right', frameon=True)
    
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    
    # Display plot
    plt.show()