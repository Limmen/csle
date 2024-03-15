

# updates LDL^T factorization when a unit j-th row and column
# are replaced by column g 
# if the new matrix is definite (signalled by p=[]) 
# otherwise, the original L,d and 
# a direction p of null or negative curvature are returned
#
# d contains diag(D) and is assumed positive
# Note that g must have zeros in other unit rows!!!
import numpy as np
from minq.ldlrk1 import ldlrk1

def ldlup(L,d,j,g):
    
    #tempg = g
    #L,d,j,g = L,dd,j,p
    
    p=[] 
    eps = 2.2204e-16
    n = d.shape[0] 
    I = [i for i in range(0,j)]
    K = [i for i in range(j+1,n)] 
    
    if j == 0:
        v = np.zeros(0) 
        delta = g[j] 
        if delta <= n*eps:
            p = np.asarray([1] + np.zeros(n-1).tolist())
            #if test, 
                #  A,p
                #  Nenner=abs(p)'*abs(A)*abs(p) 
                #  if Nenner==0, indef1=0 ,else indef1=(p'*A*p)/Nenner, #
                #  disp('leave ldlup at 1')
            return L,d,p
        #end if delta
        w = [g[i]/delta for i in K]  
        L[j,I] = v.T 
        d[j] = delta      
        p = np.asarray(p)
        return L,d,p
    # now j>1, K nonempty
    LII = np.asarray([[L[i,j] for j in I] for i in I])
    gI = [g[i] for i in I]
    u = np.linalg.solve(LII,gI)
    dI = [d[i] for i in I]
    v = np.divide(u,dI)
    delta = g[j] - np.dot(u.T,v)    
    #print(LII,u,v,delta) # LII,u,v,del

    if delta <= n*eps:
        p = np.asarray(np.linalg.solve(LII.T,v).tolist()+[-1]+ np.zeros(n-j-1).tolist())
        #if test, 
        #A,p
        #indef1=(p'*A*p)/(abs(p)'*abs(A)*abs(p))
        #disp('leave ldlup at 2')
        return L,d,p
    
    if len(K) != 0:
        LKI = np.asarray([[L[i,j] for j in I] for i in K])
        gK = np.asarray([g[i] for i in K])
        w = np.divide(np.subtract(gK,np.dot(LKI,u)),delta)
        LKK = np.asarray([[L[i,j] for j in K] for i in K])
        dK = np.asarray([d[i] for i in K])
        #print(LKI,w,LKK,dK,w)
        # call ldlrk1
        LKK, dK, q = ldlrk1(LKK,dK,-delta,w)
        d[K] = dK
    else:
        q = []
        
    
    if len(q) == 0:
        # work around expensive sparse L(K,K)=LKK
        #r1 = np.asarray([[L[i,j] for j in range(L.shape[1])] for i in I])
        r1 = L[I,:]
        r2 = np.asarray(v.T.tolist() + [1] + L[j,K].tolist())
        r2 = r2.reshape((1,len(r2)))
        if len(K) != 0:
            r3 = np.concatenate((LKI, w.reshape(len(w),1), LKK), axis=1)
            #r1.shape, r2.shape, r3.shape
            L = np.concatenate((r1,r2,r3),  axis=0)
        else:
            L = np.concatenate((r1,r2),  axis=0)
        d[j] = delta 
    else:
        # work around expensive sparse L(K,K)=LKK
        r1 = L[0:j+1,:]
        r2 = np.concatenate((LKI, L[K,j].reshape(len(L[K,j]),1), LKK), axis=1)
        #r1.shape, r2.shape, 
        L = np.concatenate((r1,r2),  axis=0)
        w = w.reshape((len(w),1))
        q.reshape((len(q)),1)
        pi = np.dot(w.T,q)
        piv = np.multiply(pi,v)
        LKIq = np.dot(LKI.T,q)
        pivLKIq = np.subtract(piv.flatten(),LKIq.flatten())
        piSolve = np.linalg.solve(LII.T,pivLKIq)
        p = np.asarray(piSolve.flatten().tolist() + (-1*pi).flatten().tolist() + q.tolist()) 
    #retrun value
    return L,d,p
    
