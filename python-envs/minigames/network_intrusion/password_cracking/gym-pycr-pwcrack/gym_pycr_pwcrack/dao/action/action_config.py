from typing import List
import gym
from gym_pycr_pwcrack.dao.action.action import Action

class ActionConfig:

    def __init__(self, num_indices : int, actions: List[Action] = None, nmap_action_ids : List[int] = None,
                 network_service_action_ids: List[int] = None,
                 shell_action_ids : List[int] = None, nikto_action_ids : List[int] = None,
                 masscan_action_ids : List[int] = None):
        self.actions = actions
        self.num_actions = len(self.actions)
        self.num_indices = num_indices
        self.action_space = gym.spaces.Discrete(self.num_actions)
        self.action_lookup_d = {}
        self.action_lookup_d_val = {}
        for action in actions:
            self.action_lookup_d[(action.id, action.index)] = action
            self.action_lookup_d_val[(action.id.value, action.index)] = action

        self.nmap_action_ids = nmap_action_ids
        self.network_service_action_ids = network_service_action_ids
        self.shell_action_ids = shell_action_ids
        self.nikto_action_ids = nikto_action_ids
        self.masscan_action_ids = masscan_action_ids
        self.action_ids = self.nmap_action_ids + self.network_service_action_ids + self.shell_action_ids \
                          + self.nikto_action_ids + self.masscan_action_ids
        self.num_node_specific_actions = len(self.action_ids)
        self.m_action_space = gym.spaces.Discrete(self.num_node_specific_actions)
        self.ar_action_converter = {}

        # Add all (temp
        for j, a in enumerate(self.actions):
            idx2 = self.action_ids.index(a.id)
            key = (num_indices, idx2)
            self.ar_action_converter[key] = j

        # Add subnet actions
        for j, a in enumerate(self.actions):
            idx2 = self.action_ids.index(a.id)
            if a.index == self.num_indices:
                key = (num_indices, idx2)
                self.ar_action_converter[key] = j

        # Add subnet actions to all machines
        for i in range(num_indices):
            for j, a in enumerate(self.actions):
                idx2 = self.action_ids.index(a.id)
                if a.index == self.num_indices:
                    key = (i, idx2)
                    self.ar_action_converter[key] = j

        # Add rest of actions
        for i, a in enumerate(self.actions):
            if a.index != self.num_indices:
                idx2 = self.action_ids.index(a.id)
                key = (a.index, idx2)
                self.ar_action_converter[key] = i

    def print_actions(self) -> None:
        """
        Utility function for printing the list of actions

        :return: None
        """
        print("Actions:")
        for i, action in enumerate(self.actions):
            tag = "-"
            if not action.subnet:
                if action.index is not None:
                    tag = str(action.index)
            else:
                tag = "*"
            print(str(i) + ":" + action.name + "[" + tag + "] c:" + str(action.cost))