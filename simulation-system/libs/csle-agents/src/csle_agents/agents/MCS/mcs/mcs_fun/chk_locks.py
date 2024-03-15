import numpy as np
import copy
#from optimization.parameter.mcs.mcs_fun.chk_flag import chrelerr 
#------------------------------------------------------------------------------
def chkloc(nloc, xloc, x):
    loc = 1
    for k in range(nloc):
        if np.array_equal(x,xloc[k]):
            loc = 0
            break
    return loc

#------------------------------------------------------------------------------
def addloc(nloc, xloc, x):
    nloc = nloc + 1
    xloc.append(copy.deepcopy(x))
    return nloc, xloc

#------------------------------------------------------------------------------
def fbestloc(fmi,fbest,xmin,xbest,nbasket0,stop):
    if fmi[nbasket0] < fbest:
        fbest = copy.deepcopy(fmi[nbasket0])
        xbest = copy.deepcopy(xmin[nbasket0])
        #flag = chrelerr(fbest,stop)
    return fbest, xbest#, flag