import argparse
import csle_common.constants.constants as constants
from csle_common.envs_model.config.generator.container_manager import ContainerManager


def parse_args():
    parser = argparse.ArgumentParser(description='Parse flags for which networks to create')
    parser.add_argument("-n", "--numnetworks", help="number of networks", type=int, default=5)
    parser.add_argument("-d", "--delete", help="Boolean parameter, if true, delete networks instead of creating",
                        action="store_true")
    args = parser.parse_args()
    return args


def create_delete_networks(num_networks : int, create = True):
    internal_subnet_mask_prefix = constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX
    external_subnet_mask_prefix = constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX
    subnetmask_suffix = constants.CSLE.CSLE_SUBNETMASK
    internal_network_name_base = constants.CSLE.CSLE_INTERNAL_NET_PREFIX
    external_network_name_base = constants.CSLE.CSLE_EXTERNAL_NET_PREFIX

    for i in range(1, num_networks+1):
        internal_subnet_mask = internal_subnet_mask_prefix + str(i) + subnetmask_suffix
        internal_network_name= internal_network_name_base + str(i)
        external_subnet_mask = external_subnet_mask_prefix + str(i) + subnetmask_suffix
        external_network_name= external_network_name_base + str(i)
        if create:
            ContainerManager.create_network(name=internal_network_name, subnetmask=internal_subnet_mask)
        else:
            ContainerManager.remove_network(name=internal_network_name)

        if create:
            ContainerManager.create_network(name=external_network_name, subnetmask=external_subnet_mask)
        else:
            ContainerManager.remove_network(name=external_network_name)


if __name__ == '__main__':
    args = parse_args()
    num_nets = args.numnetworks
    create_delete_networks(num_networks=num_nets, create=(not args.delete))
