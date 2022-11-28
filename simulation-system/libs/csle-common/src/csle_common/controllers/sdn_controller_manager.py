import subprocess
import time
import json
import requests
import csle_common.constants.constants as constants
import csle_ryu.constants.constants as ryu_constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.sdn_controller_config import SDNControllerConfig
from csle_common.dao.emulation_config.sdn_controller_type import SDNControllerType
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
        Starts the SDN controller

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
            cmd = (constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP + constants.COMMANDS.SPACE_DELIM +
                   constants.TRAFFIC_COMMANDS.SDN_CONTROLLER_FILE_NAME)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd,
                conn=emulation_env_config.get_connection(
                    ip=emulation_env_config.sdn_controller_config.container.get_ips()[0]))

            if constants.COMMANDS.SEARCH_SDN_CONTROLLER not in str(o):
                Logger.__call__().get_logger().info(
                    "Starting SDN controller manager node "
                    f"{emulation_env_config.sdn_controller_config.container.get_ips()[0]}")

                # Stop old background job if running
                cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
                       constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.SDN_CONTROLLER_FILE_NAME)
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
                             "not recognized")

    @staticmethod
    def start_controller_producer(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Starts the Kafka producer at the SDN controller

        :param emulation_env_config: the emulation env config
        :return: None
        """
        if emulation_env_config.sdn_controller_config is None:
            return
        Logger.__call__().get_logger().info("Sends request to the SDN controller to start the Kafka producer"
                                            " for telemetry")
        kafka_ip = emulation_env_config.kafka_config.container.get_ips()[0]
        controller_ip = emulation_env_config.sdn_controller_config.container.get_ips()[0]
        time_step_len = emulation_env_config.sdn_controller_config.time_step_len_seconds
        controller_web_port = emulation_env_config.sdn_controller_config.controller_web_api_port
        response = requests.put(
            f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{controller_ip}:{controller_web_port}"
            f"{ryu_constants.RYU.START_PRODUCER_HTTP_RESOURCE}",
            data=json.dumps({ryu_constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: kafka_ip,
                             ryu_constants.KAFKA.TIME_STEP_LEN_SECONDS: time_step_len}))
        assert response.status_code == 200
        Logger.__call__().get_logger().info("Kafka producer started successfully")

    @staticmethod
    def stop_controller_producer(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Stops the Kafka producer at the SDN controller

        :param emulation_env_config: the emulation env config
        :return: None
        """
        if emulation_env_config.sdn_controller_config is None:
            return
        Logger.__call__().get_logger().info("Sends request to the SDN controller to stop the Kafka producer"
                                            " for telemetry")
        response = requests.post(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                 f"{emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                 f"{emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                 f"{ryu_constants.RYU.STOP_PRODUCER_HTTP_RESOURCE}")
        assert response.status_code == 200
        Logger.__call__().get_logger().info("Kafka producer stopped successfully")

    @staticmethod
    def get_controller_producer_status(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Gets the status of the Kafka producer at the SDN controller

        :param emulation_env_config: the emulation env config
        :return: None
        """
        if emulation_env_config.sdn_controller_config is None:
            return
        Logger.__call__().get_logger().info("Sends request for the status of the Kafka producer at the SDN controller")
        response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                f"{emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                f"{emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                f"{ryu_constants.RYU.STATUS_PRODUCER_HTTP_RESOURCE}")
        assert response.status_code == 200
        Logger.__call__().get_logger().info(f"Kafka producer status: {response.content}")
