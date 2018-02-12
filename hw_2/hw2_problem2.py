# -*- coding: utf-8 -*-
"""
Spyder Editor
Nick Cinko
AY250 HW2 Problem 2
Goal: Reproduce in matplotlib the provided plot stocks.png
"""

import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import rcParams
import numpy as np

#global styling parameters; Arial is close to original figure font
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams.update({'font.size':14})
rc('axes', linewidth = 2)

#read in data from text files; skip header line and separate times/values
ny_data = np.loadtxt("data/ny_temps.txt", skiprows = 1, unpack = True)
yahoo_data = np.loadtxt("data/yahoo_data.txt", skiprows = 1, unpack = True)
google_data = np.loadtxt("data/google_data.txt", skiprows = 1, unpack = True)

#create figure and first axis; weird image ratio, but it matches original by eye in my photo viewer
f, ax0 = plt.subplots(figsize=(14,11))

#set title
ax0.set_title('New York Temperature, Google, and Yahoo!', fontsize=34, fontweight='bold', fontname='Times New Roman', y=1.02)

#format dollars axis
ax0.set_xlabel('Date (MJD)', fontsize=20)
ax0.set_ylabel('Value (Dollars)', fontsize=20)

#create/format second axis (temp)
ax1 = ax0.twinx()
ax1.set_ylabel('Temperature ($^\circ$F)', fontsize=20)
ax1.set_ylim(-150,100)


#make axis ticks look pretty
ax0.minorticks_on()
ax1.minorticks_on()
ax0.tick_params(direction='in', length = 8, width = 2,  which='major', pad=10)
ax0.tick_params(direction='in', length = 4, width = 1,  which='minor')
ax1.tick_params(direction='in', length = 8, width = 2,  which='major', pad=10)
ax1.tick_params(direction='in', length = 4, width = 1,  which='minor')

#make border lines thicker
plt.setp(f.lines, linewidth=4)

#plot data
ax0.plot(yahoo_data[0], yahoo_data[1], 'indigo', label='Yahoo! Stock Value')
ax0.plot(google_data[0], google_data[1], 'b', label='Google Stock Value')
ax1.plot(ny_data[0], ny_data[1], 'r--', label='NY Mon. High Temp')

#Must combine labels from both axes before creating a single legend
lines0, labels0 = ax0.get_legend_handles_labels()
lines1, labels1 = ax1.get_legend_handles_labels()
ax1.legend(lines0 + lines1, labels0 + labels1, loc="center left", bbox_to_anchor=(0.05,0.58), frameon=False)

#save figure
#plt.savefig('stocks_mpl.png', bbox_inches='tight')

#show figure
plt.show()