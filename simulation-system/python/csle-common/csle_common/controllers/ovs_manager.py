import subprocess
import time
from csle_common.logging.log import Logger
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
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
                    container_name = c.get_full_name()
                    bridge_name = constants.OVS.DEFAULT_BRIDGE_NAME
                    cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} {constants.OVS.OVS_VSCTL} " \
                          f"{constants.OVS.ADD_BR} {bridge_name}"
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                    time.sleep(5)
                    cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} ifconfig {bridge_name} up"
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                    time.sleep(5)
                    idx = 0
                    for ip_net in c.ips_and_networks:
                        ip, net = ip_net
                        cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} {constants.OVS.OVS_VSCTL} " \
                              f"{constants.OVS.ADD_PORT} {bridge_name} {net.interface}"
                        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                        time.sleep(5)
                        cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} ifconfig {net.interface} 0"
                        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                        time.sleep(5)
                        if idx==0:
                            bridge_intf = bridge_name
                        else:
                            bridge_intf = f"{bridge_name}:{idx}"
                        cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {container_name} ifconfig {bridge_intf} {ip} " \
                              f"netmask {net.bitmask}"
                        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
                        time.sleep(5)
                        idx+=1

    @staticmethod
    def create_bridges_on_docker_host(emulation_execution: EmulationExecution) -> None:
        """
        Creates OVS bridges on the Docker host

        :param emulation_execution: the emulation execution to create the bridges for
        :return: None
        """
        if not emulation_execution.emulation_env_config.host_ovs:
            return

        for bridge in emulation_execution.emulation_env_config.ovs_config.bridges:
            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_VSCTL} {constants.OVS.ADD_BR} {bridge.get_name()}"
            Logger.__call__().get_logger().info(f"executing {cmd}")
            subprocess.call(cmd, shell=True)
            time.sleep(0.5)


    @staticmethod
    def create_ports_on_docker_host(emulation_execution: EmulationExecution) -> None:
        """
        Creates OVS ports on the Docker host

        :param emulation_execution: the emulation execution to create the ports for
        :return: None
        """
        if not emulation_execution.emulation_env_config.host_ovs:
            return
        for bridge in emulation_execution.emulation_env_config.ovs_config.bridges:
            for port in bridge.ports:
                cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_DOCKER} {constants.OVS.ADD_PORT} " \
                      f"{bridge.get_name()} {port.port_name} {port.container_name} " \
                      f"{constants.OVS.IPADDRESS}={port.ip}/{port.subnetmask_bits}"
                Logger.__call__().get_logger().info(f"executing {cmd}")
                subprocess.call(cmd, shell=True)
                time.sleep(0.5)
                cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_DOCKER} {constants.OVS.SET_VLAN} " \
                      f"{bridge.get_name()} {port.port_name} {port.container_name} " \
                      f"{port.vlan_id}"
                Logger.__call__().get_logger().info(f"executing {cmd}")
                subprocess.call(cmd, shell=True)
                time.sleep(0.5)

    @staticmethod
    def connect_bridges_on_docker_host(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Connects OVS bridges on the Docker host

        :param emulation_env_config: the configuration of the emulation to create connect the bridges for
        :return: None
        """
        if not emulation_env_config.host_ovs:
            return

        for bridge_conn in emulation_env_config.ovs_config.bridge_connections:
            cmd = f"{constants.COMMANDS.SUDO} " \
                  f"{constants.OVS.ADD_VETH_PEER_LINK.format(bridge_conn.port_1_name, bridge_conn.port_2_name)}"
            Logger.__call__().get_logger().info(f"executing {cmd}")
            subprocess.call(cmd, shell=True)

            # Bridge 1
            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_VSCTL} " \
                  f"{constants.OVS.ADD_PORT} {bridge_conn.bridge_1.get_name()} " \
                  f"{bridge_conn.port_1_name}"
            Logger.__call__().get_logger().info(f"executing {cmd}")
            subprocess.call(cmd, shell=True)

            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_VSCTL} " \
                  f"{constants.OVS.SET_INTERFACE} {bridge_conn.port_1_name} {constants.OVS.TYPE_PATCH}"
            Logger.__call__().get_logger().info(f"executing {cmd}")
            subprocess.call(cmd, shell=True)

            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_VSCTL} " \
                  f"{constants.OVS.SET_INTERFACE} {bridge_conn.port_1_name} " \
                  f"{constants.OVS.OPTIONS_PEER}={bridge_conn.port_2_name}"
            Logger.__call__().get_logger().info(f"executing {cmd}")
            subprocess.call(cmd, shell=True)

            # Bridge 2
            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_VSCTL} " \
                  f"{constants.OVS.ADD_PORT} {bridge_conn.bridge_2.get_name()} " \
                  f"{bridge_conn.port_2_name}"
            Logger.__call__().get_logger().info(f"executing {cmd}")
            subprocess.call(cmd, shell=True)

            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_VSCTL} " \
                  f"{constants.OVS.SET_INTERFACE} {bridge_conn.port_2_name} {constants.OVS.TYPE_PATCH}"
            Logger.__call__().get_logger().info(f"executing {cmd}")
            subprocess.call(cmd, shell=True)

            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_VSCTL} " \
                  f"{constants.OVS.SET_INTERFACE} {bridge_conn.port_2_name} " \
                  f"{constants.OVS.OPTIONS_PEER}={bridge_conn.port_1_name}"
            Logger.__call__().get_logger().info(f"executing {cmd}")
            subprocess.call(cmd, shell=True)


    @staticmethod
    def remove_bridges_on_docker_host(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Removes bridges from the Docker host

        :param emulation_env_config: the configuration of the emulation to remove the bridges for
        :return: None
        """
        if not emulation_env_config.host_ovs:
            return
        for bridge in emulation_env_config.ovs_config.bridges:
            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_VSCTL} {constants.OVS.DEL_BR} {bridge.get_name()}"
            Logger.__call__().get_logger().info(f"executing {cmd}")
            subprocess.call(cmd, shell=True)
            time.sleep(0.5)

    @staticmethod
    def remove_bridge_connections_on_docker_host(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Removes bridge connections on Docker host

        :param emulation_env_config: the config of the emulation to remove the bridge connections for
        :return: None
        """
        if not emulation_env_config.host_ovs:
            return
        for bridge_conn in emulation_env_config.ovs_config.bridge_connections:
            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.DELETE_VETH_PEER_LINK.format(bridge_conn.port_1_name)}"
            Logger.__call__().get_logger().info(f"executing {cmd}")
            subprocess.call(cmd, shell=True)
            time.sleep(0.5)
            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.DELETE_VETH_PEER_LINK.format(bridge_conn.port_2_name)}"
            Logger.__call__().get_logger().info(f"executing {cmd}")
            subprocess.call(cmd, shell=True)
            time.sleep(0.5)
