#Assignment 4

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from scipy import stats
#get list of university towns
University_Town = pd.read_csv('university_towns.txt', sep='\n', header=None)
df = pd.DataFrame()
datadic = {}
stateName = ''
regionName =''
dataTup = []
for index, row in University_Town.iterrows():
        regionName = ''
        #print(row[0])
        if '[edit]' in row[0]:
            stateName = row[0]
            continue
        else:
            regionName = row[0]

        #if stateName in datadic.keys():
        #    print(stateName, regionName)
        #    datadic[stateName].append(regionName)
        #else:
        #    datadic[stateName] = regionName
        s = stateName.split('[')
        r = regionName.split(' (')
        tup = [s[0], r[0]]
        dataTup.append(tup)

df = pd.DataFrame(dataTup)
df.columns = ['State', 'RegionName']
University_Town = df
#print(df)
#print('Done')


#get_recession_start

gdp = pd.read_excel("gdplev.xls", skiprows=5)
gdp.rename( columns={'Unnamed: 4':'Quarter'}, inplace=True )
gdp = gdp[['Quarter','GDP in billions of chained 2009 dollars.1']]
for i in range(0, gdp.shape[0] - 1):
    if gdp['GDP in billions of chained 2009 dollars.1'][i] > gdp['GDP in billions of chained 2009 dollars.1'][i + 1] and gdp['GDP in billions of chained 2009 dollars.1'][i + 1] > \
            gdp['GDP in billions of chained 2009 dollars.1'][i + 2]:
        recession_startdate = gdp['Quarter'][i - 1]
print(recession_startdate)

#get recession end date

enddate_list = list()
for i in range(gdp.index[gdp['Quarter'] == recession_startdate][0], gdp.shape[0] - 2):
    if gdp['GDP in billions of chained 2009 dollars.1'][i] < gdp['GDP in billions of chained 2009 dollars.1'][i + 1] < gdp['GDP in billions of chained 2009 dollars.1'][i + 2]:
        enddate_list.append(gdp['Quarter'][i + 2])
recession_enddate = enddate_list[0]
print(recession_enddate)


#get recession bottom
rise_list = list()
for i in range(gdp.index[gdp['Quarter'] == recession_startdate][0], gdp.shape[0] - 2):
    if gdp['GDP in billions of chained 2009 dollars.1'][i] < gdp['GDP in billions of chained 2009 dollars.1'][i + 1] < gdp['GDP in billions of chained 2009 dollars.1'][i + 2]:
        rise_list.append(gdp['Quarter'][i + 2])
recession_enddate = rise_list[0]

row = gdp[gdp['Quarter'] == recession_startdate].index[0]
temp_min =  gdp['GDP in billions of chained 2009 dollars.1'][row]

for i in range(gdp.index[gdp['Quarter'] == recession_startdate][0], gdp.index[gdp['Quarter'] == recession_enddate][0]):
    if gdp['GDP in billions of chained 2009 dollars.1'][i] < temp_min:
        temp_min = gdp['GDP in billions of chained 2009 dollars.1'][i]
        bottomdate = gdp['Quarter'][i]
print(bottomdate)

#get convert housing data to quarters
HousingData = pd.read_csv('City_Zhvi_AllHomes.csv')
State = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
HousingData['State'] = HousingData['State'].replace(State)
Quarter_Columns = HousingData.iloc[:,51:]
#print(Quarter_Columns).head()
Quarter_Mean = (Quarter_Columns.groupby(pd.PeriodIndex(Quarter_Columns.columns, freq='Q'), axis=1).mean().rename(columns=lambda c: str(c).lower()))
#print(Quarter_Mean).head()
HousingData = HousingData[['State','RegionName']]
HousingData = HousingData.join(Quarter_Mean, how= 'outer')
HousingData.set_index(['State', 'RegionName'], inplace=True)
#print(HousingData).head()

#run_ttest

#recession_startdate
Quarter_before_recession = HousingData.columns.get_loc(recession_startdate)
cols = list(HousingData)
requiredQ = cols[Quarter_before_recession-1]
#print(requiredQ)

HousingData = HousingData[[requiredQ, bottomdate]]
HousingData['price_ratio'] = HousingData[requiredQ]/HousingData[bottomdate]
HousingData['Result'] = HousingData.apply( lambda row: 'Growth' if ['price_ratio'] <= 1 else 'Decline', axis =1 )


#print(HousingData)

UniversityTown_Inner = pd.merge(HousingData, University_Town, on=['State', 'RegionName'], how='inner')
#print(UniversityTown_Inner)
Union_University_Town = pd.merge(HousingData, University_Town, how='outer', on=['State', 'RegionName'])
#print(Union_University_Town)

#complement = Union_University_Town[Union_University_Town.isnull().any(axis=1)]

#print(complement)

Non_University_Town = Union_University_Town.drop(UniversityTown_Inner.index, axis=0)
#print(Non_University_Town).head()

#UniversityTown_Inner
#Non_University_Town
meanU = UniversityTown_Inner['price_ratio'].mean()
meanN = Non_University_Town['price_ratio'].mean()
U = UniversityTown_Inner.dropna()
N = Non_University_Town.dropna()
result = stats.ttest_ind(U['price_ratio'], N['price_ratio'])


tup = []
if(result.pvalue < 0.01):
    tup.append(True)
else:
    tup.append(False)

tup.append(result.pvalue)

if(meanU > meanN):
    tup.append('non-university town')
else:
    tup.append('university town')

print(tup)