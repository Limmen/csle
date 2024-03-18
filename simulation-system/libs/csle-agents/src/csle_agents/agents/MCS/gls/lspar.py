# ; 		
# local parabolic minimization
#
import copy
import numpy as np
from functions.functions import feval
from gls.lsnew import lsnew
from gls.lsguard import lsguard
from gls.lssort import lssort

def lspar(func,nloc,small,sinit,short,x,p,alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s):
    cont = 1	# continue?
    fac = short
    if s < 3:
        alist,flist,alp,fac = lsnew(func,nloc,small,sinit,short,x,p,s,alist,flist,amin,amax,alp,abest,fmed,unitlen) 
        cont=0 #
    
    #print('cond:',cont)
    if cont:
        # select three points for parabolic interpolation
        fmin = min(flist) # unused
        i = np.argmin(flist)
        if i <= 1: # first two
            ind = [j for j in range(3)]
            ii = copy.deepcopy(i)
        elif i >= s-2: # last two
            ind = [j for j in range(s-2-1,s)]
            ii = i - (s-1) + 2 # corrections for index
        else:
            ind = [j for j in range(ii-1,i+1)]
            ii = 2 - 1 # -1 for index
            
        # in natural order
        aa = [alist[j] for j in ind]
        # the local minimum is at ff(ii)
        ff = [flist[j] for j in ind]	
        
        # get divided differences 
        f12 = (ff[1]- ff[0])/(aa[1]-aa[0])
        f23 = (ff[2]- ff[1])/(aa[2]-aa[1])
        f123 = (f23 - f12)/(aa[2]-aa[0])
        
        # handle concave case
        if not (f123 > 0):
            alist,flist,alp,fac = lsnew(func,nloc,small,sinit,short,x,p,s,alist,flist,amin,amax,alp,abest,fmed,unitlen) 
            #alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
            cont = 0
    
    if cont:
        # parabolic minimizer
        alp0 = 0.5*(aa[1]+aa[2] - f23/f123)
        alp = lsguard(alp0,alist,amax,amin,small)
        alptol = small*(aa[2]-aa[0])
        
        
        # handle infinities and close predictor
        if f123 == np.Inf or min([abs(i-alp) for i in alist]) <= alptol:
            # split best interval
            #if prt>1, disp('split best interval'); #
            if ii == 0 or ( ii == 1 and (aa[1] >= 0.5*(aa[0] + aa[2]))):
                alp = 0.5*(aa[0]+aa[1])
            else:
                alp = 0.5*(aa[1]+aa[2])
        else:
            np_print = alp0
            #print('parabolic predictor: alp0 = ',alp0)
            
        # add point to the list     # new function value
        falp = feval(func,x+alp*p)
        alist.append(alp)
        flist.append(falp)
        #if prt>1, abest_anew_xnew=[alist(i),alp,(x+alp*p)']; #     
        #alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
        
    alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
    return alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,alp,fac
    
