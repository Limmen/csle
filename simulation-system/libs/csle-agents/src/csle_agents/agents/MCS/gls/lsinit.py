# find first two points and establish correct scale
import numpy as np
import sys
from functions.functions import feval

def lsinit(func,x,p,alist,flist,amin,amax,scale):
    '''
        Line search intilization
    '''
    alp = 0
    alp1 = 0
    alp2 = 0
    falp = 0
    
    if len(alist) == 0:
        # evaluate at absolutely smallest point
        alp = 0
        if amin > 0:
            alp = amin
        if amax < 0:
            alp = amax
        # new function value
        falp = feval(func,x+alp*p)
        alist.append(alp)
        flist.append(falp)
    elif len(alist) == 1:
        # evaluate at absolutely smallest point
        alp = 0
        if amin > 0:
            alp = amin
        if amax < 0:
            alp = amax
        if alist[0] != alp:
            # new function value
            falp = feval(func,x+alp*p)
            alist.append(alp)
            flist.append(falp)
            
    # alist and f lis are set -  now comut min and max
    aamin = min(alist) # scalr
    aamax = max(alist) # scalr
    if amin > aamin  or  amax < aamax:
        #print(alist, amin, amax)
        sys.exit('GLS Error: non-admissible step in alist')
    
    # establish correct scale
    if aamax - aamin <= scale:
        alp1 = max(amin,min(-scale,amax)) # scalr
        alp2 = max(amin,min(+scale,amax)) # scalr
        alp = np.Inf # scalr
        
        if aamin - alp1 >= alp2 - aamax:
            alp = alp1
        if alp2 - aamax >= aamin - alp1:
            alp = alp2
        if alp < aamin  or  alp > aamax:
            # new function value
            falp = feval(func,x+alp*p)
            alist.append(alp)
            flist.append(falp)
    if len(alist)==1:
        #print(scale,aamin,aamax,alp1,alp2)
        sys.exit('GLS Error: lsinit bug: no second point found')
    
    return alist,flist,alp,alp1,alp2,falp

