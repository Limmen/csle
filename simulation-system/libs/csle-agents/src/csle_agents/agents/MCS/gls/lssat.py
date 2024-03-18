# lssat #		
# check saturation condition
# 
import numpy as np
def lssat(small,alist,flist,alp,amin,amax,s,saturated):
    cont = saturated #
    
    if cont:
        # check boundary minimizer
        fmin =  min(flist)
        i =np.argmin(flist) #
        if i==0 or  i==s-1:
            cont = 0
    
    if cont:
        # select three points for parabolic interpolation
        aa = [alist[j] for j in range(i-1,i+1+1)]
        ff = [flist[j] for j in range(i-1,i+1+1)]
        
        # get divided differences 
        f12=(ff[1]-ff[0])/(aa[1]-aa[0]) #
        f23=(ff[2]-ff[1])/(aa[2]-aa[1]) #
        f123=(f23-f12)/(aa[2]-aa[0]) #
        
        if f123>0:
            # parabolic minimizer
            alp=0.5*(aa[1]+aa[2]-f23/f123) #
            alp = max(amin,min(alp,amax)) #
            alptol = small*(aa[2]-aa[0]) #
            saturated = (abs(alist[i]-alp)<=alptol)
        else:
            saturated = 0
        if not saturated:
            no_print = 0
            #print('saturation check negative')
    return alp, saturated