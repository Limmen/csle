from csle_common.envs_model.config.generator.container_manager import ContainerManager
import csle_common.constants.constants as constants


def create_network(network_id : int = 1) -> None:
    """
    Creates the docker networks

    :param network_id: the id of the internal network for this emulation
    :return: None
    """
    networks = ContainerManager.get_network_references()
    networks = list(map(lambda x: x.name, networks))
    ContainerManager.create_network(name=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}{network_id}",
                                    subnetmask=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}"
                                               f"{constants.CSLE.CSLE_SUBNETMASK_SUFFIX}",
                                    existing_network_names=networks)
    ContainerManager.create_network(name=f"{constants.CSLE.CSLE_EXTERNAL_NET_PREFIX}{network_id}",
                                    subnetmask=f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}"
                                               f"{constants.CSLE.CSLE_SUBNETMASK_SUFFIX}",
                                    existing_network_names=networks)


# Creates the docker networks
if __name__ == '__main__':
    network_id = 1
    create_network(network_id=network_id)