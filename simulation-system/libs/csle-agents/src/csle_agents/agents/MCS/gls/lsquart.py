# lsquart# 	
# quartic interpolation step
# 	unfortunately, this may be unstable for huge extrapolation
#	(interpolant loses inflection points)
# 	maybe expansion around boundary points work better
#
import numpy as np
from functions.functions import feval
from gls.lslocal import lslocal
from gls.lsguard import lsguard
from gls.quartic import quartic
from gls.lssort import lssort


# find quartic interpolant
def lsquart(func,nloc,small,sinit,short,x,p,alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,saturated): 
    '''
    ''' 
    if alist[0] == alist[1]:
        f12 = 0
    else:
        f12=(flist[1]-flist[0])/(alist[1]-alist[0])
    
    if alist[1] == alist[2]:
        f23 = 0
    else:
        f23=(flist[2]-flist[1])/(alist[2]-alist[1])# 
    
    if alist[2]==alist[3]:
        f34 = 0
    else:
        f34=(flist[3]-flist[2])/(alist[3]-alist[2])
    
    if alist[3]==alist[4]:
        f45 = 0
    else:
        f45 = (flist[4]-flist[3])/(alist[4]-alist[3])
    #print(f12,f23,f34,f45)
    
    f123=(f23-f12)/(alist[2]-alist[0])
    f234=(f34-f23)/(alist[3]-alist[1])
    f345=(f45-f34)/(alist[4]-alist[2])
    f1234=(f234-f123)/(alist[3]-alist[0])
    f2345=(f345-f234)/(alist[4]-alist[1])
    f12345=(f2345-f1234)/(alist[4]-alist[0])
    #print(f123,f234,f345,f1234,f2345,f12345)
    
    good = np.Inf
    if f12345 <= 0: 
        # quartic not bounded below
        #print('local step (quartic not bounded below)')
        good = 0
        alist,flist,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,saturated = lslocal(func,nloc,small,sinit,short,x,p,alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,saturated)
        quart = 0
    else:
        #print('quartic step')
        quart = 1
    
    if quart:
        # expand around alist[2]
        c = np.zeros(len(alist))
        c[0]=f12345
        c[1]=f1234+c[0]*(alist[2]-alist[0])
        c[2]=f234+c[1]*(alist[2]-alist[3])
        c[1]=c[1]+c[0]*(alist[2]-alist[3])
        c[3]=f23+c[2]*(alist[2]-alist[1])
        c[2]=c[2]+c[1]*(alist[2]-alist[1])
        c[1]=c[1]+c[0]*(alist[2]-alist[1])
        c[4]=flist[2]
        #print(c)
        #if prt>3:
        #  test_quartic_fit=[flist#quartic(c,alist-alist[2])]

        # find critical points of quartic as zeros of gradient
        cmax = max(c)
        c = np.divide(c,cmax)
        hk = 4*c[0]#
        compmat = [[0,0,-c[3]], [hk, 0, -2*c[2]], [0,hk,-3*c[1]]]
        ev = np.divide(np.linalg.eig(compmat)[0],hk)
        i = np.where(ev.imag ==0)
        #print(c,hk,compmat,ev,i)
    
        if i[0].shape[0] == 1:
            # only one minimizer
            #if prt>1, disp('quartic has only one minimizer')# #
            alp = alist[2] + ev[i[0][0]]#
            #if prt>3:
            # f=quartic(c,ev(i))#
            #  plot(alp,f,'ro')#
        else:
            # two minimizers
            ev = np.sort(ev)#
            #print('quartic has two minimizers')# 
            alp1 = lsguard(alist[2]+ev[0],alist,amax,amin,small)
            alp2 = lsguard(alist[2]+ev[2],alist,amax,amin,small)
            f1 = cmax*quartic(c,alp1-alist[2])
            f2 = cmax*quartic(c,alp2-alist[2])
            #print(ev,alp1,alp2,f1,f2)
            #    if prt>3,
            #      alp3=alist[2]+ev[1]#
            #      f3=cmax*quartic(c,ev[1])#
            #      plot(alp1,f1,'ro')#
            #      plot(alp2,f2,'ro')#
            #      plot(alp3,f3,'ro')#

            # pick extrapolating minimizer if possible 
            if alp2>alist[4] and f2<max(flist):
                alp=alp2
            elif alp1<alist[0] and f1<max(flist):
                alp=alp1
            elif f2<=f1:
                alp=alp2
            else:
                alp=alp1
    
        if max([i == alp for i in alist]):
              # predicted point already known
              #if prt, disp('quartic predictor already known')# #
              quart = 0#
    
        if quart:
            alp = lsguard(alp,alist,amax,amin,small)
            #print('new function value')
            falp = feval(func,x+alp*p)#
            alist.append(alp)
            flist.append(falp)
            alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
    
    return alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,good,saturated


