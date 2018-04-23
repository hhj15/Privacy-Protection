# -*- coding: utf-8 -*-
"""
Created on Wed Apr 04 09:30:39 2018

@author: huanghongjia
"""

import time
import numpy as np

def calendtime(W, StartTime):
    if ((StartTime + W) % 100) < 24:
        return (StartTime + W)
    else:
        return (StartTime + W - 24 + 100)

def addStartTime(T):
    if (T+time_interval) % 100 >= 24:
        return (T+100+time_interval-24)
    else:
        return T+time_interval
    
def checkeachtrace(tracechoice, StartTime, EndTime):         #检查一条轨迹情况
    tracerecord = []
    for i in range(len(tracechoice)):
        if int(tracechoice[i][0]) < StartTime:
            continue
        else:
            if int(tracechoice[i][0]) >= EndTime:
                break
            else:
                tracerecord = list(set(tracerecord + tracechoice[i][1]))
    return tracerecord

def checkuniontrace(tracelist):
    StartTime = 2018010100
    while StartTime <= 2018013124 - time_window:
        record = []
        EndTime = calendtime(time_window, StartTime)
        for i in tracelist:
            record = list(set(record + checkeachtrace(trace[i],StartTime,EndTime)))
        if len(record) >= l_diverse or len(record) == 0:
            StartTime = addStartTime(StartTime)
            continue
        else:
            return False
    return True




trace = list(np.load('trace_merge.npy'))
    
time_window = 16    #滑动窗口长8h
time_interval = 1  #滑动粒度为1h
l_diverse = 8     #包含位置达40个

length = len(trace)

record = []

start = time.asctime( time.localtime(time.time()) )

#for i in range(4500):
#    if i == 0 or 1:
#        continue
#    set1 = []
#    set2 = []
#    for j in range(i):
#        for k in range(j):
#            continue

p = 0
flag = 0 
for j in range(2,length,1):
    if j == length - 2:
        break
    if flag == 1:
        break
    for k in range(j+1,length,1):
        if flag == 1:
            break
        for m in range(k+1,length,1):
            if flag == 1:
                break
            for u in range(m+1,length,1):
                if flag == 1:
                    break
                for r in range(u+1,length,1):
                    temp = [j,k,m,u,r]
                    p = p + 1
                    if checkuniontrace(temp):
                        record.append(temp)
                    if p > 5000000:
                        flag = 1
                        break


#if checkuniontrace([0]):
#    print 1
#else:
#    print 0


end = time.asctime( time.localtime(time.time()) )

print "本地时间为 :", start
print "本地时间为 :", end