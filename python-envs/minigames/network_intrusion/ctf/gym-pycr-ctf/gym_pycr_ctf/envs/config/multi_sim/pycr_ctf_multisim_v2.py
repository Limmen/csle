from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.render.render_config import RenderConfig
from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.action.attacker.attacker_action_config import AttackerActionConfig
from gym_pycr_ctf.dao.action.attacker.attacker_nmap_actions import AttackerNMAPActions
from gym_pycr_ctf.dao.action.attacker.attacker_network_service_actions import AttackerNetworkServiceActions
from gym_pycr_ctf.dao.action.attacker.attacker_shell_actions import AttackerShellActions
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_pycr_ctf.dao.state_representation.state_type import StateType

class PyCrCTFMultiSimV2:
    """
    V2 configuration of random conf of the PyCrCTF environment.
    """

    @staticmethod
    def actions_conf(num_nodes: int, subnet_mask: str, hacker_ip: str = None) -> AttackerActionConfig:
        """
        :param num_nodes: max number of nodes to consider (whole subnetwork in most general case)
        :param subnet_mask: subnet mask of the network
        :param hacker_ip: ip of the agent
        :return: the action config
        """
        actions = []

        # Host actions
        for idx in range(num_nodes):
            actions.append(AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.NMAP_VULNERS(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.UDP_PORT_SCAN(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.PING_SCAN(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.OS_DETECTION_SCAN(index=idx, subnet=False))

        # Subnet actions
        actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=num_nodes + 1, ip=subnet_mask,
                                                                subnet=True))
        actions.append(AttackerNMAPActions.NMAP_VULNERS(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerShellActions.FIND_FLAG(index=num_nodes + 1))
        actions.append(AttackerNetworkServiceActions.SERVICE_LOGIN(index=num_nodes + 1))
        actions.append(AttackerShellActions.INSTALL_TOOLS(index=num_nodes + 1))
        actions.append(AttackerShellActions.SSH_BACKDOOR(index=num_nodes + 1))
        actions.append(
            AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                                 subnet=True))
        actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                                         subnet=True))
        actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                                         subnet=True))
        actions.append(AttackerNMAPActions.UDP_PORT_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.PING_SCAN(index=num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.OS_DETECTION_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))

        actions = sorted(actions, key=lambda x: (x.id.value, x.index))
        nmap_action_ids = [
            AttackerActionId.TCP_SYN_STEALTH_SCAN_HOST, AttackerActionId.TCP_SYN_STEALTH_SCAN_SUBNET,
            AttackerActionId.NMAP_VULNERS_HOST, AttackerActionId.NMAP_VULNERS_SUBNET,
            AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.UDP_PORT_SCAN_HOST, AttackerActionId.UDP_PORT_SCAN_SUBNET,
            AttackerActionId.PING_SCAN_HOST, AttackerActionId.PING_SCAN_SUBNET,
            AttackerActionId.OS_DETECTION_SCAN_HOST, AttackerActionId.OS_DETECTION_SCAN_SUBNET
        ]
        network_service_action_ids = [AttackerActionId.NETWORK_SERVICE_LOGIN]
        shell_action_ids = [AttackerActionId.FIND_FLAG, AttackerActionId.INSTALL_TOOLS, AttackerActionId.SSH_BACKDOOR]
        nikto_action_ids = []
        masscan_action_ids = []
        action_config = AttackerActionConfig(num_indices=num_nodes + 1, actions=actions, nmap_action_ids=nmap_action_ids,
                                             network_service_action_ids=network_service_action_ids,
                                             shell_action_ids=shell_action_ids, nikto_action_ids=nikto_action_ids,
                                             masscan_action_ids=masscan_action_ids)
        return action_config

    @staticmethod
    def env_config(action_conf: AttackerActionConfig, render_conf: RenderConfig,
                   emulation_config: EmulationConfig, num_nodes :int) -> EnvConfig:
        """
        Generates the environment configuration

        :param containers_config: the containers config of the generated env
        :param num_nodes: max number of nodes (defines obs space size and action space size)
        :param network_conf: the network config
        :param action_conf: the action config
        :param emulation_config: the emulation config
        :param render_conf: the render config
        :return: The complete environment config
        """
        network_conf = None
        env_config = EnvConfig(network_conf=network_conf, attacker_action_conf=action_conf, num_ports=10, num_vuln=10,
                               num_sh=3, num_nodes=num_nodes, render_config=render_conf,
                               env_mode=EnvMode.SIMULATION,
                               emulation_config=emulation_config,
                               simulate_detection=True, detection_reward=10, base_detection_p=0.05,
                               hacker_ip=None, state_type=StateType.BASE,
                               router_ip=None)
        env_config.ping_scan_miss_p = 0.00
        env_config.udp_port_scan_miss_p = 0.00
        env_config.syn_stealth_scan_miss_p = 0.00
        env_config.os_scan_miss_p = 0.00
        env_config.vulners_miss_p = 0.00

        env_config.attacker_shell_access_found_reward_mult = 0
        env_config.attacker_new_tools_installed_reward_mult = 0
        env_config.attacker_new_backdoors_installed_reward_mult = 0
        env_config.attacker_new_login_reward_mult = 0
        env_config.attacker_machine_found_reward_mult = 0

        env_config.attacker_final_steps_reward_coefficient = 0

        env_config.attacker_flag_found_reward_mult = 10
        env_config.attacker_all_flags_reward = 0
        env_config.attacker_base_step_reward = -1
        env_config.attacker_illegal_reward_action = -1

        env_config.attacker_port_found_reward_mult = 0
        env_config.attacker_os_found_reward_mult = 0
        env_config.attacker_cve_vuln_found_reward_mult = 0
        env_config.attacker_osvdb_vuln_found_reward_mult = 0
        env_config.attacker_root_found_reward_mult = 0
        env_config.attacker_cost_coefficient = 0
        env_config.attacker_detection_reward = 0

        env_config.max_episode_length = 10000
        return env_config
