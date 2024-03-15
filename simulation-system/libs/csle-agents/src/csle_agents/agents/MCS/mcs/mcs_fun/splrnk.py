import numpy as np
#------------------------------------------------------------------------------
from mcs_fun.split_func import split2
#------------------------------------------------------------------------------
def splrnk(n,n0,p,x,y):
    '''# determines the splitting index and splitting value for splitting a
    % box by rank
    % Input:
    % n        dimension of the problem
    % n0(1:n)  coordinate i has been split n0(i) times in the history of the
    %          box to split
    % p(1:n)   ranking of estimated variability of the function in the 
    %          different coordinates
    % x(1:n)   base vertex of the box
    % y(1:n)   opposite vertex of the box
    % Output:
    % isplit   splitting index
    % splval   = Inf  if n0(isplit) = 0 (indicates that the box has to be
    %                 split according to the initialization list)
    %          = splitting value  otherwise
    '''
    
    isplit = 0
    n1 = n0[0]
    p1 = p[0]
    for i in range(1,n):
        if n0[i] < n1 or (n0[i] == n1 and p[i] < p1):
            isplit = i
            n1 = n0[i]
            p1 = p[i]
    if n1 > 0:
        splval = split2(x[isplit],y[isplit])
    else:
     splval =  np.Inf
    # end
    return isplit,splval