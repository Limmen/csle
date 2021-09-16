import os
from pycr_common.dao.container_config.containers_config import ContainersConfig
from pycr_common.dao.container_config.node_container_config import NodeContainerConfig
from pycr_common.envs_model.config.generator.container_generator import ContainerGenerator
from pycr_common.util.experiments_util import util

def default_containers_config():
    containers = [
        NodeContainerConfig(name="client1", network="pycr_net_7", minigame="ctf", version="0.0.1", level="7",
                            ip="172.18.7.254"),
        NodeContainerConfig(name="ftp1", network="pycr_net_7", minigame="ctf", version="0.0.1", level="7",
                            ip="172.18.7.79"),
        NodeContainerConfig(name="hacker_kali1", network="pycr_net_7", minigame="ctf", version="0.0.1", level="7",
                            ip="172.18.7.191"),
        NodeContainerConfig(name="honeypot1", network="pycr_net_7", minigame="ctf", version="0.0.1", level="7",
                            ip="172.18.7.21"),
        NodeContainerConfig(name="router2", network="pycr_net_7", minigame="ctf", version="0.0.1", level="7",
                            ip="172.18.7.10"),
        NodeContainerConfig(name="ssh1", network="pycr_net_7", minigame="ctf", version="0.0.1", level="7",
                            ip="172.18.7.2"),
        NodeContainerConfig(name="telnet1", network="pycr_net_7", minigame="ctf", version="0.0.1", level="7",
                            ip="172.18.7.3"),
        NodeContainerConfig(name="samba1", network="pycr_net_7", minigame="ctf", version="0.0.1", level="7",
                            ip="172.18.7.19"),
        NodeContainerConfig(name="shellshock1", network="pycr_net_7", minigame="ctf", version="0.0.1", level="7",
                            ip="172.18.7.31"),
        NodeContainerConfig(name="sql_injection1", network="pycr_net_7", minigame="ctf", version="0.0.1", level="7",
                            ip="172.18.7.42"),
        NodeContainerConfig(name="cve_2015_3306_1", network="pycr_net_7", minigame="ctf", version="0.0.1", level="7",
                            ip="172.18.7.37"),
        NodeContainerConfig(name="cve_2015_1427_1", network="pycr_net_7", minigame="ctf", version="0.0.1",
                            level="7", ip="172.18.7.82"),
        NodeContainerConfig(name="cve_2016_10033_1", network="pycr_net_7", minigame="ctf", version="0.0.1",
                            level="7", ip="172.18.7.75"),
        NodeContainerConfig(name="cve_2010_0426_1", network="pycr_net_7", minigame="ctf", version="0.0.1",
                            level="7", ip="172.18.7.71"),
        NodeContainerConfig(name="cve_2015_5602_1", network="pycr_net_7", minigame="ctf", version="0.0.1",
                            level="7", ip="172.18.7.11")
    ]
    containers_cfg = ContainersConfig(containers=containers, network="pycr_net_7", agent_ip="172.18.7.191",
                                      router_ip="172.18.7.10", subnet_mask="172.18.7.0/24", subnet_prefix="172.18.7.",
                                      ids_enabled=True)
    return containers_cfg

if __name__ == '__main__':
    if os.path.exists(util.default_containers_path(out_dir=util.default_output_dir())):
        os.remove(util.default_containers_path(out_dir=util.default_output_dir()))
    containers_cfg = default_containers_config()
    ContainerGenerator.write_containers_config(containers_cfg, path=util.default_output_dir())