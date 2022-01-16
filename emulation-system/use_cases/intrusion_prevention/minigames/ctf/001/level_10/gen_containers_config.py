import os
from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.dao.container_config.node_container_config import NodeContainerConfig
from csle_common.envs_model.config.generator.container_generator import ContainerGenerator
from csle_common.util.experiments_util import util

def default_containers_config() -> ContainersConfig:
    """
    :return: the ContainersConfig of the emulation
    """
    containers = [
        NodeContainerConfig(name="client_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1", level="10",
                            ip="172.18.10.254"),
        NodeContainerConfig(name="ftp_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1", level="10",
                            ip="172.18.10.79"),
        NodeContainerConfig(name="hacker_kali_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1", level="10",
                            ip="172.18.10.191"),
        NodeContainerConfig(name="honeypot_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1", level="10",
                            ip="172.18.10.21"),
        NodeContainerConfig(name="router_2", network="csle_internal_net_10", minigame="ctf", version="0.0.1", level="10",
                            ip="172.18.10.10"),
        NodeContainerConfig(name="ssh_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1", level="10",
                            ip="172.18.10.2"),
        NodeContainerConfig(name="telnet_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1", level="10",
                            ip="172.18.10.3"),
        NodeContainerConfig(name="samba_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1", level="10",
                            ip="172.18.10.19"),
        NodeContainerConfig(name="shellshock_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1", level="10",
                            ip="172.18.10.31"),
        NodeContainerConfig(name="sql_injection_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1", level="10",
                            ip="172.18.10.42"),
        NodeContainerConfig(name="cve_2015_3306_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1", level="10",
                            ip="172.18.10.37"),
        NodeContainerConfig(name="cve_2015_1427_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1",
                            level="10", ip="172.18.10.82"),
        NodeContainerConfig(name="cve_2016_10033_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1",
                            level="10", ip="172.18.10.75"),
        NodeContainerConfig(name="cve_2010_0426_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1",
                            level="10", ip="172.18.10.71"),
        NodeContainerConfig(name="cve_2015_5602_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1",
                            level="10", ip="172.18.10.11"),
        NodeContainerConfig(name="pengine_exploit_1", network="csle_internal_net_10", minigame="ctf", version="0.0.1",
                            level="10", ip="172.18.10.104")
    ]
    containers_cfg = ContainersConfig(containers=containers, network="csle_internal_net_10", agent_ip="172.18.10.191",
                                      router_ip="172.18.10.10", subnet_mask="172.18.10.0/24", subnet_prefix="172.18.10.",
                                      ids_enabled=True)
    return containers_cfg

# Generates the containers.json configuration file
if __name__ == '__main__':
    if os.path.exists(util.default_containers_path(out_dir=util.default_output_dir())):
        os.remove(util.default_containers_path(out_dir=util.default_output_dir()))
    containers_cfg = default_containers_config()
    ContainerGenerator.write_containers_config(containers_cfg, path=util.default_output_dir())