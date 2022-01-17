from csle_common.envs_model.config.generator.container_manager import ContainerManager
import csle_common.constants.constants as constants


def delete_network(network_id : int = 1) -> None:
    """
    Deletes the docker networks

    :param network_id: the id of the internal network for this emulation
    :return: None
    """
    ContainerManager.remove_network(name=f"{constants.CSLE.CSLE_INTERNAL_NET_PREFIX}{network_id}")
    print("Removing 1000 client networks, this may take a while..")
    network_names = []
    for i in range(len(constants.CSLE.CSLE_EXTERNAL_SECOND_OCTET_VALUES)):
        for j in range(len(constants.CSLE.CSLE_EXTERNAL_THIRD_OCTET_VALUES)):
            network_id = i*len(constants.CSLE.CSLE_EXTERNAL_THIRD_OCTET_VALUES) + j
            network_name = f"{constants.CSLE.CSLE_EXTERNAL_NET_PREFIX}{network_id}"
            network_names.append(network_name)

    ContainerManager.remove_networks(names=network_names)


# Deletes the docker networks
if __name__ == '__main__':
    delete_network(network_id=1)