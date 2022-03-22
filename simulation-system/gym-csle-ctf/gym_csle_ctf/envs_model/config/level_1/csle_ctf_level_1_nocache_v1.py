from csle_common.dao.network.network_config import NetworkConfig
from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.dao.state_representation.state_type import StateType
from gym_csle_ctf.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.dao.render.render_config import RenderConfig
from gym_csle_ctf.dao.action.attacker.attacker_action_config import AttackerActionConfig
from gym_csle_ctf.dao.action.attacker.attacker_nmap_actions import AttackerNMAPActions
from gym_csle_ctf.dao.action.attacker.attacker_network_service_actions import AttackerNetworkServiceActions
from gym_csle_ctf.dao.action.attacker.attacker_shell_actions import AttackerShellActions
from gym_csle_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_csle_ctf.envs_model.config.level_1.csle_ctf_level_1_base import CSLECTFLevel1Base
from gym_csle_ctf.dao.action.defender.defender_action_config import DefenderActionConfig
from gym_csle_ctf.dao.action.defender.defender_action_id import DefenderActionId
from gym_csle_ctf.dao.action.defender.defender_stopping_actions import DefenderStoppingActions

class CSLECTFLevel1NoCacheV1:
    """
    V1 configuration of level 1 of the CSLECTF environment.
    """

    @staticmethod
    def attacker_actions_conf(num_nodes : int, subnet_mask: str, hacker_ip: str = None) -> AttackerActionConfig:
        """
        :param num_nodes: max number of nodes to consider (whole subnetwork in most general case)
        :param subnet_mask: subnet mask of the network
        :param hacker_ip: ip of the agent
        :return: the action config
        """
        attacker_actions = []

        # Host actions
        for idx in range(num_nodes):
            attacker_actions.append(AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))

        # Subnet actions
        attacker_actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=num_nodes + 1, ip=subnet_mask,
                                                                subnet=True))
        attacker_actions.append(AttackerNMAPActions.NMAP_VULNERS(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerShellActions.FIND_FLAG(index=num_nodes + 1))
        attacker_actions.append(AttackerNetworkServiceActions.SERVICE_LOGIN(index=num_nodes + 1))
        attacker_actions.append(
            AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                                 subnet=True))
        attacker_actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                                         subnet=True))
        attacker_actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask,
                                                                         subnet=True))

        attacker_actions = sorted(attacker_actions, key=lambda x: (x.id.value, x.index))
        nmap_action_ids = [
            AttackerActionId.TCP_SYN_STEALTH_SCAN_SUBNET,
            AttackerActionId.NMAP_VULNERS_SUBNET,
            AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET
        ]
        network_service_action_ids = [AttackerActionId.NETWORK_SERVICE_LOGIN]
        shell_action_ids = [AttackerActionId.FIND_FLAG]
        nikto_action_ids = []
        masscan_action_ids = []
        stopping_action_ids = []
        attacker_action_config = AttackerActionConfig(num_indices=num_nodes + 1, actions=attacker_actions,
                                                      nmap_action_ids=nmap_action_ids,
                                                      network_service_action_ids=network_service_action_ids,
                                                      shell_action_ids=shell_action_ids,
                                                      nikto_action_ids=nikto_action_ids,
                                                      masscan_action_ids=masscan_action_ids,
                                                      stopping_action_ids=stopping_action_ids)
        return attacker_action_config

    @staticmethod
    def defender_actions_conf(num_nodes: int, subnet_mask: str) -> DefenderActionConfig:
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
    def env_config(network_conf : NetworkConfig, attacker_action_conf: AttackerActionConfig,
                   defender_action_conf: DefenderActionConfig,
                   emulation_config: EmulationConfig,
                   render_conf: RenderConfig) -> CSLEEnvConfig:
        """
        :param network_conf: the network config
        :param attacker_action_conf: the attacker action config
        :param defender_action_conf: the defender action config
        :param emulation_config: the emulation config
        :param render_conf: the render config
        :return: The complete environment config
        """
        env_config = CSLEEnvConfig(network_conf=network_conf, attacker_action_conf=attacker_action_conf,
                                   defender_action_conf=defender_action_conf,
                                   attacker_num_ports_obs=10, attacker_num_vuln_obs=10,
                                   attacker_num_sh_obs=3, num_nodes = CSLECTFLevel1Base.num_nodes(),
                                   render_config=render_conf, env_mode=EnvMode.SIMULATION,
                                   emulation_config=emulation_config,
                                   simulate_detection=True, detection_reward=10, base_detection_p=0.05,
                                   hacker_ip=CSLECTFLevel1Base.hacker_ip(), state_type=StateType.COMPACT,
                                   router_ip=CSLECTFLevel1Base.router_ip())

        env_config.ping_scan_miss_p = 0.00
        env_config.udp_port_scan_miss_p = 0.00
        env_config.syn_stealth_scan_miss_p = 0.00
        env_config.os_scan_miss_p = 0.00
        env_config.vulners_miss_p = 0.00
        env_config.num_flags = 3
        env_config.blacklist_ips = [f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}1.1", f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}1.254"]

        env_config.attacker_shell_access_found_reward_mult = 0
        env_config.attacker_new_tools_installed_reward_mult = 0
        env_config.attacker_new_backdoors_installed_reward_mult = 0
        env_config.attacker_new_login_reward_mult = 0
        env_config.attacker_machine_found_reward_mult = 0

        env_config.attacker_final_steps_reward_coefficient = 0

        env_config.attacker_flag_found_reward_mult = 3
        env_config.attacker_all_flags_reward = 0
        env_config.attacker_base_step_reward = -10
        env_config.attacker_illegal_reward_action = -10

        env_config.attacker_port_found_reward_mult = 0
        env_config.attacker_os_found_reward_mult = 0
        env_config.attacker_cve_vuln_found_reward_mult = 0
        env_config.attacker_osvdb_vuln_found_reward_mult = 0
        env_config.attacker_root_found_reward_mult = 0
        env_config.attacker_cost_coefficient = 0
        env_config.attacker_detection_reward = 0

        env_config.max_episode_length = 10000

        env_config.attacker_use_user_command_cache = False
        env_config.attacker_use_nikto_cache = False
        env_config.attacker_use_file_system_cache = False
        env_config.attacker_use_nmap_cache = False
        env_config.ids_router = False
        return env_config
