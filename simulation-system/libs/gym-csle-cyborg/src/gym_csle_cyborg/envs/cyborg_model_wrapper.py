from typing import Tuple, Dict, List, Any, Union
import numpy as np
import gym_csle_cyborg.constants.constants as env_constants
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil


class CyborgModelWrapper():

    def __init__(self, transition_model: Dict[int, Dict[int, List[int]]], observation_model: Dict[int, List[int]],
                 initial_state: int, action_id_to_type_and_host: Dict[id, Tuple[BlueAgentActionType, str]]):
        self.transition_model = transition_model
        self.observation_model = observation_model
        self.initial_state = initial_state
        self.s = initial_state
        self.hosts = ['Defender', 'Enterprise0', 'Enterprise1', 'Enterprise2', 'Op_Host0', 'Op_Host1', 'Op_Host2',
                      'Op_Server0', 'User0', 'User1', 'User2', 'User3', 'User4']
        self.host_compromised_costs = {
            "User0": 0,
            "User1": -0.1,
            "User2": -0.1,
            "User3": -0.1,
            "User4": -0.1,
            "Enterprise0": -1,
            "Enterprise1": -1,
            "Enterprise2": -1,
            "Op_Server0": -1,
            "Op_Host1": -0.1,
            "Op_Host2": -0.1,
            "Op_Host3": -0.1,
            "Defender": 0
        }
        self.action_id_to_type_and_host = action_id_to_type_and_host
        self.decoy_action_types = CyborgEnvUtil.get_decoy_action_types(scenario=2)
        self.get_decoy_actions_per_host = CyborgEnvUtil.get_decoy_actions_per_host(scenario=2)

    def step(self, action: int):
        print(f"feasible actions: {list(self.transition_model[self.s].keys())}")
        s_prime = np.random.choice(self.transition_model[self.s][action])
        # o = np.random.choice(self.observation_model[s_prime])
        o = 1
        r = self.reward_function(s_prime=s_prime, action=action)
        self.s = s_prime
        info = {}
        info[env_constants.ENV_METRICS.STATE] = s_prime
        info[env_constants.ENV_METRICS.OBSERVATION] = o
        return 0, r, False, False, info


    def reset(self, seed: Union[None, int] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None):
        self.s = self.initial_state
        o = np.random.choice(self.observation_model[self.s])
        info = {}
        info[env_constants.ENV_METRICS.STATE] = self.s
        info[env_constants.ENV_METRICS.OBSERVATION] = o
        return o, info

    def reward_function(self, s_prime, action: int):
        r = 0
        a_type, _ = self.action_id_to_type_and_host[action]
        if a_type == BlueAgentActionType.RESTORE:
            r -= -1
        state_vector = CyborgEnvUtil.state_id_to_state_vector(state_id=s_prime, observation=False)
        for i, host in enumerate(self.hosts):
            access_state = state_vector[i][2]
            if access_state > 0:
                r += self.host_compromised_costs[host]
        return r

    def set_state(self, s: int):
        self.s = s


    def get_observation_from_history(self, history: List[int]) -> List[Any]:
        obs_id = history[-1]
        obs_vector = CyborgEnvUtil.state_id_to_state_vector(state_id=obs_id, observation=True)
        obs_tensor = []
        for i in range(len(self.hosts)):
            activity = obs_vector[i][0]
            host_obs = []
            if activity == 0:
                host_obs.extend([0,0])
            elif activity == 1:
                host_obs.extend([1,0])
            elif activity == 2:
                host_obs.extend([1,1])
            access = obs_vector[i][0]
            if access == 0:
                host_obs.extend([0,0])
            elif access == 1:
                host_obs.extend([0,1])
            elif access == 2:
                host_obs.extend([1,1])
            elif access == 3:
                host_obs.extend([1,0])

            scan = obs_vector[i][1]
            if scan == 0:
                host_obs.extend([0,0])
            elif scan == 1:
                host_obs.extend([0,1])
            elif scan == 2:
                host_obs.extend([1,1])

            decoy_state = obs_vector[i][3]
            decoy_obs = [0]*len(self.decoy_action_types)
            for j in range(decoy_state):
                decoy_obs[self.decoy_action_types.index(self.get_decoy_actions_per_host[i][j])] = 1
            host_obs.extend(decoy_obs)
            obs_tensor.extend(host_obs)

        return np.array(obs_tensor)


    def is_state_terminal(self, state: int) -> bool:
        """
        Checks whether a given state is terminal or not

        :param state: the state id
        :return: True if terminal, else False
        """
        return False
