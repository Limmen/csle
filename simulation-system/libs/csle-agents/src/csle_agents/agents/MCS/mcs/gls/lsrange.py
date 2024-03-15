"""

Created on Mon Oct 14 09:36:17 2019

@author: yl918888

"""

# lsrange 
# find range of useful alp in truncated or bent line search

import numpy as np
import sys
from functions.functions import feval

def lsrange(func,xl,xu,x,p,prt,bend):
    '''
        Defining line search range
    '''
    if np.max(np.abs(p)) == 0:
        sys.exit('GLS Error: zero search direction in line search')
    
    # find sensible step size scale
    if type(p) != np.ndarray:
        if type(p) != list:
            p = [p]
        p = np.asarray(p)
    
    if type(x) != np.ndarray:
        if type(x) != list:
            x= [x]
            xl= [xl]
            xu= [xu]
        x = np.asarray(x)
        xl = np.asarray(xl)
        xu = np.asarray(xu)

    # this is test for python
    if x.shape != p.shape:
        sys.exit('GLS Error: dim of x and p does not match: program is going to fail')
    
    pp = np.abs(p[p !=0])
    u = np.divide(np.abs(x[p != 0]),pp)
    scale = min(u)
    
    if scale == 0:
        u[u == 0] = np.divide(1,pp[u==0])
        scale = min(u) 
    
    if not bend:
        # find range of useful alp in truncated line search
        amin = -np.Inf
        amax = np.Inf
        for i in range(len(x)):
            if p[i] > 0:
                amin = max(amin,(xl[i] - x[i])/p[i]) 
                amax = min(amax,(xu[i] - x[i])/p[i])
            elif p[i] < 0:
                amin = max(amin,(xu[i] - x[i])/p[i])
                amax = min(amax,(xl[i] - x[i])/p[i])
        
        if amin > amax:
            sys.exit('GLS Error: no admissible step in line search')
            #return 
        # not needed if do not print any thing
#        if prt:
#            aa = amin + np.arange(101)*(amax - amin)/100
#            ff=[]
#            for alp in aa:
#                xx = np.asarray([max(xl[i],min(x[i]+alp*p[i],xu[i])) for i in  range(len(x))])
#                ff.append(feval(func,xx))
    else:
        # find range of useful alp in bent line search
        amin = np.Inf
        amax = -np.Inf
        for i in range(len(x)):
            if p[i] > 0:
                amin = min(amin,(xl[i] - x[i])/p[i])
                amax = max(amax,(xu[i] - x[i])/p[i])
            elif p[i] < 0:
                amin = min(amin,(xu[i]-x[i])/p[i])
                amax = max(amax,(xl[i]-x[i])/p[i])
#        if prt:
#            aa = amin +  np.arange(101)*(amax - amin)/100 
#            ff=[]
#            for alp in aa:
#                xx = max(xl, min(x+alp*p,xu)) 
#                ff.append(feval(func,xx))

    return xl,xu,x,p,amin,amax,scale#,aa,ff
            
