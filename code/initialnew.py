# -*- coding: utf-8 -*-
"""
Created on Sun Apr 01 16:57:49 2018

@author: huanghongjia
"""

import numpy as np
import re

f = open("checkin_trace","r")

content = f.readlines()
trace_in = []
trace = []
count = []
   
for i in range(len(content)):
    trace_in.append(content[i].split("\t")[1].split(";"))
    trace.append([])
    count.append([])
    length = len(trace_in[i])
    for j in range(length):
        trace[-1].append(trace_in[i][j].split(","))
        if (float(trace[-1][-1][1]) <= 116.92 and float(trace[-1][-1][1]) >= 115.45) and (float(trace[-1][-1][2]) >= 39.44 and float(trace[-1][-1][2]) <= 41):
            continue
        else:
            del trace[-1][-1]
    if trace[-1]:
        length = len(trace[-1])
    else:
        del trace[-1]
        del count[-1]
        continue
    for k in range(length):
        trace[-1][k][0] = re.sub("\D", "", trace[-1][k][0])
        trace[-1][k][0] = trace[-1][k][0][:-2]
        trace[-1][k][1] = float(trace[-1][k][1])
        trace[-1][k][2] = float(trace[-1][k][2])
        trace[-1][k][3] = int(trace[-1][k][3])
        trace[-1][k].insert(2,trace[-1][k][1])
        trace[-1][k].insert(4,trace[-1][k][3])
        trace[-1][k].insert(1,trace[-1][k][0])
        count[-1].append(trace[-1][k][6])

if __name__ == "__main__":
    np.save('trace.npy',trace)
    np.save('count.npy',count)