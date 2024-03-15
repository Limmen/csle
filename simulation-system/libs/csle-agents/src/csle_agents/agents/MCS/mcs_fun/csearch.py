import numpy as np
import copy
#------------------------------------------------------------------------------
from functions.functions import feval
from mcs_fun.hessian import hessian
from mcs_fun.polint import polint1
from gls.gls import gls
#------------------------------------------------------------------------------
def csearch(fcn,x,f,u,v,hess):
    n = len(x)
    x = [min(v[i],max(x[i],u[i])) for i in range(len(x))]

    nfcsearch = 0
    smaxls = 6
    small = 0.1
    nloc = 1  
    hess = np.ones((n,n))
    xmin = copy.deepcopy(x)  
    fmi = copy.deepcopy(f) 
    xminnew = copy.deepcopy(xmin)
    fminew = copy.deepcopy(fmi)
    g = np.zeros(n)
    ind0 = []
    
    x1 =  np.zeros(n)
    x2 =  np.zeros(n)
    G = np.zeros((n,n))
    eps = 2.220446049250313e-16
    
    for i in range(n):
        p = np.zeros(n)
        p[i] = 1
        if xmin[i]:
            delta = eps**(1/3)*abs(xmin[i])
        else:
            delta = eps**(1/3)
        linesearch = True  
        if xmin[i] <= u[i]:
            f1 = feval(fcn,xmin+delta*p)  
            nfcsearch = nfcsearch + 1
            if f1 >= fmi:
                f2 = feval(fcn,xmin+2*delta*p)
                nfcsearch = nfcsearch + 1
                x1[i] = xmin[i] + delta
                x2[i] = xmin[i] + 2*delta
                if f2 >= fmi:
                    xminnew[i] = xmin[i]
                    fminew = fmi
                else:
                    xminnew[i] = x2[i]
                    fminew = copy.deepcopy(f2)
                linesearch = False  
            else:
                alist = [0, delta] 
                flist = [fmi, f1]
        elif xmin[i] >= v[i]:
            f1 = feval(fcn,xmin-delta*p)
            nfcsearch = nfcsearch + 1 
            if f1 >= fmi:
                f2 = feval(fcn,xmin-2*delta*p)
                nfcsearch = nfcsearch + 1 
                x1[i] = xmin[i] - delta
                x2[i] = xmin[i] - 2*delta 
                if f2 >= fmi:
                    xminnew[i] = xmin[i]
                    fminew = fmi
                else:
                    xminnew[i] = x2[i]
                    fminew = f2
                linesearch = False
            else:
                alist = [0, -delta]#  
                flist = [fmi, f1]#  
        else:
            alist = 0
            flist = fmi
        
        if linesearch:
            #print('line search:',xmin)
            alist,flist,nfls = gls(fcn,u,v,xmin,p,alist,flist,nloc,small,smaxls)
            nfcsearch = nfcsearch + nfls #print('test gls') #print(alist,flist)
            
            j = np.argmin(flist)
            fminew = min(flist)   #print(fminew,j)
            
            if fminew == fmi:
                j = [inx for inx in range(len(alist)) if not alist[inx]][0]

            ind = [inx for inx in range(len(alist)) if abs(alist[inx]-alist[j])<delta]   #print(ind)
            ind1 = [inx for inx in range(len(ind)) if ind[inx] == j]  #print(ind1)
            
            for inx in ind1:
                del  ind[inx] 

            for inx in ind:
                del  alist[inx]
                del  flist[inx]
            
            j = np.argmin(flist)
            fminew = min(flist) 
            xminnew[i] = xmin[i] + alist[j] #print('test csearch')  #print(flist,j,fminew, xminnew)
            if i == 0 or not alist[j]:#
                if j == 0: 
                    x1[i] = xmin[i] + alist[1]  
                    f1 = flist[1]  
                    x2[i] = xmin[i] + alist[2]  
                    f2 = flist[2]  
                elif j == len(alist)-1:
                    x1[i] = xmin[i] + alist[j-1]
                    f1 = flist[j-1]
                    x2[i] = xmin[i] + alist[j-2]  
                    f2 = flist[j-2]
                else:
                    #print(xmin[i],alist[j-1],alist[j+1])
                    x1[i] = xmin[i] + alist[j-1]
                    f1 = flist[j-1]
                    x2[i] = xmin[i] + alist[j+1]
                    f2 = flist[j+1]
                #end if j == 0 elsif, else    
                xmin[i] = xminnew[i]  
                fmi = copy.deepcopy(fminew) 
            else:
                x1[i] = xminnew[i]
                f1 = copy.deepcopy(fminew)
                if xmin[i] < x1[i] and j < len(alist)-1:
                    x2[i] = xmin[i] + alist[j+1]
                    f2 = flist[j+1]
                elif j == 0:
                    if alist[j+1]:
                        x2[i] = xmin[i] + alist[j+1]  
                        f2 = flist[j+1]
                    else:
                        x2[i] = xmin[i] + alist[j+2]
                        f2 = flist[j+2]
                elif alist[j-1]:
                    x2[i] = xmin[i] + alist[j-1]
                    f2 = flist[j-1]
                else:
                    x2[i] = xmin[i] + alist[j-2]
                    f2 = flist[j-2]
        #end if linesearch
        g[i], G[i,i] = polint1([xmin[i], x1[i], x2[i]],[fmi, f1, f2])                 
        x = copy.deepcopy(xmin)
        k1 = -1
        if f1 <= f2:
            x[i] = x1[i]
        else:
            x[i] = x2[i]
        for k in range(i):
            if hess[i,k]:
                q1 = fmi + g[k]*(x1[k]-xmin[k])+0.5*G[k,k]*(x1[k]-xmin[k])**2  
                q2 = fmi + g[k]*(x2[k]-xmin[k])+0.5*G[k,k]*(x2[k]-xmin[k])**2  
                if q1 <= q2:
                    x[k] = x1[k]
                else:
                    x[k] = x2[k]
                f12 = feval(fcn,x)
                nfcsearch = nfcsearch + 1
                G[i,k] = hessian(i,k,x,xmin,f12,fmi,g,G)#  
                G[k,i] = G[i,k]
                if f12 < fminew:
                    fminew = f12 
                    xminnew = copy.deepcopy(x)
                    k1 = k
                x[k] = xmin[k]
            else:
                G[i,k] = 0
                G[k,i] = 0
        # end for k in i        
        if fminew <= fmi:
            if x1[i] == xminnew[i]:
                x1[i] = xmin[i]
            elif x2[i] == xminnew[i]:
                x2[i] = xmin[i]
            if k1 > -1:
                if xminnew[k1] == x1[k1]:
                    x1[k1] = xmin[k1]
                elif xminnew[k1] == x2[k1]:
                    x2[k1] = xmin[k1]
            #print('xmins',k1,xminnew[i],xmin[i])  
            for k in range(i+1):
                g[k] = g[k] + G[i,k]*(xminnew[i] - xmin[i])
                if k1 > -1:
                    g[k] = g[k] + G[k1,k]*(xminnew[k1] - xmin[k1])
            #end for k in i
        xmin = copy.deepcopy(xminnew)
        fmi = copy.deepcopy(fminew) 
        #print('check',i)  print(g[i], G[i,i])
    #end for i
    return xmin,fmi,g,G,nfcsearch