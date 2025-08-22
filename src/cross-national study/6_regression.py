import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

data_folder = '../../data/processed/cross-national study'
climate_df = pd.read_csv(f"{data_folder}/climate_data.csv")
agri_df = pd.read_csv(f"{data_folder}/agricultural_production_data_LongPanel.csv")
control_df = pd.read_csv(f"{data_folder}/four_country_control_variables.csv")
# (1) Climate cross-national study: Calculate average annual temperature by country and year
climate_avg = climate_df.groupby(['Country', 'Year'], as_index=False)[
    ['Temperature (°C)', 'Precipitation (mm)']
].mean()

climate_avg.rename(columns={
    'Temperature (°C)': 'Avg_Temperature',
    'Precipitation (mm)': 'Avg_Precipitation'
}, inplace=True)


# (2) Filter for rows where Element = 'Production' and aggregate total production
agri_prod = agri_df[agri_df['Element'] == 'Production']
agri_total = agri_prod.groupby(['Area', 'Year'], as_index=False)['Value'].sum()
agri_total.rename(columns={'Area': 'Country', 'Value': 'Total_Production'}, inplace=True)

# (3) Control variables: Rename country column for consistency
control_df.rename(columns={'countryname': 'Country'}, inplace=True)


# Merge agricultural cross-national study with climate cross-national study
merged_df = pd.merge(agri_total, climate_avg, on=['Country', 'Year'], how='inner')
# Merge with control variables
merged_df = pd.merge(merged_df, control_df, on=['Country', 'Year'], how='inner')
# List of variables to be log-transformed
log_vars = ['Total_Production', 'Real GDP per capita', 'Nominal GDP', 'Population',
            'Government expenditure (%GDP)', 'Government revenue (%GDP)']
# Remove any rows with non-positive values before applying logarithm
for var in log_vars:
    merged_df = merged_df[merged_df[var] > 0]
# Create new columns for log-transformed variables
merged_df['Log_Total_Production'] = np.log(merged_df['Total_Production'])
merged_df['Log_GDP_per_capita'] = np.log(merged_df['Real GDP per capita'])
merged_df['Log_Nominal_GDP'] = np.log(merged_df['Nominal GDP'])
merged_df['Log_Population'] = np.log(merged_df['Population'])
merged_df['Log_Gov_Expenditure'] = np.log(merged_df['Government expenditure (%GDP)'])
merged_df['Log_Gov_Revenue'] = np.log(merged_df['Government revenue (%GDP)'])

# Create and save a correlation heatmap for selected numeric columns
corr_matrix = merged_df[[
    'Log_Total_Production', 'Avg_Temperature','Avg_Precipitation',
    'Log_GDP_per_capita', 'Log_Nominal_GDP', 'Log_Population',
    'Inflation (%)', 'Unemployment (%)',
    'Log_Gov_Expenditure', 'Log_Gov_Revenue']].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', square=True)
plt.title('Correlation Matrix of Key Variables')
plt.tight_layout()
plt.show()
plt.close()

# Define independent variables (including climate and control variables)
X = merged_df[['Avg_Temperature','Avg_Precipitation',
               'Log_GDP_per_capita', 'Log_Nominal_GDP', 'Log_Population',
               'Inflation (%)', 'Unemployment (%)',
               'Log_Gov_Expenditure', 'Log_Gov_Revenue']]

# Define dependent variable (log of total agricultural production)
y = merged_df['Log_Total_Production']

# Add a constant term to the model for the intercept
X = sm.add_constant(X)

# Fit the OLS regression model
model = sm.OLS(y, X, missing='drop')
results = model.fit()

# Print the summary of regression results
print("\n[Regression Results]\n", results.summary())


import matplotlib.pyplot as plt

# 提取回归结果（使用 summary2 得到结构化 DataFrame）
summary_df = results.summary2().tables[1].reset_index()
summary_df.rename(columns={
    'index': 'Variable',
    'Coef.': 'Coefficient',
    '[0.025': 'Lower_CI',
    '0.975]': 'Upper_CI'
}, inplace=True)

# 排序：将气温和降水放最上方
climate_vars = ['Avg_Temperature', 'Avg_Precipitation']
other_vars = [v for v in summary_df['Variable'] if v not in climate_vars + ['const']]
final_order = climate_vars + other_vars

# 去掉常数项并按顺序排序
summary_df = summary_df[summary_df['Variable'] != 'const']
summary_df['Variable'] = pd.Categorical(summary_df['Variable'], categories=final_order[::-1], ordered=True)
summary_df = summary_df.sort_values('Variable')

# 计算误差棒
summary_df['xerr_low'] = (summary_df['Coefficient'] - summary_df['Lower_CI']).abs()
summary_df['xerr_high'] = (summary_df['Upper_CI'] - summary_df['Coefficient']).abs()

# 绘制图形
plt.figure(figsize=(10, 6))
plt.errorbar(
    summary_df['Coefficient'], summary_df['Variable'],
    xerr=[summary_df['xerr_low'], summary_df['xerr_high']],
    fmt='o', color='blue', ecolor='gray', capsize=5
)

plt.axvline(x=0, color='red', linestyle='--', label='Zero Effect')
plt.title('OLS Regression Coefficients with 95% Confidence Interval')
plt.xlabel('Coefficient')
plt.ylabel('Variable')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

#Two-Way Fixed Effects Regression
from linearmodels.panel import PanelOLS

merged_df = merged_df.rename(columns={
    'Inflation (%)': 'Inflation',
    'Unemployment (%)': 'Unemployment'
})

formula = (
    'Log_Total_Production ~ Avg_Temperature + Avg_Precipitation + '
    'Log_GDP_per_capita + Log_Nominal_GDP + Log_Population + '
    'Inflation + Unemployment + '
    'Log_Gov_Expenditure + Log_Gov_Revenue + '
    'EntityEffects + TimeEffects'
)
model = PanelOLS.from_formula(formula, data=merged_df)
results = model.fit(cov_type='clustered', cluster_entity=True)

print(results.summary)

import matplotlib.pyplot as plt
import pandas as pd

# Step 1: 提取系数与标准误
params = results.params
stderr = results.std_errors

# Step 2: 构造 DataFrame
df = pd.DataFrame({
    'Variable': params.index,
    'Coefficient': params.values,
    'StdErr': stderr.values
})

# 去除固定效应变量
df = df[~df['Variable'].str.contains('Effect')]
df = df[df['Variable'] != '']

# 计算置信区间
df['Lower_CI'] = df['Coefficient'] - 1.96 * df['StdErr']
df['Upper_CI'] = df['Coefficient'] + 1.96 * df['StdErr']

# Step 3: 排序，气候变量放最上方
climate_vars = ['Avg_Temperature', 'Avg_Precipitation']
other_vars = [v for v in df['Variable'] if v not in climate_vars]
final_order = climate_vars + other_vars
df['Variable'] = pd.Categorical(df['Variable'], categories=final_order[::-1], ordered=True)
df = df.sort_values('Variable')

# Step 4: 绘图
plt.figure(figsize=(10, 6))
plt.errorbar(
    df['Coefficient'], df['Variable'],
    xerr=[(df['Coefficient'] - df['Lower_CI']).abs(),
          (df['Upper_CI'] - df['Coefficient']).abs()],
    fmt='o', color='green', ecolor='gray', capsize=5
)

plt.axvline(x=0, color='red', linestyle='--', label='Zero Effect')
plt.title('Fixed Effects Regression Coefficients (95% CI)')
plt.xlabel('Coefficient')
plt.ylabel('Variable')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()


