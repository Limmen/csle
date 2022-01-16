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
        NodeContainerConfig(name="client_1", network="csle_internal_net_2", minigame="ctf", version="0.0.1", level="2",
                            ip="172.18.2.254"),
        NodeContainerConfig(name="ftp_1", network="csle_internal_net_2", minigame="ctf", version="0.0.1", level="2",
                            ip="172.18.2.79"),
        NodeContainerConfig(name="hacker_kali_1", network="csle_internal_net_2", minigame="ctf", version="0.0.1", level="2",
                            ip="172.18.2.191"),
        NodeContainerConfig(name="honeypot_1", network="csle_internal_net_2", minigame="ctf", version="0.0.1", level="2",
                            ip="172.18.2.21"),
        NodeContainerConfig(name="router_1", network="csle_internal_net_2", minigame="ctf", version="0.0.1", level="2",
                            ip="172.18.2.10"),
        NodeContainerConfig(name="ssh_1", network="csle_internal_net_2", minigame="ctf", version="0.0.1", level="2",
                            ip="172.18.2.2"),
        NodeContainerConfig(name="telnet_1", network="csle_internal_net_2", minigame="ctf", version="0.0.1", level="2",
                            ip="172.18.2.3"),
        NodeContainerConfig(name="ftp_2", network="csle_internal_net_2", minigame="ctf", version="0.0.1", level="2",
                            ip="172.18.2.7"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_2", minigame="ctf", version="0.0.1", level="2",
                            ip="172.18.2.101"),
        NodeContainerConfig(name="ssh_2", network="csle_internal_net_2", minigame="ctf", version="0.0.1", level="2",
                            ip="172.18.2.54"),
        NodeContainerConfig(name="ssh_3", network="csle_internal_net_2", minigame="ctf", version="0.0.1", level="2",
                            ip="172.18.2.74"),
        NodeContainerConfig(name="telnet_2", network="csle_internal_net_2", minigame="ctf", version="0.0.1", level="2",
                            ip="172.18.2.61"),
        NodeContainerConfig(name="telnet_3", network="csle_internal_net_2", minigame="ctf", version="0.0.1", level="2",
                            ip="172.18.2.62")
    ]
    containers_cfg = ContainersConfig(containers=containers, network="csle_internal_net_2", agent_ip="172.18.2.191",
                                      router_ip="172.18.2.10", subnet_mask="172.18.2.0/24", subnet_prefix="172.18.2.",
                                      ids_enabled=False)
    return containers_cfg

# Generates the containers.json configuration file
if __name__ == '__main__':
    if os.path.exists(util.default_containers_path(out_dir=util.default_output_dir())):
        os.remove(util.default_containers_path(out_dir=util.default_output_dir()))
    containers_cfg = default_containers_config()
    ContainerGenerator.write_containers_config(containers_cfg, path=util.default_output_dir())