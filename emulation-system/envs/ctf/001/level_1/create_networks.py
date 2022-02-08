import os
from csle_common.util.experiments_util import util
import create_containers_config
from csle_common.envs_model.config.generator.container_generator import ContainerGenerator
from csle_common.envs_model.config.generator.container_manager import ContainerManager


def create_networks(network_id : int = 1, level="1", version = "0.0.1") -> None:
    """
    Creates the docker networks

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
            networks = ContainerManager.get_network_references()
            networks = list(map(lambda x: x.name, networks))
            ip, net = ip_net
            ContainerManager.create_network_from_dto(network_dto=net, existing_network_names=networks)


# Creates the docker networks
if __name__ == '__main__':
    network_id = 1
    level = "1"
    version = "0.0.1"
    create_networks(network_id=network_id, level=level, version=version)