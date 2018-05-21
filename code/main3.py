# This Python file uses the following encoding: utf-8
"""
Created on Sat Dec 02 17:21:06 2017

@author: huanghongjia
"""
# calculate stretch to get a matrix  only stretch

import numpy as np
import random
import time
#from calDistance import *


sThreshold = 100.0      # 空间阈值(A2-A1)^2+(B2-B1)^2
tThreshold = 12.0       # 时间阈值8h，最小粒度为he

start = time.time()

w1 = 0.5
w2 = 0.5
                  
def Time(t1,t2):
    if t1 == t2:
        return 0
    else:
        return abs((int(t2[-4:-2])-int(t1[-4:-2])) * 24 + int(t2[-2:]) - int(t1[-2:]))
 
def calcDistance2(A1, B1, A2, B2):
    return abs((max(A1,A2)-min(A1,A2)+1)*(max(B1,B2)-min(B1,B2)+1))-1
            

def calstretch(tr1,tr2,n1,n2):
    if (n1 + n2) == 0:
        return 0
    else:
        stretch = 0
        for id1 in tr1:
            stretchid1 = np.ones((len(tr2),3))
            for c2 in range(len(tr2)):
                stretchid1[c2][0] = Time(id1[0],tr2[c2][0])/tThreshold
                stretchid1[c2][1] = calcDistance2(int(id1[1][0:3]),int(id1[1][3:]),int(tr2[c2][1][0:3]),int(tr2[c2][1][3:]))/sThreshold
                stretchid1[c2][2] = w1 * stretchid1[c2][0] + w2 * stretchid1[c2][1]
            minindex = np.argmin(stretchid1[:,2])
            stretch = stretch + stretchid1[minindex][2]
        for id2 in tr2:
            stretchid2 = np.ones((len(tr1),3))
            for c1 in range(len(tr1)):
                stretchid2[c1][0] = Time(id2[0],tr1[c1][0])/tThreshold
                stretchid2[c1][1] = calcDistance2(int(id2[1][0:3]),int(id2[1][3:]),int(tr1[c1][1][0:3]),int(tr1[c1][1][3:]))/sThreshold
                stretchid2[c1][2] = w1 * stretchid2[c1][0] + w2 * stretchid2[c1][1]
            minindex = np.argmin(stretchid2[:,2])
            stretch = stretch + stretchid2[minindex][2]
        return stretch/(n1 + n2)


if __name__ == "__main__":
    
    checkin = list(np.load('./data/test_countinhour_sp.npy'))
    cnt = list(np.load('./data/test_cnt_num.npy'))
    
    start = time.asctime( time.localtime(time.time()) )
    
    length = len(cnt)
    
    index = 0
    
    # merge
    checkin_stretch = np.zeros((length,length))    # 记录i和谁匹配最好
    
    for i in range(0,length):
        for j in range(i, length):
            if i != j:
                try:
                    checkin_stretch[i][j] = checkin_stretch[j][i] = calstretch(checkin[i],checkin[j],cnt[i],cnt[j])
                except ZeroDivisionError:
                    checkin_stretch[i][j] = checkin_stretch[j][i] = 0
                        
                             
    
    end = time.asctime( time.localtime(time.time()) )
    print "本地时间为 :", start
    print "本地时间为 :", end
    np.save('./data/test_stretch_matrix1.npy',checkin_stretch)