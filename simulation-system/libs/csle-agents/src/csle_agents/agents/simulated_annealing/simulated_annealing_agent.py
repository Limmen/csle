from typing import Union, List, Dict, Optional, Any
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
import csle_agents.constants.constants as agents_constants

class SimulatedAnnealingAgent(BaseAgent):
    """
    Random Search Agent
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig],
                 experiment_config: ExperimentConfig, env: Optional[BaseEnv] = None,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True):
        """
        Initializes the Random Search Agent

        :param simulation_env_config: the simulation env config
        :param emulation_env_config: the emulation env config
        :param experiment_config: the experiment config
        :param env: (optional) the gym environment to use for simulation
        :param training_job: (optional) a training job configuration
        :param save_to_metastore: boolean flag that can be set to avoid saving results and progress to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.RANDOM_SEARCH
        self.env = env
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore
        
    def J(self, theta):
        return theta**4 - 4*theta**2 + theta**3

    def sim_anneal(self):
        lower_bound = -0.7
        upper_bound = 1.5
        cooling_factor = 0.5
        theta = random.uniform(lower_bound, upper_bound) # set random initial value of theta
        J_current = self.J(theta)
        T_0 = 100
        T = T_0
        J_best = J_current
        no_attempts = 100
        for i in range(no_attempts):
            theta = random.uniform(lower_bound, upper_bound)
            J_new = self.J(theta)
            # print("theta: ", theta)
            d_J = J_new - J_current
            if d_J < 0:
                if np.exp(d_J / T) > random.random():
                    J_best = J_new
                else:
                    continue
            else:
                J_best = J_new

            J_current = J_new
            T = T * cooling_factor
        return J_best
