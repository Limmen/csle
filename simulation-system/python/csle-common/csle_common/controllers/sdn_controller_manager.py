import subprocess
import time
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.sdn_controller_config import SDNControllerConfig
from csle_common.logging.log import Logger


class SDNControllerManager:
    """
    Class managing interaction with the SDN controller
    """


    @staticmethod
    def connect_sdn_controller_to_network(sdn_controller_config: SDNControllerConfig) -> None:
        if sdn_controller_config is None:
            return

        c = sdn_controller_config.container
        container_name = c.get_full_name()
        # Disconnect from none
        cmd = f"docker network disconnect none {container_name}"
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)

        # Wait a few seconds before connecting
        time.sleep(2)

        for ip_net in c.ips_and_networks:
            ip, net = ip_net
            cmd = f"{constants.DOCKER.NETWORK_CONNECT} --ip {ip} {net.name} " \
                  f"{container_name}"
            Logger.__call__().get_logger().info(f"Connecting container:{container_name} to network:{net.name} "
                                                f"with ip: {ip}")
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)