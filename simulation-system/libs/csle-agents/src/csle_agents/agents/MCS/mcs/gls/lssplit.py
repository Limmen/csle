# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 07:33:34 2019

@author: yl918888
"""
def lssplit(i,alist,flist,short):
    if flist[i] < flist[i+1]:
        fac = short
    elif flist[i] > flist[i+1]:
        fac = 1 - short
    else:
        fac = 0.5
        
    alp = alist[i] + fac*(alist[i+1] - alist[i])
    #if prt>2, disp(['split at ',num2str(alp)]); end;
    return alp, fac
