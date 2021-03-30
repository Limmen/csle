import os
from gym_pycr_ctf.dao.container_config.containers_config import ContainersConfig
from gym_pycr_ctf.dao.container_config.node_container_config import NodeContainerConfig
from gym_pycr_ctf.envs.config.generator.container_generator import ContainerGenerator
from gym_pycr_ctf.util.experiments_util import util

def default_containers_config():
    containers = [
        NodeContainerConfig(name="client1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.254"),
        NodeContainerConfig(name="ftp1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.79"),
        NodeContainerConfig(name="hacker_kali1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.191"),
        NodeContainerConfig(name="honeypot1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.21"),
        NodeContainerConfig(name="router2", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.10"),
        NodeContainerConfig(name="ssh1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.2"),
        NodeContainerConfig(name="telnet1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.3"),
        NodeContainerConfig(name="samba1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.19"),
        NodeContainerConfig(name="shellshock1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.31"),
        NodeContainerConfig(name="sql_injection1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.42"),
        NodeContainerConfig(name="cve_2015_3306_1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.37"),
        NodeContainerConfig(name="cve_2015_1427_1", network="pycr_net_8", minigame="ctf", version="0.0.1",
                            level="8", ip="172.18.8.82"),
        NodeContainerConfig(name="cve_2016_10033_1", network="pycr_net_8", minigame="ctf", version="0.0.1",
                            level="8", ip="172.18.8.75"),
        NodeContainerConfig(name="cve_2010_0426_1", network="pycr_net_8", minigame="ctf", version="0.0.1",
                            level="8", ip="172.18.8.71"),
        NodeContainerConfig(name="cve_2015_5602_1", network="pycr_net_8", minigame="ctf", version="0.0.1",
                            level="8", ip="172.18.8.11"),
        NodeContainerConfig(name="ssh1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.51"),
        NodeContainerConfig(name="ssh1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.52"),
        NodeContainerConfig(name="honeypot1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.53"),
        NodeContainerConfig(name="samba1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.54"),
        NodeContainerConfig(name="shellshock1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.55"),
        NodeContainerConfig(name="sql_injection1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.56"),
        NodeContainerConfig(name="cve_2015_3306_1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.57"),
        NodeContainerConfig(name="cve_2015_1427_1", network="pycr_net_8", minigame="ctf", version="0.0.1",
                            level="8", ip="172.18.8.58"),
        NodeContainerConfig(name="cve_2016_10033_1", network="pycr_net_8", minigame="ctf", version="0.0.1",
                            level="8", ip="172.18.8.59"),
        NodeContainerConfig(name="cve_2010_0426_1", network="pycr_net_8", minigame="ctf", version="0.0.1",
                            level="8", ip="172.18.8.60"),
        NodeContainerConfig(name="cve_2015_5602_1", network="pycr_net_8", minigame="ctf", version="0.0.1",
                            level="8", ip="172.18.8.61"),
        NodeContainerConfig(name="ssh1", network="pycr_net_8", minigame="ctf", version="0.0.1", level="8",
                            ip="172.18.8.62"),
    ]
    containers_cfg = ContainersConfig(containers=containers, network="pycr_net_8", agent_ip="172.18.8.191",
                                      router_ip="172.18.8.10", subnet_mask="172.18.8.0/24", subnet_prefix="172.18.8.",
                                      ids_enabled=True)
    return containers_cfg

if __name__ == '__main__':
    if os.path.exists(util.default_containers_path(out_dir=util.default_output_dir())):
        os.remove(util.default_containers_path(out_dir=util.default_output_dir()))
    containers_cfg = default_containers_config()
    ContainerGenerator.write_containers_config(containers_cfg, path=util.default_output_dir())