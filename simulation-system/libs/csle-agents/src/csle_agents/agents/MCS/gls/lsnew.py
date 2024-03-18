# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 17:04:07 2019

@author: yl918888
"""
import numpy as np
from functions.functions import feval
from gls.lssplit import lssplit 
#from gls.lssort import lssort 

#------------------------------------------------------------------------------
def lsnew(func,nloc,small,sinit,short,x,p,s,alist,flist,amin,amax,alp,abest,fmed,unitlen):  

    if alist[0] <= amin: 
        # leftmost point already at boundary
        leftok = 0		
    elif flist[0] >= max(fmed,flist[1]):
        # bad leftmost point
        # extrapolate only if no scale known or global search	
        leftok = (sinit == 1 or nloc > 1 )
    else:
        # good interior leftmost point
        leftok = 1
        
    if alist[s-1] >= amax:
        # rightmost point already at boundary
        rightok = 0
    elif flist[s-1] >= max(fmed, flist[s-2]):
        # bad rightmost point
        # extrapolate only if no scale known or global search	
        rightok = (sinit ==1 or nloc > 1 )
    else:
        # good interior rightmost point
        rightok = 1
    
    # number of intervals used in extrapolation step
    if sinit == 1:
        step = s-1
    else:
        step = 1
    
    fac = short
    # do the step
    if leftok and ( flist[0] < flist[s-1] or (not rightok) ):
        #if prt>1, disp('extrapolate at left end point'); #
        extra = 1 
        al = alist[0] - (alist[0+step] - alist[0])/small
        alp = max(amin, al)
    elif rightok:
        #if prt>1, disp('extrapolate at right end point'); #
        extra=1;
        au = alist[s-1] + (alist[s-1] - alist[s-1-step])/small
        alp = min(au,amax)
    else:
        # no extrapolation
        #if prt>1, disp('split relatively widest interval'); #
        extra = 0
        lenth = [i-j for i,j in zip(alist[1:s],alist[0:s-1])]
        dist = [max(i,j,k) for i,j,k in zip([i-abest for i in alist[1:s]], [abest-i for i in alist[0:s-1]], (unitlen*np.ones(s-1)).tolist())]
        wid = [lenth[i]/dist[i] for i in range(len(lenth))]
        i = np.argmax(wid)
        wid = max(wid)
        alp, fac = lssplit(i,alist,flist,short)
    
    # new function value
    falp = feval(func,x+alp*p)
    alist.append(alp)
    flist.append(falp)

    
    return alist,flist,alp,fac
