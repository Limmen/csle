# lslocal#		
# refine nloc best local minimizers
#

import numpy as np
from functions.functions import feval
from gls.lsguard import lsguard
from gls.lssort import lssort


# find all strict local minima
def lslocal(func,nloc,small,sinit,short,x,p,alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,saturated):
    #fmin = min(flist) # unsued
    up = [i<j for i, j in zip(flist[0:s-1], flist[1:s])]
    down = [i<=j for i, j in zip(flist[1:s], flist[0:s-1])]
    down[s-2] = (flist[s-1] < flist[s-2])
    minima = [i and j for i,j in zip(up + [True], [True] + down)]
    imin = [i for i in range(len(minima)) if minima[i]]
    #print(up,down,minima,imin)
    
    # consider nloc best local minima only
    ff = [flist[i] for i in imin]
    perm = np.argsort(ff)
    ff.sort()
    
    imin = [imin[i] for i in perm] 
    nind = min(nloc,len(imin))
    imin = imin[nind-1::-1]# best point last for final improvement
    #if prt>3: 
    #  disp([alist#flist])#
    #  disp([num2str(nloc),' best local minimizers at [a#f]:'])#
    #  disp([imin#alist(imin)#flist(imin)])#
    #elif prt>2,
    #  disp([num2str(nloc),' best local minimizers at [a#f]:'])#
    #  disp([alist(imin)#flist(imin)])#
    ##
    
    nadd = 0#			# number of added points
    nsat = 0#			# number of saturated points
    
    for i in imin:
        # select nearest five points for local formula
        if i<=1:
            ind = [j for j in range(5)]
            ii = i#
        elif i >= s-2:
            ind = [j for j in range(s-5,s)]
            ii = i - (s-1) + 4
        else:
            ind = [j for j in range(i-2,i+3)]
            ii = 2
        # in natural order
        aa = [alist[i] for i in ind]
        # the local minimum is at ff(ii)
        ff = [flist[i] for i in ind]
        
        # get divided differences 
        f12=(ff[1]-ff[0])/(aa[1]-aa[0])
        f23=(ff[2]-ff[1])/(aa[2]-aa[1])
        f34=(ff[3]-ff[2])/(aa[3]-aa[2])
        f45=(ff[4]-ff[3])/(aa[4]-aa[3])
        f123=(f23-f12)/(aa[2]-aa[0])
        f234=(f34-f23)/(aa[3]-aa[1])
        f345=(f45-f34)/(aa[4]-aa[2])
        #print(f12,f23,f34,f45,f123,f234,f345)
        
        # decide on action
        # cas=-1: 	no local refinement at boundary
        # cas=0: 	use parabolic minimizer
        # cas=1: 	use higher order predictor in i-2:i+1
        # cas=5: 	use higher order predictor in i-1:i+2
        # select formula on convex interval
        if ii==0:		# boundary minimum
            # parabolic minimizer or extrapolation step
            cas = 0#
            if f123>0 and f123<np.Inf:
                alp = 0.5*(aa[1]+aa[2]-f23/f123)
                if alp < amin:
                    cas = -1
            else:
                alp = -np.Inf
                if alist[0]==amin and flist[1]<flist[2]:
                    cas=-1
            alp = lsguard(alp,alist,amax,amin,small)#
        elif ii==4:		# boundary minimum
            # parabolic minimizer or extrapolation step
            cas=0#
            if f345>0 and f345<np.Inf:
                alp=0.5*(aa[2]+aa[3]-f34/f345)#
                if alp>amax:
                    cas=-1##
            else: 
                alp = np.Inf#
                if alist[s-1] == amax and flist[s-2] < flist[s-3]:
                    cas=-1
            alp=lsguard(alp,alist,amax,amin,small)
        elif not (f234>0 and f234 < np.Inf):
            # parabolic minimizer
            cas=0#
            if ii<2:
                alp=0.5*(aa[1]+aa[2]-f23/f123)#
            else:
                alp=0.5*(aa[2]+aa[3]-f34/f345)
                
        elif not (f123>0 and f123 < np.Inf):
            if f345>0 and f345<np.Inf:
                cas=5#		# use 2345
            else:
                # parabolic minimizer
                cas=0#
                alp=0.5*(aa[2]+aa[3]-f34/f234)# 
        elif f345>0 and f345<np.Inf and ff[1]>ff[3]:
            cas=5#		# use 2345
        else:
            cas=1#		# use 1234
        #end ii
        
        
        if cas==0:
            # parabolic minimizer might extrapolate at the boundary
            alp = max(amin,min(alp,amax))
        elif cas==1:
            # higher order minimizer using 1234
            if ff[1]<ff[2]: 
                # compute f1x4=f134
                f13=(ff[2]-ff[0])/(aa[2]-aa[0])
                f1x4=(f34-f13)/(aa[3]-aa[0])
            else:
                # compute f1x4=f124
                f24=(ff[3]-ff[1])/(aa[3]-aa[1])#
                f1x4=(f24-f12)/(aa[3]-aa[0])#
            #end if ff[1]<ff[2]
            alp=0.5*(aa[1]+aa[2]-f23/(f123+f234-f1x4))#
            if alp<=min(aa) or alp>= max(aa):
                cas=0#
                alp=0.5*(aa[1]+aa[2]-f23/max(f123,f234))#
                #if prt>1, disp('predictor outside interval')#
        elif cas==5: 	
            # higher order minimizer using 2345
            if ff[2]<ff[3]:
                # compute f2x5=f245
                f24=(ff[3]-ff[1])/(aa[3]-aa[1])
                f2x5=(f45-f24)/(aa[4]-aa[1])
            else:
                # compute f2x5=f235
                f35=(ff[4]-ff[2])/(aa[4]-aa[2])#
                f2x5=(f35-f23)/(aa[4]-aa[1])#
            #end if ff[2]<ff[3]
            alp=0.5*(aa[2]+aa[3]-f34/(f234+f345-f2x5))#
            if alp<=min(aa) or alp>= max(aa):
                cas=0#
                alp=0.5*(aa[2]+aa[3]-f34/max(f234,f345))#  
            #end
        #end if cas
     
        # tolerance for accepting new step
        if cas<0 or flist[i]>fmed:
            alptol=0#
        elif cas>=0:
            if i==0: # minimum boundry
                alptol = small*(alist[2]-alist[0])
            elif i==s-1:# maximim boundry
                alptol = small*(alist[s-1]-alist[s-3]) # s is the length to index
            else:# somwhere in between
                alptol=small*(alist[i+1]-alist[i-1]) # i is index
        close = (min([abs(i-alp) for i in alist]) <= alptol )
    
        if cas<0 or close:
            nsat = nsat+1
        #        if prt>2, 
        #            if cas<0, disp('no local refinement at boundary')#
        #        elif alptol>0:
        #            disp('predicted point close to known point')#
        #        else:
        #            disp('predicted point matches known point')#
    
        saturated = (nsat==nind)
        # check if saturated and best point changes
        final = saturated and not max([i==alp for i in alist])
        if cas>=0 and ( final or not close ):
            #if prt>1, disp(['add local point at alp=',num2str(alp)])##
            # add point to the list
            nadd=nadd+1#
            # new function value
            falp = feval(func,x+alp*p)#
            alist.append(alp)
            flist.append(falp)
            # no sort since this would destroy old index set!!!
            #if prt>1, abest_anew_xnew=[alist(i),alp,(x+alp*p)']##
        #end if
    #end for
    if nadd:
        alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
    #    if prt>1,
    #        if saturated, disp(['saturated at s = ',num2str(s)])#
    #        else disp(['not saturated at s = ',num2str(s)])#
    return alist,flist,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,saturated

