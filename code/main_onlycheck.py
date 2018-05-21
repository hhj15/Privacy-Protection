# -*- coding: utf-8 -*-
"""
Created on Sat May 12 16:25:20 2018

@author: huanghongjia
"""

import numpy as np
import time
import copy
import itertools

sThreshold1 = 1000.0      # 空间阈值 检查干扰点
tThreshold1 = 120.0       # 时间阈值 检查干扰点

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

def Time3(t1,t2,t3):
    if t1 <= t3 and t1 >= t2:
        return 0
    else:
        return min(abs((int(t2[-4:-2])-int(t1[-4:-2])) * 24 + int(t2[-2:]) - int(t1[-2:])), abs((int(t3[-4:-2])-int(t1[-4:-2])) * 24 + int(t3[-2:]) - int(t1[-2:])))

def calcDistance3(A1, B1, A2, B2, A3, B3):
    if A1 <= A3 and A1 >= A2 and B1 <= B3 and B1 >= B2:
        return 0
    else:
        dx = max(A1,A2,A3) - min(A1,A2,A3) + 1
        dy = max(B1,B2,B3) - min(B1,B2,B3) + 1
        return dx*dy - abs((max(A2,A3)-min(A2,A3)+1)*(max(B2,B3)-min(B2,B3)+1))

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

def split(p1, p2, traceset_):
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
    return [set1, set2]

def findthepoint(indpoint, tr_):
    stretchid = []
    for c2 in range(len(tr_)):
        gaptime = Time3(indpoint[0],tr_[c2][0],tr_[c2][1])
        temp1 = gaptime/tThreshold
        temp2 = calcDistance3(int(indpoint[2][0:3]),int(indpoint[2][3:]),int(tr_[c2][2][0:3]),int(tr_[c2][2][3:]),int(tr_[c2][3][0:3]),int(tr_[c2][3][3:]))/sThreshold
        stretchid.append([c2,temp1, temp2, w1*temp1+w2*temp2])
    stretchid = np.array(stretchid)
    minindex = np.argmin(stretchid[:,3])
    return int(stretchid[minindex][0])

def calstretch(pt_ori,pt_aft):
    timegap = Time(pt_aft[0],pt_aft[1]) - Time(pt_ori[0],pt_ori[1])
    locgap = calcDistance2(int(pt_aft[2][0:3]),int(pt_aft[2][3:]),int(pt_aft[3][0:3]),int(pt_aft[3][3:])) - calcDistance2(int(pt_ori[2][0:3]),int(pt_ori[2][3:]),int(pt_ori[3][0:3]),int(pt_ori[3][3:]))
    return [min(timegap/tThreshold1, 1.0), min(locgap/sThreshold1, 1.0)]

def mergetwopoint(p1, p2):
    t1 = min(p1[0],p1[1],p2[0],p2[1])
    t2 = max(p1[0],p1[1],p2[0],p2[1])
    loc1 = min(p1[2][0:3],p2[2][0:3])+min(p1[2][3:],p2[2][3:])
    loc2 = max(p1[3][0:3],p2[3][0:3])+max(p1[3][3:],p2[3][3:])
    return [t1,t2,loc1,loc2]

def mergeintrace(pt,tr):  #将轨迹中没有被合并过的点与被合并过的点合并  pt为序号  tr为basetracetag
    num1 = -1
    num2 = -1
    for i in range(pt-1,-1,-1):
        if tr[i] == 1:
            num1 = i
            break
        else:
            continue
    for i in range(pt+1,len(tr),1):
        if tr[i] == 1:
            num2 = i
            break
        else:
            continue
    return num1,num2

def mergealltrace(traceset_):
    traceset = copy.deepcopy(traceset_)
    trace_num = []   #记录每条轨迹有多少点
    tr_ = []           # 记录每条轨迹的具体时空点
    stretch_t = 0
    stretch_loc = 0
    for i in traceset:
        trace_num.append(len(trace[i]))
        tr_.append(trace[i])
    basetracenum = np.argmin(trace_num)    #最少点数的轨迹序号
    basetrace = copy.deepcopy(tr_[basetracenum])   #保存最少点数的轨迹，即每次merge后的轨迹
    basetracetag = [0]*len(basetrace)  #记录每个点是否被merge过
    del tr_[basetracenum]
    del trace_num[basetracenum]
    while len(trace_num) > 0:
        curtracenum = np.argmin(trace_num)
        curtr = copy.deepcopy(tr_[curtracenum])
        for c1 in range(len(curtr)):
            pointind = findthepoint(curtr[c1],basetrace)
            basetracetag[pointind] = 1
            mergepoint = mergetwopoint(basetrace[pointind],curtr[c1])   #两个点合并后的点
            res1 = calstretch(basetrace[pointind],mergepoint)
            res2 = calstretch(curtr[c1],mergepoint)
            stretch_t = stretch_t + res1[0] + res2[0]
            stretch_loc = stretch_loc + res1[1] + res2[1]
            basetrace[pointind] = mergepoint
        for i in range(len(basetracetag)):
            if basetracetag[i] == 0:
                possnum = mergeintrace(i,basetracetag)
                possmerge = []    #记录合并后的点
                possstretch = []
                possno = []
                for j in possnum:
                    if j != -1:
                        possno.append(j)
                        possmerge.append(mergetwopoint(basetrace[i],basetrace[j]))
                        res1 = calstretch(basetrace[i],possmerge[-1])
                        res2 = calstretch(basetrace[j],possmerge[-1])
                        possstretch.append([res1[0]+res2[0], res1[1]+res2[1], res1[0]+res2[0]+res1[1]+res2[1]])
                possstretch = np.array(possstretch)
                choice = np.argmin(possstretch[:,2])   #选择的第i个要和第possno[choice]个合并
                basetrace[possno[choice]] = possmerge[choice]
                basetracetag[i] = 2
                stretch_t = stretch_t + possstretch[choice][0]
                stretch_loc = stretch_loc + possstretch[choice][1]
        for i in range(len(basetracetag)-1,-1,-1):
            if basetracetag[i] == 2:
                del basetrace[i]
        del tr_[curtracenum]
        del trace_num[curtracenum]
        basetracetag = [0]*len(basetrace)  #记录每个点是否被merge过
    
    return [stretch_t,stretch_loc]

if __name__ == "__main__":
    stretch = np.load('./data/stretch_matrix_check.npy')
    trace = list(np.load('./data/trace_checkins.npy'))
    chek = 37782.0
#    chek = 2515

#    i = [645, 1793, 5807, 7893]
#    mergealltrace(i)
    
    start = time.asctime(time.localtime(time.time()))   
    
    length = len(trace)
    closs_t = []
    closs_loc = []
    for k in [5,7,9,11]:
    
        loss_t = 0
        loss_loc = 0
        poss_tr = []
        final_tr = []
        
        pts = pick(range(length))
        res = split(pts[0],pts[1],range(length))
        restemp = copy.deepcopy(res)
        poss_tr.append(restemp[0])
        poss_tr.append(restemp[1])
        
        while len(poss_tr) > 0:
            if len(poss_tr[0]) < 2 * k:
                posstemp = copy.deepcopy(poss_tr[0])
                final_tr.append(posstemp)
                del poss_tr[0]
            else:
                pts = pick(poss_tr[0])
                res = split(pts[0],pts[1],poss_tr[0])
                restemp = copy.deepcopy(res)
                poss_tr.append(restemp[0])
                poss_tr.append(restemp[1])
                del poss_tr[0]
        
        for i in final_tr:
            res = mergealltrace(i)
            loss_t = loss_t + res[0]
            loss_loc = loss_loc + res[1]
        
        closs_t.append(loss_t/chek * tThreshold1)
        closs_loc.append(loss_loc/chek * sThreshold1)
    
    end = time.asctime(time.localtime(time.time()))
    
    print "本地时间为 :", start
    print "本地时间为 :", end
