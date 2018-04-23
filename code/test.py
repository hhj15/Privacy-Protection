# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 14:30:19 2018

@author: huanghongjia
"""

def test(tr1,tr2):
    i = 0
    while i < 3:
        if len(tr2) > 3:
            tr2 = tr2 + ['1']
        i = i + 1
    return tr1,tr2


if __name__ == "__main__":
    tr1 = [1,2,3]
    tr2 = [4,5,6,7]
    tr1,tr2 = test(tr1,tr2)