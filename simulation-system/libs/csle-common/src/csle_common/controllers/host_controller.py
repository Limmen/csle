import logging
from typing import List, Tuple
import grpc
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.host_managers_info import HostManagersInfo
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
import csle_common.constants.constants as constants
import csle_collector.host_manager.host_manager_pb2_grpc
import csle_collector.host_manager.host_manager_pb2
import csle_collector.host_manager.query_host_manager
import csle_collector.host_manager.host_manager_util
from csle_common.util.emulation_util import EmulationUtil
from csle_common.logging.log import Logger


class HostController:
    """
    Class controlling host managers and host specific configurations
    """

    @staticmethod
    def start_host_managers(emulation_env_config: EmulationEnvConfig, logger: logging.Logger) -> None:
        """
        Utility method for checking if the host manager is running and starting it if it is not running

        :param emulation_env_config: the emulation env config
        :param logger: the logger to use for logging
        :return: None
        """

        # Start host managers on emulation containers
        for c in emulation_env_config.containers_config.containers:
            # Connect
            HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=c.docker_gw_bridge_ip,
                                              logger=logger)

        # Start host manager on kafka container
        HostController.start_host_manager(emulation_env_config=emulation_env_config,
                                          ip=emulation_env_config.kafka_config.container.docker_gw_bridge_ip,
                                          logger=logger)

        # Start host manager on ELK container
        HostController.start_host_manager(emulation_env_config=emulation_env_config,
                                          ip=emulation_env_config.elk_config.container.docker_gw_bridge_ip,
                                          logger=logger)

        if emulation_env_config.sdn_controller_config is not None:
            # Start host manager on SDN controller container
            HostController.start_host_manager(
                emulation_env_config=emulation_env_config,
                ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def start_host_manager(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) -> None:
        """
        Utility method for starting the host manager on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)

        # Check if host_manager is already running
        cmd = (constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP +
               constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.HOST_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd,
                                                conn=emulation_env_config.get_connection(ip=ip))

        if constants.COMMANDS.SEARCH_HOST_MANAGER not in str(o):
            logger.info(f"Host manager is not running on: {ip}, starting it. Output of {cmd} was: {str(o)}, "
                        f"err output was: {str(e)}")

            # Stop old background job if running
            cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
                   constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.HOST_MANAGER_FILE_NAME)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd,
                                                    conn=emulation_env_config.get_connection(ip=ip))

            # Start the host_manager
            cmd = constants.COMMANDS.START_HOST_MANAGER.format(
                emulation_env_config.host_manager_config.host_manager_port,
                emulation_env_config.host_manager_config.host_manager_log_dir,
                emulation_env_config.host_manager_config.host_manager_log_file,
                emulation_env_config.host_manager_config.host_manager_max_workers)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd,
                                                    conn=emulation_env_config.get_connection(ip=ip))
            time.sleep(5)

    @staticmethod
    def stop_host_managers(emulation_env_config: EmulationEnvConfig, physical_host_ip: str) -> None:
        """
        Utility method for stopping host managers

        :param emulation_env_config: the emulation env config
        :param physical_host_ip: the ip of the physical host
        :return: None
        """
        # Stop host manager on emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip == physical_host_ip:
                HostController.stop_host_manager(emulation_env_config=emulation_env_config, ip=c.docker_gw_bridge_ip)

        # Stop host manager on Kafka container
        if emulation_env_config.kafka_config.container.physical_host_ip == physical_host_ip:
            HostController.stop_host_manager(emulation_env_config=emulation_env_config,
                                             ip=emulation_env_config.kafka_config.container.docker_gw_bridge_ip)

        # Stop host manager on ELK container
        if emulation_env_config.elk_config.container.physical_host_ip == physical_host_ip:
            HostController.stop_host_manager(emulation_env_config=emulation_env_config,
                                             ip=emulation_env_config.elk_config.container.docker_gw_bridge_ip)

        if emulation_env_config.sdn_controller_config is not None:
            # Stop host manager on the SDN controller container
            if emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_host_ip:
                HostController.stop_host_manager(
                    emulation_env_config=emulation_env_config,
                    ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip)

    @staticmethod
    def stop_host_manager(emulation_env_config: EmulationEnvConfig, ip: str) -> None:
        """
        Utility method for stopping the host manager on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :return: None
        """
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)

        Logger.__call__().get_logger().info(f"Stopping host manager on node {ip}")

        # Stop old background job if running
        cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
               constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.HOST_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd,
                                                conn=emulation_env_config.get_connection(ip=ip))

    @staticmethod
    def start_host_monitor_threads(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                   logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and the monitor thread

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        # Start host monitor on emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            HostController.start_host_monitor_thread(emulation_env_config=emulation_env_config,
                                                     ip=c.docker_gw_bridge_ip, logger=logger)

        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            # Start host monitor on the Kafka container
            HostController.start_host_monitor_thread(
                emulation_env_config=emulation_env_config,
                ip=emulation_env_config.kafka_config.container.docker_gw_bridge_ip, logger=logger)

        if emulation_env_config.elk_config.container.physical_host_ip == physical_server_ip:
            # Start host monitor on the ELK container
            HostController.start_host_monitor_thread(
                emulation_env_config=emulation_env_config,
                ip=emulation_env_config.elk_config.container.docker_gw_bridge_ip, logger=logger)

        if emulation_env_config.sdn_controller_config is not None and \
                emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
            # Start host monitor on the SDN controller container
            HostController.start_host_monitor_thread(
                emulation_env_config=emulation_env_config,
                ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def start_filebeats(emulation_env_config: EmulationEnvConfig, physical_server_ip: str, logger: logging.Logger,
                        initial_start: bool = False) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and filebeat

        :param emulation_env_config: the emulation env config
        :param initial_start: boolean indicating whether this method is called on emulation initialziation or not
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        # Start filebeat on emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            HostController.start_filebeat(emulation_env_config=emulation_env_config,
                                          ips=[c.docker_gw_bridge_ip] + c.get_ips(),
                                          initial_start=initial_start, logger=logger)

        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            # Start filebeat on the Kafka container
            HostController.start_filebeat(
                emulation_env_config=emulation_env_config,
                ips=([emulation_env_config.kafka_config.container.docker_gw_bridge_ip] +
                     emulation_env_config.kafka_config.container.get_ips()),
                initial_start=initial_start, logger=logger)

        if emulation_env_config.elk_config.container.physical_host_ip == physical_server_ip:
            # Start filebeat on the ELK container
            HostController.start_filebeat(
                emulation_env_config=emulation_env_config,
                ips=([emulation_env_config.elk_config.container.docker_gw_bridge_ip] +
                     emulation_env_config.elk_config.container.get_ips()),
                initial_start=initial_start, logger=logger)

        if emulation_env_config.sdn_controller_config is not None \
                and emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
            # Start filebeat on the SDN controller container
            HostController.start_filebeat(
                emulation_env_config=emulation_env_config,
                ips=([emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip] +
                     emulation_env_config.sdn_controller_config.container.get_ips()),
                initial_start=initial_start, logger=logger)

    @staticmethod
    def start_packetbeats(emulation_env_config: EmulationEnvConfig, physical_server_ip: str, logger: logging.Logger,
                          initial_start: bool = False) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and packetbeat

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param initial_start: boolean indicating whether this method is called on emulation initialziation or not
        :param logger: the logger to use for logging
        :return: None
        """
        # Start packetbeat on emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            HostController.start_packetbeat(
                emulation_env_config=emulation_env_config,
                ips=[c.docker_gw_bridge_ip] + c.get_ips(),
                initial_start=initial_start, logger=logger)

        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            # Start packetbeat on the Kafka container
            HostController.start_packetbeat(
                emulation_env_config=emulation_env_config,
                ips=([emulation_env_config.kafka_config.container.docker_gw_bridge_ip] +
                     emulation_env_config.kafka_config.container.get_ips()),
                initial_start=initial_start, logger=logger)

        if emulation_env_config.elk_config.container.physical_host_ip == physical_server_ip:
            # Start packetbeat on the ELK container
            HostController.start_packetbeat(
                emulation_env_config=emulation_env_config,
                ips=([emulation_env_config.elk_config.container.docker_gw_bridge_ip] +
                     emulation_env_config.elk_config.container.get_ips()),
                initial_start=initial_start, logger=logger)

        if emulation_env_config.sdn_controller_config is not None \
                and emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
            # Start packetbeat on the SDN controller container
            HostController.start_packetbeat(
                emulation_env_config=emulation_env_config,
                ips=([emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip] +
                     emulation_env_config.sdn_controller_config.container.get_ips()),
                initial_start=initial_start, logger=logger)

    @staticmethod
    def start_metricbeats(emulation_env_config: EmulationEnvConfig, physical_server_ip: str, logger: logging.Logger,
                          initial_start: bool = False) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and metricbeat

        :param emulation_env_config: the emulation env config
        :param initial_start: boolean indicating whether this method is called on emulation initialization or not
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        # Start packetbeat on emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            HostController.start_metricbeat(
                emulation_env_config=emulation_env_config,
                ips=[c.docker_gw_bridge_ip] + c.get_ips(),
                initial_start=initial_start, logger=logger)

        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            # Start metricbeat on the Kafka container
            HostController.start_metricbeat(
                emulation_env_config=emulation_env_config,
                ips=([emulation_env_config.kafka_config.container.docker_gw_bridge_ip] +
                     emulation_env_config.kafka_config.container.get_ips()),
                initial_start=initial_start, logger=logger)

        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            # Start metricbeat on the ELK container
            HostController.start_metricbeat(
                emulation_env_config=emulation_env_config,
                ips=([emulation_env_config.elk_config.container.docker_gw_bridge_ip] +
                     emulation_env_config.elk_config.container.get_ips()),
                initial_start=initial_start, logger=logger)

        if emulation_env_config.sdn_controller_config is not None \
                and emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
            # Start metricbeat on the SDN controller container
            HostController.start_metricbeat(
                emulation_env_config=emulation_env_config,
                ips=([emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip] +
                     emulation_env_config.sdn_controller_config.container.get_ips()),
                initial_start=initial_start, logger=logger)

    @staticmethod
    def start_heartbeats(emulation_env_config: EmulationEnvConfig, physical_server_ip: str, logger: logging.Logger,
                         initial_start: bool = False) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and heartbeat

        :param emulation_env_config: the emulation env config
        :param initial_start: boolean indicating whether this method is called on emulation initialization or not
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        # Start heartbeat on emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            HostController.start_heartbeat(
                emulation_env_config=emulation_env_config,
                ips=[c.docker_gw_bridge_ip] + c.get_ips(),
                initial_start=initial_start, logger=logger)

        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            # Start heartbeat on the Kafka container
            HostController.start_heartbeat(
                emulation_env_config=emulation_env_config,
                ips=([emulation_env_config.kafka_config.container.docker_gw_bridge_ip] +
                     emulation_env_config.kafka_config.container.get_ips()),
                initial_start=initial_start, logger=logger)

        if emulation_env_config.elk_config.container.physical_host_ip == physical_server_ip:
            # Start heartbeat on the ELK container
            HostController.start_heartbeat(
                emulation_env_config=emulation_env_config,
                ips=([emulation_env_config.elk_config.container.docker_gw_bridge_ip] +
                     emulation_env_config.elk_config.container.get_ips()),
                initial_start=initial_start, logger=logger)

        if emulation_env_config.sdn_controller_config is not None \
                and emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
            # Start heartbeat on the SDN controller container
            HostController.start_heartbeat(
                emulation_env_config=emulation_env_config,
                ips=([emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip] +
                     emulation_env_config.sdn_controller_config.container.get_ips()),
                initial_start=initial_start, logger=logger)

    @staticmethod
    def stop_filebeats(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                       logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and to stop filebeat

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the physical host ip
        :param logger: the logger to use for logging
        :return: None
        """
        # Stop filebeat on emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip == physical_server_ip:
                HostController.stop_filebeat(emulation_env_config=emulation_env_config, ip=c.docker_gw_bridge_ip,
                                             logger=logger)

        # Stop filebeat on the kafka container
        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            HostController.stop_filebeat(emulation_env_config=emulation_env_config,
                                         ip=emulation_env_config.kafka_config.container.docker_gw_bridge_ip,
                                         logger=logger)

        # Stop filebeat on the ELK container
        if emulation_env_config.elk_config.container.physical_host_ip == physical_server_ip:
            HostController.stop_filebeat(emulation_env_config=emulation_env_config,
                                         ip=emulation_env_config.elk_config.container.docker_gw_bridge_ip,
                                         logger=logger)

        if emulation_env_config.sdn_controller_config is not None:
            if emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
                # Stop filebeat on the SDN controller container
                HostController.stop_filebeat(
                    emulation_env_config=emulation_env_config,
                    ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip,
                    logger=logger)

    @staticmethod
    def stop_packetbeats(emulation_env_config: EmulationEnvConfig, logger: logging.Logger,
                         physical_server_ip: str) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and to stop packetbeat

        :param emulation_env_config: the emulation env config
        :param logger: the logger to use for logging
        :param physical_server_ip: the of of the physical host
        :return: None
        """
        # Stop packetbeat on emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip == physical_server_ip:
                HostController.stop_packetbeat(emulation_env_config=emulation_env_config, ip=c.docker_gw_bridge_ip,
                                               logger=logger)

        # Stop packetbeat on the kafka container
        if physical_server_ip == emulation_env_config.kafka_config.container.physical_host_ip:
            HostController.stop_packetbeat(emulation_env_config=emulation_env_config,
                                           ip=emulation_env_config.kafka_config.container.docker_gw_bridge_ip,
                                           logger=logger)

        # Stop packetbeat on the ELK container
        if physical_server_ip == emulation_env_config.elk_config.container.physical_host_ip:
            HostController.stop_packetbeat(emulation_env_config=emulation_env_config,
                                           ip=emulation_env_config.elk_config.container.docker_gw_bridge_ip,
                                           logger=logger)

        if emulation_env_config.sdn_controller_config is not None:
            if emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
                # Stop packetbeat on the SDN controller container
                HostController.stop_packetbeat(
                    emulation_env_config=emulation_env_config,
                    ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip,
                    logger=logger)

    @staticmethod
    def stop_metricbeats(emulation_env_config: EmulationEnvConfig, logger: logging.Logger,
                         physical_server_ip: str) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and to stop metricbeat

        :param emulation_env_config: the emulation env config
        :param logger: the logger to use for logging
        :param physical_server_ip: the physical server ip
        :return: None
        """
        # Stop metricbeat on emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip == physical_server_ip:
                HostController.stop_metricbeat(emulation_env_config=emulation_env_config, ip=c.docker_gw_bridge_ip,
                                               logger=logger)

        # Stop metricbeat on the kafka container
        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            HostController.stop_metricbeat(emulation_env_config=emulation_env_config,
                                           ip=emulation_env_config.kafka_config.container.docker_gw_bridge_ip,
                                           logger=logger)

        # Stop metricbeat on the ELK container
        if emulation_env_config.elk_config.container.physical_host_ip == physical_server_ip:
            HostController.stop_metricbeat(emulation_env_config=emulation_env_config,
                                           ip=emulation_env_config.elk_config.container.docker_gw_bridge_ip,
                                           logger=logger)

        if emulation_env_config.sdn_controller_config is not None:
            if emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
                # Stop metricbeat on the SDN controller container
                HostController.stop_metricbeat(
                    emulation_env_config=emulation_env_config,
                    ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def stop_heartbeats(emulation_env_config: EmulationEnvConfig, logger: logging.Logger,
                        physical_server_ip: str) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and to stop heartbeat

        :param emulation_env_config: the emulation env config
        :param logger: the logger to use for logging
        :param physical_server_ip: the physical server ip
        :return: None
        """
        # Stop heartbeat on emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip == physical_server_ip:
                HostController.stop_heartbeat(emulation_env_config=emulation_env_config,
                                              ip=c.docker_gw_bridge_ip, logger=logger)

        # Stop heartbeat on the kafka container
        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            HostController.stop_heartbeat(emulation_env_config=emulation_env_config,
                                          ip=emulation_env_config.kafka_config.container.docker_gw_bridge_ip,
                                          logger=logger)

        # Stop heartbeat on the ELK container
        if emulation_env_config.elk_config.container.physical_host_ip == physical_server_ip:
            HostController.stop_heartbeat(emulation_env_config=emulation_env_config,
                                          ip=emulation_env_config.elk_config.container.docker_gw_bridge_ip,
                                          logger=logger)

        if emulation_env_config.sdn_controller_config is not None:
            if emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
                # Stop heartbeat on the SDN controller container
                HostController.stop_heartbeat(
                    emulation_env_config=emulation_env_config,
                    ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip,
                    logger=logger)

    @staticmethod
    def config_filebeats(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                         logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and to setup the configuration of filebeat

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        # Configure filebeat on the emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            HostController.config_filebeat(emulation_env_config=emulation_env_config, container=c, logger=logger)

        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            # Configure filebeat on the kafka container
            HostController.config_filebeat(emulation_env_config=emulation_env_config,
                                           container=emulation_env_config.kafka_config.container, logger=logger)

        if emulation_env_config.elk_config.container.physical_host_ip == physical_server_ip:
            # Configure filebeat on the ELK container
            HostController.config_filebeat(emulation_env_config=emulation_env_config,
                                           container=emulation_env_config.elk_config.container, logger=logger)

        if emulation_env_config.sdn_controller_config is not None \
                and emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
            # Configure filebeat on the SDN controller container
            HostController.config_filebeat(emulation_env_config=emulation_env_config,
                                           container=emulation_env_config.sdn_controller_config.container,
                                           logger=logger)

    @staticmethod
    def config_packetbeats(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                           logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and to setup the configuration of packetbeat

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        # Configure packetbeat on the emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            HostController.config_packetbeat(emulation_env_config=emulation_env_config, container=c, logger=logger)

        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            # Configure packetbeat on the kafka container
            HostController.config_packetbeat(emulation_env_config=emulation_env_config,
                                             container=emulation_env_config.kafka_config.container, logger=logger)

        if emulation_env_config.elk_config.container.physical_host_ip == physical_server_ip:
            # Configure packetbeat on the ELK container
            HostController.config_packetbeat(emulation_env_config=emulation_env_config,
                                             container=emulation_env_config.elk_config.container, logger=logger)

        if emulation_env_config.sdn_controller_config is not None \
                and emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
            # Configure packetbeat on the SDN controller container
            HostController.config_packetbeat(emulation_env_config=emulation_env_config,
                                             container=emulation_env_config.sdn_controller_config.container,
                                             logger=logger)

    @staticmethod
    def config_metricbeats(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                           logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and to setup the configuration of metricbeat

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        # Configure metricbeat on the emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            HostController.config_metricbeat(emulation_env_config=emulation_env_config, container=c, logger=logger)

        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            # Configure metricbeat on the kafka container
            HostController.config_metricbeat(emulation_env_config=emulation_env_config,
                                             container=emulation_env_config.kafka_config.container, logger=logger)

        if emulation_env_config.elk_config.container.physical_host_ip == physical_server_ip:
            # Configure metricbeat on the ELK container
            HostController.config_metricbeat(emulation_env_config=emulation_env_config,
                                             container=emulation_env_config.elk_config.container, logger=logger)

        if emulation_env_config.sdn_controller_config is not None \
                and emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
            # Configure metricbeat on the SDN controller container
            HostController.config_metricbeat(emulation_env_config=emulation_env_config,
                                             container=emulation_env_config.sdn_controller_config.container,
                                             logger=logger)

    @staticmethod
    def config_heartbeats(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                          logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and to setup the configuration of heartbeat

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        # Configure heartbeat on the emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            HostController.config_heartbeat(emulation_env_config=emulation_env_config, container=c, logger=logger)

        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            # Configure heartbeat on the kafka container
            HostController.config_heartbeat(emulation_env_config=emulation_env_config,
                                            container=emulation_env_config.kafka_config.container, logger=logger)

        if emulation_env_config.elk_config.container.physical_host_ip == physical_server_ip:
            # Configure heartbeat on the ELK container
            HostController.config_heartbeat(emulation_env_config=emulation_env_config,
                                            container=emulation_env_config.elk_config.container, logger=logger)

        if emulation_env_config.sdn_controller_config is not None \
                and emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
            # Configure heartbeat on the SDN controller container
            HostController.config_heartbeat(emulation_env_config=emulation_env_config,
                                            container=emulation_env_config.sdn_controller_config.container,
                                            logger=logger)

    @staticmethod
    def start_host_monitor_thread(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on a specific IP
        to start the Host manager and the monitor thread

        :param emulation_env_config: the emulation env config
        :param ip: IP of the container
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=ip, logger=logger)

        host_monitor_dto = HostController.get_host_monitor_thread_status_by_port_and_ip(
            ip=ip, port=emulation_env_config.host_manager_config.host_manager_port)
        if not host_monitor_dto.monitor_running:
            logger.info(f"Host monitor thread is not running on {ip}, starting it.")
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{ip}:{emulation_env_config.host_manager_config.host_manager_port}',
                    options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                csle_collector.host_manager.query_host_manager.start_host_monitor(
                    stub=stub, kafka_ip=emulation_env_config.kafka_config.container.get_ips()[0],
                    kafka_port=emulation_env_config.kafka_config.kafka_port,
                    time_step_len_seconds=emulation_env_config.kafka_config.time_step_len_seconds)

    @staticmethod
    def start_filebeat(emulation_env_config: EmulationEnvConfig, ips: List[str], logger: logging.Logger,
                       initial_start: bool = False) -> None:
        """
        A method that sends a request to the HostManager on a specific IP
        to start the Host manager and filebeat

        :param emulation_env_config: the emulation env config
        :param ips: IP of the container
        :param initial_start: boolean indicating whether this method is called on emulation initialization or not
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=ips[0], logger=logger)
        if initial_start:
            node_beats_config = emulation_env_config.beats_config.get_node_beats_config_by_ips(ips=ips)
            if node_beats_config is None or not node_beats_config.start_filebeat_automatically:
                return
        host_monitor_dto = HostController.get_host_monitor_thread_status_by_port_and_ip(
            ip=ips[0], port=emulation_env_config.host_manager_config.host_manager_port)
        if not host_monitor_dto.filebeat_running:
            logger.info(f"Filebeat is not running on {ips[0]}, starting it.")
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{ips[0]}:{emulation_env_config.host_manager_config.host_manager_port}',
                    options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                csle_collector.host_manager.query_host_manager.start_filebeat(stub=stub)

    @staticmethod
    def start_packetbeat(emulation_env_config: EmulationEnvConfig, ips: List[str],
                         logger: logging.Logger, initial_start: bool = False) -> None:
        """
        A method that sends a request to the HostManager on a specific IP
        to start the Host manager and packetbeat

        :param emulation_env_config: the emulation env config
        :param ips: IP of the container
        :param initial_start: boolean indicating whether this method is called on emulation initialization or not
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=ips[0], logger=logger)
        if initial_start:
            node_beats_config = emulation_env_config.beats_config.get_node_beats_config_by_ips(ips=ips)
            if node_beats_config is None or not node_beats_config.start_packetbeat_automatically:
                return
        host_monitor_dto = HostController.get_host_monitor_thread_status_by_port_and_ip(
            ip=ips[0], port=emulation_env_config.host_manager_config.host_manager_port)
        if not host_monitor_dto.packetbeat_running:
            logger.info(
                f"Packetbeat is not running on {ips[0]}, starting it.")
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{ips[0]}:{emulation_env_config.host_manager_config.host_manager_port}',
                    options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                csle_collector.host_manager.query_host_manager.start_packetbeat(stub=stub)

    @staticmethod
    def start_metricbeat(emulation_env_config: EmulationEnvConfig, ips: List[str],
                         logger: logging.Logger, initial_start: bool = False) -> None:
        """
        A method that sends a request to the HostManager on a specific IP
        to start the Host manager and metricbeat

        :param emulation_env_config: the emulation env config
        :param ips: IP of the container
        :param initial_start: boolean indicating whether this method is called on emulation initialization or not
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=ips[0], logger=logger)
        if initial_start:
            node_beats_config = emulation_env_config.beats_config.get_node_beats_config_by_ips(ips=ips)
            if node_beats_config is None or not node_beats_config.start_metricbeat_automatically:
                return
        host_monitor_dto = HostController.get_host_monitor_thread_status_by_port_and_ip(
            ip=ips[0], port=emulation_env_config.host_manager_config.host_manager_port)
        if not host_monitor_dto.metricbeat_running:
            logger.info(
                f"Metricbeat is not running on {ips[0]}, starting it.")
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{ips[0]}:{emulation_env_config.host_manager_config.host_manager_port}',
                    options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                csle_collector.host_manager.query_host_manager.start_metricbeat(stub=stub)

    @staticmethod
    def start_heartbeat(emulation_env_config: EmulationEnvConfig, ips: List[str],
                        logger: logging.Logger,
                        initial_start: bool = False) -> None:
        """
        A method that sends a request to the HostManager on a specific IP
        to start the Host manager and heartbeat

        :param emulation_env_config: the emulation env config
        :param ips: IPs of the container
        :param initial_start: boolean indicating whether this method is called on emulation initialization or not
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=ips[0], logger=logger)
        if initial_start:
            node_beats_config = emulation_env_config.beats_config.get_node_beats_config_by_ips(ips=ips)
            if node_beats_config is None or not node_beats_config.start_heartbeat_automatically:
                return
        host_monitor_dto = HostController.get_host_monitor_thread_status_by_port_and_ip(
            ip=ips[0], port=emulation_env_config.host_manager_config.host_manager_port)
        if not host_monitor_dto.heartbeat_running:
            logger.info(
                f"Heartbeat is not running on {ips[0]}, starting it.")
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{ips[0]}:{emulation_env_config.host_manager_config.host_manager_port}',
                    options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                csle_collector.host_manager.query_host_manager.start_heartbeat(stub=stub)

    @staticmethod
    def start_sparks(emulation_env_config: EmulationEnvConfig, physical_server_ip: str, logger: logging.Logger) -> None:
        """
        Utility function for starting Spark on compute nodes

        :param emulation_config: the emulation env configuration
        :param physical_server_ip: the ip of the phsyical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.SPARK_IMAGES:
                if ids_image in c.name:
                    logger.info(f"Starting Spark on IP: {c.docker_gw_bridge_ip}")
                    HostController.start_spark(emulation_env_config=emulation_env_config, ips=[c.docker_gw_bridge_ip],
                                               logger=logger)

    @staticmethod
    def stop_sparks(emulation_env_config: EmulationEnvConfig, physical_server_ip: str, logger: logging.Logger) -> None:
        """
        Utility function for stopping Spark on compute nodes

        :param emulation_config: the emulation env configuration
        :param physical_server_ip: the ip of the phsyical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.SPARK_IMAGES:
                if ids_image in c.name:
                    logger.info(f"Stopping Spark on IP: {c.docker_gw_bridge_ip}")
                    HostController.stop_spark(emulation_env_config=emulation_env_config,
                                              ips=[c.docker_gw_bridge_ip], logger=logger)

    @staticmethod
    def start_spark(emulation_env_config: EmulationEnvConfig, ips: List[str], logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on a specific IP
        to start the Host manager and spark

        :param emulation_env_config: the emulation env config
        :param ips: IPs of the container
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=ips[0], logger=logger)
        # Open a gRPC session
        with grpc.insecure_channel(
                f'{ips[0]}:{emulation_env_config.host_manager_config.host_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
            csle_collector.host_manager.query_host_manager.start_spark(stub=stub)

    @staticmethod
    def stop_spark(emulation_env_config: EmulationEnvConfig, ips: List[str], logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on a specific IP
        to stop spark

        :param emulation_env_config: the emulation env config
        :param ips: IPs of the container
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=ips[0], logger=logger)
        # Open a gRPC session
        with grpc.insecure_channel(
                f'{ips[0]}:{emulation_env_config.host_manager_config.host_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
            csle_collector.host_manager.query_host_manager.stop_spark(stub=stub)

    @staticmethod
    def config_filebeat(emulation_env_config: EmulationEnvConfig, container: NodeContainerConfig,
                        logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on a specific container
        to setup the filebeat configuration

        :param emulation_env_config: the emulation env config
        :param container: the container
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=container.docker_gw_bridge_ip,
                                          logger=logger)
        node_beats_config = emulation_env_config.beats_config.get_node_beats_config_by_ips(ips=container.get_ips())
        if node_beats_config is None:
            return
        kafka_topics = list(map(lambda topic: topic.name, emulation_env_config.kafka_config.topics))

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{container.docker_gw_bridge_ip}:'
                f'{emulation_env_config.host_manager_config.host_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
            logger.info(f"Configuring filebeat on {container.docker_gw_bridge_ip}, {container.get_full_name()}, "
                        f"ips: {container.get_ips()}")
            csle_collector.host_manager.query_host_manager.config_filebeat(
                stub=stub, log_files_paths=node_beats_config.log_files_paths,
                kibana_ip=emulation_env_config.elk_config.container.get_ips()[0],
                kibana_port=emulation_env_config.elk_config.kibana_port,
                elastic_ip=emulation_env_config.elk_config.container.get_ips()[0],
                elastic_port=emulation_env_config.elk_config.elastic_port,
                num_elastic_shards=emulation_env_config.beats_config.num_elastic_shards, kafka_topics=kafka_topics,
                kafka_ip=emulation_env_config.kafka_config.container.get_ips()[0],
                kafka_port=emulation_env_config.kafka_config.kafka_port,
                filebeat_modules=node_beats_config.filebeat_modules,
                reload_enabled=emulation_env_config.beats_config.reload_enabled,
                kafka=node_beats_config.kafka_input)

    @staticmethod
    def config_packetbeat(emulation_env_config: EmulationEnvConfig, container: NodeContainerConfig,
                          logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on a specific container
        to setup the packetbeat configuration

        :param emulation_env_config: the emulation env config
        :param container: the container
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=container.docker_gw_bridge_ip,
                                          logger=logger)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{container.docker_gw_bridge_ip}:'
                f'{emulation_env_config.host_manager_config.host_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
            logger.info(f"Configuring packetbeat on {container.docker_gw_bridge_ip}, {container.get_full_name()}, "
                        f"ips: {container.get_ips()}")
            csle_collector.host_manager.query_host_manager.config_packetbeat(
                stub=stub, kibana_ip=emulation_env_config.elk_config.container.get_ips()[0],
                kibana_port=emulation_env_config.elk_config.kibana_port,
                elastic_ip=emulation_env_config.elk_config.container.get_ips()[0],
                elastic_port=emulation_env_config.elk_config.elastic_port,
                num_elastic_shards=emulation_env_config.beats_config.num_elastic_shards)

    @staticmethod
    def config_metricbeat(emulation_env_config: EmulationEnvConfig, container: NodeContainerConfig,
                          logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on a specific container
        to setup the metricbeat configuration

        :param emulation_env_config: the emulation env config
        :param container: the container
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=container.docker_gw_bridge_ip,
                                          logger=logger)
        node_beats_config = emulation_env_config.beats_config.get_node_beats_config_by_ips(ips=container.get_ips())
        if node_beats_config is None:
            return

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{container.docker_gw_bridge_ip}:'
                f'{emulation_env_config.host_manager_config.host_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
            logger.info(f"Configuring metricbeat on {container.docker_gw_bridge_ip}, {container.get_full_name()}, "
                        f"ips: {container.get_ips()}")
            csle_collector.host_manager.query_host_manager.config_metricbeat(
                stub=stub, kibana_ip=emulation_env_config.elk_config.container.get_ips()[0],
                kibana_port=emulation_env_config.elk_config.kibana_port,
                elastic_ip=emulation_env_config.elk_config.container.get_ips()[0],
                elastic_port=emulation_env_config.elk_config.elastic_port,
                num_elastic_shards=emulation_env_config.beats_config.num_elastic_shards,
                kafka_ip=emulation_env_config.kafka_config.container.get_ips()[0],
                kafka_port=emulation_env_config.kafka_config.kafka_port,
                metricbeat_modules=node_beats_config.metricbeat_modules,
                reload_enabled=emulation_env_config.beats_config.reload_enabled)

    @staticmethod
    def config_heartbeat(emulation_env_config: EmulationEnvConfig, container: NodeContainerConfig,
                         logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on a specific container
        to setup the heartbeat configuration

        :param emulation_env_config: the emulation env config
        :param container: the container
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=container.docker_gw_bridge_ip,
                                          logger=logger)
        node_beats_config = emulation_env_config.beats_config.get_node_beats_config_by_ips(ips=container.get_ips())
        if node_beats_config is None:
            return

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{container.docker_gw_bridge_ip}:'
                f'{emulation_env_config.host_manager_config.host_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
            logger.info(f"Configuring heartbeat on {container.docker_gw_bridge_ip}, {container.get_full_name()}, "
                        f"ips: {container.get_ips()}")
            csle_collector.host_manager.query_host_manager.config_heartbeat(
                stub=stub, kibana_ip=emulation_env_config.elk_config.container.get_ips()[0],
                kibana_port=emulation_env_config.elk_config.kibana_port,
                elastic_ip=emulation_env_config.elk_config.container.get_ips()[0],
                elastic_port=emulation_env_config.elk_config.elastic_port,
                num_elastic_shards=emulation_env_config.beats_config.num_elastic_shards,
                hosts_to_monitor=node_beats_config.heartbeat_hosts_to_monitor)

    @staticmethod
    def stop_host_monitor_threads(emulation_env_config: EmulationEnvConfig, logger: logging.Logger,
                                  physical_host_ip: str) -> None:
        """
        A method that sends a request to the HostManager on every container to stop the monitor threads

        :param emulation_env_config: the emulation env config
        :param physical_host_ip: the IP of the physical host
        :param logger: the logger to use for logging
        :return: None
        """
        # Stop host monitor threads on emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip == physical_host_ip:
                HostController.stop_host_monitor_thread(emulation_env_config=emulation_env_config,
                                                        ip=c.docker_gw_bridge_ip, logger=logger)
        if emulation_env_config.kafka_config.container.physical_host_ip == physical_host_ip:
            # Stop host monitor threads on the kafka container
            HostController.stop_host_monitor_thread(emulation_env_config=emulation_env_config,
                                                    ip=emulation_env_config.kafka_config.container.docker_gw_bridge_ip,
                                                    logger=logger)

        if emulation_env_config.elk_config.container.physical_host_ip == physical_host_ip:
            # Stop host monitor threads on the ELK container
            HostController.stop_host_monitor_thread(emulation_env_config=emulation_env_config,
                                                    ip=emulation_env_config.elk_config.container.docker_gw_bridge_ip,
                                                    logger=logger)

        if emulation_env_config.sdn_controller_config is not None:
            if emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_host_ip:
                # Stop host monitor threads on the SDN controller container
                HostController.stop_host_monitor_thread(
                    emulation_env_config=emulation_env_config,
                    ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def stop_host_monitor_thread(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on a specific container to stop the monitor threads

        :param emulation_env_config: the emulation env config
        :param ip: the IP of the container
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=ip, logger=logger)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{ip}:'
                f'{emulation_env_config.host_manager_config.host_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
            logger.info(f"Stopping the Host monitor thread on {ip}.")
            csle_collector.host_manager.query_host_manager.stop_host_monitor(stub=stub)

    @staticmethod
    def stop_filebeat(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on a specific container to stop filebeat

        :param emulation_env_config: the emulation env config
        :param ip: the IP of the container
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=ip, logger=logger)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{ip}:'
                f'{emulation_env_config.host_manager_config.host_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
            logger.info(f"Stopping filebeat on {ip}.")
            csle_collector.host_manager.query_host_manager.stop_filebeat(stub=stub)

    @staticmethod
    def stop_packetbeat(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on a specific container to stop packetbeat

        :param emulation_env_config: the emulation env config
        :param ip: the IP of the container
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=ip, logger=logger)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{ip}:'
                f'{emulation_env_config.host_manager_config.host_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
            logger.info(f"Stopping packetbeat on {ip}.")
            csle_collector.host_manager.query_host_manager.stop_packetbeat(stub=stub)

    @staticmethod
    def stop_metricbeat(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on a specific container to stop metricbeat

        :param emulation_env_config: the emulation env config
        :param ip: the IP of the container
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=ip, logger=logger)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{ip}:'
                f'{emulation_env_config.host_manager_config.host_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
            logger.info(f"Stopping metricbeat on {ip}.")
            csle_collector.host_manager.query_host_manager.stop_metricbeat(stub=stub)

    @staticmethod
    def stop_heartbeat(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) -> None:
        """
        A method that sends a request to the HostManager on a specific container to stop heartbeat

        :param emulation_env_config: the emulation env config
        :param ip: the IP of the container
        :param logger: the logger to use for logging
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=ip, logger=logger)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{ip}:'
                f'{emulation_env_config.host_manager_config.host_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
            logger.info(f"Stopping heartbeat on {ip}.")
            csle_collector.host_manager.query_host_manager.stop_heartbeat(stub=stub)

    @staticmethod
    def get_host_monitor_threads_statuses(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                          logger: logging.Logger) -> \
            List[Tuple[csle_collector.host_manager.host_manager_pb2.HostStatusDTO, str]]:
        """
        A method that sends a request to the HostManager on every container to get the status of the Host monitor thread

        :param emulation_env_config: the emulation config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: List of monitor thread statuses
        """
        statuses = []
        HostController.start_host_managers(emulation_env_config=emulation_env_config, logger=logger)

        # Get statuses of emulation containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip == physical_server_ip:
                status = HostController.get_host_monitor_thread_status_by_port_and_ip(
                    ip=c.docker_gw_bridge_ip, port=emulation_env_config.host_manager_config.host_manager_port)
                statuses.append((status, c.docker_gw_bridge_ip))

        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            # Get status of kafka container
            status = HostController.get_host_monitor_thread_status_by_port_and_ip(
                ip=emulation_env_config.kafka_config.container.docker_gw_bridge_ip,
                port=emulation_env_config.host_manager_config.host_manager_port)
            statuses.append((status, emulation_env_config.kafka_config.container.docker_gw_bridge_ip))

        if emulation_env_config.elk_config.container.physical_host_ip == physical_server_ip:
            # Get status of ELK container
            status = HostController.get_host_monitor_thread_status_by_port_and_ip(
                ip=emulation_env_config.elk_config.container.docker_gw_bridge_ip,
                port=emulation_env_config.host_manager_config.host_manager_port)
            statuses.append((status, emulation_env_config.elk_config.container.docker_gw_bridge_ip))

        if emulation_env_config.sdn_controller_config is not None:
            if emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
                # Get status of SDN controller container
                status = HostController.get_host_monitor_thread_status_by_port_and_ip(
                    ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip,
                    port=emulation_env_config.host_manager_config.host_manager_port)
                statuses.append((status, emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip))

        return statuses

    @staticmethod
    def get_host_monitor_thread_status_by_port_and_ip(ip: str, port: int) -> \
            csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        A method that sends a request to the HostManager on a specific container
        to get the status of the Host monitor thread

        :param ip: the ip of the container
        :param port: the port of the host manager
        :return: the status of the host manager
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
            status = csle_collector.host_manager.query_host_manager.get_host_status(stub=stub)
            return status

    @staticmethod
    def get_host_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the ips of the Host managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        ips = []

        # Get ips of emulation containers
        for c in emulation_env_config.containers_config.containers:
            ips.append(c.docker_gw_bridge_ip)

        # Get ip of Kafka container
        ips.append(emulation_env_config.kafka_config.container.docker_gw_bridge_ip)

        # Get ip of ELK container
        ips.append(emulation_env_config.elk_config.container.docker_gw_bridge_ip)

        if emulation_env_config.sdn_controller_config is not None:
            # Get ip of SDN controller container
            ips.append(emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip)

        return ips

    @staticmethod
    def get_host_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the Host managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of ports
        """
        ports = []

        # Get port of emulation containers
        for c in emulation_env_config.containers_config.containers:
            ports.append(emulation_env_config.host_manager_config.host_manager_port)

        # Get port of kafka container
        ports.append(emulation_env_config.host_manager_config.host_manager_port)

        # Get port of ELK container
        ports.append(emulation_env_config.host_manager_config.host_manager_port)

        if emulation_env_config.sdn_controller_config is not None:
            # Get port of SDN controller container
            ports.append(emulation_env_config.host_manager_config.host_manager_port)

        return ports

    @staticmethod
    def get_host_managers_info(emulation_env_config: EmulationEnvConfig, active_ips: List[str],
                               logger: logging.Logger, physical_host_ip: str) -> HostManagersInfo:
        """
        Extracts the information of the Host managers for a given emulation

        :param emulation_env_config: the configuration of the emulation
        :param active_ips: list of active IPs
        :param logger: the logger to use for logging
        :param physical_host_ip: the ip of the physical host
        :return: a DTO with the status of the Host managers
        """
        host_managers_ips = HostController.get_host_managers_ips(emulation_env_config=emulation_env_config)
        host_managers_ports = HostController.get_host_managers_ports(emulation_env_config=emulation_env_config)
        host_managers_statuses = []
        host_managers_running = []
        for ip in host_managers_ips:
            if ip not in active_ips or not EmulationUtil.physical_ip_match(
                    emulation_env_config=emulation_env_config, ip=ip, physical_host_ip=physical_host_ip):
                continue
            status = None
            running = False
            try:
                status = HostController.get_host_monitor_thread_status_by_port_and_ip(
                    port=emulation_env_config.host_manager_config.host_manager_port, ip=ip)
                running = True
            except Exception as e:
                logger.debug(f"Could not fetch Host manager status on IP:{ip}, error: {str(e)}, {repr(e)}")
            if status is not None:
                host_managers_statuses.append((status, ip))
            else:
                host_managers_statuses.append(
                    csle_collector.host_manager.host_manager_util.HostManagerUtil.host_monitor_dto_empty())
            host_managers_running.append(running)
        execution_id = emulation_env_config.execution_id
        emulation_name = emulation_env_config.name
        host_manager_info_dto = HostManagersInfo(host_managers_running=host_managers_running, ips=host_managers_ips,
                                                 execution_id=execution_id, emulation_name=emulation_name,
                                                 host_managers_statuses=host_managers_statuses,
                                                 ports=host_managers_ports)
        return host_manager_info_dto
