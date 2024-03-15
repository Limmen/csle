# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 09:21:08 2019

@author: yl918888
"""
#inbild libraries
#import matplotlib.pyplot as plt
# packages from gls
import numpy as np
from gls.lsrange import lsrange
from gls.lsinit import lsinit
from gls.lssort import lssort
from gls.lspar import lspar
from gls.lsnew import lsnew
from gls.lsquart import lsquart  
from gls.lsdescent import lsdescent
from gls.lsconvex import lsconvex
from gls.lssat import lssat 
from gls.lssep import lssep
from gls.lslocal import lslocal
#%%
def gls(func,xl,xu,x,p,alist,flist,nloc,small,smax,prt=2):
    '''
    Global line search main function
    arg:
        func -  funciton name which is subjected to optimization
        xl -  lower bound
        xu -  upper bound
        x -  starting point
        p -  search direction [1 or -1 ? need to check]
        alist -  list of known steps
        flist -  funciton values of known steps
        nloc -  best local optimizal
        small - tollarance values
        smax -  search list size
        prt =  print - unsued in this implementation so far
    '''
    #%%    
    if np.isscalar(alist):
        alist = [alist]
        flist = [flist]
        #print('alist in gls:',alist)
        #print('flist in gls:',flist)
        
            
    if type(alist) != list:
        alist = alist.tolist()
    if type(flist) != list:
        flist = flist.tolist()
        
    # golden section fraction is (3-sqrt(5))/2= 0.38196601125011
    short=0.381966 #fraction for splitting intervals
    
    # save information for nf computation and extrapolation decision
    sinit = len(alist)  #initial list size
    
    # get 5 starting points (needed for lslocal)
    bend = 0
    xl,xu,x,p,amin,amax,scale = lsrange(func,xl,xu,x,p,prt,bend)	# find range of useful alp 
    #plt.plot(aa,ff)
    alist,flist,alp,alp1,alp2,falp = lsinit(func,x,p,alist,flist,amin,amax,scale) # 2 points needed for lspar and lsnew
    alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
    nf = s - sinit	# number of function values used
    
       
    #print(alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s)
    while s < min(5,smax):
        if nloc == 1:
            #print('interpol')
            # parabolic interpolation step
            alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,alp,fac = lspar(func,nloc,small,sinit,short,x,p,alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s) 
            # when s==3 we haven't done a true parabolic step 
            # and may appear monotonic without being so!
            if s > 3 and monotone and (abest==amin or abest==amax):
                #print('return since monotone')  # 
                nf = s - sinit 		# number of function values used
                #lsdraw  
                return alist,flist,nf
        else:
            #print('explore')
            # extrapolation or split
            alist,flist,alp,fac = lsnew(func,nloc,small,sinit,short,x,p,s,alist,flist,amin,amax,alp,abest,fmed,unitlen) 
            alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
        #print('while \n:')
        #print(alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s) 
    # end while
    #%%
    saturated=0	#is reset in lsquart
    # shape detection phase
    if nmin == 1:
        if monotone and (abest==amin or abest==amax):
            #if prt>1,disp('return since monotone'); end;
            nf = s-sinit # number of function values used
            #lsdraw; 
            #print('return since monotone')
            return alist,flist,nf
        if s == 5:
            # try quartic interpolation step
            alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,good,saturated = lsquart(func,nloc,small,sinit,short,x,p,alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,saturated) 
         # check descent condition 		
        alist,flist,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lsdescent(func,x,p,alist,flist,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s)
        # check convexity	
        convex = lsconvex(alist,flist,nmin,s)
        if convex:
            #print('return since convex')
            nf = s-sinit # number of function values used
            #lsdraw; 
            return alist,flist,nf
    sold = 0
    # refinement phase
    while 1:
        #lsdraw
        #print('***** new refinement iteration *****')
        # check descent condition 		
        alist,flist,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lsdescent(func,x,p,alist,flist,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s)
        # check saturation
        alp,saturated = lssat(small,alist,flist,alp,amin,amax,s,saturated) 
        if saturated or s == sold or s >= smax:
            if saturated:
                no_print = 0
                #print('return since saturated')
            if s==sold:
                no_print = 0
                #print('return since s==sold')
            if s>=smax:
                no_print = 0
                #print('return since s>=smax')
            break
        sold = s
        nminold = nmin #if prt>1,nmin,end;
        if not saturated and nloc > 1:
            # separate close minimizers
            alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssep(func,nloc,small,sinit,short,x,p,alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s)
        # local interpolation step
        alist,flist,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,saturated = lslocal(func,nloc,small,sinit,short,x,p,alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,saturated)
        if nmin>nminold:
            saturated=0
    #end while
    #get output information
    nf = s-sinit # number of function values used
    #print(nf)
    return alist,flist,nf #  search list,function values,number of fucntion evaluation