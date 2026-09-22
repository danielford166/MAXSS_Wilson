# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 14:50:32 2026

@author: dw557
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Global file path definition
file_path = r"C:/Users/dw557/OneDrive - University of Exeter/Desktop/storm_component_flux_summary_2010_to_2019.csv"

# Load the data
df = pd.read_csv(file_path)

# Calculate means
mean_no_grad = df["SST_NO_GRADIENTS_RUN"].mean()
mean_with_grad = df["SST_WITH_GRADIENTS_RUN"].mean()

# Set visual style
sns.set_theme(style="white")
plt.figure(figsize=(11, 6))

# Plot histogram with 50 bins
sns.histplot(
    data=df[["SST_WITH_GRADIENTS_RUN", "SST_NO_GRADIENTS_RUN"]],
    element="step",
    fill=True,
    alpha=0.25,
    binwidth=1,
    palette=["#1B9E77", "#D95F02"],
    common_bins=True,
)

# Reference line at zero flux
plt.axvline(0, color="black", linestyle=":", linewidth=1.2, zorder=2)

# Mean line for No SST Gradients
plt.axvline(
    mean_no_grad,
    color="#D95F02",
    linestyle="--",
    linewidth=2,
    label=f"Mean (No Gradients): {mean_no_grad:.2f}",
)

# Mean line for With SST Gradients
plt.axvline(
    mean_with_grad,
    color="#1B9E77",
    linestyle="--",
    linewidth=2,
    label=f"Mean (With Gradients): {mean_with_grad:.2f}",
)

# Grid and styling
plt.grid(axis="y", linestyle="--", alpha=0.5)
# plt.title(
#     "Impact of SST Gradients on Tropical Cyclone $\mathrm{CO}_2$ Flux"
#     " (2010–2019)",
#     fontsize=14,
#     fontweight="bold",
#     pad=15,
# )
plt.xlabel("Total $\mathrm{CO}_2$ Flux Tg C per storm", fontsize=12)
plt.ylabel("Count of Tropical Cyclones", fontsize=12)

# Legend positioning
plt.legend(
    title="Model Run / Statistics",
    frameon=True,
    facecolor="white",
    loc="upper left",
)

plt.tight_layout()
plt.show()

###############################################################################

# Calculate paired difference for each cyclone
df["DELTA_FLUX"] = df["SST_WITH_GRADIENTS_RUN"] - df["SST_NO_GRADIENTS_RUN"]

plt.figure(figsize=(9, 5))
sns.histplot(
    df["DELTA_FLUX"],
    binwidth=0.1,  # finer resolution for small differences
    color="#1B9E77",
    kde=False,
    element="step",
    alpha=0.4,
)

# Reference line at zero impact
plt.axvline(
    0, color="black", linestyle=":", linewidth=1.5, label="No Gradient Impact"
)
plt.axvline(
    df["DELTA_FLUX"].mean(),
    color="red",
    linestyle="--",
    linewidth=1.5,
    label=f"Mean Delta: {df['DELTA_FLUX'].mean():.1f} Tg C",
)

plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.xlabel("$\Delta\mathrm{CO}_2$ Flux (With Gradients − No Gradients) [Tg C]", fontsize=11)
plt.ylabel("Count of Tropical Cyclones", fontsize=11)
plt.legend(frameon=True, facecolor="white")
plt.tight_layout()
plt.show()