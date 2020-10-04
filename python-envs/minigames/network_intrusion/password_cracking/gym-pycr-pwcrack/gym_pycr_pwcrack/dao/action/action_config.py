from typing import List
import gym
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_id import ActionId

class ActionConfig:

    def __init__(self, actions: List[Action]):
        self.actions = actions
        self.num_actions = len(self.actions)
        self.action_space = gym.spaces.Discrete(self.num_actions)
        self.action_lookup_d = {}
        for action in actions:
            self.action_lookup_d[action.id] = action

        self.nmap_action_ids = [ActionId.TCP_SYN_STEALTH_SCAN_HOST, ActionId.PING_SCAN_HOST,
                                ActionId.UDP_PORT_SCAN_HOST, ActionId.TCP_CON_NON_STEALTH_SCAN_HOST,
                                ActionId.TCP_FIN_SCAN_HOST, ActionId.TCP_NULL_SCAN_HOST,
                                ActionId.TCP_XMAS_TREE_SCAN_HOST, ActionId.OS_DETECTION_SCAN_HOST,
                                ActionId.VULSCAN_HOST, ActionId.NMAP_VULNERS_HOST,
                                ActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST,
                                ActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST,
                                ActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST,
                                ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST,
                                ActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST,
                                ActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST,
                                ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST,
                                ActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST,
                                ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST,
                                ActionId.TCP_SYN_STEALTH_SCAN_SUBNET,
                                ActionId.PING_SCAN_SUBNET,
                                ActionId.UDP_PORT_SCAN_SUBNET,
                                ActionId.TCP_CON_NON_STEALTH_SCAN_SUBNET,
                                ActionId.TCP_FIN_SCAN_SUBNET,
                                ActionId.TCP_NULL_SCAN_SUBNET,
                                ActionId.TCP_XMAS_TREE_SCAN_SUBNET,
                                ActionId.OS_DETECTION_SCAN_SUBNET,
                                ActionId.VULSCAN_SUBNET,
                                ActionId.NMAP_VULNERS_SUBNET,
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
        self.network_service_action_ids = [ActionId.NETWORK_SERVICE_LOGIN]
        self.shell_action_ids = [ActionId.FIND_FLAG]