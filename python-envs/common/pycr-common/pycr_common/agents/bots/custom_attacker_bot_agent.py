"""
A bot attack agent for the pycr-ctf environment that acts according to a custom pre-defined policy
"""
from typing import List, Tuple
import numpy as np
from pycr_common.dao.network.base_env_config import BaseEnvConfig


class CustomAttackerBotAgent:
    """
    Class implementing an attack policy that acts according to a custom pre-defined policy
    """

    def __init__(self, env_config: BaseEnvConfig, env, strategy: List[int], random_start : bool = False,
                 start_p : float = 0.2, continue_action : int = 372):
        """
        Constructor, initializes the policy

        :param env_config: the environment configuration
        :param env: the environment
        :param strategy: the strategy
        :param random_start: boolean flag whether to randomize start or not
        :param start_p: Bernoulli probability of starting an intrusion at any time-step t
        """
        self.env_config = env_config
        self.env = env
        self.num_actions = env.env_config.attacker_action_conf.num_actions
        self.actions = np.array(list(range(self.num_actions)))
        self.strategy = strategy
        self.random_start = random_start
        if self.random_start:
            self.started = False
        else:
            self.started = True
        self.start_p = start_p
        self.continue_action = continue_action

    def action(self, env, filter_illegal: bool = True, step= None) -> Tuple[int, bool]:
        """
        Samples an action from the policy.

        :param env: the environment
        :param filter_illegal: whether to filter illegal actions
        :param step: the current time-step
        :return: action_id, done
        """
        done = False
        if step is None:
            step = env.env_state.attacker_obs_state.step-1

        if not self.started:
            if np.random.rand() <= self.start_p:
                self.started = True

        if self.started:

            if step < len(self.strategy):
                done = step == (len(self.strategy)-1)
                action = self.strategy[step]
            else:
                if filter_illegal:
                    legal_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state),
                                                self.actions))
                else:
                    legal_actions = self.actions
                action = np.random.choice(legal_actions)

        else:
            action = self.continue_action


        return action, done


    def reset(self) -> None:
        """
        Resets the agent state

        :return: None
        """
        if self.random_start:
            self.started = False
        else:
            self.started = True
