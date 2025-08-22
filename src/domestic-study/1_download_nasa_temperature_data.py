# --------------------------------------------
# Script: download_nasa_temperature.py
# Author: Yu Kaijin
# Purpose:
#     Download daily temperature data (T2M_MAX and T2M_MIN) from NASA POWER API
#     for three representative cities in Northeast China (Harbin, Changchun, Shenyang)
#     from 2005 to 2023.
#
# Why this matters:
#     We use this daily temperature data to compute Growing Degree Days (GDD),
#     which is a key agroclimatic indicator measuring accumulated heat relevant to crop growth.
#
# Method:
#     - For each city, we specify its latitude and longitude.
#     - For each year from 2005 to 2023, we query NASA's POWER API for daily data.
#     - The script sends requests for T2M_MAX (daily max temp) and T2M_MIN (min temp).
#     - The downloaded CSV files are saved under `nasa_power_gdd_raw/`.
#
# API Info:
#     - Source: NASA POWER (https://power.larc.nasa.gov/)
#     - Endpoint: https://power.larc.nasa.gov/api/temporal/daily/point
#     - Parameters used: T2M_MAX, T2M_MIN
#
# Notes:
#     - We use a 1-second delay between requests to avoid hitting rate limits.
#     - These CSV files are later processed to calculate daily and annual GDD values.
# --------------------------------------------

import os
import requests
import time

cities = {
    "Harbin": {"lat": 45.75, "lon": 126.63},
    "Changchun": {"lat": 43.88, "lon": 125.35},
    "Shenyang": {"lat": 41.80, "lon": 123.43}
}

start_year = 2005
end_year = 2023
output_dir = "nasa_power_gdd_raw"
os.makedirs(output_dir, exist_ok=True)

for city, info in cities.items():
    lat, lon = info["lat"], info["lon"]
    for year in range(start_year, end_year + 1):
        start = f"{year}0101"
        end = f"{year}1231"
        url = (
            f"https://power.larc.nasa.gov/api/temporal/daily/point?"
            f"parameters=T2M_MAX,T2M_MIN&community=AG&longitude={lon}&latitude={lat}"
            f"&start={start}&end={end}&format=CSV"
        )
        file_path = os.path.join(output_dir, f"{city}_{year}.csv")
        try:
            print(f"Downloading: {city} {year}")
            r = requests.get(url)
            if r.status_code == 200:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(r.text)
            else:
                print(f"Failed: {city} {year} {r.status_code}")
            time.sleep(1)  # 防止API限速
        except Exception as e:
            print(f"Error downloading {city} {year}: {e}")