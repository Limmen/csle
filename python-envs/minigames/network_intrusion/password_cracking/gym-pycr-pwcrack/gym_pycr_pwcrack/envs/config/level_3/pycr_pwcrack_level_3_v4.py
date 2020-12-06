from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.network.network_config import NetworkConfig
from gym_pycr_pwcrack.dao.render.render_config import RenderConfig
from gym_pycr_pwcrack.dao.network.env_mode import EnvMode
from gym_pycr_pwcrack.dao.action.action_config import ActionConfig
from gym_pycr_pwcrack.dao.action.nmap_actions import NMAPActions
from gym_pycr_pwcrack.dao.action.network_service_actions import NetworkServiceActions
from gym_pycr_pwcrack.dao.action.shell_actions import ShellActions
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.envs.state_representation.state_type import StateType
from gym_pycr_pwcrack.envs.config.level_3.pycr_pwcrack_level_3_base import PyCrPwCrackLevel3Base
from gym_pycr_pwcrack.dao.action.nikto_actions import NIKTOActions
from gym_pycr_pwcrack.dao.action.masscan_actions import MasscanActions

class PyCrPwCrackLevel3V4:
    """
    V4 configuration of level 4 of the PyCrPwCrack environment.
    """

    @staticmethod
    def actions_conf(num_nodes: int, subnet_mask: str, hacker_ip: str) -> ActionConfig:
        """
        :param num_nodes: max number of nodes to consider (whole subnetwork in most general case)
        :param subnet_mask: subnet mask of the network
        :param hacker_ip: hacker ip
        :return: the action config
        """
        actions = []

        # Host actions
        for idx in range(num_nodes):
            actions.append(NMAPActions.TCP_SYN_STEALTH_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.PING_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.UDP_PORT_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.TCP_CON_NON_STEALTH_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.TCP_FIN_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.TCP_NULL_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.TCP_XMAS_TREE_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.OS_DETECTION_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.NMAP_VULNERS(index=idx, subnet=False))
            actions.append(NMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.IRC_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NIKTOActions.NIKTO_WEB_HOST_SCAN(index=idx))
            actions.append(MasscanActions.MASSCAN_HOST_SCAN(index=idx, subnet=False, host_ip=hacker_ip))
            actions.append(NMAPActions.FIREWALK(index=idx, subnet=False))
            actions.append(NMAPActions.HTTP_ENUM(index=idx, subnet=False))
            actions.append(NMAPActions.HTTP_GREP(index=idx, subnet=False))
            actions.append(NMAPActions.VULSCAN(index=idx, subnet=False))
            actions.append(NMAPActions.FINGER(index=idx, subnet=False))

        # Subnet actions
        actions.append(
            NMAPActions.TCP_SYN_STEALTH_SCAN(index=num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.PING_SCAN(index=num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.UDP_PORT_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(
            NMAPActions.TCP_CON_NON_STEALTH_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.TCP_FIN_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.TCP_NULL_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(
            NMAPActions.TCP_XMAS_TREE_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.OS_DETECTION_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.NMAP_VULNERS(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(
            NMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                         subnet=True))
        actions.append(NMAPActions.SSH_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                                 subnet=True))
        actions.append(NMAPActions.FTP_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                                 subnet=True))
        actions.append(
            NMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                            subnet=True))
        actions.append(NMAPActions.IRC_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                                 subnet=True))
        actions.append(NMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                                   subnet=True))
        actions.append(NMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                                   subnet=True))
        actions.append(NMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                                  subnet=True))
        actions.append(
            NMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                           subnet=True))
        actions.append(ShellActions.FIND_FLAG(index=num_nodes + 1))
        actions.append(NetworkServiceActions.SERVICE_LOGIN(index=num_nodes + 1))
        actions.append(ShellActions.INSTALL_TOOLS(index=num_nodes + 1))
        actions.append(ShellActions.SSH_BACKDOOR(index=num_nodes + 1))
        actions.append(MasscanActions.MASSCAN_HOST_SCAN(index=num_nodes + 1, subnet=True,
                                                        host_ip=hacker_ip, ip=subnet_mask))
        actions.append(NMAPActions.FIREWALK(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.HTTP_ENUM(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.HTTP_GREP(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.VULSCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.FINGER(num_nodes + 1, ip=subnet_mask, subnet=True))

        actions = sorted(actions, key=lambda x: (x.id.value, x.index))
        nmap_action_ids = [
            ActionId.TCP_SYN_STEALTH_SCAN_HOST, ActionId.TCP_SYN_STEALTH_SCAN_SUBNET,
            ActionId.PING_SCAN_HOST, ActionId.PING_SCAN_SUBNET,
            ActionId.UDP_PORT_SCAN_HOST, ActionId.UDP_PORT_SCAN_SUBNET,
            ActionId.TCP_CON_NON_STEALTH_SCAN_HOST, ActionId.TCP_CON_NON_STEALTH_SCAN_SUBNET,
            ActionId.TCP_FIN_SCAN_HOST, ActionId.TCP_FIN_SCAN_SUBNET,
            ActionId.TCP_NULL_SCAN_HOST, ActionId.TCP_NULL_SCAN_SUBNET,
            ActionId.TCP_XMAS_TREE_SCAN_HOST, ActionId.TCP_XMAS_TREE_SCAN_SUBNET,
            ActionId.OS_DETECTION_SCAN_HOST, ActionId.OS_DETECTION_SCAN_SUBNET,
            ActionId.NMAP_VULNERS_HOST, ActionId.NMAP_VULNERS_SUBNET,
            ActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST, ActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST, ActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST, ActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST, ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST, ActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST, ActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST, ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST, ActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST, ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.FIREWALK_HOST, ActionId.FIREWALK_SUBNET,
            ActionId.HTTP_ENUM_HOST, ActionId.HTTP_ENUM_SUBNET,
            ActionId.HTTP_GREP_HOST, ActionId.HTTP_GREP_SUBNET,
            ActionId.VULSCAN_HOST, ActionId.VULSCAN_SUBNET,
            ActionId.FINGER_HOST, ActionId.FINGER_SUBNET
        ]
        network_service_action_ids = [ActionId.NETWORK_SERVICE_LOGIN]
        shell_action_ids = [ActionId.FIND_FLAG, ActionId.INSTALL_TOOLS, ActionId.SSH_BACKDOOR]
        nikto_action_ids = [ActionId.NIKTO_WEB_HOST_SCAN]
        masscan_action_ids = [ActionId.MASSCAN_HOST_SCAN, ActionId.MASSCAN_SUBNET_SCAN]
        action_config = ActionConfig(num_indices=num_nodes, actions=actions,
                                     nmap_action_ids=nmap_action_ids,
                                     network_service_action_ids=network_service_action_ids,
                                     shell_action_ids=shell_action_ids, nikto_action_ids=nikto_action_ids,
                                     masscan_action_ids=masscan_action_ids)
        return action_config

    @staticmethod
    def env_config(network_conf : NetworkConfig, action_conf: ActionConfig, cluster_conf: ClusterConfig,
                   render_conf: RenderConfig) -> EnvConfig:
        """
        Generates the environment configuration

        :param network_conf: the network config
        :param action_conf: the action config
        :param cluster_conf: the cluster config
        :param render_conf: the render config
        :return: The complete environment config
        """
        env_config = EnvConfig(network_conf=network_conf, action_conf=action_conf, num_ports=10, num_vuln=10,
                               num_sh=3, num_nodes = PyCrPwCrackLevel3Base.num_nodes(),
                               render_config=render_conf, env_mode=EnvMode.CLUSTER,
                               cluster_config=cluster_conf,
                               simulate_detection=True, detection_reward=10, base_detection_p=0.05,
                               hacker_ip=PyCrPwCrackLevel3Base.hacker_ip(), state_type=StateType.ESSENTIAL,
                               router_ip=PyCrPwCrackLevel3Base.router_ip())
        env_config.ping_scan_miss_p = 0.00
        env_config.udp_port_scan_miss_p = 0.00
        env_config.syn_stealth_scan_miss_p = 0.00
        env_config.os_scan_miss_p = 0.00
        env_config.vulners_miss_p = 0.00
        env_config.num_flags = 6
        env_config.blacklist_ips = ["172.18.3.1"]

        env_config.shell_access_found_reward_mult = 1
        env_config.new_tools_installed_reward_mult = 1
        env_config.new_backdoors_installed_reward_mult = 1
        env_config.new_login_reward_mult = 1
        env_config.machine_found_reward_mult = 0

        env_config.final_steps_reward_coefficient = 0

        env_config.flag_found_reward_mult = 10
        env_config.all_flags_reward = 0
        env_config.base_step_reward = -1
        env_config.illegal_reward_action = -1

        env_config.port_found_reward_mult = 0
        env_config.os_found_reward_mult = 0
        env_config.cve_vuln_found_reward_mult = 0
        env_config.osvdb_vuln_found_reward_mult = 0
        env_config.root_found_reward_mult = 0
        env_config.cost_coefficient = 0
        env_config.detection_reward = 0

        env_config.max_episode_length = 10000
        return env_config
