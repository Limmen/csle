import numpy as np
#------------------------------------------------------------------------------
def updtf(n,i,x1,x2,f1,f2,fold,f):
    for i1 in range(n):
        if i1 != i:
            if x1[i1] == np.Inf:
                f1[i1] = f1[i1] + fold - f
            if x2[i1] == np.Inf:
                f2[i1] = f2[i1] + fold - f
    fold = f
    return f1,f2,fold
