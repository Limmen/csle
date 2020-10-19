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

class PyCrPwCrackSimpleV1:
    """
    V1 configuration of level 1 of the PyCrPwCrack environment.
    """

    @staticmethod
    def actions_conf(network_conf : NetworkConfig) -> ActionConfig:
        """
        :param network_conf: the network config
        :return: the action config
        """
        actions = []

        # Host actions
        for idx in range(len(network_conf.nodes)):
            actions.append(NMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NetworkServiceActions.SERVICE_LOGIN(index=idx))

        # Subnet actions
        actions.append(NMAPActions.TCP_SYN_STEALTH_SCAN(index=len(network_conf.nodes), ip=network_conf.subnet_mask,
                                                        subnet=True))
        actions.append(NMAPActions.UDP_PORT_SCAN(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True))
        actions.append(NMAPActions.OS_DETECTION_SCAN(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True))
        actions.append(NMAPActions.NMAP_VULNERS(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True))
        actions.append(ShellActions.FIND_FLAG(index=len(network_conf.nodes)))

        actions = sorted(actions, key=lambda x: (x.id.value, x.index))
        nmap_action_ids = [
            ActionId.TCP_SYN_STEALTH_SCAN_SUBNET,
            ActionId.UDP_PORT_SCAN_SUBNET,
            ActionId.OS_DETECTION_SCAN_SUBNET,
            ActionId.NMAP_VULNERS_SUBNET,
            ActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST,
            ActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST,
            ActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST
        ]
        network_service_action_ids = [ActionId.NETWORK_SERVICE_LOGIN]
        shell_action_ids = [ActionId.FIND_FLAG]
        nikto_action_ids = []
        masscan_action_ids = []
        action_config = ActionConfig(num_indices=len(network_conf.nodes), actions=actions, nmap_action_ids=nmap_action_ids,
                                     network_service_action_ids=network_service_action_ids,
                                     shell_action_ids=shell_action_ids, nikto_action_ids=nikto_action_ids,
                                     masscan_action_ids=masscan_action_ids)
        return action_config

    @staticmethod
    def env_config(network_conf : NetworkConfig, action_conf: ActionConfig, cluster_conf: ClusterConfig,
                   render_conf: RenderConfig) -> EnvConfig:
        """
        :param network_conf: the network config
        :param action_conf: the action config
        :param cluster_conf: the cluster config
        :param render_conf: the render config
        :return: The complete environment config
        """
        env_config = EnvConfig(network_conf=network_conf, action_conf=action_conf, num_ports=10, num_vuln=10,
                               num_sh=3, render_config=render_conf, env_mode=EnvMode.SIMULATION,
                               cluster_config=cluster_conf,
                               simulate_detection=True, detection_reward=10, base_detection_p=0.05,
                               hacker_ip="172.18.1.191", state_type=StateType.COMPACT)
        env_config.ping_scan_miss_p = 0.02
        env_config.udp_port_scan_miss_p = 0.07
        env_config.syn_stealth_scan_miss_p = 0.04
        env_config.os_scan_miss_p = 0.08
        env_config.vulners_miss_p = 0.09
        env_config.num_flags = 3
        env_config.blacklist_ips = ["172.18.1.1"]
        return env_config
