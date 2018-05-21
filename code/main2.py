# This Python file uses the following encoding: utf-8
"""
Created on Sat Dec 02 17:21:06 2017

@author: huanghongjia
"""
# calculate stretch to get a matrix  basic

import numpy as np
import random
import time
#from calDistance import *


sThreshold = 1.0      # 空间阈值(A2-A1)^2+(B2-B1)^2
tThreshold = 1.0       # 时间阈值8h，最小粒度为he

w1 = 0.5
w2 = 0.5
                  
def Time(t1,t2):
    if t1 == t2:
        return 0
    else:
        return abs((int(t2[-4:-2])-int(t1[-4:-2])) * 24 + int(t2[-2:]) - int(t1[-2:]))
 
def calcDistance2(A1, B1, A2, B2):
    return abs((max(A1,A2)-min(A1,A2)+1)*(max(B1,B2)-min(B1,B2)+1))-1
            
def calstretch(tr1,tr2,cnt1,cnt2):
    index1 = [k for k,v in enumerate(cnt1) if v == 1]
    index2 = [k for k,v in enumerate(cnt2) if v == 1]
    stretch = 0
    for id1 in index1:
        stretchid1 = np.ones((len(tr2),3))
        for c2 in range(len(tr2)):
            stretchid1[c2][0] = Time(tr1[id1][0],tr2[c2][0])/tThreshold
            stretchid1[c2][1] = calcDistance2(int(tr1[id1][1][0:3]),int(tr1[id1][1][3:]),int(tr2[c2][1][0:3]),int(tr2[c2][1][3:]))/sThreshold
            stretchid1[c2][2] = w1 * stretchid1[c2][0] + w2 * stretchid1[c2][1]
        minindex = np.argmin(stretchid1[:,2])
        stretch = stretch + stretchid1[minindex][2]

    for id2 in index2:
        stretchid2 = np.ones((len(tr1),3))
        for c1 in range(len(tr1)):
            stretchid2[c1][0] = Time(tr2[id2][0],tr1[c1][0])/tThreshold
            stretchid2[c1][1] = calcDistance2(int(tr2[id2][1][0:3]),int(tr2[id2][1][3:]),int(tr1[c1][1][0:3]),int(tr1[c1][1][3:]))/sThreshold
            stretchid2[c1][2] = w1 * stretchid2[c1][0] + w2 * stretchid2[c1][1]
        minindex = np.argmin(stretchid2[:,2])
        stretch = stretch + stretchid2[minindex][2]
        
    if (len(index1)+len(index2)) == 0:
        return 0
    else:
        return stretch/(len(index1)+len(index2))


if __name__ == "__main__":
    
    trace = list(np.load('./data/test_trace_merge.npy'))
    count = list(np.load('./data/test_countinhour.npy'))
    
    start = time.asctime( time.localtime(time.time()) )
    
    length = 500
    
    index = 0
    
#    res = calstretch(trace[0],trace[1],count[0],count[1])
    
    # merge
    record_stretch = np.zeros((length,length))    # 记录i和谁匹配最好
    
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
    np.save('./data/stretch_matrix.npy',record_stretch)