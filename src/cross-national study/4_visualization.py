# Part 4: visualization
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
data_folder = '../../data/processed/cross-national study'
df = pd.read_csv(f"{data_folder}/merged_agri_climate_control.csv")
## 4.1 Time series
plt.figure(figsize=(12, 6), dpi=300)
sns.lineplot(data=df, x="Year", y="Temperature (°C)", hue="Country", errorbar=None)
plt.title("Time Series of Average Temperature", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Temperature (°C)")
plt.grid(True)

plt.savefig("temperature_trend_highres.png", dpi=300)

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6), dpi=150)  # 高分辨率

sns.lineplot(
    data=df,
    x="Year",
    y="Precipitation (mm)",
    hue="Country",
    errorbar=None,
    linewidth=2
)

plt.title("Annual Precipitation by Country", fontsize=16, weight='bold')
plt.xlabel("Year", fontsize=12)
plt.ylabel("Precipitation (mm)", fontsize=12)

plt.legend(title="Country", fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("Annual Precipitation by Country.png", dpi=300)


## 4.2 Bar plot

import matplotlib.pyplot as plt
import seaborn as sns

crop_avg = df.groupby("Item")["Value"].mean().sort_values(ascending=False).head(10).reset_index()

# 图像设置
plt.figure(figsize=(12, 6), dpi=150)

# 显式指定 hue
ax = sns.barplot(data=crop_avg, x="Value", y="Item", hue="Item", dodge=False, palette="viridis", legend=False)

# 添加数值标签
ax.bar_label(container=ax.containers[0], fmt="%.0f", padding=3, fontsize=10)

# 标题与坐标轴
plt.title("Top 10 Crops by Average Production", fontsize=16, weight="bold")
plt.xlabel("Average Production (tons)", fontsize=12)
plt.ylabel("Crop", fontsize=12)

# 网格与布局
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("Top 10 Crops by Average Production.png", dpi=300)


## 4.3 Scatter plots

import matplotlib.pyplot as plt
import seaborn as sns

# 只选取一个代表性作物（例如 Wheat）
crop_name = "Wheat"  # 你也可以替换成 'Rice', 'Maize', 'Barley' 等
df_crop = df[df["Item"] == crop_name]

# 绘图
plt.figure(figsize=(10, 6), dpi=150)
sns.scatterplot(
    data=df_crop,
    x="Temperature (°C)",
    y="Value",
    hue="Country",
    alpha=0.6,
    edgecolor="w",
    s=60,
    palette="Set2"
)
plt.title(f"{crop_name} Yield vs. Temperature", fontsize=16, weight="bold")
plt.xlabel("Average Annual Temperature (°C)", fontsize=12)
plt.ylabel("Crop Yield (tons)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()

plt.savefig("Wheat Yield vs. Temperature.png", dpi=300)