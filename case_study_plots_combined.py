# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 16:29:49 2026

@author: dw557
"""

import os
import glob
import netCDF4 as nc
import matplotlib.pyplot as plt

# Base data folder
base_dir = r"D:\MAXSS_working_directory\MAXSS_case_study_data"

# Explicit desired order for subplots
target_order = ['CHRIS', 'AL09', 'RAFAEL']

# Find all subdirectories
all_folders = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

# Sort folders according to target_order
def get_order_key(folder_path):
    folder_name = os.path.basename(folder_path).upper()
    for idx, key in enumerate(target_order):
        if key.upper() in folder_name:
            return idx
    return 99  # Fallback to end if not matched

folders = sorted(all_folders, key=get_order_key)

# Create a 3-panel stacked plot figure
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(14, 12), sharey=True)

panel_idx = 0

print("=== SIMULATION DURATION SUMMARY ===")

for folder in folders:
    if panel_idx >= 3:
        break  # Limit to 3 panels

    maxss_files = glob.glob(os.path.join(folder, "*_MAXSS_RUN.nc"))
    ref_files = glob.glob(os.path.join(folder, "*_REF_RUN.nc"))
    
    if not maxss_files or not ref_files:
        print(f"Skipping {os.path.basename(folder)}: Missing matching NetCDF files.")
        continue
    
    cyclone_name = os.path.basename(folder)
    ax = axes[panel_idx]
    
    # Read MAXSS Storm dataset
    ds_storm = nc.Dataset(maxss_files[0], mode='r')
    flux_storm = ds_storm.variables['Hourly_flux'][:]
    raw_time = ds_storm.variables['time'][:]
    ds_storm.close()
    
    # Read Reference dataset
    ds_ref = nc.Dataset(ref_files[0], mode='r')
    flux_ref = ds_ref.variables['Hourly_flux'][:]
    ds_ref.close()
    
    # Print length diagnostics
    len_storm = len(flux_storm)
    len_ref = len(flux_ref)
    duration_days_storm = (raw_time[-1] - raw_time[0]) / 86400.0
    
    print(f"\n[ Panel {panel_idx + 1}: {cyclone_name} ]")
    print(f"  Storm Run length:     {len_storm} steps (~{duration_days_storm:.1f} days)")
    print(f"  Reference Run length: {len_ref} steps")

    # Calculate relative hours
    relative_hours = (raw_time - raw_time[0]) / 3600.0
    
    # Plotting using relative_hours
    ax.plot(relative_hours, flux_storm, color='#0072B2', linewidth=1.8, label='TC Storm Run')
    ax.plot(relative_hours, flux_ref, color='#E69F00', linewidth=1.8, linestyle='--', label='Reference Run (No TC)')
    ax.axhline(0, color='#000000', linestyle=':', linewidth=1, alpha=0.5, label='Zero Flux')
    
    # Panel formatting
    ax.set_title(f'Tropical Cyclone: {cyclone_name} ( ~{duration_days_storm:.0f} days)', 
                 fontsize=12, fontweight='bold', loc='left')
    ax.set_ylabel('Hourly Flux', fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='lower left', frameon=True)
    
    panel_idx += 1

print("\n===================================")

# Label bottom panel x-axis
axes[-1].set_xlabel('Hours Since Simulation Start', fontsize=12)

# Figure main title
#fig.suptitle('Hourly Air-Sea Flux Comparison Across Tropical Cyclones (Relative Time)', fontsize=16, fontweight='bold', y=0.99)

plt.tight_layout()
plt.show()