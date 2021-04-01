import re
from gym_pycr_ctf.dao.network.network_config import NetworkConfig
from gym_pycr_ctf.dao.action.attacker.attacker_action_config import AttackerActionConfig
from gym_pycr_ctf.dao.action.defender.defender_action_config import DefenderActionConfig
from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.render.render_config import RenderConfig
from gym_pycr_ctf.dao.action_results.nmap_scan_cache import NMAPScanCache
from gym_pycr_ctf.dao.action_results.action_costs import ActionCosts
from gym_pycr_ctf.dao.action_results.filesystem_scan_cache import FileSystemScanCache
from gym_pycr_ctf.dao.action_results.nikto_scan_cache import NiktoScanCache
from gym_pycr_ctf.dao.state_representation.state_type import StateType
from gym_pycr_ctf.dao.action_results.user_command_cache import UserCommandCache
from gym_pycr_ctf.dao.action_results.action_alerts import ActionAlerts

class EnvConfig:
    """
    Class containing the complete configuration of a pycrctf env
    """

    def __init__(self, network_conf : NetworkConfig, attacker_action_conf : AttackerActionConfig,
                 defender_action_conf: DefenderActionConfig,
                 attacker_num_ports_obs : int, attacker_num_vuln_obs : int,
                 attacker_num_sh_obs : int, num_nodes : int, hacker_ip : str, router_ip : str,
                 render_config : RenderConfig, env_mode : EnvMode = EnvMode.SIMULATION,
                 emulation_config : EmulationConfig = None, simulate_detection : bool = True,
                 detection_reward : int = 10,
                 base_detection_p : float = 0.01, manual_play : bool = False, state_type: StateType = StateType.BASE):
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
        """
        self.network_conf = network_conf
        self.attacker_action_conf = attacker_action_conf
        self.defender_action_conf = defender_action_conf
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
        self.shell_read_wait = 0.1
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
        self.attacker_detection_reward = -50
        self.attacker_all_flags_reward = 500
        self.attacker_sum_costs = 1
        self.attacker_max_costs = 1
        self.attacker_sum_alerts = 1
        self.attacker_max_alerts = 1
        self.max_episode_length = 1000
        self.attacker_base_step_reward = -1
        self.attacker_illegal_reward_action = 0
        self.attacker_final_steps_reward_coefficient = 1

        self.defender_final_steps_reward_coefficient = 0
        self.defender_caught_attacker_reward = 50
        self.defender_early_stopping = -50
        self.defender_intrusion_reward = -100

        self.defender_sum_costs = 1
        self.defender_max_costs = 1

        self.attacker_filter_illegal_actions = True
        self.checkpoint_dir = None
        self.checkpoint_freq = 1000
        self.num_flags = 0

        self.ip_to_machine_id_mapping = {}
        self.save_trajectories = False
        self.blacklist_ips = ["172.18.1.1"]
        self.manual_play = manual_play
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
        self.attacker_exploration_filter_illegal = True
        self.domain_randomization = False
        self.compute_pi_star_attacker = False
        self.use_upper_bound_pi_star_attacker = False
        self.pi_star_tau_attacker = None
        self.pi_star_rew_attacker = -1
        self.pi_star_rew_list_attacker = []

        self.attacker_install_tools_sleep_seconds = 3
        self.attacker_retry_check_root = 3
        self.attacker_retry_sambacry = 2
        self.attacker_retry_shellshock = 2
        self.attacker_retry_dvwa_sql_injection = 2
        self.attacker_retry_cve_2015_3306 = 2
        self.attacker_retry_cve_2015_1427 = 2
        self.attacker_retry_cve_2016_10033 = 2
        self.attacker_retry_cve_2010_0426 = 2
        self.attacker_retry_cve_2015_5602 = 2
        self.attacker_sambacry_sleep_retry = 2
        self.attacker_shellshock_sleep_retry = 2
        self.attacker_dvwa_sql_injection_sleep_retry = 2
        self.attacker_cve_2015_3306_sleep_retry = 2
        self.attacker_cve_2015_1427_sleep_retry = 2
        self.attacker_cve_2016_10033_sleep_retry = 2
        self.attacker_cve_2010_0426_sleep_retry = 2
        self.attacker_cve_2015_5602_sleep_retry = 2
        self.attacker_continue_action_sleep = 5

        self.defender_update_state = False
        self.defender_ids_severity_threshold=3
        self.defender_ids_recent_threshold_seconds = 30
        self.explore_defense_states = False


    def get_port_forward_port(self) -> int:
        """
        :return: Gets the next port to forward
        """
        p = self.emulation_config.port_forward_next_port
        self.emulation_config.port_forward_next_port +=1
        return p

    def _create_flags_lookup(self) -> dict:
        """
        Creates a lookup dict of (flagpath -> FlagDTO)

        :return: returns dict of (flagpath -> FlagDTO)
        """
        if self.network_conf is not None:
            return self.network_conf.flags_lookup
        else:
            return None

    def scale_rewards_prep_attacker(self):
        sum_costs = sum(list(map(lambda x: x.cost, self.attacker_action_conf.actions)))
        max_costs = max(max(list(map(lambda x: x.cost, self.attacker_action_conf.actions))), 1)
        self.attacker_sum_costs = sum_costs
        self.attacker_max_costs = max_costs
        if self.ids_router:
            sum_alerts = sum(list(map(lambda x: x.alerts[0], self.attacker_action_conf.actions)))
            max_alerts = max(max(list(map(lambda x: x.alerts[0], self.attacker_action_conf.actions))), 1)
            self.attacker_sum_alerts = sum_alerts
            self.attacker_max_alerts = max_alerts


    def scale_rewards_prep_defender(self):
        sum_costs = sum(list(map(lambda x: x.cost, self.attacker_action_conf.actions)))
        max_costs = max(max(list(map(lambda x: x.cost, self.attacker_action_conf.actions))), 1)
        self.defender_sum_costs = sum_costs
        self.defender_max_costs = max_costs


    def copy(self):
        env_config = EnvConfig(
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
        return env_config
