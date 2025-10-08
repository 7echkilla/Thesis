import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

def plot_parameter(df, x_slice=0.0005, tol=1e-9, param='G', log_scale=False):
    """
    Function to plot a selected parameter from the 3DThesis simulation data on the YZ plane.
    
    Parameters:
    - df: DataFrame containing the simulation data.
    - x_slice: The X-slice value to extract the data.
    - tol: Tolerance for the X-slice value.
    - param: The parameter to plot (e.g., 'G', 'V', 'eqFrac', etc.).
    - log_scale: If True, apply log scale to the parameter for better contrast.
    """
    
    # filter the data based on the X-slice
    df_slice = df[abs(df['x'] - x_slice) < tol]

    # avoid division by zero in case of V or other parameters
    if param == 'V':
        df_slice = df_slice[df_slice['V'] > 1e-10]
    
    # apply log scale if requested
    if log_scale and param not in ['x', 'y', 'z']:  # avoid log for spatial coordinates
        df_slice[param] = np.log10(df_slice[param].replace(0, np.nan))  # avoid log(0)

    # interpolate missing values using griddata (for missing values in y and z)
    points = df_slice[['y', 'z']].values  # (y, z) coordinates
    values = df_slice[param].values  # parameter values at (y, z)
    
    # grid points for interpolation (creating a grid covering the range of y and z)
    grid_y, grid_z = np.mgrid[df_slice['y'].min():df_slice['y'].max():100j, 
                               df_slice['z'].min():df_slice['z'].max():100j]
    
    # perform interpolation
    grid_param = griddata(points, values, (grid_y, grid_z), method='linear')  # linear interpolation

    # set up the plot
    plt.figure(figsize=(10, 8))
    sc = plt.contourf(grid_y, grid_z, grid_param, 20, cmap='coolwarm')  # filled contour plot for smoother look

    # customize axis labels and title dynamically based on parameter
    plt.xlabel('y (mm)')
    plt.ylabel('z (mm)')
    plt.title(f'{param} on Y-Z Plane at x = {x_slice}')
    
    # add a color bar to show the parameter scale
    plt.colorbar(sc, label=f'{param}')
    
    # Adjust axis limits and grid for better visibility
    plt.axis('equal')
    plt.grid(True)
    plt.tight_layout()
    
    plt.show()

# load data
df = pd.read_csv("Data/AlCuCe100.Solidification.Final.csv")

plot_parameter(df, x_slice=0.0005, param='eqFrac', log_scale=False)
