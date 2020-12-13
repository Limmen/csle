import os
from gym_pycr_pwcrack.dao.container_config.containers_config import ContainersConfig
from gym_pycr_pwcrack.dao.container_config.node_container_config import NodeContainerConfig
from gym_pycr_pwcrack.envs.config.generator.container_generator import ContainerGenerator
from gym_pycr_pwcrack.util.experiments_util import util

def default_containers_config():
    containers = [
        NodeContainerConfig(name="ftp1", network="pycr_net_5", minigame="pwcrack", version="0.0.1", level="5", ip="172.18.5.79"),
        NodeContainerConfig(name="hacker_kali1", network="pycr_net_5", minigame="pwcrack", version="0.0.1", level="5",
                            ip="172.18.5.191"),
        NodeContainerConfig(name="honeypot1", network="pycr_net_5", minigame="pwcrack", version="0.0.1", level="5",
                            ip="172.18.5.21"),
        NodeContainerConfig(name="router1", network="pycr_net_5", minigame="pwcrack", version="0.0.1", level="5",
                            ip="172.18.5.10"),
        NodeContainerConfig(name="ssh1", network="pycr_net_5", minigame="pwcrack", version="0.0.1", level="5",
                            ip="172.18.5.2"),
        NodeContainerConfig(name="telnet1", network="pycr_net_5", minigame="pwcrack", version="0.0.1", level="5",
                            ip="172.18.5.3"),
        NodeContainerConfig(name="ftp2", network="pycr_net_5", minigame="pwcrack", version="0.0.1", level="5",
                            ip="172.18.5.7"),
        NodeContainerConfig(name="honeypot2", network="pycr_net_5", minigame="pwcrack", version="0.0.1", level="5",
                            ip="172.18.5.101"),
        NodeContainerConfig(name="ssh2", network="pycr_net_5", minigame="pwcrack", version="0.0.1", level="5",
                            ip="172.18.5.54"),
        NodeContainerConfig(name="ssh3", network="pycr_net_5", minigame="pwcrack", version="0.0.1", level="5",
                            ip="172.18.5.74"),
        NodeContainerConfig(name="telnet2", network="pycr_net_5", minigame="pwcrack", version="0.0.1", level="5",
                            ip="172.18.5.61"),
        NodeContainerConfig(name="telnet3", network="pycr_net_5", minigame="pwcrack", version="0.0.1", level="5",
                            ip="172.18.5.62")
    ]
    containers_cfg = ContainersConfig(containers=containers, network="pycr_net_5", agent_ip="172.18.5.191",
                                      router_ip="172.18.5.10", subnet_mask="172.18.5.0/24", subnet_prefix="172.18.5",
                                      ids_enabled=True)
    return containers_cfg

if __name__ == '__main__':
    if os.path.exists(util.default_containers_path(out_dir=util.default_output_dir())):
        os.remove(util.default_containers_path(out_dir=util.default_output_dir()))
    containers_cfg = default_containers_config()
    ContainerGenerator.write_containers_config(containers_cfg, path=util.default_output_dir())