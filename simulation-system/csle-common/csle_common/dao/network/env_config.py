from typing import Union
import re
import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.network.network_config import NetworkConfig
from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.dao.container_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.action_results.nmap_scan_cache import NMAPScanCache
from csle_common.dao.action_results.action_costs import ActionCosts
from csle_common.dao.action_results.filesystem_scan_cache import FileSystemScanCache
from csle_common.dao.action_results.nikto_scan_cache import NiktoScanCache
from csle_common.dao.state_representation.state_type import StateType
from csle_common.dao.action_results.user_command_cache import UserCommandCache
from csle_common.dao.action_results.action_alerts import ActionAlerts
from csle_common.dao.action.attacker.attacker_action_config import AttackerActionConfig
from csle_common.dao.action.defender.defender_action_config import DefenderActionConfig
from csle_common.dao.render.render_config import RenderConfig
from csle_common.dao.network.node_type import NodeType
from csle_common.dao.network.credential import Credential
from csle_common.dao.network.node import Node


class CSLEEnvConfig:
    """
    Class containing the complete configuration of a csle-ctf env
    """

    def __init__(self, network_conf : NetworkConfig, attacker_action_conf : AttackerActionConfig,
                 defender_action_conf: DefenderActionConfig,
                 attacker_num_ports_obs : int, attacker_num_vuln_obs : int,
                 attacker_num_sh_obs : int, num_nodes : int, hacker_ip : str, router_ip : str,
                 render_config : RenderConfig, env_mode : EnvMode = EnvMode.SIMULATION,
                 emulation_config : EmulationConfig = None, simulate_detection : bool = True,
                 detection_reward : int = 10,
                 base_detection_p : float = 0.01, manual_play : bool = False, state_type: StateType = StateType.BASE,
                 emulation_env_config : EmulationEnvConfig = None):
        """
        Initialize the config

        :param network_conf: the network config
        :param attacker_action_conf: the action config for the attacker
        :param defender_action_conf: the action config for the defender
        :param attacker_num_ports_obs: number of ports per machine in the state
        :param attacker_num_vuln_obs: number of vuln per machine to keep in state
        :param attacker_num_sh_obs: number of shell connections per machine to keep in state
        :param num_nodes: number of nodes
        :param hacker_ip: ip of the hacker
        :param router_ip: ip of the default gw for the hacker
        :param render_config: the render config
        :param env_mode: the env mode (e.g. emulation or sim)
        :param emulation_config: the emulation config
        :param simulate_detection: boolean flag whether to simulate detections or not
        :param detection_reward: reward when a detection happens
        :param base_detection_p: base detection probability for simulation
        :param manual_play: boolean flag whether manual play is used
        :param emulation_env_config: the emulation environment configuration
        """
        self.attacker_action_conf = attacker_action_conf
        self.defender_action_conf = defender_action_conf
        self.manual_play = manual_play
        self.attacker_exploration_filter_illegal = True
        self.emulation_env_config = emulation_env_config
        self.network_conf = network_conf
        self.attacker_num_ports_obs = attacker_num_ports_obs
        self.attacker_num_vuln_obs = attacker_num_vuln_obs
        self.attacker_num_sh_obs = attacker_num_sh_obs
        self.num_nodes = num_nodes
        self.env_mode = env_mode
        self.emulation_config = emulation_config
        self.render_config = render_config
        self.simulate_detection = simulate_detection
        self.attacker_detection_reward = detection_reward
        self.base_detection_p = base_detection_p
        self.detection_alerts_threshold = 100
        self.detection_prob_factor = 0.05
        self.emulate_detection = False
        self.hacker_ip = hacker_ip
        self.router_ip = router_ip

        self.ping_scan_miss_p = 0.00
        self.udp_port_scan_miss_p = 0.00
        self.syn_stealth_scan_miss_p = 0.00
        self.os_scan_miss_p = 0.00
        self.vulscan_miss_p = 0.00
        self.vulners_miss_p = 0.00
        self.telnet_dict_attack_miss_p = 0.00
        self.ssh_dict_attack_miss_p = 0.00
        self.irc_dict_attack_miss_p = 0.00
        self.mongo_dict_attack_miss_p = 0.00
        self.cassandra_dict_attack_miss_p = 0.00
        self.ftp_dict_attack_miss_p = 0.00

        self.shell_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
        self.shell_read_wait = 0.5
        self.shell_max_timeouts = 4000
        self.max_nmap_command_output_size = 10000000
        self.nmap_cache_dir = "/home/agent/"
        self.nmap_cache = []
        self.retry_timeout = 2
        self.num_retries = 2
        self.attacker_use_nmap_cache = True
        self.attacker_nmap_scan_cache = NMAPScanCache()
        self.attacker_use_nikto_cache = True
        self.attacker_nikto_scan_cache = NiktoScanCache()
        self.attacker_action_costs = ActionCosts()
        self.attacker_action_alerts = ActionAlerts()
        self.flag_lookup = self._create_flags_lookup()
        self.attacker_use_file_system_cache = True
        self.attacker_filesystem_scan_cache = FileSystemScanCache()
        self.attacker_filesystem_file_cache = []
        self.attacker_use_user_command_cache = True
        self.attacker_user_command_cache = UserCommandCache()
        self.attacker_user_command_cache_files_cache = []

        self.attacker_flag_found_reward_mult = 20
        self.attacker_port_found_reward_mult = 1
        self.attacker_os_found_reward_mult = 1
        self.attacker_cve_vuln_found_reward_mult = 1
        self.attacker_osvdb_vuln_found_reward_mult = 1
        self.attacker_machine_found_reward_mult = 1
        self.attacker_shell_access_found_reward_mult = 10
        self.attacker_root_found_reward_mult = 10
        self.attacker_new_login_reward_mult = 1
        self.attacker_new_tools_installed_reward_mult = 1
        self.attacker_new_backdoors_installed_reward_mult = 1
        self.attacker_cost_coefficient = 1
        self.attacker_alerts_coefficient = 1
        self.attacker_detection_reward = -100
        self.attacker_all_flags_reward = 500
        self.attacker_sum_costs = 1
        self.attacker_max_costs = 1
        self.attacker_sum_alerts = 1
        self.attacker_max_alerts = 1
        self.max_episode_length = 1000
        self.attacker_base_step_reward = -1
        self.attacker_illegal_reward_action = -100
        self.attacker_final_steps_reward_coefficient = 1

        self.defender_final_steps_reward_coefficient = 0
        self.defender_caught_attacker_reward = 200
        self.defender_early_stopping_reward = -100
        self.defender_service_reward = 10
        self.defender_intrusion_reward = -100

        # self.multistop_costs = [0, -6.25, -12.5, -25, -100]
        # self.multistop_costs = [-100, -25, -12.5, -6.25, 0]
        # self.multistop_costs = [-100, -25, -12.5, -6.25, 0]
        self.multistop_costs = [-100, -50, -25, -12.5, 0]


        self.defender_sum_costs = 1
        self.defender_max_costs = 1

        self.attacker_filter_illegal_actions = True
        self.checkpoint_dir = None
        self.checkpoint_freq = 1000
        self.num_flags = 0

        self.ip_to_machine_id_mapping = {}
        self.save_trajectories = False
        self.blacklist_ips = [f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}1.1"]
        self.state_type = state_type

        self.attacker_ssh_retry_find_flag = 5
        self.attacker_retry_find_users = 5
        self.attacker_ftp_retry_find_flag = 2
        self.attacker_retry_install_tools = 5
        self.attacker_exploration_policy = None
        self.attacker_max_exploration_steps = 100
        self.attacker_max_exploration_trajectories = 100

        self.load_cves_from_server = True
        self.load_services_from_server = True
        self.cache_misses = 0
        self.print_cache_details_freq = 500
        self.ids_router = False
        self.idx = 0
        self.domain_randomization = False
        self.compute_pi_star_attacker = False
        self.use_upper_bound_pi_star_attacker = False
        self.pi_star_tau_attacker = None
        self.pi_star_rew_attacker = -1
        self.pi_star_rew_list_attacker = []

        self.use_upper_bound_pi_star_defender = True
        self.pi_star_tau_defender = None
        self.pi_star_rew_defender = -100
        self.pi_star_rew_list_defender = []

        self.attacker_install_tools_sleep_seconds = 3
        self.attacker_retry_check_root = 3
        self.attacker_retry_sambacry = 4
        self.attacker_retry_shellshock = 4
        self.attacker_retry_dvwa_sql_injection = 4
        self.attacker_retry_cve_2015_3306 = 4
        self.attacker_retry_cve_2015_1427 = 4
        self.attacker_retry_cve_2016_10033 = 4
        self.attacker_retry_cve_2010_0426 = 4
        self.attacker_retry_cve_2015_5602 = 4
        self.attacker_sambacry_sleep_retry = 4
        self.attacker_shellshock_sleep_retry = 4
        self.attacker_dvwa_sql_injection_sleep_retry = 4
        self.attacker_cve_2015_3306_sleep_retry = 4
        self.attacker_cve_2015_1427_sleep_retry = 4
        self.attacker_cve_2016_10033_sleep_retry = 4
        self.attacker_cve_2010_0426_sleep_retry = 4
        self.attacker_cve_2015_5602_sleep_retry = 4
        self.attacker_continue_action_sleep = 0.001

        self.defender_update_state = False
        self.defender_ids_severity_threshold=3
        self.defender_ids_recent_threshold_seconds = 30
        self.explore_defense_states = False
        self.defender_sleep_before_state_update = 15
        self.stop_after_failed_detection = False
        self.snort_critical_baseline_threshold = 400
        self.snort_severe_baseline_threshold = 0
        self.snort_warning_baseline_threshold = 0
        self.var_log_baseline_threshold = 0
        self.step_baseline_threshold = 6

        self.normalize_alerts_max = 5
        self.normalize_costs_max = 5
        self.max_episode_length_reward = -100
        self.randomize_attacker_starting_state = False
        self.randomize_state_min_steps = 10
        self.randomize_state_max_steps = 20
        self.randomize_starting_state_policy = None
        self.randomize_state_steps_list = [0, 8, 16, 23]
        self.attacker_static_opponent : Union["CustomAttackerBotAgent", None] = None
        self.snort_baseline_simulate = False
        self.attacker_early_stopping_reward = 10
        self.use_attacker_action_stats_to_update_defender_state = False
        self.randomize_defender_starting_state = False

        self.multiple_stopping_environment = False
        self.maximum_number_of_defender_stop_actions = 1
        self.ids_enabled_stops_remaining = 3
        self.reset_users_stops_remaining = 2
        self.blacklist_ips_stops_remaining = 1
        self.attacker_prevented_stops_remaining = 0

    def get_port_forward_port(self) -> int:
        """
        :return: Gets the next port to forward
        """
        p = self.emulation_config.port_forward_next_port
        self.emulation_config.port_forward_next_port +=1
        return p

    def _create_flags_lookup(self) -> Union[dict, None]:
        """
        Creates a lookup dict of (flagpath -> FlagDTO)

        :return: returns dict of (flagpath -> FlagDTO)
        """
        if self.network_conf is not None:
            return self.network_conf.flags_lookup
        else:
            return None

    def scale_rewards_prep_attacker(self) -> None:
        """
        Utility function for scaling costs for the attacker to be used in the reward function

        :return: None
        """
        sum_costs = sum(list(map(lambda x: x.cost, self.attacker_action_conf.actions)))
        max_costs = max(max(list(map(lambda x: x.cost, self.attacker_action_conf.actions))), 1)
        self.attacker_sum_costs = sum_costs
        self.attacker_max_costs = max_costs
        if self.ids_router:
            sum_alerts = sum(list(map(lambda x: x.alerts[0], self.attacker_action_conf.actions)))
            max_alerts = max(max(list(map(lambda x: x.alerts[0], self.attacker_action_conf.actions))), 1)
            self.attacker_sum_alerts = sum_alerts
            self.attacker_max_alerts = max_alerts


    def scale_rewards_prep_defender(self) -> None:
        """
        Utility function for scaling costs for the defender to be used in the reward function

        :return:  None
        """
        sum_costs = sum(list(map(lambda x: x.cost, self.defender_action_conf.actions)))
        max_costs = max(max(list(map(lambda x: x.cost, self.defender_action_conf.actions))), 1)
        self.defender_sum_costs = sum_costs
        self.defender_max_costs = max_costs


    def copy(self) -> "CSLEEnvConfig":
        """
        :return: a copy of the environment configuration
        """
        env_config = CSLEEnvConfig(
            network_conf=self.network_conf, attacker_action_conf=self.attacker_action_conf,
            defender_action_conf=self.defender_action_conf,
            attacker_num_ports_obs=self.attacker_num_ports_obs,
            attacker_num_vuln_obs=self.attacker_num_vuln_obs, attacker_num_sh_obs=self.attacker_num_sh_obs, num_nodes=self.num_nodes, hacker_ip=self.hacker_ip,
            router_ip=self.router_ip, render_config=self.render_config, env_mode=self.env_mode,
            emulation_config=self.emulation_config, simulate_detection=self.simulate_detection,
            detection_reward=self.attacker_detection_reward, base_detection_p=self.base_detection_p, manual_play=self.manual_play,
            state_type=self.state_type)

        env_config.ping_scan_miss_p = self.ping_scan_miss_p
        env_config.udp_port_scan_miss_p = self.udp_port_scan_miss_p
        env_config.syn_stealth_scan_miss_p = self.syn_stealth_scan_miss_p
        env_config.os_scan_miss_p = self.os_scan_miss_p
        env_config.vulscan_miss_p = self.vulscan_miss_p
        env_config.vulners_miss_p = self.vulners_miss_p
        env_config.telnet_dict_attack_miss_p = self.telnet_dict_attack_miss_p
        env_config.ssh_dict_attack_miss_p = self.ssh_dict_attack_miss_p
        env_config.irc_dict_attack_miss_p = self.irc_dict_attack_miss_p
        env_config.mongo_dict_attack_miss_p = self.mongo_dict_attack_miss_p
        env_config.cassandra_dict_attack_miss_p = self.cassandra_dict_attack_miss_p
        env_config.ftp_dict_attack_miss_p = self.ftp_dict_attack_miss_p
        env_config.shell_escape = self.shell_escape
        env_config.shell_read_wait = self.shell_read_wait
        env_config.shell_max_timeouts = self.shell_max_timeouts
        env_config.max_nmap_command_output_size = self.max_nmap_command_output_size
        env_config.nmap_cache_dir = self.nmap_cache_dir
        env_config.nmap_cache = self.nmap_cache
        env_config.retry_timeout = self.retry_timeout
        env_config.num_retries = self.num_retries
        env_config.attacker_use_nmap_cache = self.attacker_use_nmap_cache
        env_config.attacker_nmap_scan_cache = self.attacker_nmap_scan_cache
        env_config.attacker_use_nikto_cache = self.attacker_use_nikto_cache
        env_config.attacker_action_costs = self.attacker_action_costs
        env_config.attacker_action_alerts = self.attacker_action_alerts
        env_config.flag_lookup = self.flag_lookup
        env_config.attacker_use_file_system_cache = self.attacker_use_file_system_cache
        env_config.attacker_filesystem_scan_cache = self.attacker_filesystem_scan_cache
        env_config.attacker_filesystem_file_cache = self.attacker_filesystem_file_cache
        env_config.attacker_use_user_command_cache = self.attacker_use_user_command_cache
        env_config.attacker_user_command_cache = self.attacker_user_command_cache
        env_config.attacker_user_command_cache_files_cache = self.attacker_user_command_cache_files_cache
        env_config.attacker_flag_found_reward_mult = self.attacker_flag_found_reward_mult
        env_config.attacker_port_found_reward_mult = self.attacker_port_found_reward_mult
        env_config.attacker_os_found_reward_mult = self.attacker_os_found_reward_mult
        env_config.attacker_cve_vuln_found_reward_mult = self.attacker_cve_vuln_found_reward_mult
        env_config.attacker_osvdb_vuln_found_reward_mult = self.attacker_osvdb_vuln_found_reward_mult
        env_config.attacker_machine_found_reward_mult = self.attacker_machine_found_reward_mult
        env_config.attacker_shell_access_found_reward_mult = self.attacker_shell_access_found_reward_mult
        env_config.attacker_root_found_reward_mult = self.attacker_root_found_reward_mult
        env_config.attacker_new_login_reward_mult = self.attacker_new_login_reward_mult
        env_config.attacker_new_tools_installed_reward_mult = self.attacker_new_tools_installed_reward_mult
        env_config.attacker_new_backdoors_installed_reward_mult = self.attacker_new_backdoors_installed_reward_mult
        env_config.attacker_cost_coefficient = self.attacker_cost_coefficient
        env_config.attacker_alerts_coefficient = self.attacker_alerts_coefficient
        env_config.attacker_detection_reward = self.attacker_detection_reward
        env_config.attacker_all_flags_reward = self.attacker_all_flags_reward
        env_config.attacker_sum_costs = self.attacker_sum_costs
        env_config.attacker_max_costs = self.attacker_max_costs
        env_config.attacker_sum_alerts = self.attacker_sum_alerts
        env_config.attacker_max_alerts = self.attacker_max_alerts
        env_config.max_episode_length = self.max_episode_length
        env_config.attacker_base_step_reward = self.attacker_base_step_reward
        env_config.attacker_illegal_reward_action = self.attacker_illegal_reward_action
        env_config.attacker_final_steps_reward_coefficient = self.attacker_final_steps_reward_coefficient
        env_config.attacker_filter_illegal_actions = self.attacker_filter_illegal_actions
        env_config.checkpoint_dir = self.checkpoint_dir
        env_config.checkpoint_freq = self.checkpoint_freq
        env_config.num_flags = self.num_flags
        env_config.ip_to_machine_id_mapping = self.ip_to_machine_id_mapping
        env_config.save_trajectories = self.save_trajectories
        env_config.blacklist_ips = self.blacklist_ips
        env_config.manual_play = self.manual_play
        env_config.state_type = self.state_type
        env_config.attacker_ssh_retry_find_flag = self.attacker_ssh_retry_find_flag
        env_config.attacker_retry_find_users = self.attacker_retry_find_users
        env_config.attacker_ftp_retry_find_flag = self.attacker_ftp_retry_find_flag
        env_config.attacker_retry_install_tools = self.attacker_retry_install_tools
        env_config.attacker_exploration_policy = self.attacker_exploration_policy
        env_config.attacker_max_exploration_steps = self.attacker_max_exploration_steps
        env_config.attacker_max_exploration_trajectories = self.attacker_max_exploration_trajectories
        env_config.load_cves_from_server = self.load_cves_from_server
        env_config.cache_misses = self.cache_misses
        env_config.print_cache_details_freq = self.print_cache_details_freq
        env_config.ids_router = self.ids_router
        env_config.idx = self.idx
        env_config.attacker_exploration_filter_illegal = self.attacker_exploration_policy
        env_config.domain_randomization = self.domain_randomization
        env_config.compute_pi_star_attacker = self.compute_pi_star_attacker
        env_config.use_upper_bound_pi_star_attacker = self.use_upper_bound_pi_star_attacker
        env_config.pi_star_rew_attacker = self.pi_star_rew_attacker
        env_config.pi_star_rew_list_attacker = self.pi_star_rew_list_attacker
        env_config.attacker_install_tools_sleep_seconds = self.attacker_install_tools_sleep_seconds
        env_config.attacker_retry_check_root = self.attacker_retry_check_root
        env_config.attacker_retry_sambacry = self.attacker_retry_sambacry
        env_config.attacker_retry_shellshock = self.attacker_retry_shellshock
        env_config.attacker_retry_dvwa_sql_injection = self.attacker_retry_dvwa_sql_injection
        env_config.attacker_retry_cve_2015_3306 = self.attacker_retry_cve_2015_3306
        env_config.attacker_retry_cve_2015_1427 = self.attacker_retry_cve_2015_1427
        env_config.attacker_retry_cve_2016_10033 = self.attacker_retry_cve_2016_10033
        env_config.attacker_retry_cve_2010_0426 = self.attacker_retry_cve_2010_0426
        env_config.attacker_retry_cve_2015_5602 = self.attacker_retry_cve_2015_5602
        env_config.attacker_sambacry_sleep_retry = self.attacker_sambacry_sleep_retry
        env_config.attacker_shellshock_sleep_retry = self.attacker_shellshock_sleep_retry
        env_config.attacker_dvwa_sql_injection_sleep_retry = self.attacker_dvwa_sql_injection_sleep_retry
        env_config.attacker_cve_2015_3306_sleep_retry = self.attacker_cve_2015_3306_sleep_retry
        env_config.attacker_cve_2015_1427_sleep_retry = self.attacker_cve_2015_1427_sleep_retry
        env_config.attacker_cve_2016_10033_sleep_retry = self.attacker_cve_2016_10033_sleep_retry
        env_config.attacker_cve_2010_0426_sleep_retry = self.attacker_cve_2010_0426_sleep_retry
        env_config.attacker_cve_2015_5602_sleep_retry = self.attacker_cve_2015_5602_sleep_retry
        env_config.defender_ids_severity_threshold = self.defender_ids_severity_threshold
        env_config.defender_ids_recent_threshold_seconds = self.defender_ids_recent_threshold_seconds
        env_config.defender_update_state = self.defender_update_state
        env_config.defender_intrusion_reward = self.defender_intrusion_reward
        env_config.explore_defense_states = self.explore_defense_states
        env_config.defender_sleep_before_state_update = self.defender_sleep_before_state_update
        env_config.snort_severe_baseline_threshold = self.snort_severe_baseline_threshold
        env_config.snort_warning_baseline_threshold = self.snort_warning_baseline_threshold
        env_config.snort_critical_baseline_threshold = self.snort_critical_baseline_threshold
        env_config.var_log_baseline_threshold = self.var_log_baseline_threshold
        env_config.emulate_detection = self.emulate_detection
        env_config.normalize_alerts_max = self.normalize_alerts_max
        env_config.normalize_costs_max = self.normalize_costs_max
        env_config.detection_prob_factor = self.detection_prob_factor
        env_config.randomize_attacker_starting_state = self.randomize_attacker_starting_state
        env_config.randomize_state_min_steps = self.randomize_state_min_steps
        env_config.randomize_state_max_steps = self.randomize_state_max_steps
        env_config.snort_baseline_simulate = self.snort_baseline_simulate
        env_config.attacker_early_stopping_reward = self.attacker_early_stopping_reward
        env_config.use_attacker_action_stats_to_update_defender_state = self.use_attacker_action_stats_to_update_defender_state
        env_config.multiple_stopping_environment = self.multiple_stopping_environment
        env_config.maximum_number_of_defender_stop_actions = self.maximum_number_of_defender_stop_actions
        env_config.ids_enabled_stops_remaining = self.ids_enabled_stops_remaining
        env_config.blacklist_ips_stops_remaining = self.blacklist_ips_stops_remaining
        env_config.reset_users_stops_remaining = self.reset_users_stops_remaining
        env_config.attacker_prevented_stops_remaining = self.attacker_prevented_stops_remaining
        env_config.multistop_costs = self.multistop_costs
        return env_config

    @staticmethod
    def from_emulation_config(
            emulation_env_config: EmulationEnvConfig, attacker_num_ports_obs: int =5,
            attacker_num_vuln_obs: int = 5,
            attacker_num_sh_obs : int = 5, simulate_detection=False, detection_reward=10,
            base_detection_p : float = 0.01,
            manual_play : bool = False, state_type: StateType = StateType.BASE) -> "CSLEEnvConfig":
        """
        Creates an environment configuration from an emulation environment configuration

        :param emulation_env_config: the emulation environment configuration
        :param attacker_num_ports_obs: the number of ports to store in the attacker observation
        :param attacker_num_vuln_obs: the number of vulnerabilities to store in the attacker observation
        :param attacker_num_sh_obs: the number of compromised shells to store in the attacker observation
        :param simulate_detection: whether to simulate detection or not
        :param detection_reward: the detection reward
        :param base_detection_p: the base detection probability
        :param manual_play: whether to use manual play or not
        :param state_type: the state type
        :return: the created configuration
        """
        network_conf = CSLEEnvConfig.emulation_env_config_to_network_config(emulation_env_config=emulation_env_config)
        attacker_action_conf = AttackerActionConfig.all_actions_config(
            num_nodes=len(network_conf.nodes), subnet_masks=emulation_env_config.topology_config.subnetwork_masks,
            hacker_ip=emulation_env_config.containers_config.agent_ip)
        defender_action_conf = DefenderActionConfig.all_actions_config(
            num_nodes=len(network_conf.nodes),
            subnet_masks=emulation_env_config.topology_config.subnetwork_masks)
        render_config = RenderConfig(num_levels = int(len(network_conf.nodes)/4), num_nodes_per_level = 4)

        emulation_config = EmulationConfig(agent_ip=emulation_env_config.containers_config.agent_ip,
                                           agent_username=constants.CSLE_ADMIN.USER,
                                           agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
        env_config = CSLEEnvConfig(
            attacker_action_conf=attacker_action_conf,
            defender_action_conf=defender_action_conf,
            network_conf=network_conf,
            attacker_num_ports_obs=attacker_num_ports_obs,
            attacker_num_vuln_obs=attacker_num_vuln_obs,
            attacker_num_sh_obs=attacker_num_sh_obs,
            num_nodes=len(network_conf.nodes),
            hacker_ip = emulation_env_config.containers_config.agent_ip,
            router_ip = emulation_env_config.containers_config.router_ip,
            render_config=render_config, env_mode=EnvMode.EMULATION,
            emulation_config=emulation_config, simulate_detection=simulate_detection,
            detection_reward=detection_reward, base_detection_p=base_detection_p, manual_play=manual_play,
            state_type=state_type, emulation_env_config=emulation_env_config
        )
        for c in emulation_env_config.containers_config.containers:
            if c.name in constants.CONTAINER_IMAGES.IDS_IMAGES:
                env_config.ids_router = True
        return env_config

    @staticmethod
    def emulation_env_config_to_network_config(emulation_env_config: EmulationEnvConfig) -> NetworkConfig:
        """
        Creates a network config object from the emulation config

        :return: the network config
        """
        nodes = []
        for c in emulation_env_config.containers_config.containers:

            ip_ids = list(map(lambda ip: int(ip.rsplit(".", 1)[-1]), c.get_ips()))
            node_type = NodeType.SERVER
            for router_img in constants.CONTAINER_IMAGES.ROUTER_IMAGES:
                if router_img in c.name:
                    node_type = NodeType.ROUTER
            for hacker_img in constants.CONTAINER_IMAGES.HACKER_IMAGES:
                if hacker_img in c.name:
                    node_type = NodeType.HACKER
            for client_img in constants.CONTAINER_IMAGES.CLIENT_IMAGES:
                if client_img in c.name:
                    node_type = NodeType.CLIENT

            flags = []
            for node_flags_cfg in emulation_env_config.flags_config.flags:
                if node_flags_cfg.ip in c.get_ips():
                    flags = node_flags_cfg.flags

            level = c.level
            vulnerabilities = emulation_env_config.vuln_config.vulnerabilities

            services = []
            for node_services_cfg in emulation_env_config.services_config.services_configs:
                if node_services_cfg.ip in c.get_ips():
                    services = node_services_cfg.services

            os = c.os

            credentials = []
            for vuln in vulnerabilities:
                credentials = credentials + vuln.credentials
            for serv in services:
                credentials = credentials + serv.credentials

            for user_cfg in emulation_env_config.users_config.users:
                if user_cfg.ip in c.get_ips():
                    for user in user_cfg.users:
                        credentials.append(Credential(username=user[0], pw=user[1], root=user[2]))

            root_usernames = []
            for cred in credentials:
                if cred.root:
                    root_usernames.append(cred.username)
            visible = True
            reachable_nodes = []
            network_names = list(map(lambda x: x[1].name, c.ips_and_networks))
            for c2 in emulation_env_config.containers_config.containers:
                reachable = False
                if c2.name != c.name:
                    for ip_net in c2.ips_and_networks:
                        if ip_net[1].name in network_names:
                            reachable = True
                if reachable:
                    reachable_nodes = reachable_nodes + c2.get_ips()
            node = Node(
                ips = c.get_ips(),
                ip_ids = ip_ids, id = ip_ids[0], type=node_type, flags=flags, level=int(level),
                vulnerabilities=vulnerabilities, services=services, os=os, credentials=credentials,
                root_usernames=root_usernames, visible=visible, reachable_nodes=reachable_nodes, firewall=False
            )
            nodes.append(node)

        adj_matrix = np.zeros((len(nodes), len(nodes)))
        for i in range(len(emulation_env_config.containers_config.containers)):
            for j in range(len(emulation_env_config.containers_config.containers)):
                network_names = list(map(lambda x: x[1].name, emulation_env_config.containers_config.containers[i].ips_and_networks))
                network_names2 = list(map(lambda x: x[1].name, emulation_env_config.containers_config.containers[j].ips_and_networks))
                reachable = False
                for name in network_names2:
                    if name in network_names:
                        reachable = True
                if reachable:
                    adj_matrix[i][j] = 1
        flags_lookup = {}
        for node in nodes:
            for flag in node.flags:
                flags_lookup[(node.ips[0], flag.path.replace(".txt", ""))] = flag
        net_conf = NetworkConfig(subnet_masks=emulation_env_config.topology_config.subnetwork_masks,
                                 vulnerable_nodes=emulation_env_config.containers_config.vulnerable_nodes, nodes=nodes,
                                 agent_reachable=emulation_env_config.containers_config.agent_reachable_nodes,
                                 adj_matrix=adj_matrix, flags_lookup=flags_lookup)
        return net_conf