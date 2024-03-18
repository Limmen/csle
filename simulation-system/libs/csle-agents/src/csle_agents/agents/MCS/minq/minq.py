import sys
import numpy as np
from scipy.sparse import spdiags
from minq.getalp import getalp
from minq.minqsub import minqsub
#%%------------------------------------------------------------------------------
def minq(gam,c,G,xu,xo,prt):
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
            alp,lba,uba,ier = getalp(alpu,alpo,g[k],q[k])
            
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
            nsub,free,L,dd,K,G,n,g,x,xo,xu,convex,xx,fct,nfree,alp,alpu,alpo,lba,uba,ier,unfix,subdone = minqsub(nsub,free,L,dd,K,G,n,g,x,xo,xu,convex,xx,fct,nfree,unfix,alp,alpu,alpo,lba,uba,ier,subdone)
            if not subdone:
                return x,fct,ier
            if ier:
                #print(itr)
                return x,fct,ier   
    # end while of main loop
    return x,fct,ier