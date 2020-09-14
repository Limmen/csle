from gym_pycr_pwcrack.dao.network_config import NetworkConfig
from gym_pycr_pwcrack.dao.action_config import ActionConfig
from gym_pycr_pwcrack.dao.env_mode import EnvMode
from gym_pycr_pwcrack.dao.cluster_config import ClusterConfig
from gym_pycr_pwcrack.dao.render_config import RenderConfig

class EnvConfig:

    def __init__(self, network_conf : NetworkConfig, action_conf : ActionConfig, num_ports : int, num_vuln : int,
                 render_config : RenderConfig, env_mode : EnvMode = EnvMode.SIMULATION,
                 cluster_config : ClusterConfig = None):
        self.network_conf = network_conf
        self.action_conf = action_conf
        self.num_nodes = len(network_conf.nodes)
        self.num_ports = num_ports
        self.num_vuln = num_vuln
        self.env_mode = env_mode
        self.cluster_config = cluster_config
        self.render_config = render_config