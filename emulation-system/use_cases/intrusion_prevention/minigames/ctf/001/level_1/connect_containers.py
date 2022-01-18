import os
import subprocess
import time
from csle_common.util.experiments_util import util
import create_containers_config
from csle_common.envs_model.config.generator.container_generator import ContainerGenerator
import csle_common.constants.constants as constants


def connect_networks() -> None:
    """
    Connects running containers to networks

    :return: None
    """
    network_id = 1
    level = "1"
    version = "0.0.1"
    if not os.path.exists(util.default_containers_path()):
        containers_cfg = create_containers_config.default_containers_config(
            network_id=network_id, level=level, version=version)
        ContainerGenerator.write_containers_config(containers_cfg, path=util.default_output_dir())

    containers_config = util.read_containers_config(util.default_containers_path())

    for c in containers_config.containers:
        container_name = f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-{c.name}{c.suffix}-" \
                         f"{constants.CSLE.LEVEL}{c.level}"
        # Disconnect from none
        cmd = f"docker network disconnect none {container_name}"
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)

        # Wait a few seconds before connecting
        time.sleep(2)

        for ip_net in c.ips_and_networks:
            ip, net = ip_net
            cmd = f"{constants.DOCKER.NETWORK_CONNECT} --ip {ip} {net.name} " \
                  f"{container_name}"
            print(f"Connecting container:{container_name} to network:{net.name} with ip: {ip}")
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)

# Connect containers to networks
if __name__ == '__main__':
    connect_networks()
