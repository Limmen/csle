import numpy as np
import sys
from scipy.sparse import spdiags
from scipy import sparse

class Minq():
    def __init__(self) -> None:
        pass

    def ldlrk1(self, L,d,alp,u):
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

class UtilHelpers():
    def __init__(self) -> None:
        pass

    def ldldown(self, L,d,j):
        n = d.shape[0]     
        if j<n:
            I = [i for i in range(0,j)]
            K = [i for i in range(j+1,n)] 
            
            LKK = np.asarray([[L[i,j] for j in K] for i in K])
            dK = np.asarray([d[i] for i in K])
            LKj = np.asarray([L[i,j] for i in K])
            LKK,dK,_ = Minq().ldlrk1(LKK,dK,d[j],LKj) 
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

    def ldlup(self, L,d,j,g):
        
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
            LKK, dK, q = Minq().ldlrk1(LKK,dK,-delta,w)
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

    def getalp(self, alpu,alpo,gTp,pTGp):
        '''
            #get minimizer alp in [alpu,alpo] for a univariate quadratic
            #	q(alp)=alp*gTp+0.5*alp^2*pTGp
            #lba	lower bound active
            #uba	upper bound active
            #
            #ier	 0 (finite minimizer) 
            #	 1 (unbounded minimum)
        '''
        #alpu,alpo,gTp,pTGp = alpu,alpo,g[k],q[k] #  SHOULD BE CLOSE ATER DEBUGGING - OK

        lba = False 
        uba = False
        
        #determine unboundedness
        ier=0 
        if alpu == -np.Inf and (pTGp<0 or (pTGp==0 and gTp>0)):
            ier = 1  
            lba = True 
        if alpo == np.Inf and (pTGp<0 or (pTGp==0 and gTp<0)):
            ier = 1  
            uba = True
        if ier:
            alp = np.NAN  
            return alp,lba,uba,ier
            
        #determine activity
        if pTGp == 0 and gTp == 0:
            alp = 0 
        elif pTGp <= 0:
            #concave case minimal at a bound
            if alpu == -np.Inf:
                lba = False 
            elif alpo ==  np.Inf:
                lba = True 
            else:
                lba = (2*gTp+(alpu+alpo)*pTGp>0)  
            # end  alpu == -np.Inf
            uba = not lba
        else:
            alp=-gTp/pTGp           #unconstrained optimal step
            lba = (alp <= alpu)     #lower bound active
            uba = (alp >= alpo)     #upper bound active
        
        if lba:
            alp = alpu
        if uba:
            alp = alpo
        
        if abs(alp) == np.Inf:
            gTp,pTGp,alpu,alpo,alp,lba,uba,ier
        return alp,lba,uba,ier

    def minqsub(self, nsub,free,L,dd,K,G,n,g,x,xo,xu,convex,xx,fct,nfree,unfix,alp,alpu,alpo,lba,uba,ier,subdone):
        #nsub,fct,G,L,dd,K,g,xo,xu,x,xx,n,alpu,alpo,convex,alp,lba,uba,ier,free,nfree
        nsub = nsub + 1 
        eps = 2.2204e-16
        # downdate factorization
        freelK = [i for i in range(len(free)) if (free<K)[i] == True]
        for j in freelK: 	# list of newly active indices
            #print(j)
            L,dd = self.ldldown(L,dd,j)
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
            L,dd,p = self.ldlup(L,dd,j,p)
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
        
        alp,lba,uba,ier = self.getalp(alpu,alpo,gTp,pTGp) 
        
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

class LSUtils(UtilHelpers):
    def __init__(self) -> None:
        super(LSUtils, self).__init__()


    def lsguard(self, alp, alist, amax, amin, small):
        asort = alist
        asort.sort()
        s = len(asort)
        
        # enforce extrapolation to be cautious
        al = asort[0]- (asort[s-1] - asort[0])/small
        au = asort[s-1] + (asort[s-1] - asort[0])/small
        alp = max(al, min(alp,au))
        alp = max(amin, min(alp, amax))
        
        # enforce some distance from end points
        # 	factor 1/3 ensures equal spacing if s=2 and the third point
        # 	in a safeguarded extrapolation is the maximum.
        if abs(alp-asort[0]) < small*(asort[1] - asort[0]):
            alp = (2*asort[0] + asort[1]) / 3
        
        if abs(alp-asort[s-1]) < small*(asort[s-1] - asort[s-1-1]):
            alp = (2*asort[s-1] + asort[s-1-1])/3
        
        return alp

    def lssplit(self, i, alist, flist, short):
        if flist[i] < flist[i+1]:
            fac = short
        elif flist[i] > flist[i+1]:
            fac = 1 - short
        else:
            fac = 0.5

        alp = alist[i] + fac*(alist[i+1] - alist[i])
        #if prt>2, disp(['split at ',num2str(alp)]); end;
        return alp, fac

    def minq(self, gam,c,G,xu,xo,prt):
        '''
        # minimizes an affine quadratic form subject to simple bounds,
        # using coordinate searches and reduced subspace minimizations
        # using LDL^T factorization updates
        #    min    fct  =  gam + c^T x + 0.5 x^T G x 
        #    s.t.   x in [xu,xo]    # xu <= xo is assumed
        # where G is a symmetric n x n matrix, not necessarily definite
        # (if G is indefinite, only a local minimum is found)
        #
        # if G is sparse, it is assumed that the ordering is such that
        # a sparse modified Cholesky factorization is feasible
        #
        # prt	printlevel
        # xx	initial guess (optional)
        #
        # x	minimizer (but unbounded direction if ier = 1)
        # fct	optimal function value
        # ier	0  (local minimizer found)
        # 	1  (unbounded below)
        # 	99 (maxit exceeded)
        # 	-1 (input error)
        #
        # calls getalp.m, ldl*.m, minqsub.m, pr01.m
        '''
        #%%
        #gam,c,G,xu,xo,prt = 0,cc,G,yu,yo,prt #  SHOULD BE CLOSE FATER DEBUGGING
        
        #% initialization 
        convex  =  0  
        n = G.shape[0]
            
        # check input data for consistency
        ier = 0  
        if G.shape[1] != n: 
            ier = -1  
            print('minq: Hessian has wrong dimension')  
            x = np.NAN + np.zeros(n)  
            fct = np.NAN  
            nsub = -1
            return x,fct,ier 

        if c.shape[0] != n:
            ier = -1  
            print('minq: linear term has wrong dimension')  

        if xu.shape[0] != n: 
            ier = -1  
            print('minq: lower bound has wrong dimension')  
        
        if xo.shape[0] != n:
            ier = -1  
            print('minq: lower bound has wrong dimension')  

        if 'xx' in locals():
            if xx.shape[0] != n: 
                ier = -1  
                print('minq: lower bound has wrong dimension')  
        else:
            # initialize trial point xx, function value fct and gradient g
            # cold start with absolutely smallest feasible point
            xx = np.zeros(n)
                
        if ier == -1:
            x = np.NAN + np.zeros(n)  
            fct = np.NAN  
            nsub = -1
            return x,fct,ier    
        
        maxit = 3*n  # maximal number of iterations
        # this limits the work to about 1+4*maxit/n matrix multiplies
        # usually at most 2*n iterations are needed for convergence
        nitrefmax = 3  # maximal number of iterative refinement steps
        
        # force starting point into the box
        xx = np.asarray([max(xu[i],min(xx[i],xo[i])) for i in range(len(xx))])
        
        # regularization for low rank problems
        eps = 2.2204e-16
        hpeps = 100*eps  # perturbation in last two digits
        G = G + spdiags(hpeps*np.diag(G),0,n,n).toarray()
        
        # initialize LDL^T factorization of G_KK
        K = np.zeros(n, dtype=bool) # initially no rows in factorization
        L = np.eye(n)
        dd = np.ones(n)
        
        # dummy initialization of indicator of free variables
        # will become correct after first coordinate search
        free = np.zeros(n, dtype=bool)   
        nfree = 0 
        nfree_old = -1  
        
        fct = np.Inf       # best function value
        nsub = 0  	    # number of subspace steps
        unfix = 1  	    # allow variables to be freed in csearch?
        nitref = 0      # no iterative refinement steps so far
        improvement = 1 # improvement expected
        
        #print(gam,c,G,xu,xo,xx,K,L,dd)
        #%%
        # main loop: alternating coordinate and subspace searches 
        while 1:
            #print('enter main loop')   #
            if np.linalg.norm(xx,np.inf) == np.inf:
                sys.exit('infinite xx in minq.m')

            g = np.dot(G,xx)+c 
            fctnew = gam + np.dot(0.5*xx.T,(c+g))
            #print(g,fctnew)
            if not improvement:
                # good termination 
                # print('terminate: no improvement in coordinate search')   
                ier = 0   
                break   
            elif nitref>nitrefmax:
                # good termination 
                # print('terminate: nitref>nitrefmax')
                ier = 0   
                break   
            elif nitref>0 and nfree_old == nfree and fctnew >=  fct: # Ok Chacked
                # good termination 
                # print('terminate: nitref>0 and nfree_old == nfree and fctnew >= fct')   
                ier = 0   
                break
            elif nitref == 0:
                x = xx  
                fct = min(fct,fctnew)  
            else: # more accurate g and hence f if nitref>0
                x = xx  
                fct = fctnew  
    
                
            if nitref == 0 and nsub >= maxit: # ok checked
                #print('incomplete minimization, too many iterations, iteration limit exceeded maxit')
                ier = 99  
                break  
            #print(g,x,fct,fctnew)
            #%%----------------------------------------------------------------------
            # coordinate search
        
            count = 0   	# number of consecutive free steps
            k = -1       	# current coordinate searched (initilize to -index for python array shake)
            while 1:
                while count <= n:# ok checked
                    # find next free index (or next index if unfix)
                    count = count + 1  
                    if k == n-1:
                        k = -1 # reset k to -1 for python array first index
                    k = k + 1 # increase k
                    if free[k] or unfix:
                        break
                # end while count <= n
                if count > n:
                    #print('complete sweep performed without fixing a new active bound')
                    break           
                
                #print(k)            
                q = G[:,k]
                alpu = xu[k]-x[k]   
                alpo = xo[k]-x[k]   # bounds on step
                #print(q,alpu,alpo)
        
                # find step size
                alp,lba,uba,ier = self.getalp(alpu,alpo,g[k],q[k])
                
                if ier:
                    x = np.zeros(n)   
                    if lba:
                        x[k] = -1
                    else:
                        x[k] = 1
                        
                    return x,fct,ier
                    #print(x,fct,ier,nsub)
                    break
                #end itr
                
                xnew = x[k]+alp  
                if prt and nitref>0:
                    xnew,alp
                    
                if lba or xnew <= xu[k]:# ok checked
                    # lower bound active
                    #if prt>2: print([num2str[k], ' at lower bound'])   #
                    if alpu != 0:
                        x[k] = xu[k]  
                        g = g + alpu*q  
                        count = 0  
                    free[k] = 0  
                elif uba or xnew >= xo[k]: # OK checked
                    # upper bound active
                    #if prt>2, print([num2str[k], ' at upper bound'])   #
                    if alpo != 0:
                        x[k] = xo[k]  
                        g = g + alpo*q  
                        count = 0  
                    free[k] = 0  
                else:
                    # no bound active
                    #if prt>2, print([num2str[k], ' free'])   #
                    if alp != 0.0:
                        if prt>1 and not free[k]:
                            unfixstep = [x[k],alp]
                        x[k] = xnew  
                        g = g + alp*q  
                        free[k] = 1   
                #end if bound check
                #print(g)
            # end while of coordinate search
            
            
            nfree = sum(free)  
            if (unfix and nfree_old == nfree):
                # in exact arithmetic, we are already optimal
                # recompute gradient for iterative refinement
                g = np.dot(G,x)+c
                nitref = nitref + 1  
                #if prt>0:
                #    print('optimum found   iterative refinement tried')  
            else:
                nitref = 0  
            nfree_old = nfree  
            gain_cs = fct-gam-np.dot(0.5*x.T,(c+g))
            improvement = (gain_cs>0 or not unfix)  
            # subspace search
            xx = x  
            #%%
            if not improvement or nitref>nitrefmax:
                # optimal point found - nothing done
                nothing_to_do = 'done!'
            elif nitref > nitrefmax:
                # enough refinement steps - nothing done
                nothing_to_do = 'done!'
            elif nfree == 0:
                # no free variables - no subspace step taken
                # print('no free variables - no subspace step taken')
                unfix = 1  
            else:
                # take a subspace step
                subdone = 0
                nsub,free,L,dd,K,G,n,g,x,xo,xu,convex,xx,fct,nfree,alp,alpu,alpo,lba,uba,ier,unfix,subdone = self.minqsub(nsub,free,L,dd,K,G,n,g,x,xo,xu,convex,xx,fct,nfree,unfix,alp,alpu,alpo,lba,uba,ier,subdone)
                if not subdone:
                    return x,fct,ier
                if ier:
                    #print(itr)
                    return x,fct,ier   
        # end while of main loop
        return x,fct,ier

    def quartic(self, a, x):
        return (((a[0]*x + a[1])* x + a[2])* x+a[3])*x+a[4]