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

"""
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
        assert experiment_config.agent_type == AgentType.PARTICLE_SWARM
        self.env = env
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore
    #%%----------------------------------------------------------------------------
    fcn = 'myfun' # gpr, bra, cam, hm3, s10, sh5, sh7, hm6, 'myfun' 

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
    def MCS(self, exp_result, seed: int, random_seeds: List[int], training_job: TrainingJobConfig):
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
