# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 18:32:37 2018

@author: huanghongjia
"""

# 用二进制字符串记录每个时刻轨迹中的位置

import numpy as np
import time
import random

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
    start = (int(str(StartTime)[-4:-2])-1)*24 + int(str(StartTime)[-2:])
    temp2 = bin_code[tracechoice][start]
    for i in range(1,time_window,1):
        if int(bin_code[tracechoice][start],2) == 0:
            continue
        else:
            temp2 = str(bin(int(temp2,2) | int(bin_code[tracechoice][i+start],2))[2:])
    return temp2

def checkuniontrace(tracelist):
    StartTime = 2018010100
    while StartTime <= 2018013124 - time_window:
        temp1 = '0'
        flag = 0
        cnt_diverse = 0
        for i in tracelist:
            temp2 = int(checkeachtrace(i, StartTime),2)
            if temp2 == 0:
                cnt_diverse = cnt_diverse + 1
            else:
                temp1 = str(bin(int(temp1,2) | temp2)[2:])
            if (temp1.count('1') + cnt_diverse) >= l_diverse:
#            if (sum(map(int, temp1)) + cnt_diverse) >= l_diverse:
                flag = 1
                break
        if flag:
            StartTime = addStartTime(StartTime)
            continue
        else:
            diverse = temp1.count('1')
#            diverse = sum(map(int, temp1))
            if (diverse + cnt_diverse) >= l_diverse:
                StartTime = addStartTime(StartTime)
                continue
            else:
                return False
    return True

def bindivide(tr1,tr2):
    divide = []
    stretch_div = []
    while len(tr2) > l_diverse:
        stretch_sum = []
        stretch_comb = []   #记录可行的轨迹集
        stretch_index = []
        flag = 0   # flag=1则停止循环
        stretch_sum.append(stretch[tr1,:][:,tr1].sum() + stretch[tr2,:][:,tr2].sum())
        
        for index in range(len(tr2)):
            if index > np.max(tr1):
                tr11 = tr1 + [tr2[index]]
                tr22 = list(np.array(tr2).copy())
                tr22.remove(tr2[index])
                if checkuniontrace(tr22):
                    stretch_sum.append(stretch_sum[0] + stretch[index,tr1].sum() + stretch[tr1,index].sum() - stretch[tr22,index].sum() - stretch[index,tr22].sum())
                    stretch_comb.append([tr11,tr22])
                    stretch_index.append(index)
        
        stretch_sum.remove(stretch_sum[0])
        if len(stretch_sum) > 0:
            index = np.argmin(stretch_sum)
        else:
            break 
        while not checkuniontrace(stretch_comb[index][0]):
            del stretch_comb[index]
            del stretch_index[index]
            del stretch_sum[index]
            if len(stretch_sum) > 0:
                index = np.argmin(stretch_sum)
            else:
                flag = 1
                break
        if flag:
            break
        else:
            tr1 = stretch_comb[index][0]
            tr2 = stretch_comb[index][1]
            divide.append([tr1,tr2])
            stretch_div.append(stretch_sum[index])
    return divide, stretch_div

if __name__ == "__main__":
    bin_code = list(np.load('./data/test_bin_code.npy'))
    stretch = np.load('./data/stretch_matrix.npy')
    
    time_window = 16    #滑动窗口长8h
    time_interval = 1  #滑动粒度为1h
    l_diverse = 3     #包含位置达40个
    
#    length = len(bin_code)
    length = 200

    start = time.asctime(time.localtime(time.time()))   
    
    final = []
    check_final = []
    
    tr1 = [0,1,3,10]
    tr2 = [i for i in range(0,max(tr1),1) if i not in tr1] + range (max(tr1)+1,200,1)
    
    divide, stretch_div = bindivide(tr1,tr2)
    
#    stretch_sum = []
#    stretch_comb = []   #记录可行的轨迹集
#    stretch_index = []
#    flag = 0   # flag=1则停止循环
#    stretch_sum.append(stretch[tr1,:][:,tr1].sum() + stretch[tr2,:][:,tr2].sum())
#    
#    for index in range(len(tr2)):
#        if index > np.max(tr1):
#            tr11 = tr1 + [tr2[index]]
#            tr22 = list(np.array(tr2).copy())
#            tr22.remove(tr2[index])
#            if checkuniontrace(tr22):
#                stretch_sum.append(stretch_sum[0] + stretch[index,tr1].sum() + stretch[tr1,index].sum() - stretch[tr22,index].sum() - stretch[index,tr22].sum())
#                stretch_comb.append([tr11,tr22])
#                stretch_index.append(index)
#    #            print time.asctime(time.localtime(time.time()))
#    #            print stretch_sum[-1]
#    #            print stretch_index[-1]
#    
#    stretch_sum.remove(stretch_sum[0])
#    if len(stretch_sum) > 0:
#        index = np.argmin(stretch_sum)
#    else:
#        break
#    while not checkuniontrace(stretch_comb[index][0]) or not checkuniontrace(stretch_comb[index][1]):
#        del stretch_comb[index]
#        del stretch_index[index]
#        del stretch_sum[index]
#        index = np.argmin(stretch_sum)

    
    end = time.asctime(time.localtime(time.time()))
    
    print "本地时间为 :", start
    print "本地时间为 :", end

#sorted(random.sample(range(10), 5))