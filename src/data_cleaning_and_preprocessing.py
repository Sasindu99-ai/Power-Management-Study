import os
import pandas as pd
from datetime import datetime
import glob

# ==========================================
# Configuration
# ==========================================
# Change these dates to filter which files to process
# Format: 'YYYY-MM-DD'
START_DATE = '2026-01-27'
END_DATE = '2026-07-26'

# Base paths
BASE_DATA_DIR = os.path.join('data', 'gensum')
CLEANED_DATA_DIR = 'Cleaned Data'

# Subfolders
SUBFOLDERS = {
    'Load Curve': 'Load Curve',
    'Energy Data': 'Energy Data',
    'Peak Data': 'Peak Data',
    'Night Peak Data': 'Night Peak Data',
    'Reservoir Data': 'Reservoir Data'
}

# Maximum Capacities (Water Levels) for Reservoirs missing storagePercentage
MAX_CAPACITIES = {
    'Bowatenna': 250.0,
    'Ukuwela': 440.74,
    'Rantambe': 152.0,
    'Upper Koth.': 1194.0,
    'Kukule': 206.0,
    'Inginiyagala': 73.64 # Max observed / Crest level approx
}

def create_directories():
    """Create the Cleaned Data folder and its subdirectories."""
    os.makedirs(CLEANED_DATA_DIR, exist_ok=True)
    for folder in SUBFOLDERS.values():
        os.makedirs(os.path.join(CLEANED_DATA_DIR, folder), exist_ok=True)

def get_dates_to_process(start_date_str, end_date_str):
    """Generate a list of date strings between start_date and end_date."""
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    date_list = pd.date_range(start_date, end_date).strftime('%Y-%m-%d').tolist()
    return date_list

def process_load_curve(date_str):
    """Process Load Curve data."""
    load_curve_file = os.path.join(BASE_DATA_DIR, 'load_curve', f'{date_str}.csv')
    solar_forecast_file = os.path.join(BASE_DATA_DIR, 'solar_forecast', f'{date_str}.csv')
    out_file = os.path.join(CLEANED_DATA_DIR, SUBFOLDERS['Load Curve'], f'{date_str}_load_curve.csv')
    
    if not os.path.exists(load_curve_file):
        return

    # Read Load Curve
    try:
        df_load = pd.read_csv(load_curve_file)
    except Exception as e:
        print(f"Error reading {load_curve_file}: {e}")
        return
        
    cols_to_keep = ['DateTime', 'Wind', 'SPP Biomass', 'Thermal-Oil', 'Major Hydro', 'Coal', 'Solar', 'SPP Minihydro']
    # Check if all columns exist
    missing_cols = [c for c in cols_to_keep if c not in df_load.columns]
    if missing_cols:
        print(f"Missing columns in {load_curve_file}: {missing_cols}")
        return
        
    df_load = df_load[cols_to_keep].copy()
    
    # Process Solar Forecast if available
    if os.path.exists(solar_forecast_file):
        try:
            df_solar = pd.read_csv(solar_forecast_file)
            # Omit the first row (00:00:00)
            df_solar = df_solar.iloc[1:].reset_index(drop=True)
            
            # Align rows and add pvEstimate to Solar
            min_len = min(len(df_load), len(df_solar))
            df_load.loc[:min_len-1, 'Solar'] = df_load.loc[:min_len-1, 'Solar'] + df_solar.loc[:min_len-1, 'pvEstimate'].values
            
        except Exception as e:
            print(f"Error processing solar forecast for {date_str}: {e}")
            
    df_load.to_csv(out_file, index=False)
    print(f"Processed: {out_file}")

def process_energy_data(date_str):
    """Process Energy Data."""
    in_file = os.path.join(BASE_DATA_DIR, 'energy_data', f'{date_str}.csv')
    out_file = os.path.join(CLEANED_DATA_DIR, SUBFOLDERS['Energy Data'], f'{date_str}_energy_data.csv')
    
    if not os.path.exists(in_file):
        return
        
    try:
        df = pd.read_csv(in_file)
        cols_to_keep = ['stationGroupName', 'energyGWh', 'dateTime']
        if all(c in df.columns for c in cols_to_keep):
            df = df[cols_to_keep]
            df.to_csv(out_file, index=False)
            print(f"Processed: {out_file}")
        else:
            print(f"Missing columns in {in_file}")
    except Exception as e:
        print(f"Error processing {in_file}: {e}")

def process_peak_data(date_str):
    """Process Peak Data."""
    in_file = os.path.join(BASE_DATA_DIR, 'peak_data', f'{date_str}.csv')
    out_file = os.path.join(CLEANED_DATA_DIR, SUBFOLDERS['Peak Data'], f'{date_str}_peak_data.csv')
    
    if not os.path.exists(in_file):
        return
        
    try:
        df = pd.read_csv(in_file)
        cols_to_keep = ['stationGroupName', 'activePowerMW', 'reactivePowerMvar', 'dateTime']
        if all(c in df.columns for c in cols_to_keep):
            df = df[cols_to_keep]
            df.to_csv(out_file, index=False)
            print(f"Processed: {out_file}")
        else:
            print(f"Missing columns in {in_file}")
    except Exception as e:
        print(f"Error processing {in_file}: {e}")

def process_night_peak_data(date_str):
    """Process Night Peak Data."""
    in_file = os.path.join(BASE_DATA_DIR, 'night_peak_data', f'{date_str}.csv')
    out_file = os.path.join(CLEANED_DATA_DIR, SUBFOLDERS['Night Peak Data'], f'{date_str}_night_peak_data.csv')
    
    if not os.path.exists(in_file):
        return
        
    try:
        df = pd.read_csv(in_file)
        cols_to_keep = ['stationGroupName', 'activePowerMW', 'reactivePowerMvar', 'dateTime']
        if all(c in df.columns for c in cols_to_keep):
            df = df[cols_to_keep]
            df.to_csv(out_file, index=False)
            print(f"Processed: {out_file}")
        else:
            print(f"Missing columns in {in_file}")
    except Exception as e:
        print(f"Error processing {in_file}: {e}")

def process_reservoir_data(date_str):
    """Process Reservoir Data."""
    in_file = os.path.join(BASE_DATA_DIR, 'reservoir_data', f'{date_str}.csv')
    out_file = os.path.join(CLEANED_DATA_DIR, SUBFOLDERS['Reservoir Data'], f'{date_str}_reservoir_data.csv')
    
    if not os.path.exists(in_file):
        return
        
    try:
        df = pd.read_csv(in_file)
        cols_to_keep = ['reservoirName', 'rainfallmm', 'storagePercentage', 'waterLevel', 'dateTime']
        
        if not all(c in df.columns for c in cols_to_keep):
            print(f"Missing columns in {in_file}")
            return
            
        df = df[cols_to_keep]
        
        # Delete Norton, Canyon, Laxapana
        df = df[~df['reservoirName'].isin(['Norton', 'Canyon', 'Laxapana'])].copy()
        
        # Recalculate storage percentage if it is 0
        def fix_storage_percentage(row):
            if row['storagePercentage'] == 0 or row['storagePercentage'] == 0.0:
                res_name = row['reservoirName']
                if res_name in MAX_CAPACITIES and MAX_CAPACITIES[res_name] > 0:
                    return min(100.0, (row['waterLevel'] / MAX_CAPACITIES[res_name]) * 100)
            return row['storagePercentage']
            
        df['storagePercentage'] = df.apply(fix_storage_percentage, axis=1)
        
        df.to_csv(out_file, index=False)
        print(f"Processed: {out_file}")
    except Exception as e:
        print(f"Error processing {in_file}: {e}")

def main():
    print(f"Starting data cleaning from {START_DATE} to {END_DATE}...")
    create_directories()
    dates = get_dates_to_process(START_DATE, END_DATE)
    
    for date_str in dates:
        process_load_curve(date_str)
        process_energy_data(date_str)
        process_peak_data(date_str)
        process_night_peak_data(date_str)
        process_reservoir_data(date_str)
        
    print("Data cleaning complete!")

if __name__ == '__main__':
    main()
