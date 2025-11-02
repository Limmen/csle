import logging
import subprocess
import time
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.util.emulation_util import EmulationUtil


class OVSController:
    """
    Class that contains functionality for interacting and managing OVS bridges in CSLE
    """

    @staticmethod
    def create_virtual_switches_on_container(containers_config: ContainersConfig, physical_server_ip: str,
                                             logger: logging.Logger) -> None:
        """
        Sets up OVS switches on containers

        :param containers_config: the containers configuration
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ovs_image in constants.CONTAINER_IMAGES.OVS_IMAGES:
                if ovs_image in c.name:
                    logger.info(f"Creating OVS bridge and ports "
                                f"on container: {c.get_full_name()} with IP {c.docker_gw_bridge_ip} ({c.get_ips()[0]})")
                    container_name = c.get_full_name()
                    bridge_name = constants.OVS.DEFAULT_BRIDGE_NAME
                    cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} {constants.OVS.OVS_VSCTL} " \
                          f"{constants.OVS.ADD_BR} {bridge_name}"
                    logger.info(f"Running cmd: {cmd} on container: {c.get_full_name()} "
                                f"with IP {c.docker_gw_bridge_ip} ({c.get_ips()[0]})")
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                    time.sleep(0.2)
                    cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} ifconfig {bridge_name} up"
                    logger.info(f"Running cmd: {cmd} on container: {c.get_full_name()} "
                                f"with IP {c.docker_gw_bridge_ip} ({c.get_ips()[0]})")
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                    time.sleep(0.2)
                    idx = 0
                    for ip_net in c.ips_and_networks:
                        ip, net = ip_net
                        cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} {constants.OVS.OVS_VSCTL} " \
                              f"{constants.OVS.ADD_PORT} {bridge_name} {net.interface}"
                        logger.info(f"Running cmd: {cmd} on container: {c.get_full_name()} "
                                    f"with IP {c.docker_gw_bridge_ip} ({c.get_ips()[0]})")
                        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                        time.sleep(0.2)
                        cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} ifconfig {net.interface} 0"
                        logger.info(f"Running cmd: {cmd} on container: {c.get_full_name()} "
                                    f"with IP {c.docker_gw_bridge_ip} ({c.get_ips()[0]})")
                        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                        time.sleep(0.2)
                        if idx == 0:
                            bridge_intf = bridge_name
                        else:
                            bridge_intf = f"{bridge_name}:{idx}"
                        cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} " \
                              f"ifconfig {bridge_intf} {ip} netmask {net.bitmask}"
                        logger.info(f"Running cmd: {cmd} on container: {c.get_full_name()} "
                                    f"with IP {c.docker_gw_bridge_ip} ({c.get_ips()[0]})")
                        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                        time.sleep(0.2)
                        idx += 1

    @staticmethod
    def apply_ovs_config(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                         logger: logging.Logger) -> None:
        """
        Aplies the OVS configuration on the OVS switches

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for ovs_sw in emulation_env_config.ovs_config.switch_configs:
            if ovs_sw.physical_host_ip != physical_server_ip:
                logger.info(f"Wrong host IP of switch: {ovs_sw.container_name}, {ovs_sw.physical_host_ip}, "
                            f"{physical_server_ip}")
                continue
            logger.info(f"Configuring OVS bridge on container: {ovs_sw.container_name}, "
                        f"physical host: {ovs_sw.physical_host_ip}, gw ip: {ovs_sw.docker_gw_bridge_ip} "
                        f"container IP: {ovs_sw.ip}")
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ovs_sw.docker_gw_bridge_ip)
            bridge_name = constants.OVS.DEFAULT_BRIDGE_NAME
            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_VSCTL} set bridge {bridge_name} " \
                  f"protocols={','.join(ovs_sw.openflow_protocols)}"
            logger.info(f"Running cmd:{cmd} on container: {ovs_sw.container_name}")
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.connections[ovs_sw.docker_gw_bridge_ip])
            logger.info(f"Command: {cmd} completed")
            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_VSCTL} set-controller {bridge_name} " \
                  f"{ovs_sw.controller_transport_protocol}:{ovs_sw.controller_ip}:{ovs_sw.controller_port}"
            logger.info(f"Running cmd:{cmd} on container: {ovs_sw.container_name}")
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.connections[ovs_sw.docker_gw_bridge_ip])
            logger.info(f"Command: {cmd} completed")
