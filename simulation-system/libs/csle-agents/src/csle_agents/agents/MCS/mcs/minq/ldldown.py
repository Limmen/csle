# downdates LDL^T factorization when j-th row and column are replaced 
# by j-th unit vector
#
# d contains diag(D) and is assumed positive
from scipy import sparse
import numpy as np
from minq.ldlrk1 import ldlrk1

#------------------------------------------------------------------------------
def ldldown(L,d,j):
    n = d.shape[0]     
    if j<n:
        I = [i for i in range(0,j)]
        K = [i for i in range(j+1,n)] 
        
        LKK = np.asarray([[L[i,j] for j in K] for i in K])
        dK = np.asarray([d[i] for i in K])
        LKj = np.asarray([L[i,j] for i in K])
        LKK,dK,_ = ldlrk1(LKK,dK,d[j],LKj) 
        d[K] = dK
        # work around expensive sparse L(K,K)=LKK
        r1 = L[I,:]
        r2 = sparse.coo_matrix((1,n)).toarray()
        if len(I) == 0:
            r3 = np.concatenate((sparse.coo_matrix((n-j-1,1)).toarray(), LKK), axis=1)
            L = np.concatenate((r2,r3),  axis=0)
        else:
            LKI = np.asarray([[L[i,j] for j in I] for i in K])
            #LKI = LKI.reshape((len(L[K,I]),1))
            if len(K) != 0:
                r3 = np.concatenate((LKI, sparse.coo_matrix((n-j-1,1)).toarray(), LKK), axis=1)
                #r1.shape, r2.shape, r3.shape
                L = np.concatenate((r1,r2,r3),  axis=0)   
            else:
                L = np.concatenate((r1,r2),  axis=0)   
        L[j,j] = 1 
    else:
        L[n-1,0:n-1] =  sparse.coo_matrix((1,n-1)).toarray()    
    d[j] = 1 
    return L,d

