import logging
from typing import List
import grpc
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.ossec_managers_info import OSSECIDSManagersInfo
import csle_common.constants.constants as constants
import csle_collector.constants.constants as csle_collector_constants
import csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc
import csle_collector.ossec_ids_manager.ossec_ids_manager_pb2
import csle_collector.ossec_ids_manager.query_ossec_ids_manager
import csle_collector.ossec_ids_manager.ossec_ids_manager_util
from csle_common.util.emulation_util import EmulationUtil
from csle_common.logging.log import Logger


class OSSECIDSController:
    """
    Class controlling OSSEC IDS running on nodes in the emulations, as well as OSSECIDS managers
    """

    @staticmethod
    def stop_ossec_idses(emulation_env_config: EmulationEnvConfig, physical_host_ip: str) -> None:
        """
        Utility function for stopping the OSSEC IDSes

        :param emulation_config: the emulation env configuration
        :param physical_host_ip: the physical host ip
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_host_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    OSSECIDSController.stop_ossec_ids(emulation_env_config=emulation_env_config,
                                                      ip=c.docker_gw_bridge_ip)

    @staticmethod
    def start_ossec_idses(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                          logger: logging.Logger) -> None:
        """
        Utility function for starting the OSSEC IDSes

        :param emulation_config: the emulation env configuration
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    logger.info(f"Starting the OSSEC IDS on ip: {c.docker_gw_bridge_ip}")
                    OSSECIDSController.start_ossec_ids(emulation_env_config=emulation_env_config,
                                                       ip=c.docker_gw_bridge_ip)

    @staticmethod
    def start_ossec_ids(emulation_env_config: EmulationEnvConfig, ip: str) -> None:
        """
        Utility function for starting a OSSEC IDS with a specific IP

        :param emulation_config: the emulation env configuration
        :param ip: the IP of the node where the OSSEC IDS should be started
        :return: None
        """
        OSSECIDSController.start_ossec_ids_manager(emulation_env_config=emulation_env_config, ip=ip)
        ids_monitor_dto = OSSECIDSController.get_ossec_ids_monitor_thread_status_by_ip_and_port(
            port=emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port, ip=ip)
        if not ids_monitor_dto.ossec_ids_running:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{ip}:'
                    f'{emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port}',
                    options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
                stub = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub(channel)
                Logger.__call__().get_logger().info(
                    f"Starting OSSEC IDS on {ip}.")
                csle_collector.ossec_ids_manager.query_ossec_ids_manager.start_ossec_ids(stub=stub)

    @staticmethod
    def stop_ossec_ids(emulation_env_config: EmulationEnvConfig, ip: str) -> None:
        """
        Utility function for stopping an OSSEC IDS with a specific IP

        :param emulation_config: the emulation env configuration
        :param ip: the IP of the node where the OSSEC IDS should be stopped
        :return: None
        """
        OSSECIDSController.start_ossec_ids_manager(emulation_env_config=emulation_env_config, ip=ip)
        ids_monitor_dto = OSSECIDSController.get_ossec_ids_monitor_thread_status_by_ip_and_port(
            port=emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port, ip=ip)
        if ids_monitor_dto.ossec_ids_running:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{ip}:'
                    f'{emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port}',
                    options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
                stub = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub(channel)
                Logger.__call__().get_logger().info(
                    f"Stopping OSSEC IDS on {ip}.")
                csle_collector.ossec_ids_manager.query_ossec_ids_manager.stop_ossec_ids(stub=stub)

    @staticmethod
    def start_ossec_idses_managers(emulation_env_config: EmulationEnvConfig, physical_server_ip: str) -> None:
        """
        Utility method for starting OSSEC IDS managers

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    OSSECIDSController.start_ossec_ids_manager(emulation_env_config=emulation_env_config,
                                                               ip=c.docker_gw_bridge_ip)

    @staticmethod
    def start_ossec_ids_manager(emulation_env_config: EmulationEnvConfig, ip: str) -> None:
        """
        Utility method for starting the OSSEC IDS manager on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :return: None
        """
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)

        # Check if ids_manager is already running
        cmd = (constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP + constants.COMMANDS.SPACE_DELIM +
               constants.TRAFFIC_COMMANDS.OSSEC_IDS_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))

        if constants.COMMANDS.SEARCH_OSSEC_IDS_MANAGER not in str(o):

            Logger.__call__().get_logger().info(f"Starting OSSEC IDS manager on node {ip}")

            # Stop old background job if running
            cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
                   constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.OSSEC_IDS_MANAGER_FILE_NAME)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))

            # Start the OSSEC ids_manager
            cmd = constants.COMMANDS.START_OSSEC_IDS_MANAGER.format(
                emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port,
                emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_log_dir,
                emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_log_file,
                emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_max_workers)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            time.sleep(2)

    @staticmethod
    def stop_ossec_idses_managers(emulation_env_config: EmulationEnvConfig, physical_server_ip: str) -> None:
        """
        Utility method for stopping ossec ids managers

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the IP of the physical host
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    OSSECIDSController.stop_ossec_ids_manager(emulation_env_config=emulation_env_config,
                                                              ip=c.docker_gw_bridge_ip)

    @staticmethod
    def stop_ossec_ids_manager(emulation_env_config: EmulationEnvConfig, ip: str) -> None:
        """
        Utility method for stopping an ossec ids manager with a speicific IP

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :return: None
        """
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)

        Logger.__call__().get_logger().info(f"Stopping OSSEC IDS manager on node {ip}")

        cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
               constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.OSSEC_IDS_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))

        time.sleep(2)

    @staticmethod
    def start_ossec_idses_monitor_threads(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                          logger: logging.Logger) -> None:
        """
        A method that sends a request to the OSSECIDSManager on every container that runs
        an IDS to start the IDS manager and the monitor thread

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        OSSECIDSController.start_ossec_idses_managers(emulation_env_config=emulation_env_config,
                                                      physical_server_ip=physical_server_ip)

        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    logger.info(f"Starting OSSEC IDS monitor thread on IP: {c.docker_gw_bridge_ip}")
                    OSSECIDSController.start_ossec_ids_monitor_thread(emulation_env_config=emulation_env_config,
                                                                      ip=c.docker_gw_bridge_ip)

    @staticmethod
    def start_ossec_ids_monitor_thread(emulation_env_config: EmulationEnvConfig, ip: str) -> None:
        """
        A method that sends a request to the OSSECIDSManager on a specific IP to start
        to start the IDS manager and the monitor thread

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :return: None
        """
        OSSECIDSController.start_ossec_ids_manager(emulation_env_config=emulation_env_config, ip=ip)
        ids_monitor_dto = OSSECIDSController.get_ossec_ids_monitor_thread_status_by_ip_and_port(
            port=emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port, ip=ip)
        if not ids_monitor_dto.monitor_running:
            Logger.__call__().get_logger().info(
                f"OSSEC IDS monitor thread is not running on {ip}, starting it.")
            with grpc.insecure_channel(
                    f'{ip}:'
                    f'{emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port}',
                    options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
                stub = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub(channel)
                csle_collector.ossec_ids_manager.query_ossec_ids_manager.start_ossec_ids_monitor(
                    stub=stub, kafka_ip=emulation_env_config.kafka_config.container.get_ips()[0],
                    kafka_port=emulation_env_config.kafka_config.kafka_port,
                    log_file_path=csle_collector_constants.OSSEC.OSSEC_ALERTS_FILE,
                    time_step_len_seconds=emulation_env_config.kafka_config.time_step_len_seconds)

    @staticmethod
    def stop_ossec_ids_monitor_thread(emulation_env_config: EmulationEnvConfig, ip: str) -> None:
        """
        A method that sends a request to the OSSECIDSManager for a specific IP to stop the monitor threads

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :return: None
        """
        OSSECIDSController.start_ossec_ids_manager(emulation_env_config=emulation_env_config, ip=ip)
        # Open a gRPC session
        with grpc.insecure_channel(
                f'{ip}:'
                f'{emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub(channel)
            Logger.__call__().get_logger().info(
                f"Stopping the OSSEC IDS monitor thread on {ip}.")
            csle_collector.ossec_ids_manager.query_ossec_ids_manager.stop_ossec_ids_monitor(stub=stub)

    @staticmethod
    def stop_ossec_idses_monitor_threads(emulation_env_config: EmulationEnvConfig, physical_server_ip: str) -> None:
        """
        A method that sends a request to the OSSECIDSManager on every container that runs
        an IDS to stop the monitor threads

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    OSSECIDSController.stop_ossec_ids_monitor_thread(emulation_env_config=emulation_env_config,
                                                                     ip=c.docker_gw_bridge_ip)

    @staticmethod
    def get_ossec_idses_monitor_threads_statuses(
            emulation_env_config: EmulationEnvConfig, physical_server_ip: str) \
            -> List[csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO]:
        """
        A method that sends a request to the OSSECIDSManager on every container to get the status of the
        IDS monitor thread

        :param emulation_env_config: the emulation config
        :param physical_server_ip: the IP of the physical server
        :return: List of monitor thread statuses
        """
        statuses = []
        OSSECIDSController.start_ossec_idses_managers(emulation_env_config=emulation_env_config,
                                                      physical_server_ip=physical_server_ip)

        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    status = OSSECIDSController.get_ossec_ids_monitor_thread_status_by_ip_and_port(
                        port=emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port,
                        ip=c.docker_gw_bridge_ip)
                    statuses.append(status)
        return statuses

    @staticmethod
    def get_ossec_idses_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the IPS of the OSSEC IDS managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        ips = []
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    ips.append(c.docker_gw_bridge_ip)
        return ips

    @staticmethod
    def get_ossec_idses_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the OSSEC IDS managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of ports
        """
        ports = []
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    ports.append(emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port)
        return ports

    @staticmethod
    def get_ossec_ids_monitor_thread_status_by_ip_and_port(port: int, ip: str) \
            -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO:
        """
        A method that sends a request to the OSSECIDSManager with a specific port and ip
        to get the status of the IDS monitor thread

        :param port: the port of the OSSECIDSManager
        :param ip: the ip of the OSSECIDSManager
        :return: the status of the OSSECIDSManager
        """
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub(channel)
            status = \
                csle_collector.ossec_ids_manager.query_ossec_ids_manager.get_ossec_ids_monitor_status(stub=stub)
            return status

    @staticmethod
    def get_ossec_managers_info(emulation_env_config: EmulationEnvConfig, active_ips: List[str],
                                logger: logging.Logger, physical_host_ip: str) \
            -> OSSECIDSManagersInfo:
        """
        Extracts the information of the OSSEC IDS managers for a given emulation

        :param emulation_env_config: the configuration of the emulation
        :param active_ips: list of active IPs
        :param physical_host_ip: the physical host ip
        :param logger: the logger to use for logging
        :return: a DTO with the status of the OSSEC IDS managers
        """
        ossec_ids_managers_ips = \
            OSSECIDSController.get_ossec_idses_managers_ips(emulation_env_config=emulation_env_config)
        ossec_ids_managers_ports = \
            OSSECIDSController.get_ossec_idses_managers_ports(emulation_env_config=emulation_env_config)
        ossec_ids_managers_statuses = []
        ossec_ids_managers_running = []
        for ip in ossec_ids_managers_ips:
            if ip not in active_ips or not EmulationUtil.physical_ip_match(
                    emulation_env_config=emulation_env_config, ip=ip, physical_host_ip=physical_host_ip):
                continue
            running = False
            status = None
            try:
                status = OSSECIDSController.get_ossec_ids_monitor_thread_status_by_ip_and_port(
                    port=emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port, ip=ip)
                running = True
            except Exception as e:
                logger.debug(f"Could not fetch OSSEC IDS manager status on IP:{ip}, error: {str(e)}, {repr(e)}")
            if status is not None:
                ossec_ids_managers_statuses.append(status)
            else:
                util = csle_collector.ossec_ids_manager.ossec_ids_manager_util.OSSecManagerUtil
                ossec_ids_managers_statuses.append(util.ossec_ids_monitor_dto_empty())
            ossec_ids_managers_running.append(running)
        execution_id = emulation_env_config.execution_id
        emulation_name = emulation_env_config.name
        ossec_manager_info_dto = OSSECIDSManagersInfo(
            ossec_ids_managers_running=ossec_ids_managers_running, ips=ossec_ids_managers_ips,
            execution_id=execution_id,
            emulation_name=emulation_name, ossec_ids_managers_statuses=ossec_ids_managers_statuses,
            ports=ossec_ids_managers_ports)
        return ossec_manager_info_dto
