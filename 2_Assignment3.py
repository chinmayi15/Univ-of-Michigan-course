import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import math
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650),
                   np.random.normal(43000,100000,3650),
                   np.random.normal(43500,140000,3650),
                   np.random.normal(48000,70000,3650)],
                  index=[1992,1993,1994,1995])
# df


plt.figure()
df.describe()
mean = df.mean(axis=1)
std = df.std(axis=1)
squarert = math.sqrt(len(df.columns))
standard_error = std/squarert
C=1.96

x= np.arange(len(df.index))
margin_of_error = standard_error* C

confidence_interval = (mean - margin_of_error, mean + margin_of_error)
#confidence_interval

color = []
yaxisValue = 41861.8595411#39000
for index_val, series_val in mean.iteritems():
    print series_val
    if yaxisValue < (series_val +1.0) and yaxisValue > (series_val -1.0):
        color.append('Green')
    elif yaxisValue > series_val:
        color.append('Red')
    elif yaxisValue < series_val:
        color.append('Blue')


print color
mask1 = mean < yaxisValue
mask2 = mean >= yaxisValue

fig = plt.figure()
ax = fig.add_subplot(111)
norm = matplotlib.colors.Normalize(30e3, 60e3)
# plt.bar(x[mask1], mean[mask1], color = 'red')
# plt.bar(x[mask2], mean[mask2], color = 'blue')

#bar = ax.bar(x, mean, color=color, edgecolor='Black', yerr = margin_of_error, error_kw=dict(ecolor='gray', lw=2, capsize=5, capthick=2)) #,color=plt.cm.plasma_r(norm(mean)))
bar = plt.bar(x, mean, color=color, edgecolor='Black', yerr = margin_of_error, error_kw=dict(ecolor='gray', lw=2, capsize=5, capthick=2)) #,color=plt.cm.plasma_r(norm(mean)))

# plt.colorbar()
plt.xticks(x, df.index)
#ax.legend(bar[0], 'Red' ,loc="lower right", bbox_to_anchor=(1., 1.02) , borderaxespad=0., ncol=2)

ax.axhline(yaxisValue, color="gray")
ax.text(1.02, yaxisValue, str(yaxisValue), va='center', ha="left", bbox=dict(facecolor="w",alpha=0.5),transform=ax.get_yaxis_transform())
data = pd.DataFrame(std)
data.columns = ['STD']
#cax = fig.add_axes([0.27, 0.8, 0.5, 0.05])

# fig.colorbar(bar, cax=cax, orientation='horizontal')
#cbar = fig.colorbar(bar, ax=ax, cax=ax, cmap =color, orientation='horizontal')
# fig.colorbar()
# fig, ax = plt.subplots()
#im = ax.imshow(data, cmap='gist_earth')
plt.show(block=True)
