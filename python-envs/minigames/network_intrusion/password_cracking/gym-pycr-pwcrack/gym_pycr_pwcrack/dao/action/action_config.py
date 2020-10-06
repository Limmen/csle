from typing import List
import gym
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_id import ActionId

class ActionConfig:

    def __init__(self, actions: List[Action], nmap_action_ids : List[int], network_service_action_ids: List[int],
                 shell_action_ids : List[int]):
        self.actions = actions
        self.num_actions = len(self.actions)
        self.action_space = gym.spaces.Discrete(self.num_actions)
        self.action_lookup_d = {}
        self.action_lookup_d_val = {}
        for action in actions:
            self.action_lookup_d[action.id] = action
            self.action_lookup_d_val[action.id.value] = action

        self.nmap_action_ids = nmap_action_ids
        self.network_service_action_ids = network_service_action_ids
        self.shell_action_ids = shell_action_ids
        self.action_ids = self.nmap_action_ids + self.network_service_action_ids + self.shell_action_ids
        self.num_node_specific_actions = len(self.action_ids)
        self.m_action_space = gym.spaces.Discrete(self.num_node_specific_actions)
        self.ar_action_converter = {}
        print("action 8:{}".format(self.action_ids[8]))
        for i, a in enumerate(self.actions):
            idx2 = self.action_ids.index(a.id)
            key = (a.index, idx2)
            self.ar_action_converter[key] = i