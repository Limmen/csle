import os
from pycr_common.dao.container_config.containers_config import ContainersConfig
from gym_pycr_ctf.dao.container_config.node_container_config import NodeContainerConfig
from gym_pycr_ctf.envs_model.config.generator.container_generator import ContainerGenerator
from gym_pycr_ctf.util.experiments_util import util

def default_containers_config():
    containers = [
        NodeContainerConfig(name="client1", network="pycr_net_1", minigame="ctf", version="0.0.1", level="1",
                            ip="172.18.1.254"),
        NodeContainerConfig(name="ftp1", network="pycr_net_1", minigame="ctf", version="0.0.1", level="1", ip="172.18.1.79"),
        NodeContainerConfig(name="hacker_kali1", network="pycr_net_1", minigame="ctf", version="0.0.1", level="1",
                            ip="172.18.1.191"),
        NodeContainerConfig(name="honeypot1", network="pycr_net_1", minigame="ctf", version="0.0.1", level="1",
                            ip="172.18.1.21"),
        NodeContainerConfig(name="router1", network="pycr_net_1", minigame="ctf", version="0.0.1", level="1",
                            ip="172.18.1.10"),
        NodeContainerConfig(name="ssh1", network="pycr_net_1", minigame="ctf", version="0.0.1", level="1",
                            ip="172.18.1.2"),
        NodeContainerConfig(name="telnet1", network="pycr_net_1", minigame="ctf", version="0.0.1", level="1",
                            ip="172.18.1.3")
    ]
    containers_cfg = ContainersConfig(containers=containers, network="pycr_net_1", agent_ip="172.18.1.191",
                                      router_ip="172.18.1.10", subnet_mask="172.18.1.0/24", subnet_prefix="172.18.1.",
                                      ids_enabled=False)
    return containers_cfg

if __name__ == '__main__':
    if os.path.exists(util.default_containers_path(out_dir=util.default_output_dir())):
        os.remove(util.default_containers_path(out_dir=util.default_output_dir()))
    containers_cfg = default_containers_config()
    ContainerGenerator.write_containers_config(containers_cfg, path=util.default_output_dir())