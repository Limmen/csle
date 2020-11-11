from typing import List
import gym
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_id import ActionId

class ActionConfig:
    """
    Configuration of the action space
    """
    def __init__(self, num_indices : int, actions: List[Action] = None, nmap_action_ids : List[int] = None,
                 network_service_action_ids: List[int] = None,
                 shell_action_ids : List[int] = None, nikto_action_ids : List[int] = None,
                 masscan_action_ids : List[int] = None):
        """
        Class constructor

        :param num_indices: max num machine indexes allowed
        :param actions: list of actions in the action space
        :param nmap_action_ids: list of ids of the actions that are NMAP actions
        :param network_service_action_ids: list of ids of the actions that are network service actions
        :param shell_action_ids: list of ids of the actions that are shell actions
        :param nikto_action_ids: list of ids of the actions that are Nikto actions
        :param masscan_action_ids: list of ids of the actions that are Masscan actions
        """
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


    @staticmethod
    def dict_brute_same_user_ids():
        return [
        ActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST,
        ActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST,
        ActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST,
        ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST,
        ActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST,
        ActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST,
        ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST,
        ActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST,
        ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST,
        ActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET,
        ActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET,
        ActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET,
        ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET,
        ActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET,
        ActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET,
        ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET,
        ActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET,
        ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET
        ]