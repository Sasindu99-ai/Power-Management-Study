"""
GenSum Data Extraction Script for EDLCare Portal
URL: https://edlcare.edl.lk/gensum/details

This script extracts daily generation summary tables and graphs from EDLCare.
It creates separate folders for each data table/graph and saves a CSV file per date (YYYY-MM-DD.csv).

Features:
- Configurable START_DATE and END_DATE.
- High-efficiency API scraping (direct fetch of backend endpoints triggered by the frontend date picker).
- Optional Playwright UI automation mode for browser-based scraping.
- Automatic creation of target component directories.
"""

import os
import sys
import time
import requests
import pandas as pd
from datetime import datetime, timedelta

# ==============================================================================
# CONFIGURATION
# ==============================================================================
# Define start date and end date (YYYY-MM-DD)
START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

# Output directory for extracted CSV data
DEFAULT_OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "gensum"
)

# Base URL and Endpoint mappings for graphs and tables on the page
BASE_URL = "https://edlcare.edl.lk"

COMPONENTS = {
    "daily-energy-summary": "daily_energy_summary",
    "daily-night-peak-power-summary": "daily_night_peak_power_summary",
    "energy-data": "energy_data",
    "load-curve": "load_curve",
    "load-curve-station-groups": "load_curve_station_groups",
    "night-peak-data": "night_peak_data",
    "notes": "notes",
    "peak-data": "peak_data",
    "reservoir-data": "reservoir_data",
    "solar-forecast": "solar_forecast",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

# ==============================================================================
# EXTRACTION FUNCTIONS
# ==============================================================================
def extract_gensum_data_api(start_date_str: str, end_date_str: str, output_dir: str = DEFAULT_OUTPUT_DIR):
    """
    Extracts data using direct backend REST API requests.
    This fetches the exact data loaded when changing the date picker on https://edlcare.edl.lk/gensum/details.
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    print(f"==================================================")
    print(f" Starting GenSum Data Extraction (API Mode)")
    print(f" Date Range: {start_date_str} to {end_date_str}")
    print(f" Output Directory: {output_dir}")
    print(f"==================================================\n")
    
    os.makedirs(output_dir, exist_ok=True)
    
    current_date = start_date
    total_dates = (end_date - start_date).days + 1
    processed_count = 0
    
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        processed_count += 1
        print(f"[{processed_count}/{total_dates}] Processing Date: {date_str}")
        
        for ep_key, folder_name in COMPONENTS.items():
            folder_path = os.path.join(output_dir, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            
            csv_file_path = os.path.join(folder_path, f"{date_str}.csv")
            url = f"{BASE_URL}/api/gensum/{ep_key}"
            
            try:
                response = requests.get(url, params={"date": date_str}, headers=HEADERS, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    
                    if isinstance(data, list) and len(data) > 0:
                        df = pd.DataFrame(data)
                    elif isinstance(data, dict) and data:
                        df = pd.DataFrame([data])
                    else:
                        df = pd.DataFrame()
                    
                    df.to_csv(csv_file_path, index=False)
                    print(f"   -> Saved {folder_name}/{date_str}.csv ({len(df)} records)")
                else:
                    print(f"   -> [HTTP {response.status_code}] Failed for component: {folder_name}")
            except Exception as exc:
                print(f"   -> [Error] Failed to fetch {folder_name}: {exc}")
                
        current_date += timedelta(days=1)
        
    print(f"\n[Completed] GenSum data extraction finished successfully!")


def extract_gensum_data_playwright(start_date_str: str, end_date_str: str, output_dir: str = DEFAULT_OUTPUT_DIR):
    """
    Alternative automation engine using Playwright browser.
    Automates loading https://edlcare.edl.lk/gensum/details and changing the date picker component.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[Error] Playwright package is not installed. Install via `pip install playwright`.")
        return

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    print(f"==================================================")
    print(f" Starting GenSum Data Extraction (Playwright Mode)")
    print(f" Date Range: {start_date_str} to {end_date_str}")
    print(f"==================================================\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            print(f"--- Navigating & Updating Date: {date_str} ---")
            
            page.goto(f"{BASE_URL}/gensum/details", wait_until="networkidle")
            
            date_input = page.query_selector('input[type="date"]')
            if date_input:
                date_input.fill(date_str)
                date_input.dispatch_event("change")
                time.sleep(3) # Wait for network requests to complete
                
            # Fetch data for current date
            extract_gensum_data_api(date_str, date_str, output_dir)
            current_date += timedelta(days=1)
            
        browser.close()

if __name__ == "__main__":
    # Execute extraction for defined START_DATE and END_DATE
    extract_gensum_data_api(START_DATE, END_DATE, DEFAULT_OUTPUT_DIR)
