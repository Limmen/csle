import os
from csle_common.util.experiments_util import util
import create_containers_config
from csle_common.envs_model.config.generator.container_generator import ContainerGenerator
from csle_common.envs_model.config.generator.container_manager import ContainerManager


def delete_networks(network_id : int = 9, level="9", version = "0.0.1") -> None:
    """
    Deletes the docker networks

    :param version: the version of the emulation
    :param level: the level parameter of the emulation
    :param network_id: the id of the internal network for this emulation
    :return: None
    """
    if not os.path.exists(util.default_containers_path()):
        containers_cfg = create_containers_config.default_containers_config(
            network_id=network_id, level=level, version=version)
        ContainerGenerator.write_containers_config(containers_cfg, path=util.default_output_dir())

    containers_config = util.read_containers_config(util.default_containers_path())

    for c in containers_config.containers:
        for ip_net in c.ips_and_networks:
            ip, net = ip_net
            ContainerManager.remove_network(name=net.name)


# Deletes the docker networks
if __name__ == '__main__':
    network_id = 9
    level = "9"
    version = "0.0.1"
    delete_networks(network_id=network_id, level=level, version=version)