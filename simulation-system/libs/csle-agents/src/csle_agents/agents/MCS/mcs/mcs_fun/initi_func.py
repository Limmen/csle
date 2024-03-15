import numpy as np
#------------------------------------------------------------------------------        
from functions.functions import feval
from mcs_fun.sign import sign
#------------------------------------------------------------------------------
def subint(x1, x2):
    '''
    computes [min(x,y),max(x,y)] that are neither too close nor too far away from x 
    '''
    f = 1000;
    if f*abs(x1) <  1:
        if abs(x2) >  f:
            x2 = sign(x2)
    else:
        if abs(x2) >  f:
            x2 = 10*sign(x2)*abs(x1)
    x1 = x1 + (x2 -x1) / 10
    return x1, x2
            

#------------------------------------------------------------------------------    
def init(fcn,x0,l,L,n):
    '''
     computes the function values corresponding to the initialization list
     and the pointer istar to the final best point x^* of the init. list
    '''
    ncall = 0 #  set number of function call to 0    
    
    # fetch intial point x0  
    x = np.zeros(n)
    for i in range(n):
        #  feteching int the mid point; 
        x[i] = x0[i,l[i]]# value at l[i] is the indeces of mid point
    # x0 (inital point)
    #x = x.astype(int)
    
    f1 = feval(fcn,x)
    ncall = ncall + 1 # increasing the number of function call by 1
    
    f0 = np.zeros((L[0]+1,n))
    f0[l[0],0] = f1 # computing f(x) at intial point x0
    
    # searching for x*  =  x0 (inital point)
    # i* the pointer in the list indicating the potision (indecies ) of x*
    istar = np.zeros(n).astype(int) 
    
    # for all cordinate k (in this case i) in dim n
    #for k = 1 to n (in this case 0 to n-1)
    for i in range(n):
        istar[i] = l[i] # set i* to mid point
        for j in range(L[i]+1):# 1 added to make index value also work as an array length
            if j == l[i]:
                if i != 0:
                    f0[j,i] = f0[istar[i-1], i-1]
            else:
                x[i] = x0[i,j]
                f0[j,i] = feval(fcn,x)
                ncall = ncall + 1 # increasing the number of cfunction call by 1 each time
                #print(i+1,j+1,x,f0[j,i])
                if f0[j,i] < f1:
                    f1 = f0[j,i]
                    istar[i] = j
        # end search in list 
        # update x*
        x[i] = x0[i,istar[i]]
    #end for k = 1:n  
    return f0,istar,ncall



#------------------------------------------------------------------------------
from mcs_fun.genbox import genbox
from mcs_fun.polint import polint
from mcs_fun.quadratic_func import quadmin
from mcs_fun.quadratic_func import quadpol
#------------------------------------------------------------------------------
def initbox(x0,f0,l,L,istar,u,v,isplit,level,ipar,ichild,f,nboxes,prt):
    '''
        generates the boxes in the initialization procedure
    
    '''
    n = len(u)
    # intilize the ith histopy with the folowing:
    # parent  box index, 
    # level of parent box, 
    # split index of the parent box, 
    # number of child
    # 
    
    # parent of the ith box 
    # it is the index into the number of boxex 
    ipar[0]= -1 #  parent box is index -1 for the root box
    # history level o the parent box: initilize to 1 as the 0 < level s < smax of root box is 1
    # indicate box 0 with level value s = 1
    level[0] = 1
    # ichild indicate the child of box 0 
    ichild[0] = 1
    # optimi value of the box is x0
    f[0,0] = f0[l[0],0]
    # intilize partent box  = 0
    par = 0 # index of the parent box (biously 0 in this case as box index start with z)
    
    
    var = np.zeros(n)
    for i in range(n):
        #print('parent box',par)
        # boxes split in the init. procedure get a negative splitting index of the ith coordinate (dimension)
        isplit[par] = -i-1 # set a negative index value
        nchild = 0
        # check if x left endpoint is > lower bound (left endpoint)
        # if so - genetrate a box
        if x0[i,0] >  u[i]:
            nboxes = nboxes + 1 # one extra box is generated for the parent box
            nchild = nchild + 1 # therefore incerase number of child by 1 of the parent box
            # set parent of this ith box split in the ithe direction (dimension)
            ipar[nboxes], level[nboxes], ichild[nboxes], f[0,nboxes] = genbox(par, level[par]+1,-nchild, f0[0, i])
        # end if
        
        if L[i] == 2:
            v1 = v[i]
        else:
            v1 = x0[i,2]
        # end if
        
        # pollynomial interpolation to get three points for
        d = polint(x0[i,0:3],f0[0:3,i])
        xl = quadmin(u[i],v1,d,x0[i,0:3])
        fl = quadpol(xl,d,x0[i,0:3])
        xu = quadmin(u[i],v1,-d,x0[i,0:3])
        fu = quadpol(xu,d,x0[i,0:3])
        
        if istar[i] == 0:
            if xl < x0[i,0]:
                par1 = nboxes  # label of the current box for the next coordinate 
            else:
                par1 = nboxes + 1
        #end istart
    
        for j in range(L[i]):
            nboxes = nboxes + 1
            nchild = nchild + 1
            if f0[j,i] <= f0[j+1,i]:
                s = 1
            else:
                s = 2
            ipar[nboxes], level[nboxes], ichild[nboxes], f[0,nboxes] = genbox(par,level[par]+s,-nchild,f0[j,i])
            #if prt: splval = split1(x0[i,j],x0[i,j+1],f0[j,i],f0[j+1,i])
            
            if j >= 1:
                if istar[i] == j:
                    if xl <= x0[i,j]:
                        par1 = nboxes - 1  # label of the current box for the next coordinate 
                    else:
                        par1 = nboxes
                #end istar
                if j <= L[i] - 2:
                    d = polint(x0[i,j:j+1],f0[j:j+1,i])
                    if j < L[i] - 2:
                        u1 = x0[i,j+1]
                    else:
                        u1 = v[i] 
                    # end if
                    xl = quadmin(x0[i,j],u1,d,x0[i,j:j+1])
                    fl = min(quadpol(xl,d,x0[i,j:j+1]),fl)
                    xu = quadmin(x0[i,j],u1,-d,x0[i,j:j+1])
                    fu = max(quadpol(xu,d,x0[i,j:j+1]),fu)
                #end j < Li -2
            # end if j > = 1
            nboxes = nboxes + 1
            nchild = nchild + 1
            ipar[nboxes], level[nboxes], ichild[nboxes], f[0,nboxes] = genbox(par,level[par]+3-s,-nchild,f0[j+1,i])
        #end for j
        if x0[i,L[i]] < v[i]:
            nboxes = nboxes + 1
            nchild = nchild + 1            
            ipar[nboxes], level[nboxes], ichild[nboxes], f[0,nboxes] = genbox(par,level[par]+1,-nchild,f0[L[i],i])
            
        if istar[i] == L[i]:
            if x0[i,L[i]] < v[i]:
                if xl <= x0[i,L[i]]:
                    par1 = nboxes - 1  # label of the current box for the next coordinate 
                else:
                    par1 = nboxes
                #end if xl < x0
            else:
                par1 = nboxes
            #end if x0 < v
        #end if istart
        var[i] = fu - fl
        
        # the quadratic model is taken as a crude measure of the variability in the ith component
        level[par] = 0  # box is marked as split
        par = par1
    #end for
    fbest = f0[istar[n-1],n-1] #best function value after the init. procedure
    p = np.zeros(n).astype(int)
    xbest = np.zeros(n)
    #print(nboxes)
    for i in range(n):
        #var0 = max(var) 
        p[i] = np.argmax(var)
        var[p[i]] = -1
        xbest[i] = x0[i,istar[i]]  # best point after the init. procedured
     
    return  ipar,level,ichild,f,isplit,p,xbest,fbest,nboxes