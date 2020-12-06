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
from gym_pycr_pwcrack.envs.state_representation.state_type import StateType
from gym_pycr_pwcrack.dao.action_results.user_command_cache import UserCommandCache

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
        self.detection_reward = -50
        self.all_flags_reward = 500
        self.sum_costs = 1
        self.max_episode_length = 10000
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

        self.exploration_policy = None
        self.max_exploration_steps = 100
        self.max_exploration_trajectories = 10
        self.load_cves_from_server = True
        self.load_services_from_server = True
        self.cache_misses = 0
        self.print_cache_details_freq = 500
        self.ids_router = False


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
        return self.network_conf.flags_lookup

    def scale_rewards_prep(self):
        sum_costs = sum(list(map(lambda x: x.cost, self.action_conf.actions)))
        self.sum_costs = sum_costs