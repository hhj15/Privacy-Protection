# -*- coding: utf-8 -*-
"""
Created on Mon Apr 02 19:00:05 2018

@author: huanghongjia
"""

import numpy as np
import matplotlib.pyplot as plt

#def districtnum(lon, lat, lon_int, lat_int): # lon经度   lat纬度
#    lonmin = 115.45
#    latmin = 39.44
#    lon_index = int((lon-lonmin)/lon_int)
#    lat_index = int((lat-latmin)/lat_int)
#    return lon_index, lat_index
#
lonmin = 115.45
lonmax = 116.92
latmin = 39.44
latmax = 41

lon_interval = (lonmax - lonmin)/100
lat_interval = (latmax - latmin)/100
               
trace = list(np.load('./data/test_trace_merge.npy'))

distribution = []

trace_length = len(trace)
for i in range(trace_length):
    distribution.append([])
    ilength = len(trace[i])
    for j in range(ilength):
#        lon, lat = districtnum(trace[i][j][2],trace[i][j][4],lon_interval,lat_interval)
#        for i in [lon,lat]:
#            if i < 10:
#                i = '00'+str(i)
#            elif i < 100:
#                i = '0'+str(i)
#            else:
#                i = str(i)
                
        district = int(trace[i][j][1][0:3])*100+int(trace[i][j][1][3:])
        if district in distribution[i]:
            continue
        else:
            distribution[i].append(district)

countplt = [0]*10000
for i in distribution:
    for j in i:
        countplt[j] = countplt[j] + 1

plt.plot(countplt)