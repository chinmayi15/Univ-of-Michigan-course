import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateFormatter, AutoDateLocator
import datetime as dt
from matplotlib.ticker import MaxNLocator


def leaflet_plot_stations(binsize, hashid):
    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))
    station_locations_by_hash = df[df['hash'] == hashid]
    print(station_locations_by_hash)
    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8, 8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()


# leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


def plotting():
    df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
    df = df.sort_values(by='Date')

    # remove leapyear feb-29
    df.set_index('Date', inplace=True)
    df = df[~df.index.str.endswith('02-29')]
    df2015 = df[df.index.str.startswith('2015')]
    df = df[~df.index.str.startswith('2015')]

    # print(df2015)
    df = df.reset_index()
    df2015 = df2015.reset_index()
    minTemp = df.loc[df['Element'] == 'TMIN']
    maxTemp = df.loc[df['Element'] == 'TMAX']

    minTemp15 = df2015.loc[df2015['Element'] == 'TMIN']
    maxTemp15 = df2015.loc[df2015['Element'] == 'TMAX']

    plotDataMin = minTemp.set_index(pd.DatetimeIndex(minTemp['Date'])).groupby(level=0)['Data_Value'].agg(
        {'min': np.min})
    plotDataMax = maxTemp.set_index(pd.DatetimeIndex(maxTemp['Date'])).groupby(level=0)['Data_Value'].agg(
        {'max': np.max})

    plotDataMin15 = minTemp15.set_index(pd.DatetimeIndex(minTemp15['Date'])).groupby(level=0)['Data_Value'].agg(
        {'min': np.min})
    plotDataMax15 = maxTemp15.set_index(pd.DatetimeIndex(maxTemp15['Date'])).groupby(level=0)['Data_Value'].agg(
        {'max': np.max})

    minData = pd.DataFrame(index=plotDataMin.index)
    maxData = pd.DataFrame(index=plotDataMax.index)
    minData = plotDataMin[['min']] / 10
    maxData = plotDataMax[['max']] / 10

    minData15 = pd.DataFrame(index=plotDataMin15.index)
    maxData15 = pd.DataFrame(index=plotDataMax15.index)
    minData15 = plotDataMin15[['min']] / 10
    maxData15 = plotDataMax15[['max']] / 10

    minData = minData.reset_index()
    maxData = maxData.reset_index()
    minData['Date'] = pd.to_datetime(minData['Date'])
    maxData['Date'] = pd.to_datetime(maxData['Date'])
    # print(minData)
    minDataDayofYear = minData.groupby(minData['Date'].dt.dayofyear, as_index=False).min()
    maxDataDayofYear = maxData.groupby(maxData['Date'].dt.dayofyear, as_index=False).max()

    minDataDayofYear['Date'] = minDataDayofYear['Date'].dt.strftime('%m-%d')
    maxDataDayofYear['Date'] = maxDataDayofYear['Date'].dt.strftime('%m-%d')

    minData15 = minData15.reset_index()
    maxData15 = maxData15.reset_index()
    minData15['Date'] = pd.to_datetime(minData15['Date'])
    maxData15['Date'] = pd.to_datetime(maxData15['Date'])
    # print(minData)
    minDataDayofYear15 = minData15.groupby(minData15['Date'].dt.dayofyear, as_index=False).min()
    maxDataDayofYear15 = maxData15.groupby(maxData15['Date'].dt.dayofyear, as_index=False).max()

    minDataDayofYear15['Date'] = minDataDayofYear15['Date'].dt.strftime('%m-%d')
    maxDataDayofYear15['Date'] = maxDataDayofYear15['Date'].dt.strftime('%m-%d')

    maxDataDayofYear = maxDataDayofYear.set_index('Date')
    minDataDayofYear = minDataDayofYear.set_index('Date')

    maxDataDayofYear15 = maxDataDayofYear15.set_index('Date')
    minDataDayofYear15 = minDataDayofYear15.set_index('Date')

    minDataDayofYear = minDataDayofYear[:-1]
    maxDataDayofYear = maxDataDayofYear[:-1]
    drange = range(len(minDataDayofYear.index))

    minDataDayofYear15['minAll'] = minDataDayofYear['min']
    maxDataDayofYear15['maxAll'] = maxDataDayofYear['max']

    minDataDayofYear15['min15Final'] = minDataDayofYear15.apply(
        lambda row: row['min'] if row['min'] < row['minAll'] else None, axis=1)
    maxDataDayofYear15['max15Final'] = maxDataDayofYear15.apply(
        lambda row: row['max'] if row['max'] > row['maxAll'] else None, axis=1)

    plt.scatter(drange, maxDataDayofYear15['max15Final'], color='red')
    plt.scatter(drange, minDataDayofYear15['min15Final'], color='blue')
    plt.plot(drange, minDataDayofYear['min'], color='grey')
    plt.plot(drange, maxDataDayofYear['max'], color='grey', label='_nolegend_')
    labels = maxDataDayofYear.index.values

    months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Oct', 'Nov', 'Dec']

    plt.gca().fill_between(range(len(minDataDayofYear)), minDataDayofYear['min'], maxDataDayofYear['max'],
                           facecolor='lightgrey', alpha=0.25)
    plt.title('Extreme Weather in 2015')
    ax = plt.gca()

    ax.set_ylabel('Temp in (C)')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    plt.legend(['Temperature range 2005 - 2014', 'Hotter in 2015', 'Colder in 2015'])
    # ax.plot_date(dates, maxDataDayofYear, ls='-', marker='o')
    # ax.plot_date(dates, minDataDayofYear, ls='-', marker='o')
    ax2 = ax.twinx()
    mn, mx = ax.get_ylim()
    ax2.set_ylim((mn * 1.8) + 32, (mx * 1.8) + 32)
    ax2.set_ylabel('Temp in (F)')
    ax.xaxis.set_major_locator(MaxNLocator(12))
    # plt.locator_params(numticks=12)
    ax.set_xticklabels(months)

    plt.show()


plotting()

