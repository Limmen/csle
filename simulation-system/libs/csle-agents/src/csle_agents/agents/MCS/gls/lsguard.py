# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 11:08:43 2019

@author: yl918888
"""

def lsguard(alp,alist,amax,amin,small):
    asort = alist
    asort.sort()
    s = len(asort)
    
    # enforce extrapolation to be cautious
    al = asort[0]- (asort[s-1] - asort[0])/small
    au = asort[s-1] + (asort[s-1] - asort[0])/small
    alp = max(al, min(alp,au))
    alp = max(amin, min(alp, amax))
    
    # enforce some distance from end points
    # 	factor 1/3 ensures equal spacing if s=2 and the third point
    # 	in a safeguarded extrapolation is the maximum.
    if abs(alp-asort[0]) < small*(asort[1] - asort[0]):
      alp = (2*asort[0] + asort[1]) / 3
    
    if abs(alp-asort[s-1]) < small*(asort[s-1] - asort[s-1-1]):
      alp = (2*asort[s-1] + asort[s-1-1])/3
    
    return alp