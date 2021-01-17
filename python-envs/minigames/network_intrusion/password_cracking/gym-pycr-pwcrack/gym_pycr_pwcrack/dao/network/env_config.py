import re
from gym_pycr_pwcrack.dao.network.network_config import NetworkConfig
from gym_pycr_pwcrack.dao.action.action_config import ActionConfig
from gym_pycr_pwcrack.dao.network.env_mode import EnvMode
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.dao.render.render_config import RenderConfig
from gym_pycr_pwcrack.dao.action_results.nmap_scan_cache import NMAPScanCache
from gym_pycr_pwcrack.dao.action_results.action_costs import ActionCosts
from gym_pycr_pwcrack.dao.action_results.filesystem_scan_cache import FileSystemScanCache
from gym_pycr_pwcrack.dao.action_results.nikto_scan_cache import NiktoScanCache
from gym_pycr_pwcrack.dao.state_representation.state_type import StateType
from gym_pycr_pwcrack.dao.action_results.user_command_cache import UserCommandCache
from gym_pycr_pwcrack.dao.action_results.action_alerts import ActionAlerts

class EnvConfig:
    """
    Class containing the complete configuration of a pycrpwcrack env
    """

    def __init__(self, network_conf : NetworkConfig, action_conf : ActionConfig, num_ports : int, num_vuln : int,
                 num_sh : int, num_nodes : int, hacker_ip : str, router_ip : str,
                 render_config : RenderConfig, env_mode : EnvMode = EnvMode.SIMULATION,
                 cluster_config : ClusterConfig = None, simulate_detection : bool = True, detection_reward : int = 10,
                 base_detection_p : float = 0.01, manual_play : bool = False, state_type: StateType = StateType.BASE):
        """
        Initialize the config

        :param network_conf: the network config
        :param action_conf: the action config
        :param num_ports: number of ports per machine in the state
        :param num_vuln: number of vuln per machine to keep in state
        :param num_sh: number of shell connections per machine to keep in state
        :param num_nodes: number of nodes
        :param hacker_ip: ip of the hacker
        :param router_ip: ip of the default gw for the hacker
        :param render_config: the render config
        :param env_mode: the env mode (e.g. cluster or sim)
        :param cluster_config: the cluster config
        :param simulate_detection: boolean flag whether to simulate detections or not
        :param detection_reward: reward when a detection happens
        :param base_detection_p: base detection probability for simulation
        :param manual_play: boolean flag whether manual play is used
        """
        self.network_conf = network_conf
        self.action_conf = action_conf
        self.num_ports = num_ports
        self.num_vuln = num_vuln
        self.num_sh = num_sh
        self.num_nodes = num_nodes
        self.env_mode = env_mode
        self.cluster_config = cluster_config
        self.render_config = render_config
        self.simulate_detection = simulate_detection
        self.detection_reward = detection_reward
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
        self.use_nmap_cache = True
        self.nmap_scan_cache = NMAPScanCache()
        self.use_nikto_cache = True
        self.nikto_scan_cache = NiktoScanCache()
        self.action_costs = ActionCosts()
        self.action_alerts = ActionAlerts()
        self.flag_lookup = self._create_flags_lookup()
        self.use_file_system_cache = True
        self.filesystem_scan_cache = FileSystemScanCache()
        self.filesystem_file_cache = []
        self.use_user_command_cache = True
        self.user_command_cache = UserCommandCache()
        self.user_command_cache_files_cache = []

        self.flag_found_reward_mult = 20
        self.port_found_reward_mult = 1
        self.os_found_reward_mult = 1
        self.cve_vuln_found_reward_mult = 1
        self.osvdb_vuln_found_reward_mult = 1
        self.machine_found_reward_mult = 1
        self.shell_access_found_reward_mult = 10
        self.root_found_reward_mult = 10
        self.new_login_reward_mult = 1
        self.new_tools_installed_reward_mult = 1
        self.new_backdoors_installed_reward_mult = 1
        self.cost_coefficient = 1
        self.alerts_coefficient = 1
        self.detection_reward = -50
        self.all_flags_reward = 500
        self.sum_costs = 1
        self.max_costs = 1
        self.sum_alerts = 1
        self.max_alerts = 1
        self.max_episode_length = 1000
        self.base_step_reward = -1
        self.illegal_reward_action = 0
        self.final_steps_reward_coefficient = 1

        self.filter_illegal_actions = True
        self.checkpoint_dir = None
        self.checkpoint_freq = 1000
        self.num_flags = 0

        self.ip_to_machine_id_mapping = {}
        self.save_trajectories = False
        self.blacklist_ips = ["172.18.1.1"]
        self.manual_play = manual_play
        self.state_type = state_type
        self.ssh_retry_find_flag = 5
        self.retry_find_users = 5
        self.ftp_retry_find_flag = 2
        self.retry_install_tools = 5

        self.exploration_policy = None
        self.max_exploration_steps = 100
        self.max_exploration_trajectories = 100
        self.load_cves_from_server = True
        self.load_services_from_server = True
        self.cache_misses = 0
        self.print_cache_details_freq = 500
        self.ids_router = False
        self.idx = 0
        self.exploration_filter_illegal = True
        self.domain_randomization = False
        self.compute_pi_star = False
        self.use_upper_bound_pi_star = False
        self.pi_star_tau = None
        self.pi_star_rew = -1
        self.pi_star_rew_list = []


    def get_port_forward_port(self) -> int:
        """
        :return: Gets the next port to forward
        """
        p = self.cluster_config.port_forward_next_port
        self.cluster_config.port_forward_next_port +=1
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

    def scale_rewards_prep(self):
        sum_costs = sum(list(map(lambda x: x.cost, self.action_conf.actions)))
        max_costs = max(max(list(map(lambda x: x.cost, self.action_conf.actions))), 1)
        self.sum_costs = sum_costs
        self.max_costs = max_costs
        if self.ids_router:
            sum_alerts = sum(list(map(lambda x: x.alerts[0], self.action_conf.actions)))
            max_alerts = max(max(list(map(lambda x: x.alerts[0], self.action_conf.actions))), 1)
            self.sum_alerts = sum_alerts
            self.max_alerts = max_alerts


    def copy(self):
        env_config = EnvConfig(
            network_conf=self.network_conf, action_conf=self.action_conf, num_ports=self.num_ports,
            num_vuln=self.num_vuln, num_sh=self.num_sh, num_nodes=self.num_nodes, hacker_ip=self.hacker_ip,
            router_ip=self.router_ip, render_config=self.render_config, env_mode=self.env_mode,
            cluster_config=self.cluster_config, simulate_detection=self.simulate_detection,
            detection_reward=self.detection_reward, base_detection_p=self.base_detection_p, manual_play=self.manual_play,
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
        env_config.use_nmap_cache = self.use_nmap_cache
        env_config.nmap_scan_cache = self.nmap_scan_cache
        env_config.use_nikto_cache = self.use_nikto_cache
        env_config.action_costs = self.action_costs
        env_config.action_alerts = self.action_alerts
        env_config.flag_lookup = self.flag_lookup
        env_config.use_file_system_cache = self.use_file_system_cache
        env_config.filesystem_scan_cache = self.filesystem_scan_cache
        env_config.filesystem_file_cache = self.filesystem_file_cache
        env_config.use_user_command_cache = self.use_user_command_cache
        env_config.user_command_cache = self.user_command_cache
        env_config.user_command_cache_files_cache = self.user_command_cache_files_cache
        env_config.flag_found_reward_mult = self.flag_found_reward_mult
        env_config.port_found_reward_mult = self.port_found_reward_mult
        env_config.os_found_reward_mult = self.os_found_reward_mult
        env_config.cve_vuln_found_reward_mult = self.cve_vuln_found_reward_mult
        env_config.osvdb_vuln_found_reward_mult = self.osvdb_vuln_found_reward_mult
        env_config.machine_found_reward_mult = self.machine_found_reward_mult
        env_config.shell_access_found_reward_mult = self.shell_access_found_reward_mult
        env_config.root_found_reward_mult = self.root_found_reward_mult
        env_config.new_login_reward_mult = self.new_login_reward_mult
        env_config.new_tools_installed_reward_mult = self.new_tools_installed_reward_mult
        env_config.new_backdoors_installed_reward_mult = self.new_backdoors_installed_reward_mult
        env_config.cost_coefficient = self.cost_coefficient
        env_config.alerts_coefficient = self.alerts_coefficient
        env_config.detection_reward = self.detection_reward
        env_config.all_flags_reward = self.all_flags_reward
        env_config.sum_costs = self.sum_costs
        env_config.max_costs = self.max_costs
        env_config.sum_alerts = self.sum_alerts
        env_config.max_alerts = self.max_alerts
        env_config.max_episode_length = self.max_episode_length
        env_config.base_step_reward = self.base_step_reward
        env_config.illegal_reward_action = self.illegal_reward_action
        env_config.final_steps_reward_coefficient = self.final_steps_reward_coefficient
        env_config.filter_illegal_actions = self.filter_illegal_actions
        env_config.checkpoint_dir = self.checkpoint_dir
        env_config.checkpoint_freq = self.checkpoint_freq
        env_config.num_flags = self.num_flags
        env_config.ip_to_machine_id_mapping = self.ip_to_machine_id_mapping
        env_config.save_trajectories = self.save_trajectories
        env_config.blacklist_ips = self.blacklist_ips
        env_config.manual_play = self.manual_play
        env_config.state_type = self.state_type
        env_config.ssh_retry_find_flag = self.ssh_retry_find_flag
        env_config.retry_find_users = self.retry_find_users
        env_config.ftp_retry_find_flag = self.ftp_retry_find_flag
        env_config.retry_install_tools = self.retry_install_tools
        env_config.exploration_policy = self.exploration_policy
        env_config.max_exploration_steps = self.max_exploration_steps
        env_config.max_exploration_trajectories = self.max_exploration_trajectories
        env_config.load_cves_from_server = self.load_cves_from_server
        env_config.cache_misses = self.cache_misses
        env_config.print_cache_details_freq = self.print_cache_details_freq
        env_config.ids_router = self.ids_router
        env_config.idx = self.idx
        env_config.exploration_filter_illegal = self.exploration_policy
        env_config.domain_randomization = self.domain_randomization
        env_config.compute_pi_star = self.compute_pi_star
        env_config.use_upper_bound_pi_star = self.use_upper_bound_pi_star
        env_config.pi_star_rew = self.pi_star_rew
        env_config.pi_star_rew_list = self.pi_star_rew_list
        return env_config
