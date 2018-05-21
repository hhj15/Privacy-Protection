# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 17:04:33 2018

@author: huanghongjia
"""

import numpy as np

if __name__ == "__main__":
    trace_merge = list(np.load('./data/test_trace_merge.npy'))

    length = len(trace_merge)
    bin_code = []
    #time_window = 16    #滑动窗口长8h
    time_interval = 1  #滑动粒度为1h
    
    
    for i in range(length):
        bin_code.append([0]*(31*24))
        for j in range(len(trace_merge[i])):
            num = (int(trace_merge[i][j][0][-4:-2])-1)*24+int(trace_merge[i][j][0][-2:])
            a = int(trace_merge[i][j][1][0:3])
            b = int(trace_merge[i][j][1][3:]) 
    #        bin_code[-1][num] = int(bin_code[-1][num][0:(100*a+b)]+'1'+bin_code[-1][num][1+(100*a+b):],2) 2**(9999-100*a-b)
            bin_code[-1][num] = 2**(160*170-160*a-b)
    
    np.save('./data/test_bin_code.npy',bin_code)