import copy
import sys

import numpy as np
from mcs_fun.basket_func import basket, basket1

# %
# MCS algorithm supporting functions =  first layer
from mcs_fun.chk_bound import check_box_bound
from mcs_fun.chk_flag import chrelerr, chvtr
from mcs_fun.chk_locks import addloc, chkloc, fbestloc
from mcs_fun.exgain import exgain
# from mcs_fun.initi_func import init, initbox, subint
from mcs_fun.lsearch import lsearch
from mcs_fun.split_func import splinit, split
from mcs_fun.splrnk import splrnk
from mcs_fun.strtsw import strtsw
from mcs_fun.updtrec import updtrec
from mcs_fun.vertex_func import vertex

from typing import Union, List, Optional, Any, Dict, Tuple
import math
import time
import random
import gymnasium as gym
import os
import numpy as np
import numpy.typing as npt
import gym_csle_stopping_game.constants.constants as env_constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.linear_threshold_stopping_policy import LinearThresholdStoppingPolicy
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.util.general_util import GeneralUtil
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.training.policy_type import PolicyType
from csle_agents.agents.base.base_agent import BaseAgent
from csle_agents.common.objective_type import ObjectiveType
import csle_agents.constants.constants as agents_constants
#%%----------------------------------------------------------------------------
import numpy as np
from functions.defaults import defaults
from functions.functions import feval

from mcs import mcs
class MCSAgent(BaseAgent):

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig],
                 experiment_config: ExperimentConfig,
                 env: Optional[BaseEnv] = None, training_job: Optional[TrainingJobConfig] = None,
                 save_to_metastore: bool = True):
        """
        Initializes the Particle Swarm Agent

        :param simulation_env_config: the simulation env config
        :param emulation_env_config: the emulation env config
        :param experiment_config: the experiment config
        :param env: (optional) the gym environment to use for simulation
        :param training_job: (optional) a training job configuration
        :param save_to_metastore: boolean flag that can be set to avoid saving results and progress to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.MCS
        self.env = env
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore
    #%%----------------------------------------------------------------------------

    def myfun():
        """
        TODO: implemment your funciton [functions.py]')
        TODO: implemment your funciton papramter [defualts.py]')
        """
        ## For domain [-1, 1] u and v will be
        u = [-20, -20, -20]
        v = [20, 20, 20]

        nglob = 1  # number of gloabl optmial to be searhed
        fglob = 0.0  # known  gloabl optmia value
        xglob = [0, 0, 0]  # # known  gloabl optmia vector if any

        return u, v, nglob, fglob, xglob

    def myfun(x):
        # print('TODO implemment your funciton [functions.py]')

        return (x[0] - 0.2) ** 2 + (x[1] - 0.01) ** 2 + (x[2] - 2.4) ** 2



    def eval_theta(self, policy: Union[MultiThresholdStoppingPolicy, LinearThresholdStoppingPolicy],
                    max_steps: int = 200) -> Dict[str, Union[float, int]]:
        """
        Evaluates a given threshold policy by running monte-carlo simulations

        :param policy: the policy to evaluate
        :return: the average metrics of the evaluation
        """
        if self.env is None:
            raise ValueError("Need to specify an environment to run policy evaluation")
        eval_batch_size = self.experiment_config.hparams[agents_constants.COMMON.EVAL_BATCH_SIZE].value
        metrics: Dict[str, Any] = {}
        for j in range(eval_batch_size):
            done = False
            o, _ = self.env.reset()
            l = int(o[0])
            b1 = o[1]
            t = 1
            r = 0
            a = 0
            info: Dict[str, Any] = {}
            while not done and t <= max_steps:
                Logger.__call__().get_logger().debug(f"t:{t}, a: {a}, b1:{b1}, r:{r}, l:{l}, info:{info}")
                if self.experiment_config.player_type == PlayerType.ATTACKER:
                    policy.opponent_strategy = self.env.static_defender_strategy
                    a = policy.action(o=o)
                else:
                    a = policy.action(o=o)
                o, r, done, _, info = self.env.step(a)
                l = int(o[0])
                b1 = o[1]
                t += 1
            metrics = ParticleSwarmAgent.update_metrics(metrics=metrics, info=info)
        avg_metrics = ParticleSwarmAgent.compute_avg_metrics(metrics=metrics)
        return avg_metrics


    u,v,nglob,fglob,xglob = defaults(fcn)
    #feval(fcn, [2,5])
    # function paramters
    def MCS_starter(self, exp_result, seed: int, random_seeds: List[int], training_job: TrainingJobConfig):
        """
        Initiating the parameters of performing the MCS algorithm, using external functions
        """
        u =  self.experiment_config.hparams[agents_constants.MCS.U].value
        v = self.experiment_config.hparams[agents_constants.MCS.V].value
        iinit =self.experiment_config.hparams[agents_constants.MCS.IINIT].value # simple initialization list
        local = self.experiment_config.hparams[agents_constants.MCS.LOCAL].value 	# local = 0: no local search
        eps = self.experiment_config.hparams[agents_constants.MCS.EPSILON].value 
        gamma = self.experiment_config.hparams[agents_constants.MCS.GAMMA].value		         # acceptable relative accuracy for local search
        prt = self.experiment_config.hparams[agents_constants.MCS.PRT].value # print level
        m = self.experiment_config.hparams[agents_constants.MCS.M].value
        stopping_actions = self.experiment_config.hparams[agents_constants.MCS.STOPPING_ACTIONS].value
        n = len(u) #  problem dimension
        smax = 5*n+10 # number of levels used
        nf = 50*pow(n,2) #limit on number of f-calls
        stop = [3*n]  # m, integer defining stopping test
        hess = np.ones((n,n)) 	     # sparsity pattern of Hessian
        stop.append(float("-inf"))  # freach, function value to reach
        fcn = 'myfun' # gpr, bra, cam, hm3, s10, sh5, sh7, hm6, 'myfun' 

        if m == 0:
            stop[0] = 1e-4	 # run until this relative error is achieved
            stop[1] = fglob	 # known global optimum value
            stop.append(1e-10) # stopping tolerance for tiny fglob
        
        xbest,fbest,xmin,fmi,ncall,ncloc,flag = self.MCS(fcn,u,v,smax,nf,stop,iinit,local,gamma,hess, stopping_actions)

    print('The MCS Algorithms Results:')
    print('fglob',fglob)
    print('fbest',fbest)
    print('xglob',xglob)
    print('xbest',xbest)
    print('\n')

    def get_theta0(self):
        theta0 = []
        if iinit == 0:
            print
            theta0.append(u)  #  lower bound point
            theta0.append([(i + j) / 2 for i, j in zip(u, v)])  #  mid point
            theta0.append(v)  # upper bound point
            theta0 = np.array(theta0).T
        elif iinit == 1:
            theta0 = np.zeros((n, 3))
            for i in range(n):
                if u[i] >= 0:
                    theta0[i, 0] = u[i]
                    theta0[i, 1], theta0[i, 2] = subint(u[i], v[i])
                    theta0[i, 1] = 0.5 * (theta0[i, 0] + theta0[i, 2])
                elif v[i] <= 0:
                    theta0[i, 2] = v[i]
                    theta0[i, 1], theta0[i, 0] = subint(v[i], u[i])
                    theta0[i, 1] = 0.5 * (theta0[i, 0] + theta0[i, 2])
                else:
                    theta0[i, 1] = 0
                    _, theta0[i, 0], subint(0, u[i])
                    _, theta0[i, 2], subint(0, v[i])
        elif iinit == 2:
            theta0.append([(i * 5 + j) / 6 for i, j in zip(u, v)])
            theta0.append([0.5 * (i + j) for i, j in zip(u, v)])
            theta0.append([(i + j * 5) / 6 for i, j in zip(u, v)])
            theta0 = np.array(theta0).T

        # check whether there are infinities in the initialization list
        if np.any(np.isinf(theta0)):
            sys.exit("Error- MCS main: infinities in ititialization list")
        return theta0


    def get_policy(self, theta: List[float], L: int) -> Union[MultiThresholdStoppingPolicy,
                                                                LinearThresholdStoppingPolicy]:
        """
        Gets the policy of a given parameter vector

        :param theta: the parameter vector
        :param L: the number of parameters
        :return: the policy
        """
        if self.experiment_config.hparams[agents_constants.SIMULATED_ANNEALING.POLICY_TYPE].value \
                == PolicyType.MULTI_THRESHOLD.value:
            policy = MultiThresholdStoppingPolicy(
                theta=list(theta), simulation_name=self.simulation_env_config.name,
                states=self.simulation_env_config.state_space_config.states,
                player_type=self.experiment_config.player_type, L=L,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, experiment_config=self.experiment_config, avg_R=-1,
                agent_type=AgentType.SIMULATED_ANNEALING)
        else:
            policy = LinearThresholdStoppingPolicy(
                theta=list(theta), simulation_name=self.simulation_env_config.name,
                states=self.simulation_env_config.state_space_config.states,
                player_type=self.experiment_config.player_type, L=L,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, experiment_config=self.experiment_config, avg_R=-1,
                agent_type=AgentType.SIMULATED_ANNEALING)
        return policy


    def init(self, theta0, l, L, stopping_actions, n):
        '''
        computes the function values corresponding to the initialization list
        and the pointer istar to the final best point x^* of the init. list
        '''
        ncall = 0 #  set number of function call to 0    
        
        # fetch intial point theta0  
        theta = np.zeros(n)
        for i in range(n):
            #  feteching int the mid point; 
            theta[i] = theta0[i,l[i]]# value at l[i] is the indeces of mid point
        # theta0 (inital point)
        #x = x.astype(int)
        policy = self.get_policy(theta, L=stopping_actions)
        avg_metrics = self.eval_theta(policy=policy,
                                      max_steps=self.experiment_config.hparams[
                                          agents_constants.COMMON.MAX_ENV_STEPS].value)
        J1 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
        # f1 = feval(fcn,x)
        ncall = ncall + 1 # increasing the number of function call by 1
        
        J0 = np.zeros((L[0]+1,n))
        J0[l[0],0] = J1 # computing f(x) at intial point theta0
        
        # searching for x*  =  theta0 (inital point)
        # i* the pointer in the list indicating the potision (indecies ) of x*
        istar = np.zeros(n).astype(int) 

        # for all cordinate k (in this case i) in dim n
        #for k = 1 to n (in this case 0 to n-1)
        for i in range(n):
            istar[i] = l[i] # set i* to mid point
            for j in range(L[i]+1):# 1 added to make index value also work as an array length
                if j == l[i]:
                    if i != 0:
                        J0[j,i] = J0[istar[i-1], i-1]
                else:
                    theta[i] = theta0[i,j]
                    policy = self.get_policy(theta, L=stopping_actions)
                    avg_metrics = self.eval_theta(policy=policy,
                                                  max_steps=self.experiment_config.hparams[
                                                      agents_constants.COMMON.MAX_ENV_STEPS].value)
                    J0[j, i] = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                    # f0[j,i] = feval(fcn,x)
                    ncall = ncall + 1 # increasing the number of cfunction call by 1 each time
                    #print(i+1,j+1,x,f0[j,i])
                    if J0[j,i] < J1:
                        f1 = f0[j,i]
                        istar[i] = j
            # end search in list 
            # update x*
            theta[i] = theta0[i,istar[i]]
        #end for k = 1:n  
        return J0, istar, ncall

    def MCS(self, fcn, u, v, smax, nf, stop, iinit, local, gamma, hess, stopping_actions, prt=1):

        # %%
        # check box bounds
        if check_box_bound(u, v):
            sys.exit("Error MCS main: out of bound")

        n = len(u)
        # initial values for the numbers of function calls (total number/local % search)
        ncall = 0
        ncloc = 0

        # create indices
        # l indicate the mid point
        l = np.multiply(1, np.ones(n)).astype(
            int
        )  # dimension n  i.e, 0 <= i < <n; for range need to add 1 each time
        # L indicate the end point or (total number of partition of the valie x in the ith dimenstion)
        # u <= x1 <= xL <= v  in the case of L == 2 (length 3) -> theta0 = u (lower bound), x1 = mid point and x2 = v (upper bound)
        L = np.multiply(2, np.ones(n)).astype(
            int
        )  # dimension n  i.e, 0 <= i < <n; for range need to add 1 each time

        # definition of the initialization list
        theta0 = self.get_theta0(iinit, u, v)
        # find i*, and f0 that points to x* in the list of intial points in theta0
        if iinit != 3:
            f0, istar, ncall1 = self.init(theta0, l, L, stopping_actions, n)
            ncall = ncall + ncall1  # increasing number of function call count

        # Computing B[x,y] in this case y = v
        # 1 base vertex
        # definition of the base vertex of the original box
        # intial theta0 (mid point) is the base of vertex
        x = np.zeros(n)
        for i in range(n):
            x[i] = theta0[i, l[i]]
        # 2 oposite vertex -
        # definition of the opposite vertex v1 of the original box
        # selecting one of the corener of the box
        v1 = np.zeros(n)
        for i in range(n):
            if abs(theta[i] - u[i]) > abs(theta[i] - v[i]):
                #  corner at the lower bound side (left of mid point)
                v1[i] = u[i]  #  go left
            else:
                # corener of the upper bound side
                v1[i] = v[i]  #  go right of mid point

        # some parameters needed for initializing large arrays
        step = 1000
        step1 = 10000
        dim = step1

        # initialization of some large arrays
        isplit = np.zeros(step1).astype(int)  # number indicating ith coardinate split
        level = np.zeros(step1).astype(int)  # number indicating level
        ipar = np.zeros(step1).astype(int)  # number
        ichild = np.zeros(step1).astype(int)  # number
        nogain = np.zeros(step1).astype(int)  # number

        f = np.zeros((2, step1))  # function value of the splitinhg float value
        z = np.zeros((2, step1))  # splitin point float value

        # initialization of the record list, the counters nboxes, nbasket, m
        # and nloc, xloc and the output flag
        record = np.zeros(smax)  #  global variable record(1:smax-1)
        nboxes = 0  #  global variable (we start with 1 box)
        nbasket = -1  #  global variable
        nbasket0 = -1
        nsweepbest = 0
        nsweep = 0  #  global variable
        m = n
        record[0] = 1  #  check 1 of Matlab = 0 of py
        nloc = 0
        xloc = []  #  global variable
        flag = 1

        # Initialize the boxes
        # use of global vaiables global: nboxes nglob xglob
        ipar, level, ichild, f, isplit, p, xbest, fbest, nboxes = initbox(
            theta0, f0, l, L, istar, u, v, isplit, level, ipar, ichild, f, nboxes, prt
        )
        # generates the boxes in the initialization procedure
        f0min = fbest

        # print(stop)
        if stop[0] > 0 and stop[0] < 1:
            flag = chrelerr(fbest, stop)
        elif stop[0] == 0:
            flag = chvtr(fbest, stop[1])
        if not flag:
            print("glabal minumum as been found :", flag)
            # return  xbest,fbest,xmin,fmi,ncall,ncloc,flag
            # if the (known) minimum function value fglob has been found with the
            # required tolerance, flag is set to 0 and the program is terminated

        # the vector record is updated, and the minimal level s containing non-split boxes is computed
        s, record = strtsw(smax, level, f[0, :], nboxes, record)
        nsweep = nsweep + 1
        # sweep counter

        # Check values in MATLAB for these
        # theta0, u, v, l, L, x,v1, f0, istar, f, ipar,level,ichild,f,isplit,p,xbest,fbest,nboxes,nglob,xglob, s,record,nsweep
        # %%
        xmin = []
        fmi = []
        while s < smax and ncall + 1 <= nf:
            # %%
            # print('s values',s)
            par = record[s]  # the best box at level s is the current box
            # compute the base vertex x, the opposite vertex y, the 'neighboring'
            # vertices and their function values needed for quadratic
            # interpolation and the vector n0 indicating that the ith coordinate
            # has been split n0(i) times in the history of the box
            n0, x, y, x1, x2, f1, f2 = vertex(
                par, n, u, v, v1, theta0, f0, ipar, isplit, ichild, z, f, l, L
            )

            # s 'large'
            if s > 2 * n * (min(n0) + 1):
                # splitting index and splitting value z(2,par) for splitting by
                # rank are computed
                # z(2,par) is set to Inf if we split according to the init. list
                isplit[par], z[1, par] = splrnk(n, n0, p, x, y)
                splt = 1  # % indicates that the box is to be split
            else:
                # box has already been marked as not eligible for splitting by expected gain
                if nogain[par]:
                    splt = 0
                else:
                    # splitting by expected gain
                    # compute the expected gain vector e and the potential splitting
                    # index and splitting value
                    e, isplit[par], z[1, par] = exgain(
                        n, n0, l, L, x, y, x1, x2, f[0, par], f0, f1, f2
                    )
                    fexp = f[0, par] + min(e)
                    if fexp < fbest:
                        splt = 1
                    else:
                        splt = 0  # the box is not split since we expect no improvement
                        nogain[par] = (
                            1  # the box is marked as not eligible for splitting by expected gain
                        )
                # end if nogain
            # end if s > 2*n*(min(n0)+1)  else
            # print(z[1,par]) # print(f[0,par])
            # %%
            if splt == 1:  # prepare for splitting
                i = isplit[par]  #  no deduction beacuse of positive index
                level[par] = 0
                # print('check len b:',len(xmin),nbasket,nbasket0)
                if z[1, par] == np.Inf:  # prepare for splitting by initialization list
                    m = m + 1
                    z[1, par] = m
                    (
                        xbest,
                        fbest,
                        f01,
                        xmin,
                        fmi,
                        ipar,
                        level,
                        ichild,
                        f,
                        flag,
                        ncall1,
                        record,
                        nboxes,
                        nbasket,
                        nsweepbest,
                        nsweep,
                    ) = splinit(
                        fcn,
                        i,
                        s,
                        smax,
                        par,
                        theta0,
                        n0,
                        u,
                        v,
                        x,
                        y,
                        x1,
                        x2,
                        L,
                        l,
                        xmin,
                        fmi,
                        ipar,
                        level,
                        ichild,
                        f,
                        xbest,
                        fbest,
                        stop,
                        prt,
                        record,
                        nboxes,
                        nbasket,
                        nsweepbest,
                        nsweep,
                    )
                    f01 = f01.reshape(len(f01), 1)
                    f0 = np.concatenate((f0, f01), axis=1)
                    ncall = ncall + ncall1  #  print('call spl - 1')
                else:  # prepare for default splitting
                    z[0, par] = x[i]
                    (
                        xbest,
                        fbest,
                        xmin,
                        fmi,
                        ipar,
                        level,
                        ichild,
                        f,
                        flag,
                        ncall1,
                        record,
                        nboxes,
                        nbasket,
                        nsweepbest,
                        nsweep,
                    ) = split(
                        fcn,
                        i,
                        s,
                        smax,
                        par,
                        n0,
                        u,
                        v,
                        x,
                        y,
                        x1,
                        x2,
                        z[:, par],
                        xmin,
                        fmi,
                        ipar,
                        level,
                        ichild,
                        f,
                        xbest,
                        fbest,
                        stop,
                        prt,
                        record,
                        nboxes,
                        nbasket,
                        nsweepbest,
                        nsweep,
                    )
                    ncall = ncall + ncall1  # print('call spl - 2')
                # print('check len a:',len(xmin),nbasket,nbasket0)
                if nboxes > dim:
                    isplit = np.concatenate((isplit, np.zeros(step)))
                    level = np.concatenate((level, np.zeros(step)))
                    ipar = np.concatenate((ipar, np.zeros(step)))
                    ichild = np.concatenate((ichild, np.zeros(step)))
                    nogain = np.concatenate((nogain, np.zeros(step)))
                    f = np.concatenate((f, np.ones((2, step))), axis=1)
                    z = np.concatenate((z, np.ones((2, step))), axis=1)
                    dim = nboxes + step
                if not flag:
                    break
            else:  # % splt=0: no splitting, increase the level by 1
                # %%
                if s + 1 < smax:
                    level[par] = s + 1
                    record = updtrec(par, s + 1, f[0, :], record)  #  update record
                else:
                    level[par] = 0
                    nbasket = nbasket + 1
                    if len(xmin) == nbasket:
                        xmin.append(copy.deepcopy(x))  # xmin[:,nbasket] = x
                        fmi.append(f[0, par])
                    else:
                        xmin[nbasket] = copy.deepcopy(x)
                        fmi[nbasket] = f[0, par]
            # print('Level:',level)  #print('Record:',record)
            # %%
            # update s to split boxes
            s = s + 1
            while s < smax:
                if record[s] == 0:
                    s = s + 1
                else:
                    break
            # %%
            # if smax is reached, a new sweep is started
            if s == smax:
                # print(s)
                if local:
                    # print(fmi, xmin,nbasket0,nbasket)
                    fmiTemp = fmi[nbasket0 + 1 : nbasket + 1]
                    xminTemp = xmin[nbasket0 + 1 : nbasket + 1]
                    j = np.argsort(fmiTemp)
                    fmiTemp = np.sort(fmiTemp)
                    xminTemp = [copy.deepcopy(xminTemp[jInd]) for jInd in j]
                    fmi[nbasket0 + 1 : nbasket + 1] = fmiTemp
                    xmin[nbasket0 + 1 : nbasket + 1] = xminTemp
                    # print('j, fmi, xmin:',j, fmi, xmin,nbasket0,nbasket, len(xmin))

                    for j in range(nbasket0 + 1, nbasket + 1):
                        x = copy.deepcopy(xmin[j])
                        f1 = copy.deepcopy(fmi[j])
                        loc = chkloc(nloc, xloc, x)
                        # print('check lock:',j,x,f1,nloc, xloc,loc)
                        if loc:
                            # print('chaking basket ',nbasket0)
                            nloc, xloc = addloc(nloc, xloc, x)
                            (
                                xbest,
                                fbest,
                                xmin,
                                fmi,
                                x,
                                f1,
                                loc,
                                flag,
                                ncall1,
                                nsweep,
                                nsweepbest,
                            ) = basket(
                                fcn,
                                x,
                                f1,
                                xmin,
                                fmi,
                                xbest,
                                fbest,
                                stop,
                                nbasket0,
                                nsweep,
                                nsweepbest,
                            )
                            # print(xbest,fbest,xmin,fmi,loc,flag,ncall1)
                            ncall = ncall + ncall1
                            if not flag:
                                break
                            if loc:
                                xmin1, fmi1, nc, flag, nsweep, nsweepbest = lsearch(
                                    fcn,
                                    x,
                                    f1,
                                    f0min,
                                    u,
                                    v,
                                    nf - ncall,
                                    stop,
                                    local,
                                    gamma,
                                    hess,
                                    nsweep,
                                    nsweepbest,
                                )
                                ncall = ncall + nc
                                ncloc = ncloc + nc
                                if fmi1 < fbest:
                                    xbest = copy.deepcopy(xmin1)
                                    fbest = copy.deepcopy(fmi1)
                                    nsweepbest = nsweep
                                    if not flag:
                                        nbasket0 = nbasket0 + 1
                                        nbasket = copy.deepcopy(nbasket0)
                                        if len(xmin) == nbasket:
                                            xmin.append(copy.deepcopy(xmin1))
                                            fmi.append(copy.deepcopy(fmi1))
                                        else:
                                            xmin[nbasket] = copy.deepcopy(xmin1)
                                            fmi[nbasket] = copy.deepcopy(fmi1)
                                        break

                                    if stop[0] > 0 and stop[0] < 1:
                                        flag = chrelerr(fbest, stop)
                                    elif stop[0] == 0:
                                        flag = chvtr(fbest, stop[1])
                                    if not flag:
                                        return xbest, fbest, xmin, fmi, ncall, ncloc, flag
                                    # end if
                                # end if fmi1
                                # print('chaking basket 1',nbasket0)
                                (
                                    xbest,
                                    fbest,
                                    xmin,
                                    fmi,
                                    loc,
                                    flag,
                                    ncall1,
                                    nsweep,
                                    nsweepbest,
                                ) = basket1(
                                    fcn,
                                    np.array(xmin1),
                                    fmi1,
                                    xmin,
                                    fmi,
                                    xbest,
                                    fbest,
                                    stop,
                                    nbasket0,
                                    nsweep,
                                    nsweepbest,
                                )
                                ncall = ncall + ncall1
                                # print(xbest,fbest,xmin,fmi,loc,flag,ncall1)
                                if not flag:
                                    break
                                if loc:
                                    # print('check1:',nbasket0, nbasket,xmin,fmi)
                                    nbasket0 = nbasket0 + 1
                                    if len(xmin) == nbasket0:
                                        xmin.append(copy.deepcopy(xmin1))
                                        fmi.append(copy.deepcopy(fmi1))
                                    else:
                                        xmin[nbasket0] = copy.deepcopy(xmin1)
                                        fmi[nbasket0] = copy.deepcopy(fmi1)
                                    # print('check2:',nbasket0, nbasket,xmin,fmi)
                                    fbest, xbest = fbestloc(
                                        fmi, fbest, xmin, xbest, nbasket0, stop
                                    )
                                    if not flag:
                                        nbasket = nbasket0
                                        break
                    # end for  basket
                    nbasket = copy.deepcopy(nbasket0)
                    if not flag:
                        break
                # end local
                s, record = strtsw(smax, level, f[0, :], nboxes, record)
                if prt:
                    # if nsweep == 1:
                    #    print(', =)
                    # print('nsw   minl   nf     fbest        xbest\n')

                    minlevel = s
                    print("nsweep:", nsweep)
                    print("minlevel:", minlevel)
                    print("ncall:", ncall)
                    print("fbest:", fbest)
                    print("xbest: ", xbest)
                    print("\n")

                if stop[0] > 1:
                    if nsweep - nsweepbest >= stop[0]:
                        flag = 3
                        return xbest, fbest, xmin, fmi, ncall, ncloc, flag
                nsweep = nsweep + 1
            # end if  s ==  max
        # end while
        if ncall >= nf:
            flag = 2

        #    if local:
        #        print(len(fmi),nbasket)
        #        if len(fmi) > nbasket:
        #            for inx in range(nbasket+1,len(fmi)):
        #                del xmin[inx]
        #                del fmi[inx]
        return xbest, fbest, xmin, fmi, ncall, ncloc, flag
