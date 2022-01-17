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
    ContainerManager.create_network(name=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}1",
                                    subnetmask=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}"
                                               f"{constants.CSLE.CSLE_SUBNETMASK}",
                                    existing_network_names=networks)
    external_net_prefix = constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX
    print("Creating 1000 client networks, this may take a while..")
    for i, second_octet in enumerate(constants.CSLE.CSLE_EXTERNAL_SECOND_OCTET_VALUES):
        for j, third_octet in enumerate(constants.CSLE.CSLE_EXTERNAL_THIRD_OCTET_VALUES):
            external_network_subnetmask = f"{external_net_prefix}{second_octet}." \
                                          f"{third_octet}{constants.CSLE.CSLE_SUBNETMASK}"
            network_id = i*len(constants.CSLE.CSLE_EXTERNAL_THIRD_OCTET_VALUES) + j
            ContainerManager.create_network(name=f"{constants.CSLE.CSLE_EXTERNAL_NET_PREFIX}{network_id}",
                                            subnetmask=external_network_subnetmask,
                                            existing_network_names=networks)


# Creates the docker networks
if __name__ == '__main__':
    create_network()