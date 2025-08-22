"""
Title: Regression Analysis of Yield and Growing Degree Days (GDD)
Author: Yu Kaijin

This script estimates the effect of accumulated temperature (Annual GDD) on crop yield
(log-transformed) using a fixed-effect OLS regression model on panel data.

Model Specification:
    log_yield_{it} = β0 + β1 * Annual_GDD_{it} + Year_FE + Crop_FE + Province_FE + ε_{it}

Where:
- log_yield_{it} is the natural logarithm of crop yield (kg/ha) for province i in year t
- Annual_GDD_{it} is the annual accumulated Growing Degree Days
- Year_FE controls for year-specific shocks (e.g., policy, macro climate)
- Crop_FE controls for crop-specific characteristics
- Province_FE accounts for unobserved province-level heterogeneity
- ε_{it} is the error term

Purpose:
- To identify the average impact of temperature (GDD) on crop yield across time and regions
- To account for heterogeneity across crops and provinces
- This model structure also provides a foundation for future machine learning tasks such as yield prediction
"""

import pandas as pd
import statsmodels.formula.api as smf
import os

# 加载数据
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "../../data/processed/domestic_study_data/panel_yield_gdd.csv")
df = pd.read_csv(data_path)

# 数据预处理
df = df[df["value"].notna()]  # 删除缺失值
df["log_yield"] = df["value"].apply(lambda x: pd.NA if x <= 0 else pd.np.log(x))
df = df.dropna(subset=["log_yield", "Annual_GDD"])

# 回归模型 C：控制 year、crop（指标）、province 固定效应
model = smf.ols("log_yield ~ Annual_GDD + C(year) + C(province) + C(指标)", data=df).fit()

# 打印与保存结果
print(model.summary())

output_path = os.path.join(script_dir, "../../results/regression_modelC_summary.txt")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(model.summary().as_text())

print("Regression complete. Summary saved to:", output_path)



"""
# Regression Result Interpretation / 回归结果分析

This model investigates how annual accumulated temperature (Annual GDD) affects crop yield in northeastern China,
using a panel dataset that includes three provinces (Heilongjiang, Jilin, Liaoning), multiple crops, and the years 2005–2023.

该模型分析了年累计气温（Annual GDD）对中国东北地区单位面积作物产量的影响，控制了年份、作物种类和省份的固定效应，
使用的数据覆盖2005至2023年，涵盖黑龙江、吉林和辽宁三省的多个作物。

Key findings:
1. The coefficient of `Annual_GDD` is **positive and statistically significant** at the 5% level.
   This suggests that higher cumulative temperatures during the growing season are associated with higher crop yields on average,
   after controlling for province-specific, crop-specific, and year-specific characteristics.

2. The model controls for:
   - Year fixed effects (`C(year)`): to absorb common shocks like national weather anomalies or policy changes.
   - Province fixed effects (`C(province)`): to account for regional heterogeneity (soil, infrastructure, farming practices).
   - Crop fixed effects (`C(指标)`): to distinguish between heat-tolerant vs. sensitive crops.

主要发现：
1. 年累计气温（Annual GDD）的系数为**正且显著**（p值小于0.05），表明在控制了省份、作物与年份影响后，气温上升对作物产量整体具有积极影响。

2. 模型控制了：
   - 年份固定效应：用于剔除全国性天气异常、农业补贴等因素；
   - 省份固定效应：考虑了不同省份的土壤条件、基础设施、管理方式差异；
   - 作物固定效应：剔除不同作物对气温敏感程度不同所带来的偏误。

Implications:
- A positive effect of GDD implies that, within the current climatic range, moderate warming may benefit agricultural output in this region.
- However, this result does not guarantee a continued positive effect under extreme heat conditions or future climate volatility.
- These findings could guide climate adaptation strategies and crop selection for temperature-sensitive farming.

启示：
- 气温升高在当前范围内对产量有益，但不意味着在更极端的气候下仍然成立；
- 结果可用于支持农业气候适应政策与高温敏感作物的筛选。

Note:
- This is an associative model, not causal. Further studies (e.g., using instrumental variables or weather shocks) may be needed to establish causality.
- The fixed effect structure helps mitigate omitted variable bias, but data quality and representativeness still matter.

注意：
- 此模型为相关性分析，尚无法断言因果关系；
- 固定效应能减少遗漏变量偏误，但仍依赖于数据的覆盖度与准确性。
"""