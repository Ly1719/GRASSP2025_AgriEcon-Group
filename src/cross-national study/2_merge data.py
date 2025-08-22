import pandas as pd
import os

data_folder = '../../data/processed/cross-national study'
agri_df = pd.read_csv(f"{data_folder}/agricultural_production_data_LongPanel.csv")
climate_df = pd.read_csv(f"{data_folder}/climate_data.csv")
control_df = pd.read_csv(f"{data_folder}/four_country_control_variables.csv")

iso3_to_name = {
    "JPN": "Japan",
    "DEU": "Germany",
    "ESP": "Spain",
    "ITA": "Italy"
}
control_df["Country"] = control_df["Country Code"].map(iso3_to_name)
climate_control_df = pd.merge(climate_df, control_df, on=["Country", "Year"], how="inner")
agri_df = agri_df.rename(columns={"Area": "Country"})
agri_df["Year"] = agri_df["Year"].astype(int)
final_df = pd.merge(agri_df, climate_control_df, on=["Country", "Year"], how="left")
final_df = final_df.drop(columns=["Country Code", "countryname"], errors="ignore")
final_df.to_csv("merged_agri_climate_control.csv", index=False)