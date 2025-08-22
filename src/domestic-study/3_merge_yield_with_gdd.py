# -------------------------------------------------------------
# Script: merge_yield_with_gdd.py
# Author: Deng Yuting, Koizumi Paige, Yu Kaijin
# Project: Agroclimatic Analysis on Northeastern China
# Purpose:
#     Merge provincial crop yield data with annual Growing Degree Days (GDD)
#     to build a panel dataset suitable for regression and machine learning.
#
# Data Sources:
# 1. Crop Yield Data:
#     - Original data comes from the Agricultural Statistical Yearbooks
#       published by the National Bureau of Statistics of China (NBS).
#     - Covers annual crop yields (kg/ha) for Heilongjiang, Jilin, and Liaoning provinces.
#     - All tables were manually extracted, cleaned, and saved as UTF-8 encoded CSV files
#       under: `data/raw/domestic_study_data/`.
#
# 2. GDD Data:
#     - Derived from daily NASA POWER API downloads for the representative cities:
#         Harbin (Heilongjiang), Changchun (Jilin), Shenyang (Liaoning).
#     - Daily max/min temperatures were aggregated into annual Growing Degree Days (base=10°C).
#     - Final GDD summary is stored as: `annual_gdd_summary.csv`.
#
# Output:
#     - A panel dataset saved as `panel_yield_gdd.csv`.
#     - Columns include:
#         - province: Province name
#         - year: Year
#         - 指标: Yield indicator (e.g., 粮食单位面积产量(公斤/公顷))
#         - value: Yield value
#         - Annual_GDD: Accumulated GDD for that province-year
#
# Applications:
#     - This dataset is used to study the impact of climate change (GDD) on crop productivity.
#     - Regression models (e.g., province and year fixed effects) can be applied to estimate effects.
#     - This structured format is also suitable for future applications of machine learning models,
#       such as predicting yields under climate scenarios, or classifying climate-sensitive crops.
#
# Note:
#     This script is fully reproducible and path-resilient (uses relative paths based on script location).
# -------------------------------------------------------------

import pandas as pd
import os

# 获取当前脚本的绝对路径，并定位到 data 文件夹
script_dir = os.path.dirname(os.path.abspath(__file__))
raw_dir = os.path.join(script_dir, "../../data/raw/domestic_study_data")
processed_dir = os.path.join(script_dir, "../../data/processed/domestic_study_data")

# 读取数据
heilongjiang = pd.read_csv(os.path.join(raw_dir, "Heilongjiang_yield_clean.csv"))
jilin = pd.read_csv(os.path.join(raw_dir, "Jilin_yield_clean.csv"))
liaoning = pd.read_csv(os.path.join(raw_dir, "Liaoning_yield_clean.csv"))
gdd = pd.read_csv(os.path.join(processed_dir, "annual_gdd_summary.csv"))

# 添加省份
heilongjiang["province"] = "Heilongjiang"
jilin["province"] = "Jilin"
liaoning["province"] = "Liaoning"

# 合并产量数据
df = pd.concat([heilongjiang, jilin, liaoning], ignore_index=True)

# 宽转长
df_long = df.melt(id_vars=["指标", "province"], var_name="year", value_name="value")
df_long["year"] = df_long["year"].str.extract(r'(\d{4})')  # 提取年份字符串
df_long = df_long.dropna(subset=["year"])                 # 删除year列为NaN的行
df_long["year"] = df_long["year"].astype(int)             # 再转为整数

# 城市对应省份
gdd["province"] = gdd["City"].map({
    "Harbin": "Heilongjiang",
    "Changchun": "Jilin",
    "Shenyang": "Liaoning"
})

# 合并 GDD
panel = pd.merge(df_long, gdd[["province", "Year", "Annual_GDD"]],
                 left_on=["province", "year"],
                 right_on=["province", "Year"],
                 how="left").drop(columns=["Year"])

# 保存
output_path = os.path.join(script_dir, "../../data/processed/domestic_study_data/panel_yield_gdd.csv")
panel.to_csv(output_path, index=False)