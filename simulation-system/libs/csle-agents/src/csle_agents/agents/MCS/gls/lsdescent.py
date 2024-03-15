# lsdescent 		
# check descent condition
# 
import numpy as np
from functions.functions import feval
from gls.lssort import lssort

def lsdescent(func,x,p,alist,flist,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s):
    cont = max([i==0 for i in alist]) # condition for continue
    
    if cont: 
        fbest = min(flist)
        i = np.argmin(flist)
        if alist[i] < 0:
            if alist[i] >= 4*alist[i+1]:
                cont=0 # 
        elif alist[i]>0: 
            if alist[i]<4*alist[i-1]:
                cont=0 # 
        else: 
            if i==0:# lowest point
                fbest = flist[1]
            elif i==s-1:# last point
                fbest = flist[s-2]
            else:
                fbest = min(flist[i-1],flist[i+1])
                
    if cont:
        # force local descent step
        if alist[i] !=0:
            alp = alist[i]/3 
        elif i==s-1:
            alp = alist[s-2]/3
        elif i==0:
            alp=alist[1]/3 
        else:
            # split wider adjacent interval
            if alist[i+1] - alist[i]>alist[i]-alist[i-1]:
                alp = alist[i+1]/3 
            else:
                alp=alist[i-1]/3 
        # new function value
        falp = feval(func,x+alp*p)
        alist.append(alp)
        flist.append(falp)
        alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
        #print('descent check: new point at ',alp)  #
    return alist,flist,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s
  
