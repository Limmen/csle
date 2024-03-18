
import numpy as np
def lssort(alist,flist):
    '''
    '''
    perm = np.argsort(alist).tolist()    
    alist.sort()
    flist = [flist[i] for i in perm]
    
    s = len(alist)
    
    # find number of strict local minima, etc.
    #up = [flist[0:s-1] < flist[1:s]]
    up = [i<j for i, j in zip(flist[0:s-1], flist[1:s])]
    #down = [flist[1:s] <= flist[0:s-1]]
    down = [i<=j for i, j in zip(flist[1:s], flist[0:s-1])]
    if len(down) == 1:
        down[0] =  flist[s-1] < flist[s-2]
    else:
        down[s-2] = flist[s-1] < flist[s-2]
    
    monotone = (sum(up) == 0 or sum(down) == 0 )
    minima = [i and j for i,j in zip(up + [True], [True] + down)]
    nmin = sum(minima)
    
    fbest = min(flist)
    i = np.argmin(flist)
    
    abest = alist[i]
    fmed = np.median(flist)
     
    # distance from best minimum to next
    if nmin > 1:
        al = [alist[i] for i in range(len(minima)) if minima[i] == True]
        if abest in al:
            al.remove(abest)
        unitlen = min(np.abs(np.subtract(al,abest)))
    else:
        unitlen = max(abest - alist[0], alist[s-1] - abest)
    
    return alist, flist, abest, fbest, fmed, up, down, monotone, minima, nmin, unitlen, s