import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

data_folder = '../../data/processed/cross-national study'
df = pd.read_csv(f"{data_folder}/merged_agri_climate_control.csv")

# 页面标题
st.title("Cross-National Agricultural & Climate Dashboard")

# 国家 & 作物选择器
countries = df["Country"].unique()
items = df["Item"].unique()

selected_country = st.selectbox("Select a Country", sorted(countries))
selected_crop = st.selectbox("Select a Crop", sorted(items))

# 筛选数据
filtered = df[(df["Country"] == selected_country) & (df["Item"] == selected_crop)]

# 折线图：温度、降水趋势
st.subheader("Temperature(°C) Trends")
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=filtered, x="Year", y="Temperature (°C)", label="Temperature", ax=ax)
plt.title(f"Temperature in {selected_country}")
st.pyplot(fig)

st.subheader("Precipitation(mm) Trends")
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=filtered, x="Year", y="Precipitation (mm)", label="Precipitation", ax=ax)
plt.title(f"Precipitation in {selected_country}")
st.pyplot(fig)


# 数据表
st.subheader("Filtered Data Table")
st.dataframe(filtered)

# 下载按钮
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", data=csv, file_name='data.csv')
