from csle_common.envs_model.config.generator.container_manager import ContainerManager


def create_network() -> None:
    """
    Creates the docker networks

    :return: None
    """
    ContainerManager.create_network(name="csle_internal_net_1", subnetmask="172.18.1.0/24")
    ContainerManager.create_network(name="csle_external_net_1", subnetmask="192.169.1.0/24")


# Creates the docker networks
if __name__ == '__main__':
    create_network()