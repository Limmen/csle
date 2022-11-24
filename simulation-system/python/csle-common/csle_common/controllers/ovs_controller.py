import subprocess
import time
from csle_common.logging.log import Logger
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.util.emulation_util import EmulationUtil


class OVSController:
    """
    Class that contains functionality for interacting and managing OVS bridges in CSLE
    """

    @staticmethod
    def create_virtual_switches_on_container(containers_config: ContainersConfig) -> None:
        """
        Sets up OVS switches on containers

        :param containers_config: the containers configuration
        :return: None
        """
        for c in containers_config.containers:
            for ovs_image in constants.CONTAINER_IMAGES.OVS_IMAGES:
                if ovs_image in c.name:
                    Logger.__call__().get_logger().info(f"Creating OVS bridge and ports "
                                                        f"on container: {c.get_full_name()}")
                    container_name = c.get_full_name()
                    bridge_name = constants.OVS.DEFAULT_BRIDGE_NAME
                    cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} {constants.OVS.OVS_VSCTL} " \
                          f"{constants.OVS.ADD_BR} {bridge_name}"
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                    time.sleep(0.2)
                    cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} ifconfig {bridge_name} up"
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                    time.sleep(0.2)
                    idx = 0
                    for ip_net in c.ips_and_networks:
                        ip, net = ip_net
                        cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} {constants.OVS.OVS_VSCTL} " \
                              f"{constants.OVS.ADD_PORT} {bridge_name} {net.interface}"
                        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                        time.sleep(0.2)
                        cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} ifconfig {net.interface} 0"
                        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                        time.sleep(0.2)
                        if idx == 0:
                            bridge_intf = bridge_name
                        else:
                            bridge_intf = f"{bridge_name}:{idx}"
                        cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} " \
                              f"ifconfig {bridge_intf} {ip} netmask {net.bitmask}"
                        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                        time.sleep(0.2)
                        idx += 1

    @staticmethod
    def apply_ovs_config(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Aplies the OVS configuration on the OVS switches

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for ovs_sw in emulation_env_config.ovs_config.switch_configs:
            Logger.__call__().get_logger().info(f"Configuring OVS bridge on container: {ovs_sw.container_name}")
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ovs_sw.ip)
            bridge_name = constants.OVS.DEFAULT_BRIDGE_NAME
            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_VSCTL} set bridge {bridge_name} " \
                  f"protocols={','.join(ovs_sw.openflow_protocols)}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.connections[ovs_sw.ip])
            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_VSCTL} set-controller {bridge_name} " \
                  f"{ovs_sw.controller_transport_protocol}:{ovs_sw.controller_ip}:{ovs_sw.controller_port}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.connections[ovs_sw.ip])
