# patch for minq.m containing the subspace search
from minq.ldldown import ldldown
from minq.ldlup import ldlup
from minq.getalp import getalp
import numpy as np
import sys
#%%------------------------------------------------------------------------------
def minqsub(nsub,free,L,dd,K,G,n,g,x,xo,xu,convex,xx,fct,nfree,unfix,alp,alpu,alpo,lba,uba,ier,subdone):
    #nsub,fct,G,L,dd,K,g,xo,xu,x,xx,n,alpu,alpo,convex,alp,lba,uba,ier,free,nfree
    nsub = nsub + 1 
    eps = 2.2204e-16
    # downdate factorization
    freelK = [i for i in range(len(free)) if (free<K)[i] == True]
    for j in freelK: 	# list of newly active indices
        #print(j)
        L,dd = ldldown(L,dd,j)
        K[j] = False  
    
    # update factorization or find indefinite search direchtion
    definite = 1 
    freeuK = [i for i in range(len(free)) if (free>K)[i] == True]
    for j in freeuK: 	# list of newly freed indices
        #print(j)    
        # later: speed up the following by passing K to ldlup.m!
        p = np.zeros(n)
        if n>1:
            p = np.asarray([G[i,j] if K[i]==True else p[i] for i in range(len(K))])
        p[j] = G[j,j] 
        L,dd,p = ldlup(L,dd,j,p)
        definite = (len(p) == 0)
        if not definite:
            #print('indefinite or illconditioned step') # 
            break  
        K[j] = True 
    
    
    if definite:
        # find reduced Newton direction 
        p = np.zeros(n) 
        p = np.asarray([g[i] if K[i] == True else p[i] for i in range(len(K))])
        
        LPsolve = np.linalg.solve(L,p)
        LPsolve = np.divide(LPsolve,dd)
        p = np.multiply(-1,np.linalg.solve(L.T,LPsolve))
        
    # set tiny entries to zero 
    p = (x+p)-x 
    ind = [i for i in range(len(p)) if p[i] != 0]
    if len(ind) == 0:
        # zero direction
        #print('zero direction') #
        unfix = 1 
        subdone = 0
        return nsub,free,L,dd,K,G,n,g,x,xo,xu,convex,xx,fct,nfree,alp,alpu,alpo,lba,uba,ier,unfix,subdone
    
    # find range of step sizes
    pp = np.asarray([p[i] for i in ind])
    oo = np.subtract([xo[i] for i in ind],[x[i] for i in ind])/pp
    uu = np.subtract([xu[i] for i in ind],[x[i] for i in ind])/pp
    alpu = max([oo[i] for i in range(len(ind)) if pp[i]<0] +[uu[i] for i in range(len(ind)) if pp[i]>0] + [-np.inf]) 
    alpo = min([oo[i] for i in range(len(ind)) if pp[i]>0] +[uu[i] for i in range(len(ind)) if pp[i]<0] + [np.inf]) 
    if alpo <= 0 or alpu >= 0:
        sys.exit('programming error: no alp')
    
    # find step size 
    gTp = np.dot(g.T,p)
    agTp = np.dot(np.abs(g).T,np.abs(p))
    if abs(gTp) < 100*eps*agTp:
        # linear term consists of roundoff only
        gTp=0 
        
    pTGp = np.dot(p.T,np.dot(G,p)) 
    if convex:
        pTGp = max(0,pTGp)
    if not definite and pTGp >0: 
        #if prt, disp(['tiny pTGp = ',num2str(pTGp),' set to zero'])  #
        pTGp=0  
    
    alp,lba,uba,ier = getalp(alpu,alpo,gTp,pTGp) 
    
    if ier:
        x = np.zeros(n)  
        if lba:
            x = -p  
        else:
            x = p
        return nsub,free,L,dd,K,G,n,g,x,xo,xu,convex,xx,fct,nfree,alp,alpu,alpo,lba,uba,ier,unfix,subdone

    unfix = not (lba or uba)  # allow variables to be freed in csearch?    
    # update of xx
    for k in range(0,len(ind)):
        # avoid roundoff for active bounds 
        ik = ind[k]
        if alp == uu[k]:
            xx[ik] = xu[ik] 
            free[ik] = 0 
        elif alp == oo[k]:
            xx[ik] = xo[ik]  
            free[ik] = 0 
        else:
            xx[ik]=xx[ik]+alp*p[ik] 
        
        if abs(xx[ik]) == np.Inf:
            ik,alp,p[ik]
            sys.exit('infinite xx in minq')
    
    nfree = sum(free)
    subdone = 1 
    return nsub,free,L,dd,K,G,n,g,x,xo,xu,convex,xx,fct,nfree,alp,alpu,alpo,lba,uba,ier,unfix,subdone