import re
from gym_pycr_pwcrack.dao.network.network_config import NetworkConfig
from gym_pycr_pwcrack.dao.action.action_config import ActionConfig
from gym_pycr_pwcrack.dao.network.env_mode import EnvMode
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.dao.render.render_config import RenderConfig
from gym_pycr_pwcrack.dao.action_results.nmap_scan_cache import NMAPScanCache
from gym_pycr_pwcrack.dao.action_results.action_costs import ActionCosts


class EnvConfig:
    """
    Class containing the complete configuration of a pycrpwcrack env
    """

    def __init__(self, network_conf : NetworkConfig, action_conf : ActionConfig, num_ports : int, num_vuln : int,
                 num_sh : int,
                 render_config : RenderConfig, env_mode : EnvMode = EnvMode.SIMULATION,
                 cluster_config : ClusterConfig = None, simulate_detection : bool = True, detection_reward : int = 10,
                 base_detection_p : float = 0.01):
        """
        Initialize the config

        :param network_conf: the network config
        :param action_conf: the action config
        :param num_ports: number of ports per machine in the state
        :param num_vuln: number of vuln per machine to keep in state
        :param num_sh: number of shell connections per machine to keep in state
        :param render_config: the render config
        :param env_mode: the env mode (e.g. cluster or sim)
        :param cluster_config: the cluster config
        :param simulate_detection: boolean flag whether to simulate detections or not
        :param detection_reward: reward when a detection happens
        :param base_detection_p: base detection probability for simulation
        """
        self.network_conf = network_conf
        self.action_conf = action_conf
        self.num_nodes = len(network_conf.nodes)
        self.num_ports = num_ports
        self.num_vuln = num_vuln
        self.num_sh = num_sh
        self.env_mode = env_mode
        self.cluster_config = cluster_config
        self.render_config = render_config
        self.simulate_detection = simulate_detection
        self.detection_reward = detection_reward
        self.base_detection_p = base_detection_p

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
        self.max_nmap_command_output_size = 10000000
        self.nmap_cache_dir = "/home/agent/"
        self.nmap_cache = []
        self.retry_timeout = 2
        self.num_retries = 2
        self.use_nmap_cache = True
        self.nmap_scan_cache = NMAPScanCache()
        self.action_costs = ActionCosts()
        self.port_forward_next_port = 4000

    def get_port_forward_port(self) -> int:
        """
        :return: Gets the next port to forward
        """
        p = self.port_forward_next_port
        self.port_forward_next_port +=1
        return p