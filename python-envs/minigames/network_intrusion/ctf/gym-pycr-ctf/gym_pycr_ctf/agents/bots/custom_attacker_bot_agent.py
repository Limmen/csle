"""
A bot attack agent for the pycr-ctf environment that acts according to a custom pre-defined policy
"""
import time
import numpy as np
#from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
#from gym_pycr_ctf.envs.derived_envs.level4.generated_simulation.pycr_ctf_level4_gensim_env import PyCRCTFLevel4GeneratedSim5Env
#from gym_pycr_ctf.envs.derived_envs.level4.emulation.pycr_ctf_level4_emulation_env import PyCRCTFLevel4Emulation5Env
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.env_state import EnvState

class CustomAttackerBotAgent:
    """
    Class implementing an attack policy that acts according to a custom pre-defined policy
    """

    def __init__(self, env_config: EnvConfig, env):
        """
        Constructor, initializes the policy

        :param env_config: the environment configuration
        :param env: the environment
        """
        self.env_config = env_config
        self.env = env
        self.num_actions = env.env_config.attacker_action_conf.num_actions
        self.actions = np.array(list(range(self.num_actions)))
        self.strategy = []
        self.strategy = [18, 18, 15, 18, 18, 18, 5, 16, 15, 18, 18, 18, 18, 1, 16, 15,
                         18, 18, 18, 18, 14, 16, 15, 18, 18, 18, 17]
        # if isinstance(self.env, PyCRCTFLevel4GeneratedSim5Env) or isinstance(self.env, PyCRCTFLevel4Emulation5Env):
        #     self.strategy = [18, 18, 15, 18, 18, 18, 5, 16, 15, 18, 18, 18, 18, 1, 16, 15,
        #                      18, 18, 18, 18, 14, 16, 15, 18, 18, 18, 17]
        # else:
        #     raise ValueError("Environment not recognized")

    def action(self, s: EnvState, agent_state) -> int:
        """
        Samples an action from the policy.

        :param s: the environment state
        :return: action_id
        """
        legal_actions = list(filter(lambda x: self.env.is_attack_action_legal(x, self.env_config, s), self.actions))
        if self.strategy[agent_state.time_step] in legal_actions:
            action = self.strategy[agent_state.time_step]
        else:
            print("action illegal")
            action = np.random.choice(legal_actions)
        # self.step += 1
        # if self.step >= len(self.strategy):
        #     self.step = 0
        #print("custom action:{}".format(action))
        return action
