"""
A general bot attack agent for the PyCR environment that acts randomly
"""
import numpy as np
from pycr_common.dao.network.base_env_config import BasePyCREnvConfig
from pycr_common.dao.network.base_env_state import BaseEnvState


class RandomAttackerBotAgent:
    """
    Class implementing an attack policy that acts randomly
    """

    def __init__(self, env_config: BasePyCREnvConfig, env):
        """
        Constructor, initializes the policy

        :param env_config: the environment configuration
        :param env: the environment
        """
        self.env_config = env_config
        self.env = env
        self.num_actions = env.env_config.attacker_action_conf.num_actions
        self.actions = np.array(list(range(self.num_actions)))

    def action(self, s: BaseEnvState) -> int:
        """
        Samples an action from the policy.

        :param s: the environment state
        :return: action_id
        """
        legal_actions = list(filter(lambda x: self.env.is_attack_action_legal(x, self.env_config, s), self.actions))
        action = np.random.choice(legal_actions)
        return action
