import logging
from typing import List
import grpc
import time
import csle_collector.ryu_manager.ryu_manager_pb2_grpc
import csle_collector.ryu_manager.ryu_manager_pb2
import csle_collector.ryu_manager.query_ryu_manager
import csle_collector.ryu_manager.ryu_manager_util
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.ryu_managers_info import RyuManagersInfo
from csle_common.util.emulation_util import EmulationUtil


class SDNControllerManager:
    """
    Class managing interaction with the SDN controller
    """

    @staticmethod
    def start_ryu_manager(emulation_env_config: EmulationEnvConfig, logger: logging.Logger) -> None:
        """
        Utility method for starting the Ryu manager

        :param emulation_env_config: the emulation env config
        :param logger: the logger to use for logging
        :return: None
        """
        if emulation_env_config.sdn_controller_config is None:
            raise ValueError(f"Cannot start ryu manager for emulation without an SDN config. "
                             f"Emulation: {emulation_env_config.name}")
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip,
                                    create_producer=False)

        # Check if ryu_manager is already running
        cmd = (constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP + constants.COMMANDS.SPACE_DELIM +
               constants.TRAFFIC_COMMANDS.RYU_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd,
            conn=emulation_env_config.get_connection(
                ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip))
        logger.info(f"Ryu manager running?, cmd: {cmd}, out:{o.decode()}, err: {e.decode()}")

        if constants.COMMANDS.SEARCH_RYU_MANAGER not in str(o):
            logger.info(
                f"Starting ryu manager on node: "
                f"{emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip}")

            # Stop old background job if running
            cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
                   constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.RYU_MANAGER_FILE_NAME)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd,
                conn=emulation_env_config.get_connection(
                    ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip))

            # Start the ryu_manager
            cmd = constants.COMMANDS.START_RYU_MANAGER.format(
                emulation_env_config.sdn_controller_config.manager_port,
                emulation_env_config.sdn_controller_config.manager_log_dir,
                emulation_env_config.sdn_controller_config.manager_log_file,
                emulation_env_config.sdn_controller_config.manager_max_workers)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd,
                conn=emulation_env_config.get_connection(
                    ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip))
            logger.info(f"Starting the Ryu manager, cmd: {cmd}, out:{o.decode()}, err: {e.decode()}")
            time.sleep(2)

    @staticmethod
    def stop_ryu_manager(emulation_env_config: EmulationEnvConfig, logger: logging.Logger) -> None:
        """
        Utility method for stopping the Ryu manager

        :param emulation_env_config: the emulation env config
        :param logger: the logger to use for logging
        :return: None
        """
        if emulation_env_config.sdn_controller_config is None:
            raise ValueError(f"Cannot stop ryu manager for emulation without an SDN config. "
                             f"Emulation: {emulation_env_config.name}")
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip,
                                    create_producer=False)

        logger.info(
            f"Stopping ryu manager on node: "
            f"{emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip}")

        # Stop background job
        cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
               constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.RYU_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd,
            conn=emulation_env_config.get_connection(
                ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip))
        logger.info(f"Stopping the Ryu manager, cmd: {cmd}, out:{o.decode()}, err: {e.decode()}")
        time.sleep(2)

    @staticmethod
    def get_ryu_status(emulation_env_config: EmulationEnvConfig, logger: logging.Logger) -> \
            csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
        """
        Method for querying the RyuManager about the status of the Ryu SDN controller

        :param emulation_env_config: the emulation config
        :param logger: the logger to use for logging
        :return: a RyuDTO with the status
        """
        if emulation_env_config.sdn_controller_config is None:
            raise ValueError(f"Cannot get ryu status for emulation without an SDN config. "
                             f"Emulation: {emulation_env_config.name}")
        SDNControllerManager.start_ryu_manager(emulation_env_config=emulation_env_config, logger=logger)
        ryu_dto = SDNControllerManager.get_ryu_status_by_port_and_ip(
            ip=emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip,
            port=emulation_env_config.sdn_controller_config.manager_port)
        return ryu_dto

    @staticmethod
    def get_ryu_status_by_port_and_ip(ip: str, port: int) -> csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
        """
        Method for querying the RyuManager about the status of the Ryu SDN controller

        :param ip: the ip where the RyuManager is running
        :param port: the port the RyuManager is listening to
        :return: an RyuDTO with the status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.ryu_manager.ryu_manager_pb2_grpc.RyuManagerStub(channel)
            ryu_dto = csle_collector.ryu_manager.query_ryu_manager.get_ryu_status(stub)
            return ryu_dto

    @staticmethod
    def stop_ryu(emulation_env_config: EmulationEnvConfig, logger: logging.Logger) \
            -> csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
        """
        Method for requesting the RyuManager to stop the RYU SDN controller

        :param emulation_env_config: the emulation env config
        :return: a RyuDTO with the status of the server
        """
        if emulation_env_config.sdn_controller_config is None:
            raise ValueError(f"Cannot stop Ryu for emulation without an SDN config. "
                             f"Emulation: {emulation_env_config.name}")
        logger.info(
            f"Stopping RYU SDN controller on container: "
            f"{emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip}")
        SDNControllerManager.start_ryu_manager(emulation_env_config=emulation_env_config, logger=logger)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip}:'
                f'{emulation_env_config.sdn_controller_config.manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.ryu_manager.ryu_manager_pb2_grpc.RyuManagerStub(channel)
            ryu_dto = csle_collector.ryu_manager.query_ryu_manager.stop_ryu(stub)
            return ryu_dto

    @staticmethod
    def start_ryu(emulation_env_config: EmulationEnvConfig, physical_server_ip: str, logger: logging.Logger) \
            -> csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
        """
        Method for requesting the RyuManager to start the Ryu SDN controller

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: an RyuDTO with the status of the server
        """
        if emulation_env_config.sdn_controller_config is None:
            raise ValueError(f"Cannot start Ryu for emulation without an SDN config. "
                             f"Emulation: {emulation_env_config.name}")
        if emulation_env_config.sdn_controller_config.container.physical_host_ip != physical_server_ip:
            return
        logger.info(
            f"Starting Ryu SDN controller on container: "
            f"{emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip}")
        SDNControllerManager.start_ryu_manager(emulation_env_config=emulation_env_config, logger=logger)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip}:'
                f'{emulation_env_config.sdn_controller_config.manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.ryu_manager.ryu_manager_pb2_grpc.RyuManagerStub(channel)
            logger.info(
                f"Starting RYU, port: {emulation_env_config.sdn_controller_config.controller_port}, "
                f"web_port: {emulation_env_config.sdn_controller_config.controller_web_api_port}, "
                f"controller: {emulation_env_config.sdn_controller_config.controller_module_name}")
            ryu_dto = csle_collector.ryu_manager.query_ryu_manager.start_ryu(
                stub, port=emulation_env_config.sdn_controller_config.controller_port,
                web_port=emulation_env_config.sdn_controller_config.controller_web_api_port,
                controller=emulation_env_config.sdn_controller_config.controller_module_name)
            return ryu_dto

    @staticmethod
    def start_ryu_monitor(emulation_env_config: EmulationEnvConfig, physical_server_ip: str, logger: logging.Logger) \
            -> csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
        """
        Method for requesting the RyuManager to start the Ryu monitor

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: ip of the physical server
        :param logger: the logger to use for logging
        :return: an RyuDTO with the status
        """
        if emulation_env_config.sdn_controller_config is None:
            raise ValueError(f"Cannot start Ryu monitor for emulation without an SDN config. "
                             f"Emulation: {emulation_env_config.name}")
        if emulation_env_config.sdn_controller_config.container.physical_host_ip != physical_server_ip:
            return
        logger.info(
            f"Starting the ryu monitor on container: "
            f"{emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip}")
        SDNControllerManager.start_ryu_manager(emulation_env_config=emulation_env_config, logger=logger)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip}:'
                f'{emulation_env_config.sdn_controller_config.manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.ryu_manager.ryu_manager_pb2_grpc.RyuManagerStub(channel)
            ryu_dto = csle_collector.ryu_manager.query_ryu_manager.start_ryu_monitor(
                stub, kafka_ip=emulation_env_config.kafka_config.container.get_ips()[0],
                kafka_port=emulation_env_config.kafka_config.kafka_port,
                time_step_len=emulation_env_config.sdn_controller_config.time_step_len_seconds)
            return ryu_dto

    @staticmethod
    def stop_ryu_monitor(emulation_env_config: EmulationEnvConfig, logger: logging.Logger) -> \
            csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
        """
        Method for requesting the RyuManager to stop the ryu monitor

        :param emulation_env_config: the emulation env config
        :param logger: the logger to use for logging
        :return: an RyuDTO with the status of the server
        """
        if emulation_env_config.sdn_controller_config is None:
            raise ValueError(f"Cannot stop Ryu monitor for emulation without an SDN config. "
                             f"Emulation: {emulation_env_config.name}")
        logger.info(
            f"Stopping Ryu monitor on container: "
            f"{emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip}")
        SDNControllerManager.start_ryu_manager(emulation_env_config=emulation_env_config, logger=logger)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip}:'
                f'{emulation_env_config.sdn_controller_config.manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.ryu_manager.ryu_manager_pb2_grpc.RyuManagerStub(channel)
            ryu_dto = csle_collector.ryu_manager.query_ryu_manager.stop_ryu_monitor(stub)
            return ryu_dto

    @staticmethod
    def get_ryu_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the IPS of the Ryu managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        if emulation_env_config.sdn_controller_config is None:
            raise ValueError(f"Cannot get Ryu managers IPs for emulation without an SDN config. "
                             f"Emulation: {emulation_env_config.name}")
        return [emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip]

    @staticmethod
    def get_ryu_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the Ryu managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        if emulation_env_config.sdn_controller_config is None:
            raise ValueError(f"Cannot get Ryu managers ports for emulation without an SDN config. "
                             f"Emulation: {emulation_env_config.name}")
        return [emulation_env_config.sdn_controller_config.manager_port]

    @staticmethod
    def get_ryu_managers_info(emulation_env_config: EmulationEnvConfig, active_ips: List[str],
                              logger: logging.Logger, physical_server_ip: str) -> RyuManagersInfo:
        """
        Extracts the information of the Ryu managers for a given emulation

        :param emulation_env_config: the configuration of the emulation
        :param active_ips: list of active IPs
        :param logger: the logger to use for logging
        :param physical_server_ip: the ip of the physical server
        :return: a DTO with the status of the Ryu managers
        """
        if emulation_env_config.sdn_controller_config is None:
            raise ValueError(f"Cannot get ryu managers info for emulation without an SDN config. "
                             f"Emulation: {emulation_env_config.name}")
        ryu_managers_ips = SDNControllerManager.get_ryu_managers_ips(emulation_env_config=emulation_env_config)
        ryu_managers_ports = SDNControllerManager.get_ryu_managers_ports(emulation_env_config=emulation_env_config)
        ryu_managers_statuses = []
        ryu_managers_running = []
        for ip in ryu_managers_ips:
            if ip not in active_ips or not EmulationUtil.physical_ip_match(
                    emulation_env_config=emulation_env_config, ip=ip, physical_host_ip=physical_server_ip):
                continue
            status = None
            try:
                status = SDNControllerManager.get_ryu_status_by_port_and_ip(
                    port=emulation_env_config.sdn_controller_config.manager_port, ip=ip)
                running = True
            except Exception as e:
                running = False
                logger.debug(f"Could not fetch Ryu manager status on IP:{ip}, error: {str(e)}, {repr(e)}")
            if status is not None:
                ryu_managers_statuses.append(status)
            else:
                ryu_managers_statuses.append(csle_collector.ryu_manager.ryu_manager_util.RyuManagerUtil.ryu_dto_empty())
            ryu_managers_running.append(running)
        execution_id = emulation_env_config.execution_id
        emulation_name = emulation_env_config.name
        ryu_manager_info_dto = RyuManagersInfo(
            ryu_managers_running=ryu_managers_running, ips=ryu_managers_ips, execution_id=execution_id,
            emulation_name=emulation_name, ryu_managers_statuses=ryu_managers_statuses, ports=ryu_managers_ports,
            physical_server_ip=emulation_env_config.sdn_controller_config.container.physical_host_ip)
        return ryu_manager_info_dto
