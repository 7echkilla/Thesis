import pickle

def print_max_gxv_values(pickle_file="gxv_data.pkl"):

    try:
        with open(pickle_file, 'rb') as file:
            gxv_data = pickle.load(file)
        
        # iterate over the scan speeds and print the max GxV value for each
        for scan_speed, gxv_values in gxv_data.items():
            max_gxv = max(gxv_values) if gxv_values else None
            print(f"Max GxV for scan speed {scan_speed}: {max_gxv}")
    
    except FileNotFoundError:
        print(f"[ERROR] Pickle file not found: {pickle_file}")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")

print_max_gxv_values()
