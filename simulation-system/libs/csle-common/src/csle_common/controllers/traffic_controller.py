import logging
from typing import List
import time
import grpc
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
import csle_collector.client_manager.query_clients
import csle_collector.client_manager.client_manager_util
import csle_collector.traffic_manager.traffic_manager_pb2_grpc
import csle_collector.traffic_manager.traffic_manager_pb2
import csle_collector.traffic_manager.query_traffic_manager
import csle_collector.traffic_manager.traffic_manager_util
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.client_managers_info import ClientManagersInfo
from csle_common.dao.emulation_config.node_traffic_config import NodeTrafficConfig
from csle_common.dao.emulation_config.traffic_managers_info import TrafficManagersInfo
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.util.emulation_util import EmulationUtil


class TrafficController:
    """
    Class managing traffic generators in the emulation environments
    """

    @staticmethod
    def start_traffic_managers(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                               logger: logging.Logger) -> None:
        """
        Utility method for checking if the traffic manager is running and starting it if it is not running
        on every node

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:
            if node_traffic_config.physical_host_ip != physical_server_ip:
                continue
            # Connect
            TrafficController.start_traffic_manager(emulation_env_config=emulation_env_config,
                                                    node_traffic_config=node_traffic_config,
                                                    logger=logger)

    @staticmethod
    def start_traffic_manager(emulation_env_config: EmulationEnvConfig,
                              node_traffic_config: NodeTrafficConfig,
                              logger: logging.Logger) -> None:
        """
        Utility method for starting traffic manager on a specific container

        :param emulation_env_config: the emulation env config
        :param node_traffic_config: traffic config of the container
        :param logger: the logger to use for logging
        :return: None
        """
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=node_traffic_config.docker_gw_bridge_ip)

        # Check if traffic_manager is already running
        cmd = (constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP + constants.COMMANDS.SPACE_DELIM
               + constants.TRAFFIC_COMMANDS.TRAFFIC_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd,
                                                conn=emulation_env_config.get_connection(
                                                    ip=node_traffic_config.docker_gw_bridge_ip))

        if constants.COMMANDS.SEARCH_TRAFFIC_MANAGER not in str(o):
            # Stop old background job if running
            cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
                   constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.TRAFFIC_MANAGER_FILE_NAME)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd, conn=emulation_env_config.get_connection(ip=node_traffic_config.docker_gw_bridge_ip))

            # Start the _manager
            cmd = constants.COMMANDS.START_TRAFFIC_MANAGER.format(node_traffic_config.traffic_manager_port,
                                                                  node_traffic_config.traffic_manager_log_dir,
                                                                  node_traffic_config.traffic_manager_log_file,
                                                                  node_traffic_config.traffic_manager_max_workers)
            logger.info(f"Starting traffic manager on node "
                        f"{node_traffic_config.docker_gw_bridge_ip}, with cmd:{cmd}")
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd, conn=emulation_env_config.get_connection(ip=node_traffic_config.docker_gw_bridge_ip))
            time.sleep(2)

    @staticmethod
    def stop_traffic_managers(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                              logger: logging.Logger) -> None:
        """
        Utility method for stopping traffic managers on a given server

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server to stop the traffic managers
        :param logger: the logger to use for logging
        :return: None
        """
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:
            if node_traffic_config.physical_host_ip == physical_server_ip:
                TrafficController.stop_traffic_manager(emulation_env_config=emulation_env_config,
                                                       node_traffic_config=node_traffic_config, logger=logger)

    @staticmethod
    def stop_traffic_manager(emulation_env_config: EmulationEnvConfig, node_traffic_config: NodeTrafficConfig,
                             logger: logging.Logger) -> None:
        """
        Utility method for stopping a specific traffic manager

        :param emulation_env_config: the emulation env config
        :param node_traffic_config: the node traffic configuration
        :param logger: the logger to use for logging
        :return: None
        """
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=node_traffic_config.docker_gw_bridge_ip)
        logger.info(f"Stopping traffic manager on node {node_traffic_config.docker_gw_bridge_ip}")

        # Stop old background job if running
        cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
               constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.TRAFFIC_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd,
                                                conn=emulation_env_config.get_connection(
                                                    ip=node_traffic_config.docker_gw_bridge_ip))

    @staticmethod
    def start_client_manager(emulation_env_config: EmulationEnvConfig, logger: logging.Logger) -> bool:
        """
        Utility method starting the client manager

        :param emulation_env_config: the emulation env config
        :param logger: the logger to use for logging
        :return: True if the client manager was started, False otherwise
        """
        # Connect
        EmulationUtil.connect_admin(
            emulation_env_config=emulation_env_config,
            ip=emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip)

        # Check if client_manager is already running
        cmd = (f"{constants.COMMANDS.PS_AUX} {constants.COMMANDS.PIPE_DELIM} {constants.COMMANDS.GREP} "
               f"{constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME}")
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd,
            conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip))

        if constants.COMMANDS.SEARCH_CLIENT_MANAGER not in str(o):
            logger.info(
                f"Starting client manager on container "
                f"{emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip} "
                f"since it was not running. "
                f"Output of :{cmd}, was: {str(o)}")

            # Stop old background job if running
            cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
                   constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip))

            # Start the client_manager
            cmd = constants.COMMANDS.START_CLIENT_MANAGER.format(
                emulation_env_config.traffic_config.client_population_config.client_manager_port,
                emulation_env_config.traffic_config.client_population_config.client_manager_log_dir,
                emulation_env_config.traffic_config.client_population_config.client_manager_log_file,
                emulation_env_config.traffic_config.client_population_config.client_manager_max_workers
            )
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip))
            time.sleep(2)
            return True
        return False

    @staticmethod
    def stop_client_manager(emulation_env_config: EmulationEnvConfig, logger: logging.Logger) -> None:
        """
        Utility method starting the client manager

        :param emulation_env_config: the emulation env config
        :return: None
        """
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip)

        logger.info(f"Stopping client manager on node "
                    f"{emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip}")

        # Stop old background job if running
        cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
               constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(
            ip=emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip))

    @staticmethod
    def stop_client_population(emulation_env_config: EmulationEnvConfig, logger: logging.Logger) -> None:
        """
        Function for stopping the client arrival process of an emulation

        :param emulation_env_config: the emulation env config
        :param logger: the logger to use for logging
        :return: None
        """
        logger.info(
            f"Stopping client population on container: "
            f"{emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip}")

        TrafficController.start_client_manager(emulation_env_config=emulation_env_config, logger=logger)

        client_dto = TrafficController.get_clients_dto_by_ip_and_port(
            ip=emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip,
            port=emulation_env_config.traffic_config.client_population_config.client_manager_port,
            logger=logger)

        if client_dto.client_process_active:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip}:'
                    f'{emulation_env_config.traffic_config.client_population_config.client_manager_port}',
                    options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
                stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
                csle_collector.client_manager.query_clients.stop_clients(stub)

    @staticmethod
    def start_client_producer(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                              logger: logging.Logger) -> None:
        """
        Starts the Kafka producer for client metrics

        :param emulation_env_config: the emulation environment configuration
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        if emulation_env_config.traffic_config.client_population_config.physical_host_ip != physical_server_ip:
            return
        logger.info(
            f"Starting client producer on container:"
            f" {emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip}")

        client_manager_started = (
            TrafficController.start_client_manager(emulation_env_config=emulation_env_config, logger=logger))

        if client_manager_started:
            # If client manager was started we need to first start the client population
            TrafficController.start_client_population(emulation_env_config=emulation_env_config,
                                                      physical_server_ip=physical_server_ip, logger=logger)

        client_dto = TrafficController.get_clients_dto_by_ip_and_port(
            ip=emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip,
            port=emulation_env_config.traffic_config.client_population_config.client_manager_port,
            logger=logger)
        if not client_dto.producer_active:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip}:'
                    f'{emulation_env_config.traffic_config.client_population_config.client_manager_port}',
                    options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
                stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)

                # Start the producer thread
                csle_collector.client_manager.query_clients.start_producer(
                    stub=stub, ip=emulation_env_config.kafka_config.container.get_ips()[0],
                    port=emulation_env_config.kafka_config.kafka_port,
                    time_step_len_seconds=emulation_env_config.kafka_config.time_step_len_seconds)

    @staticmethod
    def stop_client_producer(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                             logger: logging.Logger) -> None:
        """
        Stops the Kafka producer for client metrics

        :param emulation_env_config: the emulation environment configuration
        :param physical_server_ip: ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        if emulation_env_config.traffic_config.client_population_config.physical_host_ip != physical_server_ip:
            return

        logger.info(
            f"Stopping client producer on container:"
            f" {emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip}")

        TrafficController.start_client_manager(emulation_env_config=emulation_env_config, logger=logger)

        client_dto = TrafficController.get_clients_dto_by_ip_and_port(
            ip=emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip,
            port=emulation_env_config.traffic_config.client_population_config.client_manager_port,
            logger=logger)

        if client_dto.producer_active:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip}:'
                    f'{emulation_env_config.traffic_config.client_population_config.client_manager_port}',
                    options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
                stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)

                # Stop the producer thread
                csle_collector.client_manager.query_clients.stop_producer(stub=stub)

    @staticmethod
    def start_client_population(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                logger: logging.Logger) -> None:
        """
        Starts the arrival process of clients

        :param emulation_env_config: the emulation environment configuration
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        if emulation_env_config.traffic_config.client_population_config.physical_host_ip != physical_server_ip:
            return
        logger.info(f"Starting client population on container: "
                    f"{emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip}")

        TrafficController.start_client_manager(emulation_env_config=emulation_env_config, logger=logger)

        client_dto = TrafficController.get_clients_dto_by_ip_and_port(
            ip=emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip,
            port=emulation_env_config.traffic_config.client_population_config.client_manager_port,
            logger=logger)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip}:'
                f'{emulation_env_config.traffic_config.client_population_config.client_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)

            # Stop the client population if it is already running
            if client_dto.client_process_active:
                csle_collector.client_manager.query_clients.stop_clients(stub)
                time.sleep(2)

            # Start the client population
            time_step_len = emulation_env_config.traffic_config.client_population_config.client_time_step_len_seconds
            num_workflows = len(
                emulation_env_config.traffic_config.client_population_config.workflows_config.workflow_markov_chains)
            num_services = len(
                emulation_env_config.traffic_config.client_population_config.workflows_config.workflow_services)
            logger.info(
                f"Starting the client population, "
                f"time_step_len_seconds: {time_step_len},\n"
                f"num client profiles: {len(emulation_env_config.traffic_config.client_population_config.clients)}, \n"
                f"num workflows: {num_workflows}, num_services: {num_services}")
            csle_collector.client_manager.query_clients.start_clients(
                stub=stub, time_step_len_seconds=time_step_len,
                workflows_config=emulation_env_config.traffic_config.client_population_config.workflows_config,
                clients=emulation_env_config.traffic_config.client_population_config.clients)

    @staticmethod
    def get_num_active_clients(emulation_env_config: EmulationEnvConfig, logger: logging.Logger) \
            -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Gets the number of active clients

        :param emulation_env_config: the emulation configuration
        :param logger: the logger to use for logging
        :return: A ClientDTO which contains the number of active clients
        """

        TrafficController.start_client_manager(emulation_env_config=emulation_env_config, logger=logger)

        client_dto = TrafficController.get_clients_dto_by_ip_and_port(
            ip=emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip,
            port=emulation_env_config.traffic_config.client_population_config.client_manager_port,
            logger=logger)
        return client_dto

    @staticmethod
    def get_clients_dto_by_ip_and_port(ip: str, port: int, logger: logging.Logger) -> \
            csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        A method that sends a request to the ClientManager on a specific container
        to get its status

        :param ip: the ip of the container
        :param port: the port of the client manager running on the container
        :param logger: the logger to use for logging
        :return: the status of the clientmanager
        """
        logger.info(f"Get client manager status from container with ip: {ip} and client manager port: {port}")
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
            status = csle_collector.client_manager.query_clients.get_clients(stub=stub)
            return status

    @staticmethod
    def stop_internal_traffic_generators(emulation_env_config: EmulationEnvConfig, logger: logging.Logger,
                                         physical_server_ip: str) -> None:
        """
        Utility function for stopping internal traffic generators

        :param emulation_env_config: the configuration of the emulation env
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:
            if node_traffic_config.physical_host_ip == physical_server_ip:
                TrafficController.stop_internal_traffic_generator(emulation_env_config=emulation_env_config,
                                                                  node_traffic_config=node_traffic_config,
                                                                  logger=logger)

    @staticmethod
    def stop_internal_traffic_generator(emulation_env_config: EmulationEnvConfig,
                                        node_traffic_config: NodeTrafficConfig, logger: logging.Logger) -> None:
        """
        Utility function for stopping a specific internal traffic generator

        :param emulation_env_config: the configuration of the emulation env
        :param logger: the logger to use for logging
        :param node_traffic_config: the node traffic config
        :return: None
        """
        TrafficController.start_traffic_manager(emulation_env_config=emulation_env_config,
                                                node_traffic_config=node_traffic_config, logger=logger)
        logger.info(f"Stopping traffic generator script, "
                    f"node ip:{node_traffic_config.docker_gw_bridge_ip}")

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{node_traffic_config.docker_gw_bridge_ip}:{node_traffic_config.traffic_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.traffic_manager.traffic_manager_pb2_grpc.TrafficManagerStub(channel)
            csle_collector.traffic_manager.query_traffic_manager.stop_traffic(stub)

    @staticmethod
    def start_internal_traffic_generators(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                          logger: logging.Logger) -> None:
        """
        Utility function for starting internal traffic generators

        :param emulation_env_config: the configuration of the emulation env
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:
            if node_traffic_config.physical_host_ip != physical_server_ip:
                continue
            container = None
            for c in emulation_env_config.containers_config.containers:
                if node_traffic_config.ip in c.get_ips():
                    container = c
                    break
            if container is None:
                continue
            else:
                TrafficController.start_internal_traffic_generator(
                    emulation_env_config=emulation_env_config, node_traffic_config=node_traffic_config,
                    container=container, logger=logger)

    @staticmethod
    def start_internal_traffic_generator(
            emulation_env_config: EmulationEnvConfig, node_traffic_config: NodeTrafficConfig,
            container: NodeContainerConfig, logger: logging.Logger) -> None:
        """
        Utility function for starting internal traffic generators

        :param emulation_env_config: the configuration of the emulation env
        :param node_traffic_config: the node traffic configuration
        :param container: the container
        :param logger: the logger to use for logging
        :return: None
        """
        TrafficController.start_traffic_manager(emulation_env_config=emulation_env_config,
                                                node_traffic_config=node_traffic_config, logger=logger)
        logger.info(f"Starting traffic generator script, "
                    f"node ip:{node_traffic_config.docker_gw_bridge_ip}")

        commands = []
        subnet_masks = []
        reachable_containers = []
        for ip_net1 in container.ips_and_networks:
            ip, net1 = ip_net1
            subnet_masks.append(net1.subnet_mask)
        for c in emulation_env_config.containers_config.containers:
            for ip_net1 in c.ips_and_networks:
                ip, net1 = ip_net1
                if net1.subnet_mask in subnet_masks and ip not in container.get_ips():
                    reachable_containers.append((ip, c.get_ips()))

        for node2 in emulation_env_config.traffic_config.node_traffic_configs:
            for rc in reachable_containers:
                ip, ips = rc
                if node2.ip in ips:
                    for cmd in node2.commands:
                        commands.append(cmd.format(ip))

        sleep_time = emulation_env_config.traffic_config.client_population_config.client_time_step_len_seconds

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{node_traffic_config.docker_gw_bridge_ip}:{node_traffic_config.traffic_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.traffic_manager.traffic_manager_pb2_grpc.TrafficManagerStub(channel)
            csle_collector.traffic_manager.query_traffic_manager.start_traffic(stub, commands=commands,
                                                                               sleep_time=sleep_time)

    @staticmethod
    def get_client_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the IPS of the Client managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        return [emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip]

    @staticmethod
    def get_client_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the Client managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of ports
        """
        return [emulation_env_config.traffic_config.client_population_config.client_manager_port]

    @staticmethod
    def get_client_managers_info(emulation_env_config: EmulationEnvConfig, active_ips: List[str],
                                 logger: logging.Logger) -> ClientManagersInfo:
        """
        Extracts the information of the Client managers for a given emulation

        :param emulation_env_config: the configuration of the emulation
        :param active_ips: list of active IPs
        :param logger: the logger to use for logging
        :return: a DTO with the status of the Client managers
        """
        client_managers_ips = TrafficController.get_client_managers_ips(emulation_env_config=emulation_env_config)
        client_managers_ports = TrafficController.get_client_managers_ports(emulation_env_config=emulation_env_config)
        client_managers_statuses = []
        client_managers_running = []
        for ip in client_managers_ips:
            if ip not in active_ips:
                continue
            running = False
            status = None
            try:
                status = TrafficController.get_clients_dto_by_ip_and_port(
                    ip=ip, port=emulation_env_config.traffic_config.client_population_config.client_manager_port,
                    logger=logger)
                running = True
            except Exception as e:
                logger.info(
                    f"Could not fetch client manager status on IP:{ip}, error: {str(e)}, {repr(e)}")
            if status is not None:
                client_managers_statuses.append(status)
            else:
                client_managers_statuses.append(
                    csle_collector.client_manager.client_manager_util.ClientManagerUtil.clients_dto_empty())
            client_managers_running.append(running)
        execution_id = emulation_env_config.execution_id
        emulation_name = emulation_env_config.name
        client_manager_info_dto = ClientManagersInfo(
            client_managers_running=client_managers_running, ips=client_managers_ips, execution_id=execution_id,
            emulation_name=emulation_name, client_managers_statuses=client_managers_statuses,
            ports=client_managers_ports)
        return client_manager_info_dto

    @staticmethod
    def get_traffic_manager_status_by_port_and_ip(ip: str, port: int) -> \
            csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO:
        """
        A method that sends a request to the TrafficManager on a specific container
        to get its status

        :param emulation_env_config: the emulation config
        :return: the status of the traffic manager
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.traffic_manager.traffic_manager_pb2_grpc.TrafficManagerStub(channel)
            status = csle_collector.traffic_manager.query_traffic_manager.get_traffic_status(stub=stub)
            return status

    @staticmethod
    def get_traffic_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the ips of the traffic managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        ips = []
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:
            ips.append(node_traffic_config.docker_gw_bridge_ip)
        return ips

    @staticmethod
    def get_traffic_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the Traffic managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of ports
        """
        ports = []
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:
            ports.append(node_traffic_config.traffic_manager_port)
        return ports

    @staticmethod
    def get_traffic_managers_info(emulation_env_config: EmulationEnvConfig, active_ips: List[str],
                                  physical_host_ip: str, logger: logging.Logger) \
            -> TrafficManagersInfo:
        """
        Extracts the information of the traffic managers for a given emulation

        :param emulation_env_config: the configuration of the emulation
        :param active_ips: list of active IPs
        :param physical_host_ip: the ip of the physical host
        :param logger: the logger to use for logging
        :return: a DTO with the status of the traffic managers
        """
        traffic_managers_ips = TrafficController.get_traffic_managers_ips(emulation_env_config=emulation_env_config)
        traffic_managers_ports = TrafficController.get_traffic_managers_ports(emulation_env_config=emulation_env_config)
        traffic_managers_statuses = []
        traffic_managers_running = []
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:
            if node_traffic_config.docker_gw_bridge_ip not in active_ips or not EmulationUtil.physical_ip_match(
                    emulation_env_config=emulation_env_config, ip=node_traffic_config.docker_gw_bridge_ip,
                    physical_host_ip=physical_host_ip):
                continue
            running = False
            status = None
            if node_traffic_config.docker_gw_bridge_ip in traffic_managers_ips:
                try:
                    status = TrafficController.get_traffic_manager_status_by_port_and_ip(
                        port=node_traffic_config.traffic_manager_port, ip=node_traffic_config.docker_gw_bridge_ip)
                    running = True
                except Exception as e:
                    logger.debug(f"Could not fetch traffic manager status on IP"
                                 f":{node_traffic_config}, error: {str(e)}, {repr(e)}")
                if status is not None:
                    traffic_managers_statuses.append(status)
                else:
                    traffic_managers_statuses.append(
                        csle_collector.traffic_manager.traffic_manager_util.TrafficManagerUtil.traffic_dto_empty())
                traffic_managers_running.append(running)
        execution_id = emulation_env_config.execution_id
        emulation_name = emulation_env_config.name
        traffic_manager_info_dto = TrafficManagersInfo(
            traffic_managers_running=traffic_managers_running, ips=traffic_managers_ips, execution_id=execution_id,
            emulation_name=emulation_name, traffic_managers_statuses=traffic_managers_statuses,
            ports=traffic_managers_ports)
        return traffic_manager_info_dto
