from typing import List
import gym
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.action.attacker.attacker_action_id import AttackerActionId
from csle_common.dao.action.attacker.attacker_nmap_actions import AttackerNMAPActions
from csle_common.dao.action.attacker.attacker_nikto_actions import AttackerNIKTOActions
from csle_common.dao.action.attacker.attacker_masscan_actions import AttackerMasscanActions
from csle_common.dao.action.attacker.attacker_network_service_actions import AttackerNetworkServiceActions
from csle_common.dao.action.attacker.attacker_shell_actions import AttackerShellActions
from csle_common.dao.action.attacker.attacker_stopping_actions import AttackerStoppingActions


class AttackerActionConfig:
    """
    Configuration of the action space for the attacker
    """

    def __init__(self, num_indices: int, actions: List[AttackerAction] = None,
                 nmap_action_ids: List[AttackerActionId] = None,
                 network_service_action_ids: List[AttackerActionId] = None,
                 shell_action_ids: List[AttackerActionId] = None, nikto_action_ids: List[AttackerActionId] = None,
                 masscan_action_ids: List[AttackerActionId] = None,
                 stopping_action_ids: List[AttackerActionId] = None):
        """
        Class constructor

        :param num_indices: max num machine indexes allowed
        :param actions: list of actions in the action space
        :param nmap_action_ids: list of ids of the actions that are NMAP actions
        :param network_service_action_ids: list of ids of the actions that are network service actions
        :param shell_action_ids: list of ids of the actions that are shell actions
        :param nikto_action_ids: list of ids of the actions that are Nikto actions
        :param masscan_action_ids: list of ids of the actions that are Masscan actions
        :param stopping_action_ids: List of ids of the actions that are actions related to optimal stopping
        """
        self.num_actions = len(actions)
        self.actions = actions
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
        self.stopping_action_ids = stopping_action_ids
        self.action_ids = self.nmap_action_ids + self.network_service_action_ids + self.shell_action_ids \
                          + self.nikto_action_ids + self.masscan_action_ids + self.stopping_action_ids
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
        print("Attacker Actions:")
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
        """
        :return: list of brute-force attack ids for teh attacker
        """
        return [
            AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET
        ]

    def get_continue_action_idx(self) -> int:
        """
        :return: the id of the continue-action
        """
        for i in range(len(self.actions)):
            if self.actions[i].id == AttackerActionId.CONTINUE:
                return i
        raise ValueError("No Continue Action in the action space")

    def get_action_by_id(self, action_id: AttackerActionId) -> AttackerAction:
        """
        Gets the action of a given id

        :param action_id: the action id
        :return: the action of the id
        """
        for a in self.actions:
            if a.id == action_id:
                return a
        raise ValueError("action id not found: {}".format(action_id))

    @staticmethod
    def all_actions_config(num_nodes: int, subnet_masks: List[str], hacker_ip: str) -> "AttackerActionConfig":
        """
        Gets the default action config for a given environment, which includes all actions

        :param num_nodes: the number of nodes in the environment
        :param subnet_masks: the subnet masks of the environment
        :param hacker_ip: the hacker ip
        :return:
        """
        attacker_actions = []

        # Host actions
        for idx in range(num_nodes):
            attacker_actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.PING_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.UDP_PORT_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.TCP_CON_NON_STEALTH_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.TCP_FIN_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.TCP_NULL_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.TCP_XMAS_TREE_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.OS_DETECTION_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.NMAP_VULNERS(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.IRC_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNIKTOActions.NIKTO_WEB_HOST_SCAN(index=idx))
            attacker_actions.append(
                AttackerMasscanActions.MASSCAN_HOST_SCAN(index=idx, subnet=False, host_ip=hacker_ip))
            attacker_actions.append(AttackerNMAPActions.FIREWALK(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.HTTP_ENUM(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.HTTP_GREP(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.VULSCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.FINGER(index=idx, subnet=False))

        # Subnet actions
        attacker_actions.append(
            AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.PING_SCAN(index=num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.UDP_PORT_SCAN(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(
            AttackerNMAPActions.TCP_CON_NON_STEALTH_SCAN(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.TCP_FIN_SCAN(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.TCP_NULL_SCAN(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.TCP_XMAS_TREE_SCAN(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.OS_DETECTION_SCAN(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.NMAP_VULNERS(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(num_nodes + 1,
                                                                                     ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(num_nodes + 1,
                                                                                  ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(num_nodes + 1,
                                                                                  ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(num_nodes + 1,
                                                                                        ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.IRC_SAME_USER_PASS_DICTIONARY(num_nodes + 1,
                                                                                  ips=subnet_masks, subnet=True))
        attacker_actions.append(
            AttackerNMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(
            AttackerNMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(
            AttackerNMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(
            AttackerNMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerShellActions.FIND_FLAG(index=num_nodes + 1))
        attacker_actions.append(AttackerNetworkServiceActions.SERVICE_LOGIN(index=num_nodes + 1))
        attacker_actions.append(AttackerMasscanActions.MASSCAN_HOST_SCAN(index=num_nodes + 1, subnet=True,
                                                                         host_ip=hacker_ip, ips=subnet_masks))
        attacker_actions.append(AttackerNMAPActions.FIREWALK(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.HTTP_ENUM(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.HTTP_GREP(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.VULSCAN(num_nodes + 1, ips=subnet_masks, subnet=True))
        attacker_actions.append(AttackerNMAPActions.FINGER(num_nodes + 1, ips=subnet_masks, subnet=True))

        attacker_actions.append(AttackerStoppingActions.STOP(index=num_nodes + 1))
        attacker_actions.append(AttackerStoppingActions.CONTINUE(index=num_nodes + 1))

        attacker_actions = sorted(attacker_actions, key=lambda x: (x.id.value, x.index))
        nmap_action_ids = [
            AttackerActionId.TCP_SYN_STEALTH_SCAN_HOST, AttackerActionId.TCP_SYN_STEALTH_SCAN_SUBNET,
            AttackerActionId.PING_SCAN_HOST, AttackerActionId.PING_SCAN_SUBNET,
            AttackerActionId.UDP_PORT_SCAN_HOST, AttackerActionId.UDP_PORT_SCAN_SUBNET,
            AttackerActionId.TCP_CON_NON_STEALTH_SCAN_HOST, AttackerActionId.TCP_CON_NON_STEALTH_SCAN_SUBNET,
            AttackerActionId.TCP_FIN_SCAN_HOST, AttackerActionId.TCP_FIN_SCAN_SUBNET,
            AttackerActionId.TCP_NULL_SCAN_HOST, AttackerActionId.TCP_NULL_SCAN_SUBNET,
            AttackerActionId.TCP_XMAS_TREE_SCAN_HOST, AttackerActionId.TCP_XMAS_TREE_SCAN_SUBNET,
            AttackerActionId.OS_DETECTION_SCAN_HOST, AttackerActionId.OS_DETECTION_SCAN_SUBNET,
            AttackerActionId.NMAP_VULNERS_HOST, AttackerActionId.NMAP_VULNERS_SUBNET,
            AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST,
            AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.FIREWALK_HOST, AttackerActionId.FIREWALK_SUBNET,
            AttackerActionId.HTTP_ENUM_HOST, AttackerActionId.HTTP_ENUM_SUBNET,
            AttackerActionId.HTTP_GREP_HOST, AttackerActionId.HTTP_GREP_SUBNET,
            AttackerActionId.VULSCAN_HOST, AttackerActionId.VULSCAN_SUBNET,
            AttackerActionId.FINGER_HOST, AttackerActionId.FINGER_SUBNET
        ]
        network_service_action_ids = [AttackerActionId.NETWORK_SERVICE_LOGIN]
        shell_action_ids = [AttackerActionId.FIND_FLAG]
        nikto_action_ids = [AttackerActionId.NIKTO_WEB_HOST_SCAN]
        masscan_action_ids = [AttackerActionId.MASSCAN_HOST_SCAN, AttackerActionId.MASSCAN_SUBNET_SCAN]
        stopping_action_ids = [AttackerActionId.STOP, AttackerActionId.CONTINUE]
        attacker_action_config = AttackerActionConfig(num_indices=num_nodes + 1, actions=attacker_actions,
                                                      nmap_action_ids=nmap_action_ids,
                                                      network_service_action_ids=network_service_action_ids,
                                                      shell_action_ids=shell_action_ids,
                                                      nikto_action_ids=nikto_action_ids,
                                                      masscan_action_ids=masscan_action_ids,
                                                      stopping_action_ids=stopping_action_ids)
        return attacker_action_config
