import argparse
import subprocess
from csle_common.envs_model.config.generator.container_manager import ContainerManager

def parse_args():
    parser = argparse.ArgumentParser(description='Parse flags for creating client networks')
    parser.add_argument("-c", "--container", help="name of the container", type=str)
    parser.add_argument("-n", "--network", help="the network to connect to", type=str)
    parser.add_argument("-i", "--ip", help="the ip prefix to configure the interface", type=str)
    args = parser.parse_args()
    return args


def create_client_interfaces(container: str, ip_prefix: str, network: str):
    ip_prefix = "192.169."
    network_prefix = "csle_external_net_"
    for i in range(3,250):
        net = network_prefix + str(i)
        ContainerManager.create_network(name=net, subnetmask=ip_prefix + str(i) + "{constants.CSLE.CSLE_SUBNETMASK}")
        ip = ip_prefix + str(i) + ".254"
        cmd = f"docker network connect --ip {ip} {net} {container}"
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)


if __name__ == '__main__':
    args = parse_args()
    container = args.container
    ip = args.ip
    network = args.network
    create_client_interfaces(container=container, ip_prefix=ip, network=network)