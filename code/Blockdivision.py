# -*- coding: utf-8 -*-
"""
Created on Mon Apr 02 19:00:05 2018

@author: huanghongjia
"""

# Find the maximum nad minimum longitude and latitude of wechat data

import numpy as np

trace = list(np.load('trace.npy'))
length = len(trace)

lonmax = 0
lonmin = 1000
latmax = 0
latmin = 1000

for i in range(length):
    i_len = len(trace[i])
    for k in range(i_len):
        if trace[i][k][2] > lonmax:
            lonmax = trace[i][k][2]
        if trace[i][k][2] < lonmin:
            lonmin = trace[i][k][2]
        if trace[i][k][4] > latmax:
            latmax = trace[i][k][4]
        if trace[i][k][4] < latmin:
            latmin = trace[i][k][4]