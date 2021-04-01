"""
A bot attack agent for the pycr-ctf environment that acts randomly
"""
import time
import numpy as np
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.env_state import EnvState

class RandomAttackerBotAgent:
    """
    Class implementing an attack policy that acts randomly
    """

    def __init__(self, env_config: EnvConfig, env: PyCRCTFEnv = None):
        """
        Constructor, initializes the policy

        :param env_config: the environment configuration
        :param env: the environment
        """
        self.env_config = env_config
        self.env = env
        self.num_actions = env.env_config.attacker_action_conf.num_actions
        self.actions = np.array(list(range(self.num_actions)))

    def action(self, s: EnvState) -> int:
        """
        Samples an action from the policy.

        :param s: the environment state
        :return: action_id
        """
        legal_actions = list(filter(lambda x: self.env.is_attack_action_legal(x, self.env_config, s), self.actions))
        action = np.random.choice(legal_actions)
        return action
