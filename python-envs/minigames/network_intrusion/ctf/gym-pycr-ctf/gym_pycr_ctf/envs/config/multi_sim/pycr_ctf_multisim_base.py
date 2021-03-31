from typing import List
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.render.render_config import RenderConfig
from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.action.attacker.attacker_action_config import AttackerActionConfig
from gym_pycr_ctf.dao.action.attacker.attacker_nmap_actions import AttackerNMAPActions
from gym_pycr_ctf.dao.action.attacker.attacker_nikto_actions import AttackerNIKTOActions
from gym_pycr_ctf.dao.action.attacker.attacker_masscan_actions import AttackerMasscanActions
from gym_pycr_ctf.dao.action.attacker.attacker_network_service_actions import AttackerNetworkServiceActions
from gym_pycr_ctf.dao.action.attacker.attacker_shell_actions import AttackerShellActions
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_pycr_ctf.dao.state_representation.state_type import StateType
from gym_pycr_ctf.dao.network.node import Node
from gym_pycr_ctf.dao.action.defender.defender_action_config import DefenderActionConfig
from gym_pycr_ctf.dao.action.defender.defender_action_id import DefenderActionId
from gym_pycr_ctf.dao.action.defender.defender_stopping_actions import DefenderStoppingActions

class PyCrCTFMultiSimBase:
    """
    Base configuration of multisim config of the PyCrCTF environment.
    """

    @staticmethod
    def nodes() -> List[Node]:
        return []

    @staticmethod
    def adj_matrix() -> List:
        return []

    @staticmethod
    def render_conf(num_nodes: int) -> RenderConfig:
        """
        :return: the render config
        """
        num_levels = (num_nodes // 10) + 3
        render_config = RenderConfig(num_levels=num_levels, num_nodes_per_level=10)
        return render_config

    @staticmethod
    def all_actions_conf(num_nodes: int, subnet_mask: str, hacker_ip: str) -> AttackerActionConfig:
        """
        :param num_nodes: max number of nodes to consider (whole subnetwork in most general case)
        :param subnet_mask: subnet mask of the network
        :param hacker_ip: ip of the agent
        :return: the action config
        """
        attack_actions = []

        # Host actions
        for idx in range(num_nodes):
            attack_actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.PING_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.UDP_PORT_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.TCP_CON_NON_STEALTH_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.TCP_FIN_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.TCP_NULL_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.TCP_XMAS_TREE_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.OS_DETECTION_SCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.NMAP_VULNERS(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.IRC_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attack_actions.append(AttackerNIKTOActions.NIKTO_WEB_HOST_SCAN(index=idx))
            attack_actions.append(AttackerMasscanActions.MASSCAN_HOST_SCAN(index=idx, subnet=False, host_ip = hacker_ip))
            attack_actions.append(AttackerNMAPActions.FIREWALK(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.HTTP_ENUM(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.HTTP_GREP(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.VULSCAN(index=idx, subnet=False))
            attack_actions.append(AttackerNMAPActions.FINGER(index=idx, subnet=False))

        # Subnet actions
        attack_actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.PING_SCAN(index=num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.UDP_PORT_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.TCP_CON_NON_STEALTH_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.TCP_FIN_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.TCP_NULL_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.TCP_XMAS_TREE_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.OS_DETECTION_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.NMAP_VULNERS(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.IRC_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNetworkServiceActions.SERVICE_LOGIN(index=num_nodes + 1))
        attack_actions.append(AttackerShellActions.FIND_FLAG(index=num_nodes + 1))
        attack_actions.append(AttackerMasscanActions.MASSCAN_HOST_SCAN(index=num_nodes + 1, subnet=True,
                                                                host_ip=hacker_ip, ip=subnet_mask))
        attack_actions.append(AttackerNMAPActions.FIREWALK(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.HTTP_ENUM(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.HTTP_GREP(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.VULSCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerNMAPActions.FINGER(num_nodes + 1, ip=subnet_mask, subnet=True))
        attack_actions.append(AttackerShellActions.INSTALL_TOOLS(index=num_nodes + 1))
        attack_actions.append(AttackerShellActions.SSH_BACKDOOR(index=num_nodes + 1))

        attack_actions = sorted(attack_actions, key=lambda x: (x.id.value, x.index))
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
            AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.FIREWALK_HOST, AttackerActionId.FIREWALK_SUBNET,
            AttackerActionId.HTTP_ENUM_HOST, AttackerActionId.HTTP_ENUM_SUBNET,
            AttackerActionId.HTTP_GREP_HOST, AttackerActionId.HTTP_GREP_SUBNET,
            AttackerActionId.VULSCAN_HOST, AttackerActionId.VULSCAN_SUBNET,
            AttackerActionId.FINGER_HOST, AttackerActionId.FINGER_SUBNET,
        ]
        network_service_action_ids = [AttackerActionId.NETWORK_SERVICE_LOGIN]
        shell_action_ids = [AttackerActionId.FIND_FLAG, AttackerActionId.INSTALL_TOOLS, AttackerActionId.SSH_BACKDOOR]
        nikto_action_ids = [AttackerActionId.NIKTO_WEB_HOST_SCAN]
        masscan_action_ids = [AttackerActionId.MASSCAN_HOST_SCAN, AttackerActionId.MASSCAN_SUBNET_SCAN]
        attacker_action_config = AttackerActionConfig(num_indices=num_nodes, actions=attack_actions, nmap_action_ids=nmap_action_ids,
                                             network_service_action_ids=network_service_action_ids,
                                             shell_action_ids=shell_action_ids, nikto_action_ids=nikto_action_ids,
                                             masscan_action_ids=masscan_action_ids)
        return attacker_action_config

    @staticmethod
    def defender_all_actions_conf(num_nodes: int, subnet_mask: str) -> AttackerActionConfig:
        """
        :param num_nodes: max number of nodes to consider (whole subnetwork in most general case)
        :param subnet_mask: subnet mask of the network
        :return: the action config
        """
        defender_actions = []

        # Host actions
        for idx in range(num_nodes):
            # actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=idx, subnet=False))
            pass

        # Subnet actions
        defender_actions.append(DefenderStoppingActions.STOP(index=num_nodes + 1))
        defender_actions.append(DefenderStoppingActions.CONTINUE(index=num_nodes + 1))

        defender_actions = sorted(defender_actions, key=lambda x: (x.id.value, x.index))
        stopping_action_ids = [
            DefenderActionId.STOP, DefenderActionId.CONTINUE
        ]
        defender_action_config = DefenderActionConfig(
            num_indices=num_nodes + 1, actions=defender_actions, stopping_action_ids=stopping_action_ids)
        return defender_action_config

    @staticmethod
    def env_config(attacker_action_conf: AttackerActionConfig,
                   defender_action_conf: DefenderActionConfig,
                   render_conf: RenderConfig,
                   emulation_config: EmulationConfig, num_nodes : int
                   ) -> EnvConfig:
        """
        :param containers_config: the containers config of the generated env
        :param num_nodes: max number of nodes (defines obs space size and action space size)
        :param network_conf: the network config
        :param attacker_action_conf: the attacker's action config
        :param defender_action_conf: the defender's action config
        :param emulation_config: the emulation config
        :param render_conf: the render config
        :return: The complete environment config
        """
        network_conf = None
        env_config = EnvConfig(network_conf=network_conf, attacker_action_conf=attacker_action_conf,
                               defender_action_conf=defender_action_conf,
                               attacker_num_ports_obs=10, attacker_num_vuln_obs=10,
                               attacker_num_sh_obs=3, num_nodes = num_nodes, render_config=render_conf,
                               env_mode=EnvMode.SIMULATION,
                               emulation_config=emulation_config,
                               simulate_detection=True, detection_reward=10, base_detection_p=0.05,
                               hacker_ip=None, state_type=StateType.BASE,
                               router_ip=None)
        env_config.ping_scan_miss_p = 0.0
        env_config.udp_port_scan_miss_p = 0.0
        env_config.syn_stealth_scan_miss_p = 0.0
        env_config.os_scan_miss_p = 0.0
        env_config.vulners_miss_p = 0.0
        env_config.max_episode_length = 10000
        return env_config
