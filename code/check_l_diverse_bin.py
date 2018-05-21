# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 18:32:37 2018

@author: huanghongjia
"""

# 用二进制字符串记录每个时刻轨迹中的位置

import numpy as np
import time
import random
#from calminloss1 import *

bin_code = list(np.load('./data/bin_code.npy'))
time_window = 24    #滑动窗口长8h
time_interval = 1  #滑动粒度为1h
#l_diverse = 7     #包含位置达3个


def mergetwostring(s1,s2):
    return(sum(map(int, str(int(s1)|int(s2)))))

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
    
def checkeachtrace(tracechoice, StartTime):         #检查一条轨迹情况
    curtime = (int(str(StartTime)[-4:-2])-1)*24 + int(str(StartTime)[-2:])
    temp=[bin_code[tracechoice][curtime]]
    cnt_temp = [1]
    for i in range(1,time_window,1):
        curtime = curtime + 1
        curcode = bin_code[tracechoice][curtime]
        flag = 0
        if curcode == 0:
            continue
        else:
            for j in range(len(temp)):
                if curcode == temp[j]:
                    cnt_temp[j] = cnt_temp[j] + 1
                    flag = 1
                    break
            if flag == 0:
                temp.append(curcode)
                cnt_temp.append(1)
            
#            try:
#                curind = temp.index(curcode)
#            except ValueError:
#                temp.append(curcode)
#                cnt_temp.append(1)
#            else:
#                cnt_temp[curind] = cnt_temp[curind] + 1
    if len(temp) == 0:
        return -1         # 该地方没有点
    else:
        cnt_mat = np.concatenate(([temp],[cnt_temp]),axis=0)
        cnt_mat = cnt_mat[:,np.argsort(-cnt_mat[1])]
        poss = [cnt_mat[0][0]]  # 可能的地址值
        poss_cnt = cnt_mat[1][0]
        for i in range(1,len(temp),1):
            if poss_cnt > cnt_mat[1][i]:
                break
            else:
                poss.append(cnt_mat[0][i])
        return random.sample(poss,1)[0]

def checkuniontrace(tracelist, l_diverse, k):
    if len(tracelist) < k:
        return False
    else:
        StartTime = 2018010100
        while StartTime <= 2018013124 - time_window:
    #            temp1 = '0'   #old
            temp1 = []
            flag = 0
            for i in tracelist:
                temp2 = checkeachtrace(i, StartTime)
                if temp2 == -1:
                    continue         # 全为空时不算diverse
                else:
                    temp1.append(temp2)
                    temp1 = list(set(temp1))
    #                    temp1 = bin(int(temp1,2) | temp2)[2:]  #old
                    
    #                if (temp1.count('1') + cnt_diverse) >= l_diverse:  #old
                if len(temp1) >= l_diverse:
                    flag = 1
                    break
            if flag:
                StartTime = addStartTime(StartTime)
                continue
            else:
    #                diverse = temp1.count('1')    #old
                if len(temp1) >= l_diverse:
                    StartTime = addStartTime(StartTime)
                    continue
                else:
                    return False
        return True




if __name__ == "__main__":
    bin_code = list(np.load('./data/bin_code1.npy'))
    length = 200
    
    a = checkuniontrace(range(1,20,1),3)
    
    start = time.asctime(time.localtime(time.time()))   
    
    final = []
    check_final = []
    
    for k in range(60):
        tr1 = random.sample(range(50),20)
        tr2 = [i for i in range(0,max(tr1),1) if i not in tr1] + range (max(tr1)+1,50,1)
        if checkuniontrace(tr1,5) == False:
            final.append(tr1)
        if checkuniontrace(tr2,5) == False:
            final.append(tr2)
#    
    
    end = time.asctime(time.localtime(time.time()))
    
    print "本地时间为 :", start
    print "本地时间为 :", end

#sorted(random.sample(range(10), 5))