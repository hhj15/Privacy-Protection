# -*- coding: utf-8 -*-
"""
Created on Sat May 12 16:25:20 2018

@author: huanghongjia
"""

import numpy as np
import time
import copy
from check_l_diverse_bin import *
import itertools


sThreshold1 = 1000.0      # 空间阈值 检查干扰点
tThreshold1 = 120.0       # 时间阈值 检查干扰点

sThreshold = 1.0      # 空间阈值(A2-A1)^2+(B2-B1)^2
tThreshold = 1.0       # 时间阈值8h，最小粒度为he
w1 = 0.5
w2 = 0.5

#def Time3(t1,t2,t3):
#    if t1 <= t3 and t1 >= t2:
#        return 0
#    else:
#        return min(abs((int(t2[-4:-2])-int(t1[-4:-2])) * 24 + int(t2[-2:]) - int(t1[-2:])), abs((int(t3[-4:-2])-int(t1[-4:-2])) * 24 + int(t3[-2:]) - int(t1[-2:])))
#
#def calcDistance3(A1, B1, A2, B2, A3, B3):
#    if A1 <= A3 and A1 >= A2 and B1 <= B3 and B1 >= B2:
#        return 0
#    else:
#        dx = max(A1,A2,A3) - min(A1,A2,A3) + 1
#        dy = max(B1,B2,B3) - min(B1,B2,B3) + 1
#        return dx*dy - abs((max(A2,A3)-min(A2,A3)+1)*(max(B2,B3)-min(B2,B3)+1))

def Time(t1,t2):
    if t1 == t2:
        return 0
    else:
        return abs((int(t2[-4:-2])-int(t1[-4:-2])) * 24 + int(t2[-2:]) - int(t1[-2:]))
 
def calcDistance2(A1, B1, A2, B2):
    return abs((max(A1,A2)-min(A1,A2)+1)*(max(B1,B2)-min(B1,B2)+1))-1

def pick(traceset_):           # 选出距离最远的那一条轨迹
    traceset = copy.deepcopy(traceset_)
    traceset.sort()
    trstretch = []
    for i in traceset:
        trstretch.append(stretch[i,traceset].sum())
    pt1 = np.argmax(trstretch)
    p1index = traceset[pt1]
    del traceset[pt1]
    pt2 = np.argmax(stretch[p1index,traceset])
    return p1index,traceset[pt2]

def split(p1, p2, traceset_, l, k):
    traceset = copy.deepcopy(traceset_)
    traceset.remove(p1)
    traceset.remove(p2)
    set1 = [p1]
    set2 = [p2]
    while traceset != []:
        p_1 = np.argmin(stretch[p1, traceset])
        set1.append(traceset[p_1])
        del traceset[p_1]
        if traceset == []:
            break
        else:
            p_2 = np.argmin(stretch[p2, traceset])
            set2.append(traceset[p_2])
            del traceset[p_2]

    checkl1 = checkuniontrace(set1, l, k)
    checkl2 = checkuniontrace(set2, l, k)
    if checkl1 == False and checkl2 == False:
        return [0]      # 0代表分组失败
#    elif (checkl1 == False and checkl2 == True) or (checkl1 == True and checkl2 == False):
#        traceset = copy.deepcopy(traceset_)
#        traceset.remove(p1)
#        traceset.remove(p2)
#        set1 = [p1]
#        set2 = [p2]
#        record_trace = []
#        record_lossval = []
#        if len(traceset)%2 == 1:  #为奇数
#            combinations = list(itertools.combinations(traceset,len(traceset)/2))+list(itertools.combinations(traceset,len(traceset)/2 +1))
#        else:
#            combinations = list(itertools.combinations(traceset,len(traceset)/2))
#        for i in combinations:
#            set11 = set1 + list(i)
#            if checkuniontrace(set11, l) == False:
#                continue
#            else:
#                set22 = set2 + [j for j in traceset if j not in list(i)]
#                if checkuniontrace(set22, l) == False:
#                    continue
#                else:
#                    record_trace.append([set11,set22])
#                    record_lossval.append(calloss(set11)+calloss(set22))
#        if len(record_lossval) == 0:
#            return [0]
#        else:
#            record_index = np.argmin(record_lossval)
#            return [1,record_trace[record_index][0],record_trace[record_index][1]]
      
        
    elif checkl1 == False and checkl2 == True:
        while checkl1 == False:
            temp = set2.pop()
            if checkuniontrace(set2, l, k) == False:
                return [0]
            else:
                set1.append(temp)
                checkl1 = checkuniontrace(set1, l, k)
        return [1, set1, set2, 1]
#        set2len = len(set2)
#        for i in range(set2len-1):
#            set11 = copy.deepcopy(set1)
#            set22 = copy.deepcopy(set2)
#            temp = set22.pop(-(i+1))
#            if checkuniontrace(set22, l) == False:
#                continue
#            else:
#                set11.append(temp)
#                checkl1 = checkuniontrace(set11, l)
#                if checkl1 == True:
#                    return [1, set11, set22]
#                else:
#                    continue
#        return [0]
    elif checkl1 == True and checkl2 == False:
        while checkl2 == False:
            temp = set1.pop()
            if checkuniontrace(set1, l, k) == False:
                return [0]
            else:
                set2.append(temp)
                checkl2 = checkuniontrace(set2, l, k)
        return [1, set1, set2, 1]
#        set1len = len(set1)
#        for i in range(set1len-1):
#            set11 = copy.deepcopy(set1)
#            set22 = copy.deepcopy(set2)
#            temp = set11.pop(-(i+1))
#            if checkuniontrace(set11, l) == False:
#                continue
#            else:
#                set22.append(temp)
#                checkl2 = checkuniontrace(set22, l)
#                if checkl2 == True:
#                    return [1, set11, set22]
#                else:
#                    continue
#        return [0]
    else:
        return [1, set1, set2, 0]

def findthepoint(indpoint, tr_):
    stretchid = []
    for c2 in range(len(tr_)):
        gaptime = Time(indpoint[0],tr_[c2][0])
        temp1 = gaptime/tThreshold
        temp2 = calcDistance2(int(indpoint[1][0:3]),int(indpoint[1][3:]),int(tr_[c2][1][0:3]),int(tr_[c2][1][3:]))/sThreshold
        stretchid.append([c2,temp1, temp2, w1*temp1+w2*temp2])
    stretchid = np.array(stretchid)
    minindex = np.argmin(stretchid[:,3])
    return stretchid[minindex][0]

def calloss(tr_):
    count_ = []
    trace_ = []
    utiloss_t = 0
    utiloss_loc = 0
    for i in tr_:
        count_.append(copy.deepcopy(count[i]))
        trace_.append(copy.deepcopy(trace[i]))
    curlen = len(tr_)
    for i in range(curlen):
        while sum(count_[i]) > 0:
            ind = count_[i].index(1)      # 寻找checkin点位置
            otherchecks = 0
            record_tr = []        # 记录每条轨迹中和该checkin点要合并的具体内容
            for j in [k for k in range(curlen) if k != i]:
                minindex_j = int(findthepoint(trace_[i][ind],trace_[j]))   #记录该checkin点和第j条轨迹stretch最小的那个点
                if count_[j][minindex_j] == 1:
                    count_[j][minindex_j] = 0
                    otherchecks = otherchecks + 1
                record_tr.append(trace_[j][minindex_j])
            mint = maxt = trace_[i][ind][0]
            min1 = max1 = trace_[i][ind][1][0:3]
            min2 = max2 = trace_[i][ind][1][3:]
            for p in record_tr:
                mint = min(mint,p[0])
                maxt = max(maxt,p[0])
                min1 = min(min1,p[1][0:3])
                max1 = max(max1,p[1][0:3])
                min2 = min(min2,p[1][3:])
                max2 = max(max2,p[1][3:])
            losst_temp = min(Time(mint,maxt)/tThreshold1, 1.0)
            lossloc_temp = min(calcDistance2(int(min1),int(min2),int(max1),int(max2))/sThreshold1, 1.0)
            utiloss_t = utiloss_t + losst_temp * (otherchecks + 1)
            utiloss_loc = utiloss_loc + lossloc_temp * (otherchecks + 1)
            count_[i][ind] = 0
    return utiloss_t, utiloss_loc


if __name__ == "__main__":
    stretch = np.load('./data/stretch_matrix.npy')
    trace = list(np.load('./data/trace_merge.npy'))
    count = list(np.load('./data/countinhour.npy'))
    chek = 37782.0
    l = 8
    
#    a= calloss([1,2,3,4])
    
    start = time.asctime(time.localtime(time.time()))   
    
    length = len(trace)
    closs_t = []
    closs_loc = []
#    fenzu = []
#    judge = []
    for k in [14]:
        
        loss_t = 0
        loss_loc = 0
        poss_tr = []
        final_tr = []
        judgetime = 0   #调整的次数
        
        pts = pick(range(length))
        res = split(pts[0],pts[1],range(length),l, k)
        restemp = copy.deepcopy(res)
        poss_tr.append(restemp[1])
        poss_tr.append(restemp[2])
        
        while len(poss_tr) > 0:
            if len(poss_tr[0]) < 2 * k:
                posstemp = copy.deepcopy(poss_tr[0])
                final_tr.append(posstemp)
                del poss_tr[0]
            else:
                pts = pick(poss_tr[0])
                res = split(pts[0],pts[1],poss_tr[0],l, k)
                if res[0] == 0:     #res[0]==1 即不能分解
                    posstemp = copy.deepcopy(poss_tr[0])
                    final_tr.append(posstemp)
                    del poss_tr[0]
                else:
                    restemp = copy.deepcopy(res)
                    poss_tr.append(restemp[1])
                    poss_tr.append(restemp[2])
                    judgetime = judgetime + restemp[3]
                    del poss_tr[0]
        
        for i in final_tr:
            res = calloss(i)
            loss_loc = loss_loc + res[1]
            loss_t = loss_t + res[0]
        
#        fenzu.append(final_tr)
        closs_t.append(loss_t/chek*tThreshold1)
        closs_loc.append(loss_loc/chek*sThreshold1)
#        judge.append(judgetime)
        
    end = time.asctime(time.localtime(time.time()))
    
    print "本地时间为 :", start
    print "本地时间为 :", end
