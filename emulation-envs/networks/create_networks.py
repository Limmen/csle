import subprocess
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Parse flags for which networks to create')
    parser.add_argument("-n", "--numnetworks", help="number of networks", type=int, default=5)
    parser.add_argument("-d", "--delete", help="Boolean parameter, if true, delete networks instead of creating",
                        action="store_true")
    args = parser.parse_args()
    return args

def create_delete_networks(num_networks : int, create = True):
    subnet_mask_prefix = "172.18."
    subnetmask_suffix = ".0/24"
    network_name_base = "pycr_net_"

    for i in range(num_networks):
        subnet_mask = subnet_mask_prefix + str(i) + subnetmask_suffix
        network_name= network_name_base + str(i)
        if create:
            cmd = "docker network create --subnet={} {} || echo 'network already created'".format(subnet_mask, network_name)
        else:
            cmd = "docker network rm {}".format(network_name)
        subprocess.Popen(cmd, shell=True)


if __name__ == '__main__':
    args = parse_args()
    num_nets = args.numnetworks
    create_delete_networks(num_networks=num_nets, create=(not args.delete))
