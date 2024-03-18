import numpy as np
# computes LDL^T factorization for LDL^T+alp*uu^T
# if alp>=0 or if the new factorization is definite 
# (both signalled by p=[]) 
# otherwise, the original L,d and 
# a direction p of null or negative curvature are returned#
# d contains diag(D) and is assumed positive
# does not work for dimension 0

def ldlrk1(L,d,alp,u):
    p=[]
    if alp==0:
        return L,d,p
    
    
#    tempL= L 
#    tempd= d
#    tempu = u
##   
#    p=[]
#    L = LKK
#    d = dK
#    alp = d[j] #-delta
#    u = LKj #w

    eps = 2.2204e-16
    n = u.shape[0]
    neps = n*eps
    
    # save old factorization
    L0=L 
    d0=d 
    
    # update
    for k in [i for i in range(n) if u[i] !=0]:
        delta = d[k] + alp*pow(u[k],2)
        if alp <0 and delta <= neps:
            # update not definite
            p = np.zeros(n) 
            p[k] = 1 
            p0Krange = [i for i in range(0,k+1)]
            p0K = np.asarray([p[i] for i in p0Krange])
            L0K = np.asarray([[L[i,j] for j in p0Krange] for i in p0Krange])
            p0K = np.linalg.solve(L0K,p0K)
            p = np.asarray([p0K[i] if (i in p0Krange) else p[i] for i in range(len(p))])
            # restore original factorization
            L = L0 
            d = d0 
            return L,d,p
        
        q = d[k]/delta 
        d[k] = delta
        # in C, the following 3 lines would be done in a single loop
        ind = [i for i in range(k+1,n)]
        LindK = np.asarray([L[i,k] for i in ind])#.reshape((len(ind),1))
        uk = u[k]#.reshape((1,1))
        c = np.dot(LindK,uk)
        for i in range(len(ind)):
            L[ind[i],k] = LindK[i]*q +(alp*u[k]/delta)*u[ind[i]]
            
        for i in range(len(ind)):
            u[ind[i]] = u[ind[i]] - c[i]
            
        alp = alp*q
        if alp==0:
            break
    return L,d,p
