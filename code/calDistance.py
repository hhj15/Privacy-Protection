# This Python file uses the following encoding: utf-8
import math as mt
from math import radians

def calcDistance(Lat_A, Lng_A, Lat_B, Lng_B):
    if abs(Lat_A-Lat_B) <= 1e-9 and abs(Lng_A-Lng_B) <= 6.1*1e-7:
        distance = 1e-5
    else:
        ra = 6378.140  
        rb = 6356.755  
        flatten = (ra - rb) / ra  
        rad_lat_A = mt.radians(Lat_A)
        rad_lng_A = mt.radians(Lng_A)
        rad_lat_B = mt.radians(Lat_B)
        rad_lng_B = mt.radians(Lng_B)
        pA = mt.atan(rb / ra * mt.tan(rad_lat_A))
        pB = mt.atan(rb / ra * mt.tan(rad_lat_B))
        xx = mt.acos(mt.sin(pA) * mt.sin(pB) + mt.cos(pA) * mt.cos(pB) * mt.cos(rad_lng_A - rad_lng_B))
        c1 = (mt.sin(xx) - xx) * (mt.sin(pA) + mt.sin(pB)) ** 2 / mt.cos(xx / 2) ** 2
        c2 = (mt.sin(xx) + xx) * (mt.sin(pA) - mt.sin(pB)) ** 2 / mt.sin(xx / 2) ** 2
        dr = flatten / 8 * (c1 - c2)
        distance = ra * (xx + dr)
    return distance

# longitude 经度
def calcArea(A_lng, B_lng, A_lat, B_lat): # A纬度，B纬度，A经度，B经度
    x = calcDistance(A_lat,A_lng,A_lat,B_lng)
    y = calcDistance(A_lat,B_lng,B_lat,B_lng)
    return x*y

