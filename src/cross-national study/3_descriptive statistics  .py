import pandas as pd
import os
data_folder = '../../data/processed/cross-national study'
df = pd.read_csv(f"{data_folder}/merged_agri_climate_control.csv")
df.describe()
missing_rate = df.isnull().mean().sort_values(ascending=False).to_frame(name="Missing Rate")
yearly_counts = df["Year"].value_counts().sort_index()