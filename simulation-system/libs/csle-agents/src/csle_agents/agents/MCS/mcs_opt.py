# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 11:56:32 2019

@author: yl918888
"""

from optimization.parameter.mh.mh_cost_function import costFunction
from optimization.structure.misc import sort_by_values
from optimization.parameter.mcs.jones.functions import feval
from optimization.parameter.mcs.mcs import mcs

import numpy as np

class TheMCS():   
    mEvaluateTree = None # Tree evaluation paramters
    mParams = None #  set of paramters
    mTree = None #  set of paramters
    mParameterToFetch = 'weights_and_bias'
    performance_record = None

    
    def __init__(self, pEvaluateTree, pParams, pTree):
        self.mEvaluateTree = pEvaluateTree
        self.mParams = pParams
        self.mTree = pTree
        self.performance_record = []
        if(pParams.n_fun_type == 'Gaussian'):
            self.mParameterToFetch = 'all'
        else:
            self.mParameterToFetch = 'weights_and_bias'
        
    #------------------------------------------------------------------------------------------    
    def optimize(self):
        '''
            Run The Multi Coordinate Search algorithm
            
        '''
        print('The MCS algorithm:', self.mParams.n_algo_param)
        self.mEvaluateTree.set_dataset_to_evaluate('train')       
        
        xCurrent = self.mTree.getTreeParameters(self.mParams.n_max_target_attr, self.mParameterToFetch)
        fcn  = {'tree_obj': self.mTree,
                'evaluate_obj': self.mEvaluateTree,
                'max_target_obj': self.mParams.n_max_target_attr,
                'paramters_obj': self.mParameterToFetch,
                'error_only_obj': True}
        
        #print('current x:', xCurrent) # too long for large objectives
        print('Best tree parameter length', len(xCurrent) ,' to start : ', feval(fcn, xCurrent), self.fobj(xCurrent))
        self.performance_record.append(self.fobj(xCurrent, False))
        
        #setting the mcs parameters
        min_x = self.mParams.n_weight_range[0] + 0.1
        max_x = self.mParams.n_weight_range[1]
        n = len(xCurrent) # problem dimension
        u = [min_x for indx in range(n)]
        v = [max_x for indx in range(n)]
        
        smax = 5*n+10 # number of levels used
        nf = 50*pow(n,2) #limit on number of f-calls
        stop = [3*n]  # m, integer defining stopping test
        stop.append(float("-inf"))  # freach, function value to reach

        iinit = 1 # 0: simple initialization list
        local = 100 	# local = 0: no local search
        eps = 2.220446049250313e-16
        gamma = eps		         # acceptable relative accuracy for local search
        hess = np.ones((n,n)) 	     # sparsity pattern of Hessian

        #call mcs algorithm
        xbest,fbest,xmin,fmi,ncall,ncloc,flag = mcs(fcn,u,v,smax,nf,stop,iinit,local,gamma,hess)

        print('The MCS Algorithms Results:')
        print('fglob',0.0)
        print('fbest',fbest)
        print('xglob','unknown')
        print('xbest',xbest)
        
        self.mTree.setTreeParameters(xbest, self.mParams.n_max_target_attr, self.mParameterToFetch)
        return self.mTree, self.performance_record 
    
    def fobj(self,pVector, only_error = True):
        return costFunction(pVector, self.mTree, self.mEvaluateTree, self.mParams.n_max_target_attr, self.mParameterToFetch, only_error)

        

        