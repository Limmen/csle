import numpy as np
import sys
from scipy.sparse import spdiags
from optimization.parameter.mcs.minq.minq import minq
#%%
def minqsep(c,d,A,b,eq,prt):
    '''
        # minimizes a definite separable quadratic form
        # subject to linear constraints
        #    min    fct = c^T x + 0.5 x^T G x 
        #    s.t.   A x >= b, with equality at indices with eq=1
        # where D=diag(d) is a definite n x n diagonal matrix
        #
        # if A is sparse, it is assumed that the ordering is such that
        # a sparse Cholesky factorization of AA^T is feasible
        #
        # eq    characteristic vector of equalities
        # prt	printlevel
        # xx	guess (optional)
        #
        # x	minimizer (but unbounded direction if ier=1)
        # y     Lagrange multiplier satisfying the KKT conditions
        #       Dx=A^Ty-c, inf(y,Ax-b)=0 at indices with eq=0
        # ier	0  (global minimizer found)
        # 	1  (approximate solution# feasible set probably empty)
        # 	99 (approximate solution# maxit exceeded)
        #
        # Method: apply minq.m to the dual
        #    min  0.5*(A^Ty-c)^TD^(-1)(A^Ty-c)-b^Ty 
        #    s.t. y(~eq)>=0
        # x is recovered as x=D^(-1)(A^Ty-c)
    '''
    #%%
    eps = 2.2204e-16
    if min(d) <=0:
        sys.exit('diagonal must be positive')
    
    m = A.shape[0]
    n = A.shape[1]
    
    D = spdiags(d,0,n,n).toarray()
    G = np.dot(A,np.linalg.solve(D,A.T))
    cc = -b - np.dot(A,(c/d))
    yo = np.Inf + np.zeros(m)
    yu = np.zeros(m)
    yu = np.asarray([-yo[i] if eq[i] else yu[i] for i in range(eq.shape[0])])
    
    #print(D,G,cc,yo,yu)
    #%%
    y,fct,ier = minq(0,cc,G,yu,yo,prt)
    
    x = (np.dot(A.T,y)-c)/d
    if ier == 99:
        return x,y,ier
    
    # check for accuracy
    res = np.dot(A,x)-b
    ressmall = np.dot(np.dot(np.count_nonzero(A),eps),np.add(np.dot(abs(A),abs(x).reshape((len(x),1))),abs(b).reshape(len(b),1)))
    res = [min(res[i],0) if not eq[i] else res[i] for i in range(len(res))]

    if min([abs(res[i])<=ressmall[i] for i in range(len(res))]):
        # accuracy satisfactory
        ier=0#
        return x,y,ier

    # one step of iterative refinement

    dy,fct,ier = minq(0,-res,G,yu-y,yo-y,prt)
    x = (np.dot(A.T,y)-c)/d
    y = y+dy

    # check for accuracy
    res = np.dot(A,x)-b
    ressmall = np.dot(np.dot(np.count_nonzero(A),eps),np.add(np.dot(abs(A),abs(x).reshape((len(x),1))),abs(b).reshape(len(b),1)))
    res = [min(res[i],0) if not eq[i] else res[i] for i in range(len(res))]

    if min([abs(res[i])<=(np.squrt(np.count_nonzero(A))*ressmall[i]) for i in range(len(res))]):
        # accuracy satisfactory
        ier = 0
    else:
        # feasible set probably empty
        ier = 1

    return x,y,ier
