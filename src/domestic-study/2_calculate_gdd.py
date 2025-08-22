"""
Project: Agroclimatic Analysis using GDD (Growing Degree Days)
Script: calculate_gdd.py
Author: Yu Kaijin

Purpose:
---------
This script calculates the annual Growing Degree Days (GDD) for three major cities
in Northeastern China — Harbin, Changchun, and Shenyang — from 2005 to 2023 using 
daily temperature data from NASA POWER.

Why these cities?
------------------
These three cities represent the capital cities of Heilongjiang, Jilin, and Liaoning
— the three provinces collectively known as "Dongbei" (Northeast China), which are 
important agricultural regions. They are chosen because:
1. They have relatively reliable climate data coverage;
2. Each serves as a representative point of their respective province;
3. Many crops (e.g., maize, soybeans) are commonly grown across all three provinces.

Why GDD?
---------
GDD (Growing Degree Days) is a widely used agroclimatic indicator that reflects 
the accumulated heat necessary for plant growth. It is defined as:

    GDD = max(0, (T_max + T_min)/2 - T_base)

In this case, we use a base temperature (T_base) of 10°C, which is common for 
temperate crops. GDD is an effective proxy for assessing how climate variability 
impacts crop development and yield, especially in empirical regression analysis.

Output:
--------
The script will generate:
1. Daily temperature files for each city and year;
2. A summary CSV file containing annual GDD totals for each city.

This dataset can then be matched with province-level crop yield data to explore 
climate-yield relationships via econometric models.
"""

import os
import pandas as pd

# 设置路径
input_dir = "../data/raw/domestic_study_data/nasa_power_gdd_raw"
output_file = "../data/processed/domestic_study_data/annual_gdd_summary.csv"
T_BASE = 10  # 基准温度

# 结果存储列表
summary = []

# 遍历文件夹中所有文件
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        parts = filename.replace(".csv", "").split("_")
        city = parts[0]
        year = parts[1]

        path = os.path.join(input_dir, filename)
        try:
            df = pd.read_csv(path, skiprows=10)  # 跳过前10行metadata
            tmax = df["T2M_MAX"]
            tmin = df["T2M_MIN"]

            gdd = ((tmax + tmin) / 2 - T_BASE).clip(lower=0)
            total_gdd = gdd.sum()

            summary.append({
                "City": city,
                "Year": int(year),
                "Annual_GDD": round(total_gdd, 2)
            })

        except Exception as e:
            print(f"Error processing {filename}: {e}")

# 输出整理结果
summary_df = pd.DataFrame(summary)
summary_df.sort_values(["City", "Year"], inplace=True)
summary_df.to_csv(output_file, index=False)