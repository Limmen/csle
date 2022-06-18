import subprocess
import time
from csle_common.logging.log import Logger
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution


class OVSManager:

    @staticmethod
    def create_bridges(emulation_execution: EmulationExecution) -> None:
        if not emulation_execution.emulation_env_config.sdn:
            return

        for bridge in emulation_execution.emulation_env_config.ovs_config.bridges:
            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_VSCTL} {constants.OVS.ADD_BR} {bridge.get_name()}"
            Logger.__call__().get_logger().info(f"executing {cmd}")
            subprocess.call(cmd, shell=True)
            time.sleep(0.5)


    @staticmethod
    def create_ports(emulation_execution: EmulationExecution) -> None:
        if not emulation_execution.emulation_env_config.sdn:
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
    def connect_bridges(emulation_env_config: EmulationEnvConfig) -> None:
        if not emulation_env_config.sdn:
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
    def remove_bridges(emulation_env_config: EmulationEnvConfig) -> None:
        if not emulation_env_config.sdn:
            return
        for bridge in emulation_env_config.ovs_config.bridges:
            cmd = f"{constants.COMMANDS.SUDO} {constants.OVS.OVS_VSCTL} {constants.OVS.DEL_BR} {bridge.get_name()}"
            Logger.__call__().get_logger().info(f"executing {cmd}")
            subprocess.call(cmd, shell=True)
            time.sleep(0.5)

    @staticmethod
    def remove_bridge_connections(emulation_env_config: EmulationEnvConfig) -> None:
        if not emulation_env_config.sdn:
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
