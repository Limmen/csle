import numpy as np
from mcs_fun.polint import polint
from mcs_fun.initi_func import subint
from mcs_fun.quadratic_func import quadmin
from mcs_fun.quadratic_func import quadpol
#------------------------------------------------------------------------------
def exgain(n,n0,l,L,x,y,x1,x2,fx,f0,f1,f2):
    '''
    % determines the splitting index, the splitting value and the expected
    % gain vector e for (potentially) splitting a box by expected gain
    % Input:
    % n        dimension of the problem
    % n0(1:n)  the ith coordinate has been split n0(i) times in the history
    %          of the box
    % l(1:n)   pointer to the initial point of the initialization list
    % L(1:n)   lengths of the initialization list
    % x(1:n)   base vertex of the box
    % y(1:n)   opposite vertex of the box
    % x1(1:n), x2(1:n), f1(1:n), f2(1:n)
    %          x1(i) and x2(i) and the corresponding function values f1(i)
    %          and f2(i) used for quadratic interpolation in the ith
    %          coordinate 
    % fx       function value at the base vertex
    % f0(1:max(L),1:n)  function values appertaining to the init. list
    % Output:
    % e(1:n)   e(i) maximal expected gain in function value by changing 
    %          coordinate i
    % isplit   splitting index
    % splval   = Inf  if n0(isplit) = 0
    %          = splitting value  otherwise
    '''
    
    e = np.zeros(n) # initialization
    emin = np.Inf;  # initialization
    for i in range(n):
        if n0[i] == 0:
            # expected gain for splitting according to the initialization list
            e[i] = min(f0[0:L[i]+1,i]) - f0[l[i],i]
            
            if e[i] < emin:
                emin = e[i]
                isplit = i
                splval = np.Inf
        else:
            z1 = [x[i], x1[i], x2[i]]
            z2 = [0, f1[i] - fx, f2[i] - fx]
            d = polint(z1,z2)
            # safeguard against splitting too close to x(i)
            eta1, eta2 = subint(x[i],y[i])
            xi1 = min(eta1,eta2)
            xi2 = max(eta1,eta2)
            z = quadmin(xi1,xi2,d,z1)
            e[i] = quadpol(z,d,z1)
            if e[i] < emin:
                emin = e[i]
                isplit = i
                splval = z
                
    return e,isplit,splval