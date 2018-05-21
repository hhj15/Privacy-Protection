# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 14:30:19 2018

@author: huanghongjia
"""

import numpy as np

# 寻找checkin点具体内容

if __name__ == "__main__":
    trace = list(np.load('./data/trace_merge_8211.npy'))
    count = list(np.load('./data/countinhour_8211.npy'))
    count_sp = []
    cnt_num = []
    
    length = len(trace)
    for i in range(length):
        count_sp.append([])
        cur_cnt = count[i]
        cur_len = len(count[i])
        for j in range(cur_len):
            if count[i][j]:
                count_sp[i].append([trace[i][j][0],trace[i][j][1]])
    
    
    for i in range(length):
        cnt_num.append(len(count_sp[i]))
    
    np.save('./data/cnt_num_8211.npy',cnt_num)
    np.save('./data/countinhour_sp_8211.npy',count_sp)