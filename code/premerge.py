# -*- coding: utf-8 -*-
"""
Created on Mon Apr 02 21:00:12 2018

@author: huanghongjia
"""

# merge point intervals into an hour

import numpy as np

from collections import Counter

def districtnum(lon, lat, lon_int, lat_int): # lon经度   lat纬度
    lonmin = 115.45
    latmin = 39.44
    lon_index = int((lon-lonmin)/lon_int)
    lat_index = int((lat-latmin)/lat_int)
    if lon_index < 10:
        lon_index = '00'+str(lon_index)
    elif lon_index < 100:
        lon_index = '0'+str(lon_index)
    else:
        lon_index = str(lat_index)
    if lat_index < 10:
        lat_index = '00'+str(lat_index)
    elif lat_index < 100:
        lat_index = '0'+str(lat_index)
    else:
        lat_index = str(lat_index)            
    district = lat_index + lon_index
    return district

lonmin = 115.45
lonmax = 116.92
latmin = 39.44
latmax = 41

lon_interval = (lonmax - lonmin)/100
lat_interval = (latmax - latmin)/100

trace = list(np.load('./data/trace.npy'))
trace_length = len(trace)

trace_merge = []
count = []

for i in range(trace_length):
    trace_merge.append([])
    count.append([])
    ilength = len(trace[i])
    flag = 0
    check_district = []
    for j in range(ilength):
        try:
            curtime = trace_merge[i][-1][0]
        except IndexError:
            trace_merge[i].append([trace[i][j][0][:-2],[],0])

        if j > 0 and trace[i][j-1][6]:
            flag = 1
            check_district.append(district)
        district = districtnum(trace[i][j][2],trace[i][j][4],lon_interval,lat_interval)
        
        if trace[i][j][0][:-2] == trace_merge[i][-1][0]:
            trace_merge[i][-1][1].append(district)
            if j == ilength - 1:
                if flag:
                    trace_merge[i][-1][1] = Counter(check_district).most_common()[0][0]
                    trace_merge[i][-1][2] = 1
                else:
                    trace_merge[i][-1][1] = Counter(trace_merge[i][-1][1]).most_common()[0][0]
                    trace_merge[i][-1][2] = 0
                count[-1].append(trace_merge[i][-1][2])
        else:
            if flag:
                trace_merge[i][-1][1] = Counter(check_district).most_common()[0][0]
                trace_merge[i][-1][2] = 1
            else:
                trace_merge[i][-1][1] = Counter(trace_merge[i][-1][1]).most_common()[0][0]
                trace_merge[i][-1][2] = 0
            count[-1].append(flag)
            flag = 0
            trace_merge[i].append([trace[i][j][0][:-2],[],0])
            trace_merge[i][-1][1].append(district)
            if j == ilength - 1:
                trace_merge[i][-1][1] = Counter(trace_merge[i][-1][1]).most_common()[0][0]
                trace_merge[i][-1][2] = trace[i][j][6]
                count[-1].append(trace_merge[i][-1][2])

#if __name__ == "__main__":
#    np.save('./data/trace_merge.npy',trace_merge)
#    np.save('./data/countinhour.npy',count)
            