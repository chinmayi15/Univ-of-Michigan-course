import pandas as pd
import sys
import matplotlib.style as style
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
housing_all_cities = pd.read_csv('City_Zhvi_AllHomes.csv')
print(housing_all_cities.head())


LosAngeles = pd.DataFrame(housing_all_cities[housing_all_cities.RegionName.isin(['Los Angeles'])])
SanFrancisco = pd.DataFrame(housing_all_cities[housing_all_cities.RegionName.isin(['San Francisco'])])
Boston = pd.DataFrame(housing_all_cities[housing_all_cities.RegionName.isin(['Boston']) & housing_all_cities.State.isin(['MA'])]
)
Seattle = pd.DataFrame(housing_all_cities[housing_all_cities.RegionName.isin(['Seattle'])])
Sanjose = pd.DataFrame(housing_all_cities[housing_all_cities.RegionName.isin(['San Jose'])])
Honolulu = pd.DataFrame(housing_all_cities[housing_all_cities.RegionName.isin(['Honolulu'])])
print(LosAngeles)

MetroPol = pd.DataFrame()
MetroPol = MetroPol.append(LosAngeles)
MetroPol = MetroPol.append(SanFrancisco)
MetroPol = MetroPol.append(Boston)
MetroPol = MetroPol.append(Seattle)
MetroPol = MetroPol.append(Sanjose)
MetroPol = MetroPol.append((Honolulu))

print(MetroPol)
MetroPol = MetroPol.set_index('RegionName')

santaClaraData = housing_all_cities[housing_all_cities.CountyName.isin(['Santa Clara'])]
Boston = housing_all_cities[housing_all_cities.Metro.isin(['Boston']) & housing_all_cities.State.isin(['MA'])]

regionidx = santaClaraData['RegionName']
santaClaraData = santaClaraData.set_index('RegionName')

year = list(MetroPol)
year = year[5:]

df = pd.DataFrame()
df = MetroPol.transpose()

df = df.drop(df.index[[0, 1, 2, 4, 4,]])

df = df.transpose()
df = df.drop('CountyName', axis=1)
print(df)
df = df.transpose()
# df.columns = pd.to_datetime(df.columns)
cmap = cm.get_cmap('Spectral')
ax = df.plot.line(cmap=cmap)
ax.set_xlabel("Year")
ax.set_ylabel("Average house cost in US$")
year = range(1996, 2017)
year_loc = range(0,245,12)
plt.legend(frameon=False)
plt.title('Average house price for last 20 years in Los Angeles, San Franciso, Boston, Seattle, San Jose and Honolulu of United States')
#plt.subtitle('The cities are Los Angeles, San Franciso, Boston, Seattle, San Jose and Honolulu ', y=1.05, fontsize=18)
print(year)
print(year_loc)
ax.set_xticks(year_loc)
ax.set_xticklabels(year)


plt.grid( linewidth='0.2', color='Lightgrey')
plt.show()