import pandas as pd
import os

# step1: agricultural_production_data(FAO)

data_folder = '../../data/raw/cross-national study/Agricultural Production_FAO'
df = pd.read_csv(f"{data_folder}/Agricultural Production_FAO/Production_Crops_Livestock_E_All_Data_NOFLAG.csv")
target_countries = ["Japan", "Germany", "Spain", "Italy"]
df = df[df["Area"].isin(target_countries)]
df = df[df["Element"] == "Production"]
df = df[[col for col in df.columns if "Code" not in col]]
df = df.reset_index(drop=True)

year_cols = [col for col in df.columns if col.startswith("Y")]

df_long = df.melt(
    id_vars=["Area", "Item", "Element", "Unit"],
    value_vars=year_cols,
    var_name="Year",
    value_name="Value"
)

df_long["Year"] = df_long["Year"].str.extract(r"(\d{4})")
df_long.to_csv("agricultural_production_data_LongPanel.csv", index=False)


# step2: climate_data (OWID)

import pandas as pd
import os

data_folder = '../../data/raw/cross-national study/climate_data _OWID/climate_data _OWID/monthly-average-surface-temperatures-by-year'
temp_df = pd.read_csv(f"{data_folder}/monthly-average-surface-temperatures-by-year.csv")
temp_df.head(2)
target_countries = ["Japan", "Germany", "Spain", "Italy"]
temp_df = temp_df[temp_df["Entity"].isin(target_countries)]

non_year_cols = ["Entity", "Code", "Year"]
year_cols = [col for col in temp_df.columns if col not in non_year_cols]
temp_long = temp_df.melt(
    id_vars="Entity",
    value_vars=year_cols,
    var_name="Year",
    value_name="Temperature (°C)"
)
temp_long["Year"] = temp_long["Year"].astype(int)
precip_df = pd.read_csv("average-precipitation-per-year.csv")
precip_df = precip_df[precip_df["Entity"].isin(target_countries)]
precip_df = precip_df.rename(columns={"Annual precipitation": "Precipitation (mm)"})
precip_df = precip_df[["Entity", "Year", "Precipitation (mm)"]]
merged = pd.merge(temp_long, precip_df, on=["Entity", "Year"])
merged = merged.rename(columns={"Entity": "Country"})
merged = merged[["Country", "Year", "Temperature (°C)", "Precipitation (mm)"]]
merged = merged.sort_values(by=["Country", "Year"])
merged.to_csv("climate_data.csv", index=False)


# step3: control_variables (global_macro_data)

from global_macro_data import gmd
import pandas as pd

countries = ["JPN", "DEU", "ESP", "ITA"]

variables = [
    "rGDP_pc", "nGDP", "pop", "urban", "infl",
    "unemp", "govexp", "govrev", "lifeexp", "open"
]

df = gmd(country=countries, variables=variables)
df.rename(columns={
    "ISO3": "Country Code",
    "year": "Year",
    "rGDP_pc": "Real GDP per capita",
    "nGDP": "Nominal GDP",
    "pop": "Population",
    "urban": "Urbanization (%)",
    "infl": "Inflation (%)",
    "unemp": "Unemployment (%)",
    "govexp": "Government expenditure (%GDP)",
    "govrev": "Government revenue (%GDP)",
    "lifeexp": "Life expectancy",
    "open": "Trade openness (%GDP)"
}, inplace=True)

df = df.sort_values(by=["Country Code", "Year"])
df = df[df["Year"] >= 1960]
df.to_csv("four_country_control_variables.csv", index=False)


