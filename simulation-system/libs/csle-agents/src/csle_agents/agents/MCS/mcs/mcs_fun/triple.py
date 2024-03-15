import numpy as np
import copy 
#------------------------------------------------------------------------------
from functions.functions import feval
from mcs_fun.hessian import hessian
from mcs_fun.polint import polint1
#------------------------------------------------------------------------------
def triple(fcn,x,f,x1,x2,u,v,hess,G,setG = False):
    nf = 0
    n = len(x)
    g = np.zeros(n)    
    nargin = 10
    if setG:
        nargin = 9
        G =  np.zeros((n,n))
    
    ind = [i for i in range(n) if (u[i] < x[i] and x[i] < v[i])]
    ind1 = [i for i in range(n) if (x[i] <= u[i] or x[i] >= v[i])]
    
    for j in range(len(ind1)):
        g[ind1[j]] = 0
        for k in range(n):
            G[ind1[j],k] = 0
            G[k,ind1[j]] = 0
            
    if len(ind) <= 1:
        xtrip = copy.deepcopy(x)
        ftrip = copy.deepcopy(f)
        if len(ind) != 0:  
            for i in ind:
                g[i] = 1
                G[i,i] = 1
        return xtrip,ftrip,g,G,x1,x2,nf    
    # end if
    
    if setG:
        #print('reset G')
        G =  np.zeros((n,n))
    
    xtrip = copy.deepcopy(x)
    ftrip = copy.deepcopy(f)
    xtripnew = copy.deepcopy(x)
    ftripnew = copy.deepcopy(f)
    
    for j in range(len(ind)):
        i = ind[j]
        x = copy.deepcopy(xtrip)
        f = copy.deepcopy(ftrip)
        
        x[i] = x1[i]
        f1 = feval(fcn,x) 
        
        x[i] = x2[i]
        f2 = feval(fcn,x)
        nf = nf + 2
        g[i], G[i,i] = polint1([xtrip[i],x1[i],x2[i]],[f,f1,f2])
        if f1 <= f2:
            if f1 < ftrip:
                ftripnew = copy.deepcopy(f1)
                xtripnew[i] = x1[i]
        else:
            if f2 < ftrip:
                ftripnew = copy.deepcopy(f2)
                xtripnew[i] = x2[i]
        
        if nargin < 10:
            k1 = -1 
            if f1 <= f2:
                x[i] = x1[i]
            else:
                x[i] = x2[i]
            
            for k in range(i):
                if hess[i,k]:
                    if xtrip[k] > u[k] and xtrip[k] < v[k] and (len([m for m in range(len(ind)) if ind[m] == k]) != 0):
                        q1 = ftrip + g[k]*(x1[k]-xtrip[k])+0.5*G[k,k]*(x1[k]-xtrip[k])**2
                        q2 = ftrip + g[k]*(x2[k]-xtrip[k])+0.5*G[k,k]*(x2[k]-xtrip[k])**2
                        if q1 <= q2:
                            x[k] = x1[k]
                        else:
                            x[k] = x2[k]
                        f12 = feval(fcn,x)
                        nf = nf + 1
                        G[i,k] = hessian(i,k,x,xtrip,f12,ftrip,g,G)
                        #print(G[i,k])
                        G[k,i] = G[i,k]
                        if f12 < ftripnew:
                            ftripnew = copy.deepcopy(f12)
                            xtripnew = copy.deepcopy(x)
                            k1 = k
                        x[k] = xtrip[k] 
                    #end if xtrip
                else:
                    G[i,k] = 0
                    G[k,i] = 0
                #end hess[i,k]
            #end for k in i-1
        #end narg
        if ftripnew < ftrip:
            if x1[i] == xtripnew[i]:
                x1[i] = xtrip[i] 
            else: 
                x2[i] = xtrip[i] 
            if nargin < 10 and k1 > -1:
                if xtripnew[k1] == x1[k1]:
                    x1[k1] = xtrip[k1]
                else:
                    x2[k1] = xtrip[k1] 
            for k in range(i+1):
                if (len([m for m in range(len(ind)) if ind[m] == k]) != 0):
                    g[k] = g[k] + G[i,k]*(xtripnew[i] - xtrip[i])
                    if nargin < 10 and k1 > -1:
                        g[k] = g[k] + G(k1,k)*(xtripnew[k1] - xtrip[k1])
                #end if empty
            xtrip = copy.deepcopy(xtripnew)
            ftrip = copy.deepcopy(ftripnew)
        # end ftripnew
    #en for j in ind
    return xtrip,ftrip,g,G,x1,x2,nf
