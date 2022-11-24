from typing import List
import gym
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_nmap_actions import EmulationAttackerNMAPActions
from csle_common.dao.emulation_action.attacker.emulation_attacker_nikto_actions import EmulationAttackerNIKTOActions
from csle_common.dao.emulation_action.attacker.emulation_attacker_masscan_actions \
    import EmulationAttackerMasscanActions
from csle_common.dao.emulation_action.attacker.emulation_attacker_network_service_actions \
    import EmulationAttackerNetworkServiceActions
from csle_common.dao.emulation_action.attacker.emulation_attacker_shell_actions import EmulationAttackerShellActions
from csle_common.dao.emulation_action.attacker.emulation_attacker_stopping_actions \
    import EmulationAttackerStoppingActions


class EmulationAttackerActionConfig:
    """
    Configuration of the action space for the attacker in the emulation
    """

    def __init__(self, num_indices: int, actions: List[EmulationAttackerAction] = None,
                 nmap_action_ids: List[EmulationAttackerActionId] = None,
                 network_service_action_ids: List[EmulationAttackerActionId] = None,
                 shell_action_ids: List[EmulationAttackerActionId] = None,
                 nikto_action_ids: List[EmulationAttackerActionId] = None,
                 masscan_action_ids: List[EmulationAttackerActionId] = None,
                 stopping_action_ids: List[EmulationAttackerActionId] = None):
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
            self.action_lookup_d_val[(action.id, action.index)] = action

        self.nmap_action_ids = nmap_action_ids
        self.network_service_action_ids = network_service_action_ids
        self.shell_action_ids = shell_action_ids
        self.nikto_action_ids = nikto_action_ids
        self.masscan_action_ids = masscan_action_ids
        self.stopping_action_ids = stopping_action_ids
        self.action_ids = (self.nmap_action_ids + self.network_service_action_ids + self.shell_action_ids
                           + self.nikto_action_ids + self.masscan_action_ids + self.stopping_action_ids)
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
            if not action.index == -1:
                if action.index is not None:
                    tag = str(action.index)
            else:
                tag = "*"
            print(str(i) + ":" + action.name + "[" + tag + "]")

    @staticmethod
    def dict_brute_same_user_ids():
        """
        :return: list of brute-force attack ids for teh attacker
        """
        return [
            EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL
        ]

    def get_continue_action_idx(self) -> int:
        """
        :return: the id of the continue-action
        """
        for i in range(len(self.actions)):
            if self.actions[i].id == EmulationAttackerActionId.CONTINUE:
                return i
        raise ValueError("No Continue Action in the action space")

    def get_action_by_id(self, action_id: EmulationAttackerActionId) -> EmulationAttackerAction:
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
    def all_actions_config(num_nodes: int, subnet_masks: List[str], hacker_ip: str) -> "EmulationAttackerActionConfig":
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
            attacker_actions.append(EmulationAttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.PING_SCAN(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.UDP_PORT_SCAN(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.TCP_CON_NON_STEALTH_SCAN(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.TCP_FIN_SCAN(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.TCP_NULL_SCAN(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.TCP_XMAS_TREE_SCAN(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.OS_DETECTION_SCAN(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.NMAP_VULNERS(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.IRC_SAME_USER_PASS_DICTIONARY(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(index=idx))
            attacker_actions.append(EmulationAttackerNIKTOActions.NIKTO_WEB_HOST_SCAN(index=idx))
            attacker_actions.append(
                EmulationAttackerMasscanActions.MASSCAN_HOST_SCAN(index=idx, host_ip=hacker_ip))
            attacker_actions.append(EmulationAttackerNMAPActions.FIREWALK(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.HTTP_ENUM(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.HTTP_GREP(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.VULSCAN(index=idx))
            attacker_actions.append(EmulationAttackerNMAPActions.FINGER(index=idx)),
            attacker_actions.append(EmulationAttackerShellActions.SAMBACRY_EXPLOIT(index=idx))
            attacker_actions.append(EmulationAttackerShellActions.SHELLSHOCK_EXPLOIT(index=idx))
            attacker_actions.append(EmulationAttackerShellActions.DVWA_SQL_INJECTION(index=idx))
            attacker_actions.append(EmulationAttackerShellActions.CVE_2015_3306_EXPLOIT(index=idx))
            attacker_actions.append(EmulationAttackerShellActions.CVE_2015_1427_EXPLOIT(index=idx))
            attacker_actions.append(EmulationAttackerShellActions.CVE_2016_10033_EXPLOIT(index=idx))
            attacker_actions.append(EmulationAttackerShellActions.CVE_2010_0426_PRIV_ESC(index=idx))
            attacker_actions.append(EmulationAttackerShellActions.CVE_2015_5602_PRIV_ESC(index=idx))

        # Subnet actions
        attacker_actions.append(
            EmulationAttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=-1, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.PING_SCAN(index=-1, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.UDP_PORT_SCAN(index=-1, ips=subnet_masks))
        attacker_actions.append(
            EmulationAttackerNMAPActions.TCP_CON_NON_STEALTH_SCAN(index=-1, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.TCP_FIN_SCAN(index=-1, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.TCP_NULL_SCAN(index=-1, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.TCP_XMAS_TREE_SCAN(index=-1, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.OS_DETECTION_SCAN(index=-1, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.NMAP_VULNERS(index=-1, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=-1,
                                                                                              ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=-1,
                                                                                           ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=-1,
                                                                                           ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(index=-1,
                                                                                                 ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.IRC_SAME_USER_PASS_DICTIONARY(index=-1,
                                                                                           ips=subnet_masks))
        attacker_actions.append(
            EmulationAttackerNMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(index=-1, ips=subnet_masks))
        attacker_actions.append(
            EmulationAttackerNMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(index=-1, ips=subnet_masks))
        attacker_actions.append(
            EmulationAttackerNMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(index=-1, ips=subnet_masks))
        attacker_actions.append(
            EmulationAttackerNMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(index=-1, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerShellActions.FIND_FLAG(index=-1))
        attacker_actions.append(EmulationAttackerNetworkServiceActions.SERVICE_LOGIN(index=-1))
        attacker_actions.append(EmulationAttackerMasscanActions.MASSCAN_HOST_SCAN(index=-1,
                                                                                  host_ip=hacker_ip, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.FIREWALK(index=-1, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.HTTP_ENUM(index=-1, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.HTTP_GREP(index=-1, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.VULSCAN(index=-1, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerNMAPActions.FINGER(index=-1, ips=subnet_masks))
        attacker_actions.append(EmulationAttackerShellActions.INSTALL_TOOLS(index=-1))
        attacker_actions.append(EmulationAttackerShellActions.SSH_BACKDOOR(index=-1))

        attacker_actions.append(EmulationAttackerStoppingActions.STOP(index=-1))
        attacker_actions.append(EmulationAttackerStoppingActions.CONTINUE(index=-1))

        attacker_actions = sorted(attacker_actions, key=lambda x: (x.id, x.index))
        nmap_action_ids = [
            EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST,
            EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_ALL,
            EmulationAttackerActionId.PING_SCAN_HOST,
            EmulationAttackerActionId.PING_SCAN_ALL,
            EmulationAttackerActionId.UDP_PORT_SCAN_HOST,
            EmulationAttackerActionId.UDP_PORT_SCAN_ALL,
            EmulationAttackerActionId.TCP_CON_NON_STEALTH_SCAN_HOST,
            EmulationAttackerActionId.TCP_CON_NON_STEALTH_SCAN_ALL,
            EmulationAttackerActionId.TCP_FIN_SCAN_HOST,
            EmulationAttackerActionId.TCP_FIN_SCAN_ALL,
            EmulationAttackerActionId.TCP_NULL_SCAN_HOST,
            EmulationAttackerActionId.TCP_NULL_SCAN_ALL,
            EmulationAttackerActionId.TCP_XMAS_TREE_SCAN_HOST,
            EmulationAttackerActionId.TCP_XMAS_TREE_SCAN_ALL,
            EmulationAttackerActionId.OS_DETECTION_SCAN_HOST,
            EmulationAttackerActionId.OS_DETECTION_SCAN_ALL,
            EmulationAttackerActionId.NMAP_VULNERS_HOST,
            EmulationAttackerActionId.NMAP_VULNERS_ALL,
            EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST,
            EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL,
            EmulationAttackerActionId.FIREWALK_HOST, EmulationAttackerActionId.FIREWALK_ALL,
            EmulationAttackerActionId.HTTP_ENUM_HOST, EmulationAttackerActionId.HTTP_ENUM_ALL,
            EmulationAttackerActionId.HTTP_GREP_HOST, EmulationAttackerActionId.HTTP_GREP_ALL,
            EmulationAttackerActionId.VULSCAN_HOST, EmulationAttackerActionId.VULSCAN_ALL,
            EmulationAttackerActionId.FINGER_HOST, EmulationAttackerActionId.FINGER_ALL
        ]
        network_service_action_ids = [EmulationAttackerActionId.NETWORK_SERVICE_LOGIN]
        shell_action_ids = [EmulationAttackerActionId.FIND_FLAG,
                            EmulationAttackerActionId.INSTALL_TOOLS,
                            EmulationAttackerActionId.SSH_BACKDOOR,
                            EmulationAttackerActionId.SAMBACRY_EXPLOIT,
                            EmulationAttackerActionId.SHELLSHOCK_EXPLOIT,
                            EmulationAttackerActionId.DVWA_SQL_INJECTION,
                            EmulationAttackerActionId.CVE_2015_3306_EXPLOIT,
                            EmulationAttackerActionId.CVE_2015_1427_EXPLOIT,
                            EmulationAttackerActionId.CVE_2016_10033_EXPLOIT,
                            EmulationAttackerActionId.CVE_2010_0426_PRIV_ESC,
                            EmulationAttackerActionId.CVE_2015_5602_PRIV_ESC
                            ]
        nikto_action_ids = [EmulationAttackerActionId.NIKTO_WEB_HOST_SCAN]
        masscan_action_ids = [EmulationAttackerActionId.MASSCAN_HOST_SCAN, EmulationAttackerActionId.MASSCAN_ALL_SCAN]
        stopping_action_ids = [EmulationAttackerActionId.STOP, EmulationAttackerActionId.CONTINUE]
        attacker_action_config = EmulationAttackerActionConfig(num_indices=num_nodes + 1, actions=attacker_actions,
                                                               nmap_action_ids=nmap_action_ids,
                                                               network_service_action_ids=network_service_action_ids,
                                                               shell_action_ids=shell_action_ids,
                                                               nikto_action_ids=nikto_action_ids,
                                                               masscan_action_ids=masscan_action_ids,
                                                               stopping_action_ids=stopping_action_ids)
        return attacker_action_config
