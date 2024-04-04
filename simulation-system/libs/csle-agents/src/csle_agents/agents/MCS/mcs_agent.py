import copy
import sys
from mcs_fun.genbox import genbox
from mcs_fun.hessian import hessian
from mcs_fun.polint import polint
from mcs_fun.quadratic_func import quadmin
from gls.lssat import lssat
from mcs_fun.neighbor import neighbor
from mcs_fun.quadratic_func import quadpol
import math
from gls.lsconvex import lsconvex
from gls.lsrange import lsrange
from gls.lssplit import lssplit
from gls.lsinit import lsinit
from gls.lssort import lssort
from mcs_fun.initi_func import subint
# from mcs_fun.chk_flag import chreler
from minq.minq import minq 
# from mcs_fun.chk_flag import chvtr
# from mcs_fun.updtrec import updtrec
from mcs_fun.sign import sign
import numpy as np
from mcs_fun.polint import polint1
# from mcs_fun.basket_func import basket, basket1

# %
# MCS algorithm supporting functions =  first layer
from mcs_fun.chk_bound import check_box_bound
from mcs_fun.chk_flag import chrelerr, chvtr
from mcs_fun.chk_locks import addloc, chkloc, fbestloc
from mcs_fun.exgain import exgain
from gls.lsguard import lsguard
from gls.quartic import quartic
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


# from mcs import mcs
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

    def simple_func(self, x):
        return (x[0] - 10)**2 + (x[1] - 2)**2 + (x[2] - 3)**2

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
            metrics = MCSAgent.update_metrics(metrics=metrics, info=info)
        avg_metrics = MCSAgent.compute_avg_metrics(metrics=metrics)
        return avg_metrics

    @staticmethod
    def update_metrics(metrics: Dict[str, List[Union[float, int]]], info: Dict[str, Union[float, int]]) \
            -> Dict[str, List[Union[float, int]]]:
        """
        Update a dict with aggregated metrics using new information from the environment

        :param metrics: the dict with the aggregated metrics
        :param info: the new information
        :return: the updated dict
        """
        for k, v in info.items():
            if k in metrics:
                metrics[k].append(round(v, 3))
            else:
                metrics[k] = [v]
        return metrics

    @staticmethod
    def compute_avg_metrics(metrics: Dict[str, List[Union[float, int]]]) -> Dict[str, Union[float, int]]:
        """
        Computes the average metrics of a dict with aggregated metrics

        :param metrics: the dict with the aggregated metrics
        :return: the average metrics
        """
        avg_metrics = {}
        for k, v in metrics.items():
            avg = round(sum(v) / len(v), 2)
            avg_metrics[k] = avg
        return avg_metrics
    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return [agents_constants.MCS.STEP, agents_constants.MCS.STEP1,
                agents_constants.MCS.U, agents_constants.MCS.V,
                agents_constants.MCS.LOCAL,agents_constants.MCS.STOPPING_ACTIONS,
                agents_constants.MCS.GAMMA, agents_constants.MCS.EPSILON,
                agents_constants.COMMON.CONFIDENCE_INTERVAL,
                agents_constants.COMMON.RUNNING_AVERAGE]


    def train(self):#, exp_result, seed: int, random_seeds: List[int], training_job: TrainingJobConfig):
        """
        Initiating the parameters of performing the MCS algorithm, using external functions
        """
        u =  self.experiment_config.hparams[agents_constants.MCS.U].value
        v = self.experiment_config.hparams[agents_constants.MCS.V].value
        iinit = self.experiment_config.hparams[agents_constants.MCS.IINIT].value # simple initialization list
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

        config = self.simulation_env_config.simulation_env_input_config
        if self.env is None:
            self.env = gym.make(self.simulation_env_config.gym_env_name, config=config)
        # if m == 0:
        #     stop[0] = 1e-4	 # run until this relative error is achieved
        #     stop[1] = fglob	 # known global optimum value
        #     stop.append(1e-10) # stopping tolerance for tiny fglob
        
        xbest,fbest,xmin,fmi,ncall,ncloc,flag = self.MCS(u, v, smax, nf, stop, iinit,
                                                         local, gamma,hess, stopping_actions, eps)

        print('The MCS Algorithms Results:')
        print('fbest', fbest)
        print('xbest', xbest)
        print('\n')

    def get_theta0(self, iinit, u, v):
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
        # print("policy theta = ", policy.theta)

        # avg_metrics = self.eval_theta(policy=policy,
        #                               max_steps=self.experiment_config.hparams[
        #                                   agents_constants.COMMON.MAX_ENV_STEPS].value)
        # J1 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
        J1 = self.simple_func(theta)
        print("J1 = ", J1)
        ncall += 1 # increasing the number of function call by 1
        
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
                    # policy = self.get_policy(theta, L=stopping_actions)
                    # avg_metrics = self.eval_theta(policy=policy,
                                                  # max_steps=self.experiment_config.hparams[
                                                  #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                    # J0[j, i] = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                    J0[j, i] = self.simple_func(theta)
                    # print(J0)
                    ncall = ncall + 1 # increasing the number of cfunction call by 1 each time
                    #print(i+1,j+1,x,f0[j,i])
                    if J0[j,i] < J1:
                        J1 = J0[j,i]
                        istar[i] = j
            # end search in list 
            # update x*
            theta[i] = theta0[i,istar[i]]
        #end for k = 1:n  
        return J0, istar, ncall

    def MCS(self, u, v, smax, nf, stop, iinit, local, gamma, hess, stopping_actions,  eps, prt=1):

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
        theta = np.zeros(n)
        for i in range(n):
            theta[i] = theta0[i, l[i]]
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
        step = self.experiment_config.hparams[agents_constants.MCS.STEP].value
        step1 = self.experiment_config.hparams[agents_constants.MCS.STEP1].value
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
        ipar, level, ichild, f, isplit, p, xbest, fbest, nboxes = self.initbox(
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
                    ) = self.splinit(
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
                        stopping_actions
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
                    ) = self.split(
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
                        stopping_actions
                    )
                    ncall = ncall + ncall1  # print('call spl - 2')
                # print('check len a:',len(xmin),nbasket,nbasket0)
                if nboxes > dim:
                    isplit = np.concatenate((isplit, np.zeros(step)))
                    level = np.concatenate((level, np.zeros(step)))
                    ipar = np.concatenate((ipar, np.zeros(step)))
                    ichild = np.concatenate((ichild, np.zeros(step)))
                    nogain = np.concatenate((nogain, np.zeros(step)))
                    J = np.concatenate((J, np.ones((2, step))), axis=1)
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
                            ) = self.basket(
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
                                stopping_actions
                            )
                            # print(xbest,fbest,xmin,fmi,loc,flag,ncall1)
                            ncall = ncall + ncall1
                            if not flag:
                                break
                            if loc:
                                xmin1, fmi1, nc, flag, nsweep, nsweepbest = self.lsearch(
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
                                    stopping_actions,
                                    eps
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
                                ) = self.basket1(
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
                                    stopping_actions
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

    def splinit(self, i,s,smax,par,x0,n0,u,v,x,y,x1,x2,L,l,xmin,fmi,ipar,level,ichild,f,xbest,fbest,stop,prt, record,nboxes,nbasket,nsweepbest,nsweep, stopping_actions):
        '''
        % splits box # par at level s according to the initialization list
        % in the ith coordinate and inserts its children and their parameters
        % in the list 
        '''
 
        # initialization 
        ncall = 0
        n = len(x)
        f0 = np.zeros(max(L)+1)
        flag = 1
        
        for j in range(L[i]+1):
            if j != l[i]:
                x[i] = x0[i,j]
                
                policy = self.get_policy(x, L=stopping_actions)
                # avg_metrics = self.eval_theta(policy=policy,
                                            # max_steps=self.experiment_config.hparams[
                                            #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                # f0[j] = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                f0[j] = self.simple_func(policy.theta)
                ncall = ncall + 1
                if f0[j] < fbest:
                    fbest = f0[j]
                    xbest = copy.deepcopy(x)
                    nsweepbest = copy.deepcopy(nsweep)
                    if stop[0] > 0 and stop[0] < 1:
                        flag = chrelerr(fbest,stop)
                    elif stop[0] == 0:
                        flag = chvtr(fbest,stop[2])      
                    if not flag:
                        return xbest,fbest,f0,xmin,fmi,ipar,level,ichild,f,flag,ncall, record,nboxes,nbasket,nsweepbest,nsweep  
            else:
                f0[j] = f[0,par]
            #end j != l[i]
        #end for j
        if s + 1 < smax:
            nchild = 0
            if u[i] < x0[i,0]: # in that case the box at the boundary gets level s + 1
                nchild = nchild + 1
                nboxes = nboxes + 1
                ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+1,-nchild,f0[0])
                record = updtrec(nboxes,level[nboxes],f[0,:], record)
            #end if ui <  xo[i,0]
            for j in range(L[i]):
                nchild = nchild + 1
                #splval = split1(x0[i,j],x0[i,j+1],f0[j],f0[j+1])
                if f0[j] <= f0[j+1] or s + 2 < smax:
                    nboxes = nboxes + 1
                    if f0[j] <= f0[j+1]:
                        level0 = s + 1
                    else:
                        level0 = s + 2
                    #end if f0
                    # the box with the smaller function value gets level s + 1, the one with
                    # the larger function value level s + 2
                    ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,level0,-nchild,f0[j])
                    record = updtrec(nboxes,level[nboxes],f[0,:], record)
                else:
                    x[i] = x0[i,j]
                    nbasket = nbasket + 1
                    if(len(xmin) == nbasket):
                        xmin.append(copy.deepcopy(x))
                        fmi.append(f0[j])                  
                    else:
                        xmin[nbasket] = copy.deepcopy(x)
                        fmi[nbasket] = f0[j]
                #end if f0[j] <= f0[j+1]  or s + 2 < smax
                nchild = nchild + 1                
                if f0[j+1] < f0[j] or s + 2 < smax:
                    nboxes = nboxes + 1
                    if f0[j+1] < f0[j]:
                        level0 = s + 1
                    else:
                        level0 = s + 2
                    #end
                    ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,level0,-nchild,f0[j+1])
                    record = updtrec(nboxes,level[nboxes],f[0,:], record)
                else:
                    x[i] = x0[i,j+1]
                    nbasket = nbasket + 1
                    if(len(xmin) == nbasket):
                        xmin.append(copy.deepcopy(x))
                        fmi.append(f0[j+1])
                    else:
                        xmin[nbasket] = copy.deepcopy(x)
                        fmi[nbasket] = f0[j+1]
                #end f0[j+1] < f0[j]
            #end for
            if x0[i,L[i]] < v[i]: # in that case the box at the boundary gets level s + 1
                nchild = nchild + 1
                nboxes = nboxes + 1
                ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+1,-nchild,f0[L[i]])
                record = updtrec(nboxes,level[nboxes],f[0,:], record)
            ##end if x0 < vi
        else:
            for j in range(L[i]+1):
                x[i] = x0[i,j]
                nbasket = nbasket + 1
                if(len(xmin) == nbasket):
                    xmin.append(copy.deepcopy(x))
                    fmi.append(f0[j])
                else:
                    xmin[nbasket] = copy.deepcopy(x)
                    fmi[nbasket] = f0[j]
        #end  s+1 < smax
        return xbest,fbest,f0,xmin,fmi,ipar,level,ichild,f,flag,ncall, record,nboxes,nbasket,nsweepbest,nsweep

    def split(self, i, s, smax, par, n0, u, v, x, y, x1, x2, z, xmin,
              fmi,ipar,level,ichild,f,xbest,fbest,stop,prt, record,
              nboxes,nbasket,nsweepbest,nsweep, stopping_actions):
        """
        Split Function
        """
        ncall = 0
        flag = 1
        x[i] = z[1]
        n = len(x)
        policy = self.get_policy(x, L=stopping_actions)
        # avg_metrics = self.eval_theta(policy=policy,
                                    # max_steps=self.experiment_config.hparams[
                                    #     agents_constants.COMMON.MAX_ENV_STEPS].value)
        # f[1,par] = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
        f[1,par] = self.simple_func(policy.theta)
        ncall = ncall + 1
        #print('fbest:',fbest)

        if f[1,par] < fbest:
            fbest = copy.deepcopy(f[1,par])
            xbest = copy.deepcopy(x)
            nsweepbest = copy.deepcopy(nsweep)
            
            if stop[0] > 0 and stop[0] < 1:
                flag = chrelerr(fbest,stop)
            elif stop[0] == 0:
                flag = chvtr(fbest,stop[2])
            #end
            if not flag:
                return xbest,fbest,xmin,fmi,ipar,level,ichild,f,flag,ncall, record,nboxes,nbasket,nsweepbest,nsweep
        #end if f-par < best
        #splval = split1(z[0],z[1],f[0,par],f[1,par])
        
        if s + 1 < smax:
            if f[0,par] <= f[1,par]:
                nboxes = nboxes + 1
                ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+1,1,f[0,par])
                record = updtrec(nboxes,level[nboxes],f[0,:],record)
                if s + 2 < smax:
                    nboxes = nboxes + 1
                    ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+2,2,f[1,par])
                    record = updtrec(nboxes,level[nboxes],f[0,:],record)
                else:
                    x[i] = z[1]
                    nbasket = nbasket + 1
                    if(len(xmin) == nbasket):
                        xmin.append(copy.deepcopy(x)) #xmin[:,nbasket] = x
                        fmi.append(f[1,par])#fmi[nbasket] = f[1,par]
                    else:
                        xmin[nbasket] = copy.deepcopy(x)
                        fmi[nbasket] = f[1,par]
                #end if s+2 < smax
            else:
                if s + 2 < smax:
                    nboxes = nboxes + 1
                    ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+2,1,f[0,par])
                    record = updtrec(nboxes,level[nboxes],f[0,:],record)
                else:
                    x[i] = z[0]
                    nbasket = nbasket + 1
                    if(len(xmin) == nbasket):
                        xmin.append(copy.deepcopy(x))
                        fmi.append(f[0,par])
                    else:
                        xmin[nbasket] = copy.deepcopy(x)
                        fmi[nbasket] = f[0,par]
                # end s+2
                nboxes = nboxes + 1
                ipar[nboxes], level[nboxes], ichild[nboxes], f[0,nboxes] = genbox(par,s+1,2,f[1,par])
                record = updtrec(nboxes,level[nboxes],f[0,:],record)
            # end if f[0,par] <= f[1,par] else 
            
            #if the third box is larger than the smaller of the other two boxes,
            # it gets level s + 1 otherwise it gets level s + 2
            if z[1] != y[i]:
                if abs(z[1]-y[i]) > abs(z[1]-z[0])*(3-np.sqrt(5))*0.5:
                    nboxes = nboxes + 1
                    ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+1,3,f[1,par])
                    record = updtrec(nboxes,level[nboxes],f[0,:],record)
                else:
                    if s + 2 < smax:
                        nboxes = nboxes + 1
                        ipar[nboxes],level[nboxes],ichild[nboxes],f[0,nboxes] = genbox(par,s+2,3,f[1,par])
                        record = updtrec(nboxes,level[nboxes],f[0,:],record)
                    else:
                        x[i] = z[1]
                        nbasket = nbasket + 1
                        if(len(xmin) == nbasket):
                            xmin.append(copy.deepcopy(x)) # xmin[:,nbasket] = x
                            fmi.append(copy.deepcopy(f[1,par])) # fmi[nbasket] = f[1,par]
                        else:
                            xmin[nbasket] = copy.deepcopy(x)
                            fmi[nbasket] = f[1,par]
                #end abs
            #end z1 ! = 
        else:
            #print(i,x,z)
            xi1 =  copy.deepcopy(x)
            xi2 =  copy.deepcopy(x)
            
            xi1[i] = z[0]
            #print(xi1)
            nbasket = nbasket + 1
            if(len(xmin) == nbasket):
                xmin.append(xi1) #xmin[:,nbasket] = x
                fmi.append(f[0,par])
            else:
                xmin[nbasket] = xi1
                fmi[nbasket] = f[0,par]
            
            xi2[i] = z[1]
            #print(xi2)
            nbasket = nbasket + 1
            if(len(xmin) == nbasket):
                xmin.append(xi2)
                fmi.append(f[1,par])
            else:
                xmin[nbasket] = xi2
                fmi[nbasket] = f[1,par]
        # end if s+1 < smax
        #print('operating on min 1')
        #print(f[0,par], f[1,par], fmi, xmin)
        #print('operating on min 1')
        return xbest,fbest,xmin,fmi,ipar,level,ichild,f,flag,ncall, record,nboxes,nbasket,nsweepbest,nsweep


#------------------------------------------------------------------------------

    def initbox(self, theta0,f0,l,L,istar,u,v,isplit,level,ipar,ichild,f,nboxes,prt):
        """
        Generates the boxes in the initializaiton procedure
        """
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
        # optimi value of the box is theta0
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
            if theta0[i,0] >  u[i]:
                nboxes = nboxes + 1 # one extra box is generated for the parent box
                nchild = nchild + 1 # therefore incerase number of child by 1 of the parent box
                # set parent of this ith box split in the ithe direction (dimension)
                ipar[nboxes], level[nboxes], ichild[nboxes], f[0,nboxes] = genbox(par, level[par]+1,-nchild, f0[0, i])
            # end if
            
            if L[i] == 2:
                v1 = v[i]
            else:
                v1 = theta0[i,2]
            # end if
            
            # pollynomial interpolation to get three points for
            d = polint(theta0[i,0:3],f0[0:3,i])
            xl = quadmin(u[i],v1,d,theta0[i,0:3])
            fl = quadpol(xl,d,theta0[i,0:3])
            xu = quadmin(u[i],v1,-d,theta0[i,0:3])
            fu = quadpol(xu,d,theta0[i,0:3])
            
            if istar[i] == 0:
                if xl < theta0[i,0]:
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
                #if prt: splval = split1(theta0[i,j],theta0[i,j+1],f0[j,i],f0[j+1,i])
                
                if j >= 1:
                    if istar[i] == j:
                        if xl <= theta0[i,j]:
                            par1 = nboxes - 1  # label of the current box for the next coordinate 
                        else:
                            par1 = nboxes
                    #end istar
                    if j <= L[i] - 2:
                        d = polint(theta0[i,j:j+1],f0[j:j+1,i])
                        if j < L[i] - 2:
                            u1 = theta0[i,j+1]
                        else:
                            u1 = v[i] 
                        # end if
                        xl = quadmin(theta0[i,j],u1,d,theta0[i,j:j+1])
                        fl = min(quadpol(xl,d,theta0[i,j:j+1]),fl)
                        xu = quadmin(theta0[i,j],u1,-d,theta0[i,j:j+1])
                        fu = max(quadpol(xu,d,theta0[i,j:j+1]),fu)
                    #end j < Li -2
                # end if j > = 1
                nboxes = nboxes + 1
                nchild = nchild + 1
                ipar[nboxes], level[nboxes], ichild[nboxes], f[0,nboxes] = genbox(par,level[par]+3-s,-nchild,f0[j+1,i])
            #end for j
            if theta0[i,L[i]] < v[i]:
                nboxes = nboxes + 1
                nchild = nchild + 1            
                ipar[nboxes], level[nboxes], ichild[nboxes], f[0,nboxes] = genbox(par,level[par]+1,-nchild,f0[L[i],i])
                
            if istar[i] == L[i]:
                if theta0[i,L[i]] < v[i]:
                    if xl <= theta0[i,L[i]]:
                        par1 = nboxes - 1  # label of the current box for the next coordinate 
                    else:
                        par1 = nboxes
                    #end if xl < theta0
                else:
                    par1 = nboxes
                #end if theta0 < v
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
            xbest[i] = theta0[i,istar[i]]  # best point after the init. procedured
        
        return  ipar,level,ichild,f,isplit,p,xbest,fbest,nboxes


    def basket(self, x, f, xmin, fmi, xbest, fbest, stop, nbasket, nsweep, nsweepbest, stopping_actions):
        """ """
        loc = 1
        flag = 1
        ncall = 0
        if not nbasket:
            return xbest, fbest, xmin, fmi, x, f, loc, flag, ncall, nsweep, nsweepbest

        dist = np.zeros(nbasket + 1)
        for k in range(len(dist)):
            dist[k] = np.linalg.norm(np.subtract(x, xmin[k]))

        dist1 = np.sort(dist)
        ind = np.argsort(dist)

        for k in range(nbasket + 1):
            i = ind[k]
            if fmi[i] <= f:
                p = xmin[i] - x

                y1 = x + 1 / 3 * p
                policy = self.get_policy(y1, L=stopping_actions)
                # avg_metrics = self.eval_theta(policy=policy,
                                            # max_steps=self.experiment_config.hparams[
                                            #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                f1 = self.simple_func(policy.theta)
                # f1 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)

                ncall = ncall + 1
                if f1 <= f:
                    y2 = x + 2 / 3 * p
                    policy = self.get_policy(y2, L=stopping_actions)
                    # avg_metrics = self.eval_theta(policy=policy,
                                                # max_steps=self.experiment_config.hparams[
                                                #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                    # f2 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                    f2 = self.simple_func(policy.theta) # TODO : if theis eval fails, then just go with y2 or something
                    ncall = ncall + 1
                    if f2 > max(f1, fmi[i]):
                        if f1 < f:
                            x = y1
                            f = f1
                            if f < fbest:
                                fbest = f
                                xbest = copy.deepcopy(x)
                                nsweepbest = nsweep
                                if stop[0] > 0 and stop[0] < 1:
                                    flag = chrelerr(fbest, stop)
                                elif stop[0] == 0:
                                    flag = chvtr(fbest, stop[1])
                                if not flag:
                                    return (
                                        xbest,
                                        fbest,
                                        xmin,
                                        fmi,
                                        x,
                                        f,
                                        loc,
                                        flag,
                                        ncall,
                                        nsweep,
                                        nsweepbest,
                                    )
                    else:
                        if f1 < min(f2, fmi[i]):
                            f = f1
                            x = copy.deepcopy(y1)
                            if f < fbest:
                                fbest = f
                                xbest = copy.deepcopy(x)
                                nsweepbest = nsweep
                                if stop[0] > 0 and stop[0] < 1:
                                    flag = chrelerr(fbest, stop)
                                elif stop[0] == 0:
                                    flag = chvtr(fbest, stop[1])
                                if not flag:
                                    return (
                                        xbest,
                                        fbest,
                                        xmin,
                                        fmi,
                                        x,
                                        f,
                                        loc,
                                        flag,
                                        ncall,
                                        nsweep,
                                        nsweepbest,
                                    )
                            elif f2 < min(f1, fmi[i]):
                                f = f2
                                x = copy.deepcopy(y2)
                                if f < fbest:
                                    fbest = f
                                    xbest = copy.deepcopy(x)
                                    nsweepbest = nsweep
                                    if stop[0] > 0 and stop[0] < 1:
                                        flag = chrelerr(fbest, stop)
                                    elif stop[0] == 0:
                                        flag = chvtr(fbest, stop[1])
                                    if not flag:
                                        return (
                                            xbest,
                                            fbest,
                                            xmin,
                                            fmi,
                                            x,
                                            f,
                                            loc,
                                            flag,
                                            ncall,
                                            nsweep,
                                            nsweepbest,
                                        )
                            else:
                                loc = 0
                                break

        return xbest, fbest, xmin, fmi, x, f, loc, flag, ncall, nsweep, nsweepbest


    def lsearch(self, x, f, f0, u, v, nf, stop, maxstep, gamma, hess, nsweep, nsweepbest, stopping_actions, eps):    
        ncall = 0# 
        n = len(x)# 
        x0 = np.asarray([min(max(u[i],0),v[i]) for i in range(len(u))])#  % absolutely smallest point

        flag = 1# 
        eps0 = 0.001# 
        nloc = 1# 
        small = 0.1# 
        smaxls = 15# 
        
        xmin,fmi,g,G,nfcsearch = self.csearch(x,f,u,v,hess, stopping_actions)
        
        xmin = [max(u[i],min(xmin[i],v[i])) for i in range(n)]
        ncall = ncall + nfcsearch
        xold = copy.deepcopy(xmin) # deep copy is must here
        fold = copy.deepcopy(fmi)
        #print('csearch ends with:') # print(xmin,fmi,g,G,nfcsearch)
        
        # eps = 2.220446049250313e-16
        
        if stop[0] > 0  and  stop[0] < 1:
            flag = chrelerr(fmi,stop)# 
        elif stop[0] == 0:
            flag = chvtr(fmi,stop[1])# 

        if not flag:
            return xmin,fmi,ncall,flag,nsweep,nsweepbest
        
        d = np.asarray([min(min(xmin[i]-u[i],v[i]-xmin[i]),0.25*(1+abs(x[i]-x0[i]))) for i in range(n)])
        # Calling MINQ function # print(fmi,g,G,-d,d,0)
        p,_,_ = minq(fmi,g,G,-d,d,0) # print('minq') # print(p) 
        
        x = [max(u[i],min(xmin[i]+p[i],v[i])) for i in range(n)]
        p = np.subtract(x,xmin)  # project search direction to box
        
        if np.linalg.norm(p):
            policy = self.get_policy(x, L=stopping_actions)
            # avg_metrics = self.eval_theta(policy=policy,
                                          # max_steps=self.experiment_config.hparams[
                                          #     agents_constants.COMMON.MAX_ENV_STEPS].value)
            # f1 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
            f1 = self.simple_func(policy.theta)
            ncall = ncall + 1
            alist = [0,1] 
            flist = [fmi,f1] 
            fpred = fmi + np.dot(g.T,p) + np.dot(0.5, np.dot(p.T,np.dot(G,p)))        
            alist,flist,nfls = self.gls(u, v, xmin, p, alist,
                                        flist, nloc, small, smaxls, stopping_actions)
            ncall = ncall + nfls

            i = np.argmin(flist)
            fminew = min(flist)
            if fminew == fmi:
                i = [i for i in range(len(alist)) if not alist[i]][0] 
            else:
                fmi = copy.deepcopy(fminew)
            
            xmin = xmin + np.dot(alist[i],p)
            xmin = np.asarray([max(u[i],min(xmin[i],v[i])) for i in range(n)])
            gain = f - fmi
            
            if stop[0] > 0  and  stop[0] < 1:
                flag = chrelerr(fmi,stop)
            elif stop[0] == 0:
                flag = chvtr(fmi,stop[1])
            
            if not flag:
                return xmin,fmi,ncall,flag,nsweep,nsweepbest
            
            if fold == fmi:
                r = 0
            elif fold == fpred:
                r = 0.5
            else:
                r = (fold-fmi)/(fold-fpred)
        else:
            gain = f - fmi 
            r = 0
            
        diag = 0
        ind = [i for i in range(n) if (u[i] < xmin[i]  and  xmin[i] < v[i])] 
        b = np.dot(np.abs(g).T,[max(abs(xmin[i]),abs(xold[i])) for i in range(len(xmin))]) # print('chek b')  print(g,xmin,xold) # print(b)
        nstep = 0
        
        #print('ncall',nf, ncall, maxstep, len(ind),fmi, gain, r)
        while (ncall < nf)  and  (nstep < maxstep)  and  ((diag or len(ind) < n) or (stop[0] == 0  and  fmi - gain <= stop[1]) or (b >= gamma*(f0-f)  and  gain > 0)):
            #print('while')
            nstep = nstep + 1
            delta = [abs(xmin[i])*eps**(1/3) for i in range(len(xmin))]
            #print('delta:',xmin, delta)        
            j = [inx for inx in range(len(delta)) if (not delta[inx])]
            if len(j)  != 0:
                for inx in j:
                    delta[inx] = eps**(1/3)*1 
                    
            x1,x2 = neighbor(xmin,delta,u,v)
            f = copy.deepcopy(fmi)

            if len(ind) < n  and  (b < gamma*(f0-f) or (not gain)):
                ind1 = [i for i in range(len(u)) if (xmin[i] == u[i] or xmin[i] == v[i])] 
                for k in range(len(ind1)):
                    i = ind1[k]
                    x = copy.deepcopy(xmin)
                    if xmin[i] == u[i]:
                        x[i] = x2[i] 
                    else:
                        x[i]  = x1[i]
                    policy = self.get_policy(x, L=stopping_actions)
                    # avg_metrics = self.eval_theta(policy=policy,
                                                  # max_steps=self.experiment_config.hparams[
                                                  #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                    # f1 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                    f1 = self.simple_func(policy.theta)
                    ncall = ncall + 1

                    if f1 < fmi:
                        alist = [0, x[i], -xmin[i]]
                        flist = [fmi, f1]
                        p = np.zeros(n) 
                        p[i]  = 1
                        alist,flist,nfls = self.gls(u, v, xmin, p, alist,
                                                    flist, nloc, small, 6, stopping_actions)
                        ncall = ncall + nfls
                        j = np.argmin(flist)
                        fminew = min(flist)# 
                        if fminew == fmi:
                            j = [inx for inx in range(len(alist)) if (not alist[inx])][0]
                        else:
                            fmi = fminew
                        xmin[i]  = xmin[i]  + alist[j]
                    else:
                        ind1[k] = -1
                #end for
                xmin = np.asarray([max(u[inx],min(xmin[inx],v[inx])) for inx in range(len(xmin))])
                if not sum(ind1):
                    break
            
                for inx in range(len(delta)):
                    delta[inx] = abs(xmin[inx])*eps**(1/3)
                j = [inx for inx in range(len(delta)) if (not delta[inx])]
                if len(j) != 0:
                    for inx in j:
                        delta[inx] = eps**(1/3)*1
                #end if
                x1,x2 = neighbor(xmin,delta,u,v)    
            #end if
            #print('r',r)
            if abs(r-1) > 0.25 or (not gain) or (b < gamma*(f0-f)):
                xmin,fmi,g,G,x1,x2,nftriple = self.triple(xmin,fmi,x1,x2,u,v,hess,0, stopping_actions, setG=True)
                ncall = ncall + nftriple
                diag = 0 
            else:
                xmin,fmi,g,G,x1,x2,nftriple = self.triple(xmin,fmi,x1,x2,u,v,hess,G, stopping_actions)
                ncall = ncall + nftriple
                diag = 1
            #end if
            #print(nftriple)
            xold = copy.deepcopy(xmin)
            fold = copy.deepcopy(fmi)
            
            if stop[0] > 0  and  stop[0] < 1:
                flag = chrelerr(fmi,stop)# 
            elif stop[0] == 0:
                flag = chvtr(fmi,stop[1])# 
        
            if not flag:
                return xmin,fmi,ncall,flag,nsweep,nsweepbest
            if r < 0.25:
                d = 0.5*d
            elif r > 0.75:
                d = 2*d

            minusd = np.asarray([max(-d[jnx],u[jnx]-xmin[jnx]) for jnx in range(len(xmin))])
            mind = np.asarray([min(d[jnx],v[jnx]-xmin[jnx]) for jnx in range(len(xmin))])
            p,_,_ = minq(fmi,g,G,minusd,mind,0)
            
            #print(p, np.linalg.norm(p))
            if not (np.linalg.norm(p))  and  (not diag)  and  (len(ind) == n):
                break
            
            if np.linalg.norm(p):
                #print(g, p, G)
                fpred = fmi + np.dot(g.T,p) + np.dot(0.5, np.dot(p.T,np.dot(G,p)))
                x = copy.deepcopy(xmin + p)
                policy = self.get_policy(x, L=stopping_actions)
                # avg_metrics = self.eval_theta(policy=policy,
                                              # max_steps=self.experiment_config.hparams[
                                              #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                # f1 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                f1 = self.simple_func(policy.theta)
                ncall = ncall + 1
                alist = [0, 1]
                flist = [fmi, f1]
                alist,flist,nfls = self.gls(u, v, xmin, p, alist,
                                            flist, nloc, small, smaxls, stopping_actions)
                ncall = ncall + nfls
                argmin = np.argmin(flist)
                fmi = min(flist)
                xmin = [xmin[jnx] + alist[argmin]*p[jnx] for jnx in range(len(xmin))] 
                xmin = np.asarray([max(u[jnx],min(xmin[jnx],v[jnx])) for jnx in range(len(xmin))])
                if stop[0] > 0  and  stop[0] < 1:
                    flag = chrelerr(fmi,stop)# 
                elif stop[0] == 0:
                    flag = chvtr(fmi,stop[1])# 
                if not flag:
                    return xmin,fmi,ncall,flag,nsweep,nsweepbest
                
                gain = f - fmi
                if fold == fmi:
                    r = 0 
                elif fold == fpred:
                    r = 0.5
                else:
                    r = (fold-fmi)/(fold-fpred);
                if fmi < fold:
                    fac = abs(1-1/r)# 
                    eps0 = max(eps,min(fac*eps0,0.001))# 
                else:
                    eps0 = 0.001# 
            else:
                gain = f - fmi
                if (not gain):
                    eps0 = 0.001
                    fac = np.Inf
                    r = 0 
                #end not gain
            #end if norm p
            ind = [inx for inx in range(len(u)) if (u[inx] < xmin[inx]  and  xmin[inx] < v[inx])]
            b = np.dot(np.abs(g).T,[max(abs(xmin[inx]),abs(xold[inx])) for inx in range(len(xmin))])
        #end while
        return xmin,fmi,ncall,flag,nsweep,nsweepbest

    def basket1(self, x, f, xmin, fmi, xbest, fbest, stop, nbasket, nsweep, nsweepbest, stopping_actions):
        """ """
        loc = 1
        flag = 1
        ncall = 0
        if not nbasket:
            return xbest, fbest, xmin, fmi, loc, flag, ncall, nsweep, nsweepbest

        dist = np.zeros(nbasket + 1)
        for k in range(len(dist)):
            dist[k] = np.linalg.norm(np.subtract(x, xmin[k]))

        dist1 = np.sort(dist)
        ind = np.argsort(dist)

        for k in range(nbasket + 1):
            i = ind[k]
            p = xmin[i] - x
            y1 = x + 1 / 3 * p
            policy = self.get_policy(y1, L=stopping_actions)
            # avg_metrics = self.eval_theta(policy=policy,
            #                               max_steps=self.experiment_config.hparams[
            #                                   agents_constants.COMMON.MAX_ENV_STEPS].value)
            # f1 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
            f1 = self.simple_func(policy.theta)
            ncall = ncall + 1
            if f1 <= max(fmi[i], f):
                y2 = x + 2 / 3 * p
                policy = self.get_policy(y2, L=stopping_actions)
                # avg_metrics = self.eval_theta(policy=policy,
                                              # max_steps=self.experiment_config.hparams[
                                              #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                # f2 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                f2 = self.simple_func(policy.theta)
                ncall = ncall + 1
                if f2 <= max(f1, fmi[i]):
                    if f < min(min(f1, f2), fmi[i]):
                        fmi[i] = f
                        xmin[i] = copy.deepcopy(x)
                        if fmi[i] < fbest:
                            fbest = copy.deepcopy(fmi[i])
                            xbest = copy.deepcopy(xmin[i])
                            nsweepbest = nsweep
                            if stop[0] > 0 and stop[0] < 1:
                                flag = chrelerr(fbest, stop)
                            elif stop[0] == 0:
                                flag = chvtr(fbest, stop[1])
                            if not flag:
                                return (
                                    xbest,
                                    fbest,
                                    xmin,
                                    fmi,
                                    loc,
                                    flag,
                                    ncall,
                                    nsweep,
                                    nsweepbest,
                                )
                        # end fmi[i] < fbest:
                        loc = 0
                        break
                    elif f1 < min(min(f, f2), fmi[i]):
                        fmi[i] = f1
                        xmin[i] = copy.deepcopy(y1)
                        if fmi[i] < fbest:
                            fbest = copy.deepcopy(fmi[i])
                            xbest = copy.deepcopy(xmin[i])
                            nsweepbest = copy.deepcopy(nsweep)

                            if stop[0] > 0 and stop[0] < 1:
                                flag = chrelerr(fbest, stop)
                            elif stop[0] == 0:
                                flag = chvtr(fbest, stop[1])
                            if not flag:
                                return (
                                    xbest,
                                    fbest,
                                    xmin,
                                    fmi,
                                    loc,
                                    flag,
                                    ncall,
                                    nsweep,
                                    nsweepbest,
                                )
                        # end fmi[i] < fbest: elif
                        loc = 0
                        break
                    elif f2 < min(min(f, f1), fmi[i]):
                        fmi[i] = f2
                        xmin[i] = copy.deepcopy(y2)
                        if fmi[i] < fbest:
                            fbest = copy.deepcopy(fmi[i])
                            xbest = copy.deepcopy(xmin[i])
                            nsweepbest = nsweep
                            if stop[0] > 0 and stop[0] < 1:
                                flag = chrelerr(fbest, stop)
                            elif stop[0] == 0:
                                flag = chvtr(fbest, stop[1])
                            if not flag:
                                return (
                                    xbest,
                                    fbest,
                                    xmin,
                                    fmi,
                                    loc,
                                    flag,
                                    ncall,
                                    nsweep,
                                    nsweepbest,
                                )
                        # end elseif
                        loc = 0
                        break
                    else:
                        loc = 0
                        break
        return xbest, fbest, xmin, fmi, loc, flag, ncall, nsweep, nsweepbest

    def csearch(self, x, f, u, v, hess, stopping_actions):
        n = len(x)
        x = [min(v[i],max(x[i],u[i])) for i in range(len(x))]

        nfcsearch = 0
        smaxls = 6
        small = 0.1
        nloc = 1  
        hess = np.ones((n,n))
        xmin = copy.deepcopy(x)  
        fmi = copy.deepcopy(f) 
        xminnew = copy.deepcopy(xmin)
        fminew = copy.deepcopy(fmi)
        g = np.zeros(n)
        ind0 = []
        
        x1 =  np.zeros(n)
        x2 =  np.zeros(n)
        G = np.zeros((n,n))
        eps = 2.220446049250313e-16
        
        for i in range(n):
            p = np.zeros(n)
            p[i] = 1
            if xmin[i]:
                delta = eps**(1/3)*abs(xmin[i])
            else:
                delta = eps**(1/3)
            linesearch = True  
            if xmin[i] <= u[i]:
                policy = self.get_policy(xmin+delta*p, L=stopping_actions)
                # avg_metrics = self.eval_theta(policy=policy,
                                            # max_steps=self.experiment_config.hparams[
                                            #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                # f1 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                f1 = self.simple_func(policy.theta)
                nfcsearch = nfcsearch + 1
                if f1 >= fmi:
                    policy = self.get_policy(xmin+2*delta*p, L=stopping_actions)
                    # avg_metrics = self.eval_theta(policy=policy,
                                                # max_steps=self.experiment_config.hparams[
                                                #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                    # f2 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                    f2 = self.simple_func(policy.theta)
                    fcsearch = nfcsearch + 1
                    x1[i] = xmin[i] + delta
                    x2[i] = xmin[i] + 2*delta
                    if f2 >= fmi:
                        xminnew[i] = xmin[i]
                        fminew = fmi
                    else:
                        xminnew[i] = x2[i]
                        fminew = copy.deepcopy(f2)
                    linesearch = False  
                else:
                    alist = [0, delta] 
                    flist = [fmi, f1]
            elif xmin[i] >= v[i]:
                policy = self.get_policy(xmin-delta*p, L=stopping_actions)
                # avg_metrics = self.eval_theta(policy=policy,
                                            # max_steps=self.experiment_config.hparams[
                                            #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                # f1 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                f1 = self.simple_func(policy.theta)
                nfcsearch = nfcsearch + 1 
                if f1 >= fmi:
                    policy = self.get_policy(xmin-2*delta*p, L=stopping_actions)
                    # avg_metrics = self.eval_theta(policy=policy,
                                                # max_steps=self.experiment_config.hparams[
                                                #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                    # f2 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                    f2 = self.simple_func(policy.theta)
                    nfcsearch = nfcsearch + 1 
                    x1[i] = xmin[i] - delta
                    x2[i] = xmin[i] - 2*delta 
                    if f2 >= fmi:
                        xminnew[i] = xmin[i]
                        fminew = fmi
                    else:
                        xminnew[i] = x2[i]
                        fminew = f2
                    linesearch = False
                else:
                    alist = [0, -delta]#  
                    flist = [fmi, f1]#
            else:
                alist = 0
                flist = fmi
            
            if linesearch:
                #print('line search:',xmin)
                alist,flist,nfls = self.gls(u, v, xmin, p, alist, flist, nloc,
                                            small, smaxls, stopping_actions)
                nfcsearch = nfcsearch + nfls #print('test gls') #print(alist,flist)
                
                j = np.argmin(flist)
                fminew = min(flist)   #print(fminew,j)
                
                if fminew == fmi:
                    j = [inx for inx in range(len(alist)) if not alist[inx]][0]

                ind = [inx for inx in range(len(alist)) if abs(alist[inx]-alist[j])<delta]   #print(ind)
                ind1 = [inx for inx in range(len(ind)) if ind[inx] == j]  #print(ind1)
                
                for inx in ind1:
                    del  ind[inx] 

                for inx in ind:
                    del  alist[inx]
                    del  flist[inx]
                
                j = np.argmin(flist)
                fminew = min(flist) 
                xminnew[i] = xmin[i] + alist[j] #print('test csearch')  #print(flist,j,fminew, xminnew)
                if i == 0 or not alist[j]:#
                    if j == 0: 
                        x1[i] = xmin[i] + alist[1]  
                        f1 = flist[1]  
                        x2[i] = xmin[i] + alist[2]  
                        f2 = flist[2]  
                    elif j == len(alist)-1:
                        x1[i] = xmin[i] + alist[j-1]
                        f1 = flist[j-1]
                        x2[i] = xmin[i] + alist[j-2]  
                        f2 = flist[j-2]
                    else:
                        #print(xmin[i],alist[j-1],alist[j+1])
                        x1[i] = xmin[i] + alist[j-1]
                        f1 = flist[j-1]
                        x2[i] = xmin[i] + alist[j+1]
                        f2 = flist[j+1]
                    #end if j == 0 elsif, else    
                    xmin[i] = xminnew[i]  
                    fmi = copy.deepcopy(fminew) 
                else:
                    x1[i] = xminnew[i]
                    f1 = copy.deepcopy(fminew)
                    if xmin[i] < x1[i] and j < len(alist)-1:
                        x2[i] = xmin[i] + alist[j+1]
                        f2 = flist[j+1]
                    elif j == 0:
                        if alist[j+1]:
                            x2[i] = xmin[i] + alist[j+1]  
                            f2 = flist[j+1]
                        else:
                            x2[i] = xmin[i] + alist[j+2]
                            f2 = flist[j+2]
                    elif alist[j-1]:
                        x2[i] = xmin[i] + alist[j-1]
                        f2 = flist[j-1]
                    else:
                        x2[i] = xmin[i] + alist[j-2]
                        f2 = flist[j-2]
            #end if linesearch
            g[i], G[i,i] = polint1([xmin[i], x1[i], x2[i]],[fmi, f1, f2])                 
            x = copy.deepcopy(xmin)
            k1 = -1
            if f1 <= f2:
                x[i] = x1[i]
            else:
                x[i] = x2[i]
            for k in range(i):
                if hess[i,k]:
                    q1 = fmi + g[k]*(x1[k]-xmin[k])+0.5*G[k,k]*(x1[k]-xmin[k])**2  
                    q2 = fmi + g[k]*(x2[k]-xmin[k])+0.5*G[k,k]*(x2[k]-xmin[k])**2  
                    if q1 <= q2:
                        x[k] = x1[k]
                    else:
                        x[k] = x2[k]
                    policy = self.get_policy(x, L=stopping_actions)
                    # avg_metrics = self.eval_theta(policy=policy,
                                                # max_steps=self.experiment_config.hparams[
                                                #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                    # f12 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                    f12 = self.simple_func(policy.theta)
                    print(f12)
                    nfcsearch = nfcsearch + 1
                    G[i,k] = hessian(i,k,x,xmin,f12,fmi,g,G)#  
                    G[k,i] = G[i,k]
                    if f12 < fminew:
                        fminew = f12 
                        xminnew = copy.deepcopy(x)
                        k1 = k
                    x[k] = xmin[k]
                else:
                    G[i,k] = 0
                    G[k,i] = 0
            # end for k in i        
            if fminew <= fmi:
                if x1[i] == xminnew[i]:
                    x1[i] = xmin[i]
                elif x2[i] == xminnew[i]:
                    x2[i] = xmin[i]
                if k1 > -1:
                    if xminnew[k1] == x1[k1]:
                        x1[k1] = xmin[k1]
                    elif xminnew[k1] == x2[k1]:
                        x2[k1] = xmin[k1]
                #print('xmins',k1,xminnew[i],xmin[i])  
                for k in range(i+1):
                    g[k] = g[k] + G[i,k]*(xminnew[i] - xmin[i])
                    if k1 > -1:
                        g[k] = g[k] + G[k1,k]*(xminnew[k1] - xmin[k1])
                #end for k in i
            xmin = copy.deepcopy(xminnew)
            fmi = copy.deepcopy(fminew) 
            #print('check',i)  print(g[i], G[i,i])
        #end for i
        return xmin,fmi,g,G,nfcsearch

    def gls(self,xl,xu,x,p,alist,flist,nloc, small, smax, stopping_actions, prt=2):
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
        xl,xu,x,p,amin,amax,scale = lsrange(xl,xu,x,p,prt,bend)	# find range of useful alp 
        #plt.plot(aa,ff)
        alist,flist,alp,alp1,alp2,falp = self.lsinit(x,p,alist,flist,amin,amax,scale, stopping_actions) # 2 points needed for lspar and lsnew
        alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
        nf = s - sinit	# number of function values used
        
        
        #print(alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s)
        while s < min(5,smax):
            if nloc == 1:
                #print('interpol')
                # parabolic interpolation step
                alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,alp,fac = self.lspar(nloc,small,sinit,short,x,p,alist,flist,
                                                                                                         amin,amax,alp,abest,fbest,fmed,up,down,
                                                                                                         monotone,minima,nmin,unitlen,s, stopping_actions) 
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
                alist,flist,alp,fac = self.lsnew(nloc,small,sinit,short,x,p,s,alist,flist,
                                                 amin,amax,alp,abest,fmed,unitlen, stopping_actions) 
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
                alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,good,saturated = self.lsquart(nloc, small, sinit,
                                                                                                                                short, x, p, alist,
                                                                                                                                flist, amin, amax, alp,
                                                                                                                                abest, fbest, fmed, up,
                                                                                                                                down, monotone, minima,
                                                                                                                                nmin, unitlen, s, saturated,
                                                                                                                                stopping_actions)
            # check descent condition 		
            alist,flist,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = self.lsdescent(x, p, alist, flist, alp,
                                                                                                     abest, fbest, fmed, up, down,
                                                                                                     monotone, minima, nmin, unitlen,
                                                                                                     s, stopping_actions)
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
            alist,flist,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = self.lsdescent(x, p, alist, flist, alp, abest,
                                                                                                     fbest, fmed, up, down, monotone,
                                                                                                     minima, nmin, unitlen, s, stopping_actions)
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
                alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = self.lssep(nloc,small,
                                                                                                               sinit,short,x,
                                                                                                               p,alist,flist,amin,
                                                                                                               amax,alp,abest,fbest,
                                                                                                               fmed,up,down,monotone,
                                                                                                               minima,nmin,unitlen,s,
                                                                                                               stopping_actions)
            # local interpolation step
            alist,flist,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,saturated = self.lslocal(nloc, small, sinit, short,
                                                                                                             x, p, alist, flist, amin, amax,
                                                                                                             alp, abest, fbest, fmed, up,
                                                                                                             down, monotone, minima, nmin,
                                                                                                             unitlen, s, saturated, stopping_actions)
            if nmin>nminold:
                saturated=0
        #end while
        #get output information
        nf = s-sinit # number of function values used
        #print(nf)
        return alist,flist,nf #  search list,function values,number of fucntion evaluation

    def lsinit(self, x, p, alist, flist, amin, amax, scale, stopping_actions):
        '''
            Line search intilization
        '''
        alp = 0
        alp1 = 0
        alp2 = 0
        falp = 0
        
        if len(alist) == 0:
            # evaluate at absolutely smallest point
            alp = 0
            if amin > 0:
                alp = amin
            if amax < 0:
                alp = amax
            # new function value
            # falp = feval(func,x+alp*p)
            policy = self.get_policy(x+alp*p, L=stopping_actions)
            # avg_metrics = self.eval_theta(policy=policy,
                                          # max_steps=self.experiment_config.hparams[
                                          #     agents_constants.COMMON.MAX_ENV_STEPS].value)
            # falp = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
            falp = self.simple_func(policy.theta)
            alist.append(alp)
            flist.append(falp)
        elif len(alist) == 1:
            # evaluate at absolutely smallest point
            alp = 0
            if amin > 0:
                alp = amin
            if amax < 0:
                alp = amax
            if alist[0] != alp:
                # new function value
                policy = self.get_policy(x+alp*p, L=stopping_actions)
                # avg_metrics = self.eval_theta(policy=policy,
                                            # max_steps=self.experiment_config.hparams[
                                            #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                # falp = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                falp = self.simple_func(policy.theta)
                alist.append(alp)
                flist.append(falp)
                
        # alist and f lis are set -  now comut min and max
        aamin = min(alist) # scalr
        aamax = max(alist) # scalr
        if amin > aamin  or  amax < aamax:
            #print(alist, amin, amax)
            sys.exit('GLS Error: non-admissible step in alist')
        
        # establish correct scale
        if aamax - aamin <= scale:
            alp1 = max(amin,min(-scale,amax)) # scalr
            alp2 = max(amin,min(+scale,amax)) # scalr
            alp = np.Inf # scalr
            
            if aamin - alp1 >= alp2 - aamax:
                alp = alp1
            if alp2 - aamax >= aamin - alp1:
                alp = alp2
            if alp < aamin  or  alp > aamax:
                # new function value
                policy = self.get_policy(x+alp*p, L=stopping_actions)
                # avg_metrics = self.eval_theta(policy=policy,
                                              # max_steps=self.experiment_config.hparams[
                                              #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                # falp = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                falp = self.simple_func(policy.theta)
                alist.append(alp)
                flist.append(falp)
        if len(alist)==1:
            #print(scale,aamin,aamax,alp1,alp2)
            sys.exit('GLS Error: lsinit bug: no second point found')
        
        return alist,flist,alp,alp1,alp2,falp

    def triple(self, x, f, x1, x2, u, v, hess, G, stopping_actions, setG = False):
        nf = 0
        n = len(x)
        g = np.zeros(n)    
        nargin = 10
        if setG:
            nargin = 9
            G =  np.zeros((n,n))
        
        ind = [i for i in range(n) if (u[i] < x[i] and x[i] < v[i])]
        ind1 = [i for i in range(n) if (x[i] <= u[i] or x[i] >= v[i])]
        
        for j in range(len(ind1)):
            g[ind1[j]] = 0
            for k in range(n):
                G[ind1[j],k] = 0
                G[k,ind1[j]] = 0
                
        if len(ind) <= 1:
            xtrip = copy.deepcopy(x)
            ftrip = copy.deepcopy(f)
            if len(ind) != 0:  
                for i in ind:
                    g[i] = 1
                    G[i,i] = 1
            return xtrip,ftrip,g,G,x1,x2,nf    
        # end if
        
        if setG:
            #print('reset G')
            G =  np.zeros((n,n))
        
        xtrip = copy.deepcopy(x)
        ftrip = copy.deepcopy(f)
        xtripnew = copy.deepcopy(x)
        ftripnew = copy.deepcopy(f)
        
        for j in range(len(ind)):
            i = ind[j]
            x = copy.deepcopy(xtrip)
            f = copy.deepcopy(ftrip)
            
            x[i] = x1[i]

            policy = self.get_policy(x, L=stopping_actions)
            # avg_metrics = # self.eval_theta(policy=policy,
                                          # max_steps=self.experiment_config.hparams[
                                          #    agents_constants.COMMON.MAX_ENV_STEPS].value)
            # f1 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
            f1 = self.simple_func(policy.theta)
            x[i] = x2[i]
            policy = self.get_policy(x, L=stopping_actions)
            # avg_metrics = self.eval_theta(policy=policy,
                                          # max_steps=self.experiment_config.hparams[
                                          #     agents_constants.COMMON.MAX_ENV_STEPS].value)
            # f2 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
            f2 = self.simple_func(policy.theta)
            nf = nf + 2
            g[i], G[i,i] = polint1([xtrip[i],x1[i],x2[i]],[f,f1,f2])
            if f1 <= f2:
                if f1 < ftrip:
                    ftripnew = copy.deepcopy(f1)
                    xtripnew[i] = x1[i]
            else:
                if f2 < ftrip:
                    ftripnew = copy.deepcopy(f2)
                    xtripnew[i] = x2[i]
            
            if nargin < 10:
                k1 = -1 
                if f1 <= f2:
                    x[i] = x1[i]
                else:
                    x[i] = x2[i]
                
                for k in range(i):
                    if hess[i,k]:
                        if xtrip[k] > u[k] and xtrip[k] < v[k] and (len([m for m in range(len(ind)) if ind[m] == k]) != 0):
                            q1 = ftrip + g[k]*(x1[k]-xtrip[k])+0.5*G[k,k]*(x1[k]-xtrip[k])**2
                            q2 = ftrip + g[k]*(x2[k]-xtrip[k])+0.5*G[k,k]*(x2[k]-xtrip[k])**2
                            if q1 <= q2:
                                x[k] = x1[k]
                            else:
                                x[k] = x2[k]
                            policy = self.get_policy(x, L=stopping_actions)
                            # avg_metrics = self.eval_theta(policy=policy,
                                                          # max_steps=self.experiment_config.hparams[
                                                          #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                            # f12 = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                            f12 = self.simple_func(policy.theta)
                            nf = nf + 1
                            G[i,k] = hessian(i,k,x,xtrip,f12,ftrip,g,G)
                            #print(G[i,k])
                            G[k,i] = G[i,k]
                            if f12 < ftripnew:
                                ftripnew = copy.deepcopy(f12)
                                xtripnew = copy.deepcopy(x)
                                k1 = k
                            x[k] = xtrip[k] 
                        #end if xtrip
                    else:
                        G[i,k] = 0
                        G[k,i] = 0
                    #end hess[i,k]
                #end for k in i-1
            #end narg
            if ftripnew < ftrip:
                if x1[i] == xtripnew[i]:
                    x1[i] = xtrip[i] 
                else: 
                    x2[i] = xtrip[i] 
                if nargin < 10 and k1 > -1:
                    if xtripnew[k1] == x1[k1]:
                        x1[k1] = xtrip[k1]
                    else:
                        x2[k1] = xtrip[k1] 
                for k in range(i+1):
                    if (len([m for m in range(len(ind)) if ind[m] == k]) != 0):
                        g[k] = g[k] + G[i,k]*(xtripnew[i] - xtrip[i])
                        if nargin < 10 and k1 > -1:
                            g[k] = g[k] + G(k1,k)*(xtripnew[k1] - xtrip[k1])
                    #end if empty
                xtrip = copy.deepcopy(xtripnew)
                ftrip = copy.deepcopy(ftripnew)
            # end ftripnew
        #en for j in ind
        return xtrip,ftrip,g,G,x1,x2,nf

    def lspar(self, nloc,small,sinit,short,x,p,alist,flist,amin,amax,alp,abest,fbest,
              fmed,up,down,monotone,minima,nmin,unitlen,s, stopping_actions):
        cont = 1	# continue?
        fac = short
        if s < 3:
            alist,flist,alp,fac = self.lsnew(nloc,small,sinit,short,x,p,s,
                                        alist,flist,amin,amax,alp,
                                        abest,fmed,unitlen, stopping_actions) 
            cont=0 #
        
        #print('cond:',cont)
        if cont:
            # select three points for parabolic interpolation
            fmin = min(flist) # unused
            i = np.argmin(flist)
            if i <= 1: # first two
                ind = [j for j in range(3)]
                ii = copy.deepcopy(i)
            elif i >= s-2: # last two
                ind = [j for j in range(s-2-1,s)]
                ii = i - (s-1) + 2 # corrections for index
            else:
                ind = [j for j in range(ii-1,i+1)]
                ii = 2 - 1 # -1 for index
                
            # in natural order
            aa = [alist[j] for j in ind]
            # the local minimum is at ff(ii)
            ff = [flist[j] for j in ind]	
            
            # get divided differences 
            f12 = (ff[1]- ff[0])/(aa[1]-aa[0])
            f23 = (ff[2]- ff[1])/(aa[2]-aa[1])
            f123 = (f23 - f12)/(aa[2]-aa[0])
            
            # handle concave case
            if not (f123 > 0):
                alist,flist,alp,fac = self.lsnew(nloc,small,sinit,short,x,p,s,alist,
                                                 flist,amin,amax,alp,abest,fmed,unitlen,
                                                 stopping_actions)
                #alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
                cont = 0
        
        if cont:
            # parabolic minimizer
            alp0 = 0.5*(aa[1]+aa[2] - f23/f123)
            alp = lsguard(alp0,alist,amax,amin,small)
            alptol = small*(aa[2]-aa[0])
            
            
            # handle infinities and close predictor
            if f123 == np.Inf or min([abs(i-alp) for i in alist]) <= alptol:
                # split best interval
                #if prt>1, disp('split best interval'); #
                if ii == 0 or ( ii == 1 and (aa[1] >= 0.5*(aa[0] + aa[2]))):
                    alp = 0.5*(aa[0]+aa[1])
                else:
                    alp = 0.5*(aa[1]+aa[2])
            else:
                np_print = alp0
                #print('parabolic predictor: alp0 = ',alp0)
                
            # add point to the list     # new function value
            # falp = feval(func,x+alp*p)
            policy = self.get_policy(x+alp*p, L=stopping_actions)
            # avg_metrics = self.eval_theta(policy=policy,
                                        # max_steps=self.experiment_config.hparams[
                                        #     agents_constants.COMMON.MAX_ENV_STEPS].value)
            # falp = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
            falp = self.simple_func(policy.theta)
            alist.append(alp)
            flist.append(falp)
            #if prt>1, abest_anew_xnew=[alist(i),alp,(x+alp*p)']; #     
            #alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
            
        alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
        return alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,alp,fac

    def lsnew(self,nloc,small,sinit,short,x,p,s,alist,flist,amin,amax,alp,abest,fmed,unitlen, stopping_actions):  

        if alist[0] <= amin: 
            # leftmost point already at boundary
            leftok = 0		
        elif flist[0] >= max(fmed,flist[1]):
            # bad leftmost point
            # extrapolate only if no scale known or global search	
            leftok = (sinit == 1 or nloc > 1 )
        else:
            # good interior leftmost point
            leftok = 1
            
        if alist[s-1] >= amax:
            # rightmost point already at boundary
            rightok = 0
        elif flist[s-1] >= max(fmed, flist[s-2]):
            # bad rightmost point
            # extrapolate only if no scale known or global search	
            rightok = (sinit ==1 or nloc > 1 )
        else:
            # good interior rightmost point
            rightok = 1
        
        # number of intervals used in extrapolation step
        if sinit == 1:
            step = s-1
        else:
            step = 1
        
        fac = short
        # do the step
        if leftok and ( flist[0] < flist[s-1] or (not rightok) ):
            #if prt>1, disp('extrapolate at left end point'); #
            extra = 1 
            al = alist[0] - (alist[0+step] - alist[0])/small
            alp = max(amin, al)
        elif rightok:
            #if prt>1, disp('extrapolate at right end point'); #
            extra=1;
            au = alist[s-1] + (alist[s-1] - alist[s-1-step])/small
            alp = min(au,amax)
        else:
            # no extrapolation
            #if prt>1, disp('split relatively widest interval'); #
            extra = 0
            lenth = [i-j for i,j in zip(alist[1:s],alist[0:s-1])]
            dist = [max(i,j,k) for i,j,k in zip([i-abest for i in alist[1:s]], [abest-i for i in alist[0:s-1]], (unitlen*np.ones(s-1)).tolist())]
            wid = [lenth[i]/dist[i] for i in range(len(lenth))]
            i = np.argmax(wid)
            wid = max(wid)
            alp, fac = lssplit(i,alist,flist,short)
        
        # new function value
        # falp = feval(func,x+alp*p)
        policy = self.get_policy(x+alp*p, L=stopping_actions)
        # avg_metrics = self.eval_theta(policy=policy,
                                      # max_steps=self.experiment_config.hparams[
                                      #     agents_constants.COMMON.MAX_ENV_STEPS].value)
        # falp = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
        falp = self.simple_func(policy.theta)
        alist.append(alp)
        flist.append(falp)

        
        return alist,flist,alp,fac

    def lsdescent(self, x,p,alist,flist,alp,abest,fbest,
                  fmed,up,down,monotone,minima,nmin,
                  unitlen,s, stopping_actions):
        cont = max([i==0 for i in alist]) # condition for continue
        
        if cont: 
            fbest = min(flist)
            i = np.argmin(flist)
            if alist[i] < 0:
                if alist[i] >= 4*alist[i+1]:
                    cont=0 # 
            elif alist[i]>0: 
                if alist[i]<4*alist[i-1]:
                    cont=0 # 
            else: 
                if i==0:# lowest point
                    fbest = flist[1]
                elif i==s-1:# last point
                    fbest = flist[s-2]
                else:
                    fbest = min(flist[i-1],flist[i+1])
                    
        if cont:
            # force local descent step
            if alist[i] !=0:
                alp = alist[i]/3 
            elif i==s-1:
                alp = alist[s-2]/3
            elif i==0:
                alp=alist[1]/3 
            else:
                # split wider adjacent interval
                if alist[i+1] - alist[i]>alist[i]-alist[i-1]:
                    alp = alist[i+1]/3 
                else:
                    alp=alist[i-1]/3 
            # new function value
            # falp = feval(func,x+alp*p)
            policy = self.get_policy(x+alp*p, L=stopping_actions)
            # avg_metrics = self.eval_theta(policy=policy,
                                        # max_steps=self.experiment_config.hparams[
                                        #     agents_constants.COMMON.MAX_ENV_STEPS].value)
            # falp = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
            falp = self.simple_func(policy.theta)
            alist.append(alp)
            flist.append(falp)
            alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
            #print('descent check: new point at ',alp)  #
        return alist,flist,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s
    def lsquart(self, nloc, small, sinit, short, x, p, alist,
                flist, amin, amax, alp, abest, fbest, fmed, up, down,
                monotone, minima, nmin, unitlen, s, saturated, stopping_actions): 
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
            alist,flist,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,saturated = self.lslocal(nloc,small,sinit,
                                                                                                             short,x,p,alist,
                                                                                                             flist,amin,amax,alp,
                                                                                                             abest,fbest,fmed,up,
                                                                                                             down,monotone,minima,nmin,
                                                                                                             unitlen,s,saturated, stopping_actions)
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
                # falp = feval(func,x+alp*p)#
                policy = self.get_policy(x+alp*p, L=stopping_actions)
                # avg_metrics = self.eval_theta(policy=policy,
                                            # max_steps=self.experiment_config.hparams[
                                            #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                # falp = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                falp = self.simple_func(policy.theta)
                alist.append(alp)
                flist.append(falp)
                alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
        
        return alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s,good,saturated
    
    def lssep(self, nloc, small, sinit, short, x, p, alist, flist,
              amin, amax, alp, abest, fbest, fmed, up, down, monotone, minima,
              nmin, unitlen, s, stopping_actions):
        '''
        '''
        nsep=0
        while nsep < nmin:
            # find intervals where the monotonicity behavior of both
            # adjacent intervals is opposite
            down = [i<j for i,j in zip(flist[1:s], flist[0:s-1])]
            sep = [i and j and k  for i,j,k in zip([True, True] + down, [False] + up + [False], down + [True, True])]
            temp_sep = [i and j and k  for i,j,k in zip([True,True] + up, [False] + down + [False], up + [True,True])]
            sep = [i or j for i,j in zip(sep,temp_sep)] 
            
            ind= [i for i in range(len(sep)) if sep[i]]
            
            if len(ind) == 0:
                #print('break ind is empty',ind)
                break
            
            # i = 0  will naver come here 
            aa = [0.5*(alist[i] + alist[i-1]) for i in ind]	# interval midpoints
            if len(aa) > nloc:
                # select nloc best interval midpoints
                ff = [min(flist[i],flist[j]) for i,j in ind]
                ind = np.argsort(ff)
                ff.sort()
                aa = [aa[ind[i]] for i in range(0,nloc)]
                
            for alp in aa:
                #print(alp)
                #if prt>2, disp(['separate minimizer at ',num2str(alp)]); #
                # new function value
                policy = self.get_policy(x+alp*p, L=stopping_actions)
                # avg_metrics = self.eval_theta(policy=policy,
                                            # max_steps=self.experiment_config.hparams[
                                            #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                # falp = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                falp = self.simple_func(policy.theta)
                alist.append(alp)
                flist.append(falp)
                nsep = nsep+1
                if nsep >= nmin:
                    break
            #end for
            alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
        #end while
        
        # instead of unnecessary separation, add some global points
        for times in range(0,nmin-nsep):
            print(times)
            # extrapolation or split
            #print('extrapolation')
            alist,flist, alp, fac = lsnew(func, nloc,small,sinit,short,x,p,s,alist,flist,amin,amax,alp,abest,fmed,unitlen)
            alist,flist,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s = lssort(alist,flist)
            
        return alist,flist,amin,amax,alp,abest,fbest,fmed,up,down,monotone,minima,nmin,unitlen,s

    def lslocal(self, nloc, small, sinit, short, x, p, alist, flist,
                amin, amax, alp, abest, fbest, fmed, up, down, monotone,
                minima, nmin, unitlen, s, saturated, stopping_actions):
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
                policy = self.get_policy(x+alp*p, L=stopping_actions)
                # avg_metrics = self.eval_theta(policy=policy,
                                            # max_steps=self.experiment_config.hparams[
                                            #     agents_constants.COMMON.MAX_ENV_STEPS].value)
                # falp = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                falp = self.simple_func(policy.theta)#
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

