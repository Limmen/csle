import numpy as np
from optimization.parameter.mcs.minq.minq import minq
#------------------------------------------------------------------------------
def minqdef(c,G,A,b,eq,prt):
    eps = 2.2204e-16
    
    m = A.shape[0]
    n = A.shape[1]
    
    R = np.linalg.cholesky(G)
    
    A0 = np.divide(A,R.diagonal())
    GG = np.dot(A0,A0.T)
    c0 = np.linalg.solve(R.T,c)
    cc = -b - np.dot(A0,c0)
    yo = np.Inf + np.zeros(m)
    yu = np.zeros(m)
    yu = np.asarray([-yo[i] if eq[i] else yu[i] for i in range(eq.shape[0])])
    
    y,fct,ier = minq(0,cc,GG,yu,yo,prt)
    
    x = np.linalg.solve(R,(np.dot(A0.T,y)-c0)) #R\(A0'*y-c0);
    if ier==99:
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
    
    dy,fct,ier = minq(0,-res,GG,yu-y,yo-y,prt)
    x = x + np.linalg.solve(R,(np.dot(A0.T,dy)))# x=x+R\(A0'*dy);
    y = y+dy
    
    #% check for accuracy
    res = np.dot(A,x)-b
    ressmall = np.dot(np.dot(np.count_nonzero(A),eps),np.add(np.dot(abs(A),abs(x).reshape((len(x),1))),abs(b).reshape(len(b),1)))
    res = [min(res[i],0) if not eq[i] else res[i] for i in range(len(res))]
        
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
