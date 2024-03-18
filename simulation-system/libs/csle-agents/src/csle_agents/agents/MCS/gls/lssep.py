# lssep; 		
# separate close local minimizers
# and maybe add a few global points
#



import numpy as np
from functions.functions import feval
from gls.lssort import lssort
from gls.lsnew import lsnew
#------------------------------------------------------------------------------
def lssep(func,nloc,small,sinit,short,x,p,alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s):
    '''
    '''
    nsep=0
    while nsep < nmin:
        # find intervals where the monotonicity behavior of both
        # adjacent intervals is opposite
        down = [i<j for i,j in zip(flist[1:s], flist[0:s-1])]
        sep = [i and j and k  for i,j,k in zip([True, True] + down, [False] + up + [False], down + [True, True])]
        temp_sep = [i and j and k  for i,j,k in zip([True,True] + up, [False] + down + [False], up + [True,True])]
        sep = [i or j for i,j in zip(sep,temp_sep)] 
        
        ind= [i for i in range(len(sep)) if sep[i]]
        
        if len(ind) == 0:
            #print('break ind is empty',ind)
            break
        
        # i = 0  will naver come here 
        aa = [0.5*(alist[i] + alist[i-1]) for i in ind]	# interval midpoints
        if len(aa) > nloc:
            # select nloc best interval midpoints
            ff = [min(flist[i],flist[j]) for i,j in ind]
            ind = np.argsort(ff)
            ff.sort()
            aa = [aa[ind[i]] for i in range(0,nloc)]
            
        for alp in aa:
            #print(alp)
            #if prt>2, disp(['separate minimizer at ',num2str(alp)]); #
            # new function value
            falp = feval(func,x+alp*p)
            alist.append(alp)
            flist.append(falp)
            nsep = nsep+1
            if nsep >= nmin:
                break
        #end for
        alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
    #end while
    
    # instead of unnecessary separation, add some global points
    for times in range(0,nmin-nsep):
        print(times)
        # extrapolation or split
        #print('extrapolation')
        alist,flist,alp,fac = lsnew(func,nloc,small,sinit,short,x,p,s,alist,flist,amin,amax,alp,abest,fmed,unitlen)
        alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
        
    return alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s

