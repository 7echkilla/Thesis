import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def plot_histogram(gxv_data, scan_speeds, output_dir="images/GxV"):
    """
    Plot histogram of G*V values for multiple scan speeds.

    Parameters:
    - gxv_data: Dictionary where keys are scan speeds and values are lists of G*V values.
    - scan_speeds: List of scan speeds to plot.
    - output_dir: Directory to save the histogram plot.
    """
    # colors = sns.color_palette("Set1", n_colors=len(scan_speeds))

    # plt.figure(figsize=(10, 8))

    # # Loop through the scan speeds and plot each histogram with a distinct color
    # for idx, scan_speed in enumerate(scan_speeds):
    #     plt.hist(gxv_data[scan_speed], bins=50, alpha=0.7, label=f"{scan_speed}mm/s", color=colors[idx])
        
    # font_size = 14

    # plt.xlabel('GxV (K/s)', fontsize=font_size)
    # plt.ylabel('Counts', fontsize=font_size)
    # plt.legend(title="Scan Speeds", fontsize=font_size)
    # plt.grid(True)
    # plt.tight_layout()

    # # font size of the axis tick labels and colour bar
    # plt.tick_params(axis='both', which='major', labelsize=font_size)

    # os.makedirs(output_dir, exist_ok=True)
    # plt.savefig(os.path.join(output_dir, "counts_histogram.png"), dpi=300)
    # plt.close()

    plt.figure(figsize=(10, 8))

    colors = sns.color_palette("Set1", n_colors=len(scan_speeds))

    for idx, scan_speed in enumerate(scan_speeds):
        sns.kdeplot(gxv_data[scan_speed], label=f"{scan_speed}mm/s", color=colors[idx], fill=True)

    font_size = 14

    plt.xlabel('GxV (K/s)', fontsize=font_size)
    plt.ylabel('Density', fontsize=font_size)
    plt.legend(title="Scan Speeds", fontsize=font_size)
    plt.grid(True)
    plt.tight_layout()

    # font size of the axis tick labels and colour bar
    plt.tick_params(axis='both', which='major', labelsize=font_size)

    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "density_histogram.png"), dpi=300)
    plt.close()

if __name__ == "__main__":
    import sys
    import pickle

    with open("gxv_data.pkl", 'rb') as f:
        gxv_data = pickle.load(f)

    scan_speeds = ["100", "200", "300", "400", "500"]
    
    plot_histogram(gxv_data, scan_speeds)
