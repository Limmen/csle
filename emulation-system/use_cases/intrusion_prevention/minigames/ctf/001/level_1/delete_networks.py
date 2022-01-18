from csle_common.envs_model.config.generator.container_manager import ContainerManager
import csle_common.constants.constants as constants


def delete_networks(network_id : int = 1) -> None:
    """
    Deletes the docker networks

    :param network_id: the id of the internal network for this emulation
    :return: None
    """
    ContainerManager.remove_network(name=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}{network_id}")
    ContainerManager.remove_network(name=f"{constants.CSLE.CSLE_EXTERNAL_NET_PREFIX}{network_id}")


# Deletes the docker networks
if __name__ == '__main__':
    delete_networks(network_id=1)