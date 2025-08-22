# graspp_2025_agriecon

# Group member
We are the students from the Department of Agricultural and Resource Economics!

- *Paige Koizumi*
- *Yu Kaijin*
- *Ren Haiyin*
- *Wang Yijin*
- *Deng Yuting*
- *Liao Yan*
- *Gong Kuiyuan*

# Bulletin board (latest update: June 26)
- We updated the notebook for the **Cross-national study** in `notebook`(data cleaning and regression included).
- We updated the data for the **Cross-national study** in `src` --> `data`.
- We made further improvements to the `README.md`, particularly expanding and refining the **Hypothesis** section.


# Research topic
Our research direction is mainly about climate change and its effect on agriculture. We plan to make two studies regarding this, they are the domestic study and the cross-national study.

**Cross-national study**:
- ***Research topic***: The Different Patterns of Climate Change and Their Impact on Agricultural Production – A Cross-National Comparison.

- ***Research Objective***: We observe that the changes in climate patterns vary from region to region. Countries like Bangladesh and the Philippines suffer more than other countries because of their geographical location and poorer economy (i.e., More typhoons and extremely high temperatures, but not enough preventive actions). On the other hand, countries in Europe may suffer less since they have better infrastructure and adaptability towards climate change and fewer natural disasters inflicted on them. Therefore, the difference among countries exists; we want to address the different patterns of climate change and their impacts on agricultural production according to countries from different continents.

- ***Country Selection***: In order to overcome a bit of the endogeneity problem, we decided to select one country from Asia and the other country from Europe that share similar conditions like GDP per capita, Population, etc, so that we can simply control for these country-level characteristics to get less biased estimation results.

- ***Empirical Method***: Regression (OLS, VAR...), forecasting (machine learning), and visualization.

- ***Data***:
  - **Data source**: FAOSTAT, World Bank.
  - **Country-level control variables**: GDP per capita, Population, Average year of education, Rate of modernization, Area of cultivated land, Rate of mechanization in agricultural production...
  - **Dependent variable**: Annual yield of wheat, Annual yield of bean...
  - **Independent variable**: Average precipitation, Average temperature...
 
- ***Hypothesis***:
  -  Higher temperatures may significantly affect the growth and productivity of specific crops, such as wheat and beans. We hypothesize that changes in key climate variables — particularly increases in average temperature and fluctuations in precipitation — lead to a measurable decline in crop yields.

  - By applying regression models such as OLS and VAR, we aim to:
    - Quantify the effect of temperature and precipitation changes on annual crop yields;
    - Identify crop-specific climate sensitivity;
    - Compare the magnitude of climate impacts between countries with similar socio-economic profiles but different climatic conditions.

    Controlling for variables such as GDP per capita, population, education level, mechanization rate, and cultivated land area, we expect to isolate the direct effects of climate change on agricultural production. This hypothesis will help uncover region-specific vulnerabilities and provide evidence to support targeted adaptation strategies in agriculture.  

- ***Gourp members assigned to this study***:
  - Yijing san
  - Liaoyan san
  - Haiyin san
  - Kuiyuan san

**Domestic study**
- ***Research topic***: The Impact of Extreme Weather on Regional Agricultural Production - A study based on Dongbei Province.

- ***Research Objective***: China is one of the biggest countries in the world, which has a vast area for agriculture. As climate change deteriorated, there have been more and more cases of extreme weather in recent years (i.e., Henan Zhengzhou Extreme Rainstorm in 2021, Hainan Super Typhoon in 2024). Agriculture is significantly sensitive to not only extreme weather, like what we mentioned above, but also climate pattern changes like temperatures and precipitation. Therefore, we firstly aim to address the impact of extreme weather on regional agricultural production and reveal the underlying mechanisms. Secondly, we also expect to discover the change in climate patterns and their impact on crop yield.

- ***Sample Selection***: We plan to select those provinces or municipalities that have a history of certain kinds of crops, like wheat, therefore, we can exclude other confounding factors but only focus on the shock of extreme weather.

- ***Empirical Method***: Regression (OLS, DID...), forecasting (machine learning), and visualization.

- ***Data***:
  - **Data source**: Yield datasets were downloaded from NBS, and the weather datasets were obtained from NASA.
  - **Dependent variable**: Wheat yield, sorghum yield...
  - **Independent variable**: Growing Degree Days.
 
- ***Hypothesis***:
  - **Hypothesis 1**: Extreme weather will significantly affect the crop yield of that year, which could result in serious production and financial loss.
  - **Hypothesis 2**: Climate change exists in China and is affecting the crop yield year by year.

- ***Gourp members assigned to this study***:
  - Kaijin san
  - Paige san
  - Yuting san
 
# Data
- **Cross-national study**: FAOSTAT, World Bank.
- **Domestic study**: NBS, NASA.

# To-do list (latest update: May 23)
- Find and process the data we need for the two studies (DDL: before May 26).

# Folder standardization
**‘src‘**: code  
**‘data‘**:  
*‘raw‘: Unprocessed Data*  
*‘processed‘: Cleaned & Transformed Data*  
**‘docs‘**: Project Documentation (Readme, Reports, Presentations)  
**‘reports‘**: Output (Visualizations, Models, Summaries)  
**‘notebooks‘**: Jupyter notebooks
