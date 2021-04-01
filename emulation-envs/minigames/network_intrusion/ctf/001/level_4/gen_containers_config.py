import os
from gym_pycr_ctf.dao.container_config.containers_config import ContainersConfig
from gym_pycr_ctf.dao.container_config.node_container_config import NodeContainerConfig
from gym_pycr_ctf.envs_model.config.generator.container_generator import ContainerGenerator
from gym_pycr_ctf.util.experiments_util import util

def default_containers_config():
    containers = [
        NodeContainerConfig(name="client1", network="pycr_net_4", minigame="ctf", version="0.0.1", level="4",
                            ip="172.18.4.254"),
        NodeContainerConfig(name="ftp1", network="pycr_net_4", minigame="ctf", version="0.0.1", level="4", ip="172.18.4.79"),
        NodeContainerConfig(name="hacker_kali1", network="pycr_net_4", minigame="ctf", version="0.0.1", level="4",
                            ip="172.18.4.191"),
        NodeContainerConfig(name="honeypot1", network="pycr_net_4", minigame="ctf", version="0.0.1", level="4",
                            ip="172.18.4.21"),
        NodeContainerConfig(name="router2", network="pycr_net_4", minigame="ctf", version="0.0.1", level="4",
                            ip="172.18.4.10"),
        NodeContainerConfig(name="ssh1", network="pycr_net_4", minigame="ctf", version="0.0.1", level="4",
                            ip="172.18.4.2"),
        NodeContainerConfig(name="telnet1", network="pycr_net_4", minigame="ctf", version="0.0.1", level="4",
                            ip="172.18.4.3")
    ]
    containers_cfg = ContainersConfig(containers=containers, network="pycr_net_4", agent_ip="172.18.4.191",
                                      router_ip="172.18.4.10", subnet_mask="172.18.4.0/24", subnet_prefix="172.18.4.",
                                      ids_enabled=True)
    return containers_cfg

if __name__ == '__main__':
    if os.path.exists(util.default_containers_path(out_dir=util.default_output_dir())):
        os.remove(util.default_containers_path(out_dir=util.default_output_dir()))
    containers_cfg = default_containers_config()
    ContainerGenerator.write_containers_config(containers_cfg, path=util.default_output_dir())