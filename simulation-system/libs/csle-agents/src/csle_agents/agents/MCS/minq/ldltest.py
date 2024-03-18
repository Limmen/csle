# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 10:28:05 2019

@author: yl918888
"""
%reset -f
%clear
#%%
## important test 
#import numpy as np
#n=5
## generate random unit lower triangular matrix
#L = tril(rand(n))
#L = L-diag(diag(L))+eye(n)
## random column
#d = np.random.rand(n)

#
import numpy as np
from optimization.parameter.mcs.minq.ldldown import ldldown
from optimization.parameter.mcs.minq.ldlup import ldlup

for i in range(100):
    n=10
    #L = np.asarray([[1,0,0,0,0],
    #                [0.879653724481905,1,0,0,0],
    #                [0.817760559370642,0.312718886820616,1,0,0],
    #                [0.260727999055465,0.161484744311750,0.470924256358334,1,0],
    #                [0.594356250664331,0.178766186752368,0.695949313301608,0.319599735180496,1]])
    
    L = np.tril(np.random.rand(n))
    L = L - np.diag(np.diag(L)) + np.eye(n)
    
    #d = np.asarray([0.968649330231094,
    #                0.531333906565675,
    #                0.325145681820560,
    #                0.105629203329022,
    #                0.610958658746201])
    d = np.random.rand(n)
    
    #g = np.asarray([0.778802241824093,
    #                0.423452918962738,
    #                0.0908232857874395,
    #                0.266471490779072,
    #                0.153656717591307])
     
    
    for j in range(n):
        #j = 2
        print(j)
        print('***** downdate *****')
        L,d = ldldown(L,d,j)
        print('***** update *****')
        g = np.random.rand(n)
        g[j] = 1 # encourage definiteness of update
        L,d,p = ldlup(L,d,j,g)
        #print(L)
        #print(d)
        #print(p)
