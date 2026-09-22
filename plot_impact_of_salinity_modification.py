# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 16:43:19 2026

@author: dw557
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# File paths
path_with_gamma = r"D:\HPC_MAXSS_working_directory\output_with_gamma_function\Spatially_integrated_fluxes\storm_component_flux_summary_2010.csv"
path_without_gamma = r"D:\HPC_MAXSS_working_directory\output_without_gamma_function\Spatially_integrated_fluxes\storm_component_flux_summary_2010_to_2011.csv"

# Target columns
target_cols = ["MAXSS_RUN", "REF_RUN", "SSS_RUN"]

# Load CSV files
df_with = pd.read_csv(path_with_gamma)
df_without = pd.read_csv(path_without_gamma)


def format_storm_label(storm_str):
    parts = str(storm_str).split("_")
    if len(parts) >= 3 and parts[-1] != "":
        return parts[-1]  # Named storm (e.g., BONNIE)
    elif len(parts) >= 2:
        return parts[-2]  # Unnamed storm ID (e.g., AL022010)
    return str(storm_str)


# Merge datasets on 'Storm'
merged_df = pd.merge(
    df_with[["Storm"] + target_cols],
    df_without[["Storm"] + target_cols],
    on="Storm",
    suffixes=("_WITH_GAMMA", "_WITHOUT_GAMMA"),
)

# Apply unique clean labels
merged_df["Storm_Label"] = merged_df["Storm"].apply(format_storm_label)

# Calculate Deltas per storm
delta_df = pd.DataFrame({"Storm_Label": merged_df["Storm_Label"]})
for col in target_cols:
    delta_df[col] = (
        merged_df[f"{col}_WITH_GAMMA"] - merged_df[f"{col}_WITHOUT_GAMMA"]
    )

# --- CALCULATE & PRINT MEAN EFFECT ---
print("=== MEAN EFFECT OF SALINITY MODIFICATION (With - Without) ===")
for col in target_cols:
    mean_val = delta_df[col].mean()
    print(f"{col}: {mean_val:.4f} Tg C")
print("============================================================\n")

# Reshape to long format for Seaborn
delta_long = pd.melt(
    delta_df,
    id_vars=["Storm_Label"],
    value_vars=target_cols,
    var_name="Run_Type",
    value_name="Delta_Flux",
)

# Set visual style
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

# Barplot without error bars
ax = sns.barplot(
    data=delta_long,
    x="Storm_Label",
    y="Delta_Flux",
    hue="Run_Type",
    palette=["#2b5c8f", "#d95f02", "#1b9e77"],
    errorbar=None,
)

# Zero baseline reference line
plt.axhline(0, color="black", linestyle="--", linewidth=1.2)

# Axis labels & Legend
plt.xlabel("")  # Removed x-axis label
plt.ylabel(
    "$\Delta\mathrm{CO}_2$ Flux (With Salinity Modification − Without) [Tg C]",
    fontsize=12,
    fontweight="bold",
)
plt.legend(
    title="Flux Calculation", frameon=True, facecolor="white", loc="best"
)

plt.tight_layout()
plt.show()