import subprocess
import time
from csle_common.logging.log import Logger
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.containers_config import ContainersConfig


class OVSManager:
    """
    Class that contains functionality for interacting and managing OVS bridges in CSLE
    """

    @staticmethod
    def create_virtual_switches_on_container(containers_config: ContainersConfig) -> None:
        """
        Sets up OVS switches on containers

        :param containers_config: the containers configuration
        :param log_sink_config: the log sink config
        :return: None
        """
        for c in containers_config.containers:
            for ovs_image in constants.CONTAINER_IMAGES.OVS_IMAGES:
                if ovs_image in c.name:
                    Logger.__call__().get_logger().info(f"Configuring OVS bridge on container: {c.get_full_name()}")
                    container_name = c.get_full_name()
                    bridge_name = constants.OVS.DEFAULT_BRIDGE_NAME
                    cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} {constants.OVS.OVS_VSCTL} " \
                          f"{constants.OVS.ADD_BR} {bridge_name}"
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                    time.sleep(1)
                    cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} ifconfig {bridge_name} up"
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                    time.sleep(1)
                    idx = 0
                    for ip_net in c.ips_and_networks:
                        ip, net = ip_net
                        cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} {constants.OVS.OVS_VSCTL} " \
                              f"{constants.OVS.ADD_PORT} {bridge_name} {net.interface}"
                        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                        time.sleep(1)
                        cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} ifconfig {net.interface} 0"
                        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                        time.sleep(1)
                        if idx==0:
                            bridge_intf = bridge_name
                        else:
                            bridge_intf = f"{bridge_name}:{idx}"
                        cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} ifconfig {bridge_intf} {ip} " \
                              f"netmask {net.bitmask}"
                        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                        time.sleep(1)
                        idx+=1