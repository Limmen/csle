import subprocess
import time
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.sdn_controller_config import SDNControllerConfig
from csle_common.dao.emulation_config.sdn_controller_type import SDNControllerType
from csle_common.dao.emulation_config.ovs_config import OVSConfig
from csle_common.util.emulation_util import EmulationUtil
from csle_common.logging.log import Logger


class SDNControllerManager:
    """
    Class managing interaction with the SDN controller
    """

    @staticmethod
    def connect_sdn_controller_to_network(sdn_controller_config: SDNControllerConfig) -> None:
        """
        Connects the SDN controller to the Docker network

        :param sdn_controller_config: the controller configuration
        :return: None
        """
        if sdn_controller_config is None:
            return

        c = sdn_controller_config.container
        container_name = c.get_full_name()
        # Disconnect from none
        cmd = f"docker network disconnect none {container_name}"
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)

        # Wait a few seconds before connecting
        time.sleep(2)

        # Connect SDN controller
        for ip_net in c.ips_and_networks:
            ip, net = ip_net
            cmd = f"{constants.DOCKER.NETWORK_CONNECT} --ip {ip} {net.name} " \
                  f"{container_name}"
            Logger.__call__().get_logger().info(f"Connecting container:{container_name} to network:{net.name} "
                                                f"with ip: {ip}")
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)

    @staticmethod
    def start_controller(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Connects the SDN controller to the Docker network

        :param emulation_env_config: the emulation env config
        :return: None
        """
        if emulation_env_config.sdn_controller_config is None:
            return
        if emulation_env_config.sdn_controller_config.controller_type == SDNControllerType.RYU:
            # Connect
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                        ip=emulation_env_config.sdn_controller_config.container.get_ips()[0])

            # Check if controller is already running
            cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
                  + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.SDN_CONTROLLER_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd,
                conn=emulation_env_config.get_connection(
                    ip=emulation_env_config.sdn_controller_config.container.get_ips()[0]))

            if not constants.COMMANDS.SEARCH_SDN_CONTROLLER in str(o):

                Logger.__call__().get_logger().info(
                    f"Starting SDN controller manager node "
                    f"{emulation_env_config.sdn_controller_config.container.get_ips()[0]}")

                # Stop old background job if running
                cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                      constants.COMMANDS.SPACE_DELIM \
                      + constants.TRAFFIC_COMMANDS.SDN_CONTROLLER_FILE_NAME
                o, e, _ = EmulationUtil.execute_ssh_cmd(
                    cmd=cmd,
                    conn=emulation_env_config.get_connection(
                        ip=emulation_env_config.sdn_controller_config.container.get_ips()[0]))

                # Start the SDN controller
                cmd = constants.COMMANDS.START_SDN_CONTROLLER.format(
                    emulation_env_config.sdn_controller_config.controller_port,
                    emulation_env_config.sdn_controller_config.controller_web_api_port,
                    emulation_env_config.sdn_controller_config.controller_module_name)
                o, e, _ = EmulationUtil.execute_ssh_cmd(
                    cmd=cmd,
                    conn=emulation_env_config.get_connection(
                        ip=emulation_env_config.sdn_controller_config.container.get_ips()[0]))
                time.sleep(0.2)
        else:
            raise ValueError(f"Controller type: {emulation_env_config.sdn_controller_config.controller_type} "
                             f"not recognized")

    @staticmethod
    def ping_all(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Pings all the OVS switches from the container so that they can populate their forwarding tables

        :param emulation_env_config: the emulation config
        :return: None
        """
        if emulation_env_config.sdn_controller_config is None:
            return
        for ovs_sw in emulation_env_config.ovs_config.switch_configs:

            # Connect
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                        ip=ovs_sw.controller_ip)
            cmd = f"{constants.COMMANDS.PING} {ovs_sw.ip} -c 5"
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(
                ip=ovs_sw.controller_ip))
            time.sleep(5)

