# This Python file uses the following encoding: utf-8
"""
Created on Sat Dec 02 17:21:06 2017

@author: huanghongjia
"""
# calculate stretch to get a matrix

import numpy as np
import random
import time
#from calDistance import *


sThreshold = 20      # 空间阈值(A2-A1)^2+(B2-B1)^2
tThreshold = 8       # 时间阈值8h，最小粒度为he

start = time.time()

w_time = 0.5
w_loc = 0.5  #时空权重
                  
def Time(t1,t2):
    t_max = max(t1,t2)
    t_min = min(t1,t2)
    return (int(t_max[-4:-2])-int(t_min[-4:-2])) * 24 + int(t_max[-2:]) - int(t_min[-2:])
 
#inte = time(trace[0][2][0],trace[0][2][1],trace[4][0][0],trace[4][0][1]) 测试
def calcDistance2(A1, B1, A2, B2):
    return (A2-A1)**2+(B2-B1)**2
            
def calstretch(tr1,tr2,cnt1,cnt2):
    w1 = 0.5
    w2 = 0.5
    index1 = [k for k,v in enumerate(cnt1) if v == 1]
    index2 = [k for k,v in enumerate(cnt2) if v == 1]
    stretch = 0
    for id1 in index1:
        stretchid1 = np.ones((len(tr2),3))
        for c2 in range(len(tr2)):
            stretchid1[c2][0] = Time(tr1[id1][0],tr2[c2][0])/tThreshold
            # calcDistance2(A1, B1, A2, B2)
            stretchid1[c2][1] = min(calcDistance2(int(tr1[id1][1][0:3]),int(tr1[id1][1][3:]),int(tr2[c2][1][0:3]),int(tr2[c2][1][3:]))/sThreshold, 1)
            stretchid1[c2][2] = w1 * stretchid1[c2][0] + w2 * stretchid1[c2][1]
        minindex = np.argmin(stretchid1[:,2])
        if stretchid1[minindex][0] <= 1:
            stretch = stretch + stretchid1[minindex][2]
        else:
            stretch = stretch + w1 + w2*stretchid1[minindex][1]
    for id2 in index2:
        stretchid2 = np.ones((len(tr1),3))
        for c1 in range(len(tr1)):
            stretchid2[c1][0] = Time(tr2[id2][0],tr1[c1][0])/tThreshold
            # calcDistance2(A1, B1, A2, B2)
            stretchid2[c1][1] = min(calcDistance2(int(tr2[id2][1][0:3]),int(tr2[id2][1][3:]),int(tr1[c1][1][0:3]),int(tr1[c1][1][3:]))/sThreshold, 1)
            stretchid2[c1][2] = w1 * stretchid2[c1][0] + w2 * stretchid2[c1][1]
        minindex = np.argmin(stretchid2[:,2])
        if stretchid2[minindex][0] <= 1:
            stretch = stretch + stretchid2[minindex][2]
        else:
            stretch = stretch + w1 + w2*stretchid2[minindex][1]
    if (len(index1)+len(index2)) == 0:
        return 0
    else:
        return stretch/(len(index1)+len(index2))
            


if __name__ == "__main__":
    
    trace = list(np.load('./data/test_trace_merge.npy'))
    count = list(np.load('./data/test_countinhour.npy'))
    
    start = time.asctime( time.localtime(time.time()) )
    
    length = len(trace)
    
    index = 0
    
    # num记录每一条数据有多少check-in点
    num = []
    for i in range(length):
        num.append(count[i].count(1))
    
    # merge
    record_stretch = np.ones((length,length)) * 2    # 记录i和谁匹配最好
    
    for i in range(0,length):
        for j in range(i, length):
            if i != j:
                try:
                    record_stretch[i][j] = record_stretch[j][i] = calstretch(trace[i],trace[j],count[i],count[j])
                except ZeroDivisionError:
                    record_stretch[i][j] = record_stretch[j][i] = 0
                        
                             
    
    end = time.asctime( time.localtime(time.time()) )
    print "本地时间为 :", start
    print "本地时间为 :", end