# -*- coding: utf-8 -*-
"""
Global optimization by multilevel coordinate search (MCS)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%                                                             %%%%%%
%%%%%  Developed by Waltraud Huyer and Arnold Neumaier            %%%%%%
%%%%%  Dept. of Mathematics, University of Vienna, Austria        %%%%%%
%%%%%                                                             %%%%%%
%%%%%  Main Source:                                               %%%%%%
%%%%%  http://solon.cma.univie.ac.at/~neum/software/mcs/          %%%%%%
%%%%%                                                             %%%%%%
%%%%%   Translated in Pyton by Varun Ojha                         %%%%%%
%%%%%                                                             %%%%%%
%%%%%                                                             %%%%%%
%%%%%                                                             %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

MCS is a Matlab (tralsation in python) program for bound constrained global optimization 
using function values only, based on a multilevel coordinate search
that balances global and local search. The local search is done via
sequential quadratic programming.

MCS attempts to find the global minimizer of the bound constrained 
optimization problem

 min  f(data,x)
 s.t. x in [u,v] (a box in R^n)

where data is a fixed data vector (or other data structure), 
and f is a function of data and x defined by a user-provided m-File,

The search is not exhaustive; so the global minimum may be missed.
However, a comparison to other global optimization algorithms shows
excellent performance in many cases, especially in low dimensions.

A derivation of the algorithm, the underlying theory, and numerical 
comparisons can be found in the paper

   W. Huyer and A. Neumaier,
   Global optimization by multilevel coordinate search,
   J. Global Optimization 14 (1999), 331-355.

This paper and the required m-files can be downloaded from
http://solon.cma.univie.ac.at/~neum/software/mcs

To run the programs you also need the Matlab programs
MINQ (bound constrained quadratic program solver)
and 
GLS (global line search)
available from
http://solon.cma.univie.ac.at/~neum/software/minq/
http://solon.cma.univie.ac.at/~neum/software/ls/


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
The use of MCS is best seen by looking at runmcs.m,
a sample driver for MCS for the test set of Jones et al.

Due to rounding errors, it is possible that functions are 
evaluated sligtly outside the given range; should this cause 
problems to your function evaluator, simply project the point 
in your evaluation routine to the desired range before 
evaluation. This will remedy the problem without affecting 
the quality of the solution.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


mcs.py		main program



@translator: Varun Ojha


"""

#%%----------------------------------------------------------------------------
import numpy as np
from functions.defaults import defaults
from functions.functions import feval

from mcs import mcs

#%%----------------------------------------------------------------------------
fcn = 'myfun' # gpr, bra, cam, hm3, s10, sh5, sh7, hm6, 'myfun' 

u,v,nglob,fglob,xglob = defaults(fcn)
#feval(fcn, [2,5])
# function paramters
n = len(u);		         # problem dimension
prt = 1 # print level
smax = 5*n+10 # number of levels used
nf = 50*pow(n,2) #limit on number of f-calls
stop = [3*n]  # m, integer defining stopping test
stop.append(float("-inf"))  # freach, function value to reach

m = 1
if m == 0:
    stop[0] = 1e-4	 # run until this relative error is achieved
    stop[1] = fglob	 # known global optimum value
    stop.append(1e-10) # stopping tolerance for tiny fglob

iinit = 0 # 0: simple initialization list
local = 50 	# local = 0: no local search
eps = 2.220446049250313e-16
gamma = eps		         # acceptable relative accuracy for local search
hess = np.ones((n,n)) 	     # sparsity pattern of Hessian

#%%call mcs algorithm
xbest,fbest,xmin,fmi,ncall,ncloc,flag = mcs(fcn,u,v,smax,nf,stop,iinit,local,gamma,hess)

print('The MCS Algorithms Results:')
print('fglob',fglob)
print('fbest',fbest)
print('xglob',xglob)
print('xbest',xbest)
print('\n')
