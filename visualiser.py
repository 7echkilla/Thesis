import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.interpolate import griddata

def plot_graph(dataframe, x_slice=0.0005, tolerance=1e-9, parameter='G', log_scale=False, colour_bands=20, scan_speed=0.0005):
    """
    Plot a parameter (including derived ones) on the Y-Z plane at a given X slice
    
    Parameters:
    - dataframe: Pandas DataFrame with 3DThesis simulation output data
    - x_slice: X-coordinate to slice the data
    - tolerance: Tolerance for selecting data near x_slice
    - parameter: Parameter to plot ('G', 'V', 'G*V', 'G/V', etc.)
    - log_scale: If True, apply log10 scaling to the parameter
    - colour_bands: Number of color levels in contour plot
    """
    
    # filter data
    dataframe_slice = dataframe[abs(dataframe['x'] - x_slice) < tolerance].copy()
    if dataframe_slice.empty:
        print(f"No data found near x = {x_slice}")
        return
    
     # handle derived parameters
    if parameter == 'GxV':
        dataframe_slice['GxV'] = dataframe_slice['G'] * dataframe_slice['V']
        unit = 'K/s'
    elif parameter == 'G/V':
        dataframe_slice = dataframe_slice[dataframe_slice['V'] > 1e-10]  # avoid division by zero
        dataframe_slice['G/V'] = dataframe_slice['G'] / dataframe_slice['V']
        unit = 'K.s/m2'
    else:
        if parameter == 'G':
            unit = 'K/m'
        elif parameter == 'V':
            dataframe_slice = dataframe_slice[dataframe_slice['V'] > 1e-10]  # avoid division by zero
            unit = 'm/s'

    # apply log scale if requested
    if log_scale and parameter not in ['x', 'y', 'z']:  # avoid log for spatial coordinates
        dataframe_slice[parameter] = np.log10(dataframe_slice[parameter].replace(0, np.nan))  # avoid log(0)
    
    # interpolate missing values using griddata
    points = dataframe_slice[['y', 'z']].values  # (y, z) coordinates
    values = dataframe_slice[parameter].values  # parameter values at (y, z)
    grid_y, grid_z = np.mgrid[dataframe_slice['y'].min():dataframe_slice['y'].max():100j, dataframe_slice['z'].min():dataframe_slice['z'].max():100j]

     # perform linear interpolation
    grid_parameter = griddata(points, values, (grid_y, grid_z), method='linear')

    # scale m to um
    grid_y_um = grid_y * 1e6
    grid_z_um = grid_z * 1e6
    x_slice_um = x_slice * 1e3 

    # plotting
    plt.figure(figsize=(10, 8))
    sc = plt.contourf(grid_y_um, grid_z_um, grid_parameter, colour_bands, cmap='coolwarm')

    font_size = 14
    plt.xlabel('y (µm)', fontsize=font_size)
    plt.ylabel('z (µm)', fontsize=font_size)
    plt.title(f'{parameter} at x = {x_slice_um:.2f}mm, v={scan_speed}mm/s', fontsize=font_size)
    
    # add a color bar to show the parameter scale
    cbar = plt.colorbar(sc)
    cbar.set_label(f'{parameter} ({unit})', fontsize=font_size)
    
    plt.axis('equal')
    plt.grid(True)
    plt.tight_layout()

    # font size of the axis tick labels and colour bar
    plt.tick_params(axis='both', which='major', labelsize=font_size)
    cbar.ax.tick_params(labelsize=font_size)

    # save output
    output_dir = os.path.join(os.getcwd(), "images", parameter)
    os.makedirs(output_dir, exist_ok=True)

    filename = f"speed{scan_speed}_x{str(x_slice).replace('.', 'p')}.png"
    output_path = os.path.join(output_dir, filename)

    plt.savefig(output_path, dpi=300)
    # plt.show()

def main():
    scan_speeds = ["100", "200", "300", "400", "500"]
    parameters = ["GxV", "G/V", "G", "V"]
    
    x_slice = 0.0005    # (0-0.001) in meters

    for parameter in parameters:
        for scan_speed in scan_speeds:
            csv_path = os.path.join(os.getcwd(), f"simulation/AlCuCe{scan_speed}/Data/AlCuCe{scan_speed}.Solidification.Final.csv")
            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"File not found: {csv_path}")

            dataframe = pd.read_csv(csv_path)

            plot_graph(dataframe=dataframe, x_slice=x_slice, parameter=parameter, scan_speed=scan_speed)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)