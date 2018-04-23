# This Python file uses the following encoding: utf-8
"""
Created on Sat Dec 02 17:21:06 2017

@author: huanghongjia
"""

import numpy as np
from calDistance import *
                  
def time(t11, t12, t21, t22):
    t_max = max(t11, t12, t21, t22)
    t_min = min(t11, t12, t21, t22)
    day_max = int(t_max[4:8])
    day_min = int(t_min[4:8])
    if (day_max - day_min) >= 2:
        return 1e10
    else:
        hour_max = int(t_max[-4:-2])
        hour_min = int(t_min[-4:-2])
        minute_max = int(t_max[-2:])
        minute_min = int(t_min[-2:])
        interval = ((day_max-day_min)*24 + hour_max - hour_min)*60 + minute_max - minute_min
        return interval

def merge(tr1,tr2,id1,id2):
    t_max = max(tr2[id2][1],tr1[id1][1])
    t_min = max(tr1[id1][0],tr2[id2][0])
    stretch_time = min((((int(t_max[4:8])-int(t_min[4:8]))*24+int(t_max[-4:-2])-int(t_min[-4:-2]))*60+int(t_max[-2:])-int(t_min[-2:]))/tThreshold, 1)
    lng1 = tr1[id1][2]
    lng2 = tr1[id1][3]
    lng3 = tr1[id1][4]
    lng4 = tr1[id1][5]
    lng5 = tr2[id2][2]
    lng6 = tr2[id2][3]
    lng7 = tr2[id2][4]
    lng8 = tr2[id2][5]
    lng_min = min(lng1, lng2, lng5, lng6)
    lng_max = max(lng1, lng2, lng5, lng6)
    lat_min = min(lng3, lng4, lng7, lng8)
    lat_max = max(lng3, lng4, lng7, lng8)
    try:
        stretch_area = min(abs(calcArea(lng_min,lng_max,lat_min,lat_max)/sThreshold), 1)
    except ZeroDivisionError:
        stretch_area = 0
    return w_time * stretch_time + w_loc * stretch_area


sThreshold = float(50)       # 面积阈值100km2
tThreshold = float(480)       # 时间阈值8h，最小粒度为min

w_time = 0.5
w_loc = 0.5  #时空权重

trace = list(np.load('./data/test_trace.npy'))
count = list(np.load('./data/test_count.npy'))

length = len(trace)

                  
# num记录每一条数据有多少check-in点
num = []
for i in range(length):
    num.append(count[i].count(1))


# merge
cur_stretch = np.zeros((length,3))
record_stretch = np.zeros((length,length))    # 记录i和谁匹配最好
for i in range(length):
    for j in range(length):
        if i == j or record_stretch[i][j] != 0:
            continue
        else:
            # merge
            tr1 = trace[i]
            tr2 = trace[j]
            stretch = 0
            index1 = [k for k,v in enumerate(count[i]) if v == 1]
            index2 = [k for k,v in enumerate(count[j]) if v == 1]
            for id1 in index1:
                if tr1[id1][1] < tr2[0][0]:
                    stretch = stretch + merge(tr1,tr2,id1,0)
                    continue
                elif tr1[id1][0] > tr2[len(tr2)-1][1]:
                    stretch = stretch + merge(tr1,tr2,id1,len(tr2)-1)
                    continue
                else:
                    stretch_id1 = np.ones((len(tr2),3))
                    lng1 = tr1[id1][2]
                    lng2 = tr1[id1][3]
                    lng3 = tr1[id1][4]
                    lng4 = tr1[id1][5]
                    for c2 in range(len(tr2)):
                        t_max = max(tr1[id1][1],tr2[c2][1])
                        t_min = min(tr1[id1][0],tr2[c2][0])
                        day_max = int(t_max[4:8])
                        day_min = int(t_min[4:8])
                        if (day_max - day_min) >= 2:
                            continue
                        else:
                            hour_max = int(t_max[-4:-2])
                            hour_min = int(t_min[-4:-2])
                            minute_max = int(t_max[-2:])
                            minute_min = int(t_min[-2:])
                            interval = ((day_max-day_min)*24 + hour_max - hour_min)*60 + minute_max - minute_min
                            stretch_id1[c2][0] = min(interval/tThreshold, 1)
                            if stretch_id1[c2][0] == 1:
                                continue
                            else:
                                lng5 = tr2[c2][2]
                                lng6 = tr2[c2][3]
                                lng7 = tr2[c2][4]
                                lng8 = tr2[c2][5]
                                lng_min = min(lng1, lng2, lng5, lng6)
                                lng_max = max(lng1, lng2, lng5, lng6)
                                lat_min = min(lng3, lng4, lng7, lng8)
                                lat_max = max(lng3, lng4, lng7, lng8)
                                try:
                                    stretch_id1[c2][1] = min(abs(calcArea(lng_min,lng_max,lat_min,lat_max)/sThreshold), 1)
                                except ZeroDivisionError:
                                    stretch_id1[c2][1] = 0
                                    continue  
                                stretch_id1[c2][2] = w_time * stretch_id1[c2][0] + w_loc * stretch_id1[c2][1]
                    stretch = stretch + float(min(stretch_id1[:,2]))
#                    id1_cur_c2 = int(np.where(stretch_id1 == np.min(stretch_id1[:,2]))[0][0])   #该id1坐标和tr2中第id1_cur_c2个坐标合并
#                    trace[i][id1][0] = trace[j][id1_cur_c2][0] = min(tr1[id1][0],tr2[id1_cur_c2][0])
#                    trace[i][id1][1] = trace[j][id1_cur_c2][1] = max(tr1[id1][1],tr2[id1_cur_c2][1])
#                    trace[i][id1][2] = trace[j][id1_cur_c2][2] = min(tr1[id1][2],tr2[id1_cur_c2][2])
#                    trace[i][id1][3] = trace[j][id1_cur_c2][3] = max(tr1[id1][3],tr2[id1_cur_c2][3])
#                    trace[i][id1][4] = trace[j][id1_cur_c2][4] = min(tr1[id1][4],tr2[id1_cur_c2][4])
#                    trace[i][id1][5] = trace[j][id1_cur_c2][5] = max(tr1[id1][5],tr2[id1_cur_c2][5])
#                    tr1 = trace[i]
#                    tr2 = trace[j]
            for id2 in index2:
                stretch_id2 = np.ones((len(tr1),3))
                if tr2[id2][1] < tr1[0][0]:
                    stretch = stretch + merge(tr1,tr2,0,id2)
                    continue
                elif tr2[id2][0] > tr1[len(tr1)-1][1]:
                    stretch = stretch + merge(tr1,tr2,len(tr1)-1,id2)
                    continue
                else:
                    lng1 = tr2[id2][2]
                    lng2 = tr2[id2][3]
                    lng3 = tr2[id2][4]
                    lng4 = tr2[id2][5]
                    for c1 in range(len(tr1)):
                        
                        
                        stretch_id2[c1][0] = min(time(tr2[id2][0],tr2[id2][1],tr1[c1][0],tr1[c1][1])/tThreshold, 1)
                        if stretch_id2[c1][0] == 1:
                            continue
                        else:
                            lng5 = tr1[c1][2]
                            lng6 = tr1[c1][3]
                            lng7 = tr1[c1][4]
                            lng8 = tr1[c1][5]
                            lng_min = min(lng1, lng2, lng5, lng6)
                            lng_max = max(lng1, lng2, lng5, lng6)
                            lat_min = min(lng3, lng4, lng7, lng8)
                            lat_max = max(lng3, lng4, lng7, lng8)
                            try:
                                stretch_id2[c1][1] = min(abs(calcArea(lng_min,lng_max,lat_min,lat_max)/sThreshold), 1)
                            except ZeroDivisionError:
                                stretch_id2[c1][1] = 0
                                continue
                            stretch_id2[c1][2] = w_time * stretch_id2[c1][0] + w_loc * stretch_id2[c1][1]
#                    if flag == 1:
#                        flag = 0
#                        continue
#                    else:
                    stretch = stretch + float(min(stretch_id2[:,2]))
#                    c2_cur_id1 = int(np.where(stretch_id2 == np.min(stretch_id2[:,2]))[0][0])   #该c2坐标和tr1中第c2_cur_id1个坐标合并
#                    trace[j][id2][0] = trace[i][c2_cur_id1][0] = min(tr2[id2][0],tr1[c2_cur_id1][0])
#                    trace[j][id2][1] = trace[i][c2_cur_id1][1] = max(tr2[id2][1],tr1[c2_cur_id1][1])
#                    trace[j][id2][2] = trace[i][c2_cur_id1][2] = min(tr2[id2][2],tr1[c2_cur_id1][2])
#                    trace[j][id2][3] = trace[i][c2_cur_id1][3] = max(tr2[id2][3],tr1[c2_cur_id1][3])
#                    trace[j][id2][4] = trace[i][c2_cur_id1][4] = min(tr2[id2][4],tr1[c2_cur_id1][4])
#                    trace[j][id2][5] = trace[i][c2_cur_id1][5] = max(tr2[id2][5],tr1[c2_cur_id1][5])
#                    tr1 = trace[i]
#                    tr2 = trace[j]
            if (sum(count[i])+sum(count[j])) == 0:
                record_stretch[j][i] = record_stretch[i][j] = 0
            else:
                record_stretch[j][i] = record_stretch[i][j] = stretch/(sum(count[i])+sum(count[j]))

    cur_stretch[i][0] = i
    istretch = record_stretch[i,:]
    istretch_sort = sorted(istretch)
    if istretch_sort[1] == 0:
        selectzero = np.where(istretch == 0)[0]
        selectzero = selectzero.tolist()
        selectzero.remove(i)
        cur_stretch[i][1] = int(selectzero[0])
    else:
        cur_stretch[i][1] = np.where(istretch == istretch_sort[1])[0][0]
    cur_stretch[i][2] = record_stretch[i][int(cur_stretch[i][1])]
                

