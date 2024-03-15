# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 09:02:55 2019

The Global line search algorithm by : https://www.mat.univie.ac.at/~neum/software/ls/
Arnold Neumaier
@author: yl918888
"""

%reset -f
%clear
#%%
import numpy as np
from optimization.parameter.mcs.gls.gls import gls

prt=2#		# print level
xx=[-9,2]#	# interval for searching minimum

func='glstest'
xl=xx[0]
xu=xx[1]#
x=(xl+xu)/2#

p=1#

alist = []
flist = []
nloc=3
small=0.1
smax=10

#%%
alist,flist,nf = gls(func,xl,xu,x,p,alist,flist,nloc,small,smax,prt)
alist,flist,nf



