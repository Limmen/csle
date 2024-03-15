import numpy as np
import math
import copy
#------------------------------------------------------------------------------
from functions.functions import feval
from mcs_fun.genbox import genbox
from mcs_fun.initi_func import subint
from mcs_fun.chk_flag import chrelerr 
from mcs_fun.chk_flag import chvtr
from mcs_fun.updtrec import updtrec
from mcs_fun.sign import sign
#------------------------------------------------------------------------------
def splinit(fcn,i,s,smax,par,x0,n0,u,v,x,y,x1,x2,L,l,xmin,fmi,ipar,level,ichild,f,xbest,fbest,stop,prt, record,nboxes,nbasket,nsweepbest,nsweep):
    '''
    % splits box # par at level s according to the initialization list
    % in the ith coordinate and inserts its children and their parameters
    % in the list 
    '''

    # initialization 
    ncall = 0
    n = len(x)
    f0 = np.zeros(max(L)+1)
    flag = 1
    
    for j in range(L[i]+1):
        if j != l[i]:
            x[i] = x0[i,j]
            f0[j] = feval(fcn,x)
            ncall = ncall + 1
            if f0[j] < fbest:
                fbest = f0[j]
                xbest = copy.deepcopy(x)
                nsweepbest = copy.deepcopy(nsweep)
                if stop[0] > 0 and stop[0] < 1:
                    flag = chrelerr(fbest,stop)
                elif stop[0] == 0:
                    flag = chvtr(fbest,stop[2])      
                if not flag:
                    return xbest,fbest,f0,xmin,fmi,ipar,level,ichild,f,flag,ncall, record,nboxes,nbasket,nsweepbest,nsweep  
        else:
            f0[j] = f[0,par]
        #end j != l[i]
    #end for j
    if s + 1 < smax:
        nchild = 0
        if u[i] < x0[i,0]: # in that case the box at the boundary gets level s + 1
            nchild = nchild + 1
            nboxes = nboxes + 1
            ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+1,-nchild,f0[0])
            record = updtrec(nboxes,level[nboxes],f[0,:], record)
        #end if ui <  xo[i,0]
        for j in range(L[i]):
            nchild = nchild + 1
            #splval = split1(x0[i,j],x0[i,j+1],f0[j],f0[j+1])
            if f0[j] <= f0[j+1] or s + 2 < smax:
                nboxes = nboxes + 1
                if f0[j] <= f0[j+1]:
                    level0 = s + 1
                else:
                    level0 = s + 2
                #end if f0
                # the box with the smaller function value gets level s + 1, the one with
                # the larger function value level s + 2
                ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,level0,-nchild,f0[j])
                record = updtrec(nboxes,level[nboxes],f[0,:], record)
            else:
                x[i] = x0[i,j]
                nbasket = nbasket + 1
                if(len(xmin) == nbasket):
                    xmin.append(copy.deepcopy(x))
                    fmi.append(f0[j])                  
                else:
                    xmin[nbasket] = copy.deepcopy(x)
                    fmi[nbasket] = f0[j]
            #end if f0[j] <= f0[j+1]  or s + 2 < smax
            nchild = nchild + 1                
            if f0[j+1] < f0[j] or s + 2 < smax:
                nboxes = nboxes + 1
                if f0[j+1] < f0[j]:
                    level0 = s + 1
                else:
                    level0 = s + 2
                #end
                ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,level0,-nchild,f0[j+1])
                record = updtrec(nboxes,level[nboxes],f[0,:], record)
            else:
                x[i] = x0[i,j+1]
                nbasket = nbasket + 1
                if(len(xmin) == nbasket):
                    xmin.append(copy.deepcopy(x))
                    fmi.append(f0[j+1])
                else:
                    xmin[nbasket] = copy.deepcopy(x)
                    fmi[nbasket] = f0[j+1]
            #end f0[j+1] < f0[j]
        #end for
        if x0[i,L[i]] < v[i]: # in that case the box at the boundary gets level s + 1
            nchild = nchild + 1
            nboxes = nboxes + 1
            ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+1,-nchild,f0[L[i]])
            record = updtrec(nboxes,level[nboxes],f[0,:], record)
        ##end if x0 < vi
    else:
        for j in range(L[i]+1):
            x[i] = x0[i,j]
            nbasket = nbasket + 1
            if(len(xmin) == nbasket):
                xmin.append(copy.deepcopy(x))
                fmi.append(f0[j])
            else:
                xmin[nbasket] = copy.deepcopy(x)
                fmi[nbasket] = f0[j]
    #end  s+1 < smax
    return xbest,fbest,f0,xmin,fmi,ipar,level,ichild,f,flag,ncall, record,nboxes,nbasket,nsweepbest,nsweep  

#------------------------------------------------------------------------------
def split(fcn,i,s,smax,par,n0,u,v,x,y,x1,x2,z,xmin,fmi,ipar,level,ichild,f,xbest,fbest,stop,prt, record,nboxes,nbasket,nsweepbest,nsweep):
    '''
        split function
    '''
    ncall = 0
    n = len(x)
     
    flag = 1
    x[i] = z[1]
    f[1,par] = feval(fcn,x)
    ncall = ncall + 1
    #print('fbest:',fbest)
    
    if f[1,par] < fbest:
        fbest = copy.deepcopy(f[1,par])
        xbest = copy.deepcopy(x)
        nsweepbest = copy.deepcopy(nsweep)
        
        if stop[0] > 0 and stop[0] < 1:
            flag = chrelerr(fbest,stop)
        elif stop[0] == 0:
            flag = chvtr(fbest,stop[2])
        #end
        if not flag:
            return xbest,fbest,xmin,fmi,ipar,level,ichild,f,flag,ncall, record,nboxes,nbasket,nsweepbest,nsweep
    #end if f-par < best
    #splval = split1(z[0],z[1],f[0,par],f[1,par])
    
    if s + 1 < smax:
        if f[0,par] <= f[1,par]:
            nboxes = nboxes + 1
            ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+1,1,f[0,par])
            record = updtrec(nboxes,level[nboxes],f[0,:],record)
            if s + 2 < smax:
                nboxes = nboxes + 1
                ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+2,2,f[1,par])
                record = updtrec(nboxes,level[nboxes],f[0,:],record)
            else:
                x[i] = z[1]
                nbasket = nbasket + 1
                if(len(xmin) == nbasket):
                    xmin.append(copy.deepcopy(x)) #xmin[:,nbasket] = x
                    fmi.append(f[1,par])#fmi[nbasket] = f[1,par]
                else:
                    xmin[nbasket] = copy.deepcopy(x)
                    fmi[nbasket] = f[1,par]
            #end if s+2 < smax
        else:
            if s + 2 < smax:
                nboxes = nboxes + 1
                ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+2,1,f[0,par])
                record = updtrec(nboxes,level[nboxes],f[0,:],record)
            else:
                x[i] = z[0]
                nbasket = nbasket + 1
                if(len(xmin) == nbasket):
                    xmin.append(copy.deepcopy(x))
                    fmi.append(f[0,par])
                else:
                    xmin[nbasket] = copy.deepcopy(x)
                    fmi[nbasket] = f[0,par]
            # end s+2
            nboxes = nboxes + 1
            ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+1,2,f[1,par])
            record = updtrec(nboxes,level[nboxes],f[0,:],record)
        # end if f[0,par] <= f[1,par] else 
        
        #if the third box is larger than the smaller of the other two boxes,
        # it gets level s + 1 otherwise it gets level s + 2
        if z[1] != y[i]:
            if abs(z[1]-y[i]) > abs(z[1]-z[0])*(3-np.sqrt(5))*0.5:
                nboxes = nboxes + 1
                ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+1,3,f[1,par])
                record = updtrec(nboxes,level[nboxes],f[0,:],record)
            else:
                if s + 2 < smax:
                    nboxes = nboxes + 1
                    ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+2,3,f[1,par])
                    record = updtrec(nboxes,level[nboxes],f[0,:],record)
                else:
                    x[i] = z[1]
                    nbasket = nbasket + 1
                    if(len(xmin) == nbasket):
                        xmin.append(copy.deepcopy(x)) # xmin[:,nbasket] = x
                        fmi.append(copy.deepcopy(f[1,par])) # fmi[nbasket] = f[1,par]
                    else:
                        xmin[nbasket] = copy.deepcopy(x)
                        fmi[nbasket] = f[1,par]
            #end abs
        #end z1 ! = 
    else:
        #print(i,x,z)
        xi1 =  copy.deepcopy(x)
        xi2 =  copy.deepcopy(x)
        
        xi1[i] = z[0]
        #print(xi1)
        nbasket = nbasket + 1
        if(len(xmin) == nbasket):
            xmin.append(xi1) #xmin[:,nbasket] = x
            fmi.append(f[0,par])
        else:
            xmin[nbasket] = xi1
            fmi[nbasket] = f[0,par]
        
        xi2[i] = z[1]
        #print(xi2)
        nbasket = nbasket + 1
        if(len(xmin) == nbasket):
            xmin.append(xi2)
            fmi.append(f[1,par])
        else:
            xmin[nbasket] = xi2
            fmi[nbasket] = f[1,par]
    # end if s+1 < smax
    #print('operating on min 1')
    #print(f[0,par], f[1,par], fmi, xmin)
    #print('operating on min 1')
    return xbest,fbest,xmin,fmi,ipar,level,ichild,f,flag,ncall, record,nboxes,nbasket,nsweepbest,nsweep

#------------------------------------------------------------------------------
def split1(x1,x2,f1,f2):
    if f1 <= f2:
      return x1 + 0.5*(-1 + math.sqrt(5))*(x2 - x1)
    else:
      return x1 + 0.5*(3 - math.sqrt(5))*(x2 - x1)

#------------------------------------------------------------------------------
def split2(x,y):
    '''
    % determines a value x1 for splitting the interval [min(x,y),max(x,y)]
    % is modeled on the function subint with safeguards for infinite y
    '''
    x2 = y
    if x == 0 and abs(y) > 1000:
        x2 = sign(y)
    elif x != 0 and abs(y) > 100*abs(x):
        x2 = 10*sign(y)*abs(x)
    x1 = x + 2*(x2 - x)/3
    return x1 

