import numpy as np
import copy
import sys
#------------------------------------------------------------------------------
from functions.functions import feval
from mcs_fun.csearch import csearch
from mcs_fun.chk_flag import chrelerr 
from mcs_fun.chk_flag import chvtr
from mcs_fun.neighbor import neighbor
from mcs_fun.triple import triple

from gls.gls import gls
from minq.minq import minq
#------------------------------------------------------------------------------
def lsearch(fcn,x,f,f0,u,v,nf,stop,maxstep,gamma,hess,nsweep,nsweepbest):    
    ncall = 0# 
    n = len(x)# 
    x0 = np.asarray([min(max(u[i],0),v[i]) for i in range(len(u))])#  % absolutely smallest point

    flag = 1# 
    eps0 = 0.001# 
    nloc = 1# 
    small = 0.1# 
    smaxls = 15# 
    
    xmin,fmi,g,G,nfcsearch = csearch(fcn,x,f,u,v,hess)
    
    xmin = [max(u[i],min(xmin[i],v[i])) for i in range(n)]
    ncall = ncall + nfcsearch
    xold = copy.deepcopy(xmin) # deep copy is must here
    fold = copy.deepcopy(fmi)
    #print('csearch ends with:') # print(xmin,fmi,g,G,nfcsearch)
    
    eps = 2.220446049250313e-16
    
    if stop[0] > 0  and  stop[0] < 1:
        flag = chrelerr(fmi,stop)# 
    elif stop[0] == 0:
        flag = chvtr(fmi,stop[1])# 

    if not flag:
        return xmin,fmi,ncall,flag,nsweep,nsweepbest
    
    d = np.asarray([min(min(xmin[i]-u[i],v[i]-xmin[i]),0.25*(1+abs(x[i]-x0[i]))) for i in range(n)])
    # Calling MINQ function # print(fmi,g,G,-d,d,0)
    p,_,_ = minq(fmi,g,G,-d,d,0) # print('minq') # print(p) 
    
    x = [max(u[i],min(xmin[i]+p[i],v[i])) for i in range(n)]
    p = np.subtract(x,xmin)  # project search direction to box
    
    if np.linalg.norm(p):
        f1 = feval(fcn,x)
        ncall = ncall + 1
        alist = [0,1] 
        flist = [fmi,f1] 
        fpred = fmi + np.dot(g.T,p) + np.dot(0.5, np.dot(p.T,np.dot(G,p)))        
        alist,flist,nfls = gls(fcn,u,v,xmin,p,alist,flist,nloc,small,smaxls)
        ncall = ncall + nfls
        
        i = np.argmin(flist)
        fminew = min(flist)
        if fminew == fmi:
            i = [i for i in range(len(alist)) if not alist[i]][0] 
        else:
            fmi = copy.deepcopy(fminew)
        
        xmin = xmin + np.dot(alist[i],p)
        xmin = np.asarray([max(u[i],min(xmin[i],v[i])) for i in range(n)])
        gain = f - fmi
        
        if stop[0] > 0  and  stop[0] < 1:
            flag = chrelerr(fmi,stop)
        elif stop[0] == 0:
            flag = chvtr(fmi,stop[1])
        
        if not flag:
            return xmin,fmi,ncall,flag,nsweep,nsweepbest
        
        if fold == fmi:
            r = 0
        elif fold == fpred:
            r = 0.5
        else:
            r = (fold-fmi)/(fold-fpred)
    else:
        gain = f - fmi 
        r = 0
        
    diag = 0
    ind = [i for i in range(n) if (u[i] < xmin[i]  and  xmin[i] < v[i])] 
    b = np.dot(np.abs(g).T,[max(abs(xmin[i]),abs(xold[i])) for i in range(len(xmin))]) # print('chek b')  print(g,xmin,xold) # print(b)
    nstep = 0
    
    #print('ncall',nf, ncall, maxstep, len(ind),fmi, gain, r)
    while (ncall < nf)  and  (nstep < maxstep)  and  ((diag or len(ind) < n) or (stop[0] == 0  and  fmi - gain <= stop[1]) or (b >= gamma*(f0-f)  and  gain > 0)):
        #print('while')
        nstep = nstep + 1
        delta = [abs(xmin[i])*eps**(1/3) for i in range(len(xmin))]
        #print('delta:',xmin, delta)        
        j = [inx for inx in range(len(delta)) if (not delta[inx])]
        if len(j)  != 0:
            for inx in j:
                delta[inx] = eps**(1/3)*1 
                
        x1,x2 = neighbor(xmin,delta,u,v)
        f = copy.deepcopy(fmi)

        if len(ind) < n  and  (b < gamma*(f0-f) or (not gain)):
            ind1 = [i for i in range(len(u)) if (xmin[i] == u[i] or xmin[i] == v[i])] 
            for k in range(len(ind1)):
                i = ind1[k]
                x = copy.deepcopy(xmin)
                if xmin[i] == u[i]:
                    x[i] = x2[i] 
                else:
                    x[i]  = x1[i]
                f1 = feval(fcn,x)
                ncall = ncall + 1

                if f1 < fmi:
                    alist = [0, x[i], -xmin[i]]
                    flist = [fmi, f1]
                    p = np.zeros(n) 
                    p[i]  = 1
                    alist,flist,nfls = gls(fcn,u,v,xmin,p,alist,flist,nloc,small,6)
                    ncall = ncall + nfls
                    j = np.argmin(flist)
                    fminew = min(flist)# 
                    if fminew == fmi:
                        j = [inx for inx in range(len(alist)) if (not alist[inx])][0]
                    else:
                        fmi = fminew
                    xmin[i]  = xmin[i]  + alist[j]
                else:
                    ind1[k] = -1
            #end for
            xmin = np.asarray([max(u[inx],min(xmin[inx],v[inx])) for inx in range(len(xmin))])
            if not sum(ind1):
                break
        
            for inx in range(len(delta)):
                delta[inx] = abs(xmin[inx])*eps**(1/3)
            j = [inx for inx in range(len(delta)) if (not delta[inx])]
            if len(j) != 0:
                for inx in j:
                    delta[inx] = eps**(1/3)*1
            #end if
            x1,x2 = neighbor(xmin,delta,u,v)    
        #end if
        #print('r',r)
        if abs(r-1) > 0.25 or (not gain) or (b < gamma*(f0-f)):
            xmin,fmi,g,G,x1,x2,nftriple = triple(fcn,xmin,fmi,x1,x2,u,v,hess,0,True)
            ncall = ncall + nftriple
            diag = 0 
        else:
            xmin,fmi,g,G,x1,x2,nftriple = triple(fcn,xmin,fmi,x1,x2,u,v,hess,G)
            ncall = ncall + nftriple
            diag = 1
        #end if
        #print(nftriple)
        xold = copy.deepcopy(xmin)
        fold = copy.deepcopy(fmi)
        
        if stop[0] > 0  and  stop[0] < 1:
            flag = chrelerr(fmi,stop)# 
        elif stop[0] == 0:
            flag = chvtr(fmi,stop[1])# 
     
        if not flag:
            return xmin,fmi,ncall,flag,nsweep,nsweepbest
        if r < 0.25:
            d = 0.5*d
        elif r > 0.75:
            d = 2*d

        minusd = np.asarray([max(-d[jnx],u[jnx]-xmin[jnx]) for jnx in range(len(xmin))])
        mind = np.asarray([min(d[jnx],v[jnx]-xmin[jnx]) for jnx in range(len(xmin))])
        p,_,_ = minq(fmi,g,G,minusd,mind,0)
        
        #print(p, np.linalg.norm(p))
        if not (np.linalg.norm(p))  and  (not diag)  and  (len(ind) == n):
            break
        
        if np.linalg.norm(p):
            #print(g, p, G)
            fpred = fmi + np.dot(g.T,p) + np.dot(0.5, np.dot(p.T,np.dot(G,p)))
            x = copy.deepcopy(xmin + p)
            f1 = feval(fcn,x)
            ncall = ncall + 1
            alist = [0, 1]
            flist = [fmi, f1]
            alist,flist,nfls = gls(fcn,u,v,xmin,p,alist,flist,nloc,small,smaxls)
            ncall = ncall + nfls
            argmin = np.argmin(flist)
            fmi = min(flist)
            xmin = [xmin[jnx] + alist[argmin]*p[jnx] for jnx in range(len(xmin))] 
            xmin = np.asarray([max(u[jnx],min(xmin[jnx],v[jnx])) for jnx in range(len(xmin))])
            if stop[0] > 0  and  stop[0] < 1:
                flag = chrelerr(fmi,stop)# 
            elif stop[0] == 0:
                flag = chvtr(fmi,stop[1])# 
            if not flag:
                return xmin,fmi,ncall,flag,nsweep,nsweepbest
            
            gain = f - fmi
            if fold == fmi:
                r = 0 
            elif fold == fpred:
                r = 0.5
            else:
                r = (fold-fmi)/(fold-fpred);
            if fmi < fold:
                fac = abs(1-1/r)# 
                eps0 = max(eps,min(fac*eps0,0.001))# 
            else:
                eps0 = 0.001# 
        else:
            gain = f - fmi
            if (not gain):
                eps0 = 0.001
                fac = np.Inf
                r = 0 
            #end not gain
        #end if norm p
        ind = [inx for inx in range(len(u)) if (u[inx] < xmin[inx]  and  xmin[inx] < v[inx])]
        b = np.dot(np.abs(g).T,[max(abs(xmin[inx]),abs(xold[inx])) for inx in range(len(xmin))])
    #end while
    return xmin,fmi,ncall,flag,nsweep,nsweepbest
  
