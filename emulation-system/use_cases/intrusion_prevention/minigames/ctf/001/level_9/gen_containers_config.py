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
        NodeContainerConfig(name="client_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.254"),
        NodeContainerConfig(name="client_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.253"),
        NodeContainerConfig(name="client_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.252"),
        NodeContainerConfig(name="ftp_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.79"),
        NodeContainerConfig(name="hacker_kali_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.191"),
        NodeContainerConfig(name="honeypot_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.21"),
        NodeContainerConfig(name="router_2", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.10"),
        NodeContainerConfig(name="ssh_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.2"),
        NodeContainerConfig(name="samba_2", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.3"),
        NodeContainerConfig(name="samba_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.7"),
        NodeContainerConfig(name="honeypot_2", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.101"),
        NodeContainerConfig(name="shellshock_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.54"),
        NodeContainerConfig(name="sql_injection_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.74"),
        NodeContainerConfig(name="cve_2010_0426", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.61"),
        NodeContainerConfig(name="cve_2015_1427_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.62"),
        NodeContainerConfig(name="honeypot_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.4"),
        NodeContainerConfig(name="honeypot_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.5"),
        NodeContainerConfig(name="honeypot_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.6"),
        NodeContainerConfig(name="honeypot_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.8"),
        NodeContainerConfig(name="honeypot_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.9"),
        NodeContainerConfig(name="cve_2015_3306_1", network="csle_net_3", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.178"),
        NodeContainerConfig(name="honeypot_2", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.11"),
        NodeContainerConfig(name="honeypot_2", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.13"),
        NodeContainerConfig(name="honeypot_2", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.14"),
        NodeContainerConfig(name="honeypot_2", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.15"),
        NodeContainerConfig(name="honeypot_2", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.16"),
        NodeContainerConfig(name="honeypot_2", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.17"),
        NodeContainerConfig(name="honeypot_2", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.18"),
        NodeContainerConfig(name="honeypot_2", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.19"),
        NodeContainerConfig(name="honeypot_2", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.22"),
        NodeContainerConfig(name="honeypot_2", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.23"),
        NodeContainerConfig(name="honeypot_2", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.24"),
        NodeContainerConfig(name="cve_2015_5602_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.25"),
        NodeContainerConfig(name="cve_2016_10033_1", network="csle_net_9", minigame="ctf", version="0.0.1", level="9",
                            ip="172.18.9.28")
    ]
    containers_cfg = ContainersConfig(containers=containers, network="csle_net_9", agent_ip="172.18.9.191",
                                      router_ip="172.18.9.10", subnet_mask="172.18.9.0/24", subnet_prefix="172.18.9.",
                                      ids_enabled=True)
    return containers_cfg

# Generates the containers.json configuration file
if __name__ == '__main__':
    if os.path.exists(util.default_containers_path(out_dir=util.default_output_dir())):
        os.remove(util.default_containers_path(out_dir=util.default_output_dir()))
    containers_cfg = default_containers_config()
    ContainerGenerator.write_containers_config(containers_cfg, path=util.default_output_dir())