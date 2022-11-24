from typing import List
import grpc
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.elk_managers_info import ELKManagersInfo
import csle_common.constants.constants as constants
import csle_collector.elk_manager.elk_manager_pb2_grpc
import csle_collector.elk_manager.elk_manager_pb2
import csle_collector.elk_manager.query_elk_server
import csle_collector.elk_manager.elk_manager_util
from csle_common.util.emulation_util import EmulationUtil
from csle_common.logging.log import Logger


class ELKController:

    @staticmethod
    def start_elk_manager(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for starting the ELK manager

        :param emulation_env_config: the emulation env config
        :return: None
        """

        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=emulation_env_config.elk_config.container.get_ips()[0],
                                    create_producer=False)

        # Check if elk_manager is already running
        cmd = (constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP + constants.COMMANDS.SPACE_DELIM +
               constants.TRAFFIC_COMMANDS.ELK_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd,
            conn=emulation_env_config.get_connection(ip=emulation_env_config.elk_config.container.get_ips()[0]))

        if constants.COMMANDS.SEARCH_ELK_MANAGER not in str(o):

            Logger.__call__().get_logger().info(f"Starting elk manager on node: "
                                                f"{emulation_env_config.elk_config.container.get_ips()[0]}")

            # Stop old background job if running
            cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
                   constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.ELK_MANAGER_FILE_NAME)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd,
                conn=emulation_env_config.get_connection(ip=emulation_env_config.elk_config.container.get_ips()[0]))

            # Start the elk_manager
            cmd = constants.COMMANDS.START_ELK_MANAGER.format(
                emulation_env_config.elk_config.elk_manager_port, emulation_env_config.elk_config.elk_manager_log_dir,
                emulation_env_config.elk_config.elk_manager_log_file,
                emulation_env_config.elk_config.elk_manager_max_workers)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd,
                conn=emulation_env_config.get_connection(ip=emulation_env_config.elk_config.container.get_ips()[0]))
            time.sleep(2)

    @staticmethod
    def stop_elk_manager(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for stopping the ELK manager

        :param emulation_env_config: the emulation env config
        :return: None
        """
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=emulation_env_config.elk_config.container.get_ips()[0],
                                    create_producer=False)

        Logger.__call__().get_logger().info(f"Stopping elk manager on node: "
                                            f"{emulation_env_config.elk_config.container.get_ips()[0]}")

        # Stop background job
        cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
               constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.ELK_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd,
            conn=emulation_env_config.get_connection(ip=emulation_env_config.elk_config.container.get_ips()[0]))

        time.sleep(2)

    @staticmethod
    def get_elk_status(emulation_env_config: EmulationEnvConfig) -> \
            csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Method for querying the ELKManager about the status of the ELK stack

        :param emulation_env_config: the emulation config
        :return: an ELKDTO with the status of the server
        """
        ELKController.start_elk_manager(emulation_env_config=emulation_env_config)
        elk_dto = ELKController.get_elk_status_by_port_and_ip(
            ip=emulation_env_config.elk_config.container.get_ips()[0],
            port=emulation_env_config.elk_config.elk_manager_port)
        return elk_dto

    @staticmethod
    def get_elk_status_by_port_and_ip(ip: str, port: int) -> \
            csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Method for querying the ElkManager about the status of the ELK stack

        :param ip: the ip where the ElkManager is running
        :param port: the port the ELkManager is listening to
        :return: an ELKDTO with the status of the server
        """
        # Open a gRPC session
        with grpc.insecure_channel(
                f'{ip}:'
                f'{port}') as channel:
            stub = csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub(channel)
            elk_dto = csle_collector.elk_manager.query_elk_server.get_elk_status(stub)
            return elk_dto

    @staticmethod
    def stop_elk_stack(emulation_env_config: EmulationEnvConfig) -> \
            csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Method for requesting the ELKManager to stop the ELK server

        :param emulation_env_config: the emulation env config
        :return: a ELKDTO with the status of the server
        """
        Logger.__call__().get_logger().info(
            f"Stopping ELK stack on container: {emulation_env_config.elk_config.container.get_ips()[0]}")
        ELKController.start_elk_manager(emulation_env_config=emulation_env_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.elk_config.container.get_ips()[0]}:'
                f'{emulation_env_config.elk_config.elk_manager_port}') as channel:
            stub = csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub(channel)
            elk_dto = csle_collector.elk_manager.query_elk_server.stop_elk(stub)
            return elk_dto

    @staticmethod
    def start_elk_stack(emulation_env_config: EmulationEnvConfig) -> \
            csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Method for requesting the ELKManager to start the ELK server

        :param emulation_env_config: the emulation env config
        :return: an ELKDTO with the status of the server
        """
        Logger.__call__().get_logger().info(
            f"Starting ELK stack on container: {emulation_env_config.elk_config.container.get_ips()[0]}")
        ELKController.start_elk_manager(emulation_env_config=emulation_env_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.elk_config.container.get_ips()[0]}:'
                f'{emulation_env_config.elk_config.elk_manager_port}') as channel:
            stub = csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub(channel)
            elk_dto = csle_collector.elk_manager.query_elk_server.start_elk(stub)
            return elk_dto

    @staticmethod
    def start_elastic(emulation_env_config: EmulationEnvConfig) -> \
            csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Method for requesting the ELKManager to start elasticsearch

        :param emulation_env_config: the emulation env config
        :return: an ELKDTO with the status of the server
        """
        Logger.__call__().get_logger().info(
            f"Starting elasticsearch on container: {emulation_env_config.elk_config.container.get_ips()[0]}")
        ELKController.start_elk_manager(emulation_env_config=emulation_env_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.elk_config.container.get_ips()[0]}:'
                f'{emulation_env_config.elk_config.elk_manager_port}') as channel:
            stub = csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub(channel)
            elk_dto = csle_collector.elk_manager.query_elk_server.start_elastic(stub)
            return elk_dto

    @staticmethod
    def start_kibana(emulation_env_config: EmulationEnvConfig) -> \
            csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Method for requesting the ELKManager to start kibana

        :param emulation_env_config: the emulation env config
        :return: an ELKDTO with the status of the server
        """
        Logger.__call__().get_logger().info(
            f"Starting kibana on container: {emulation_env_config.elk_config.container.get_ips()[0]}")
        ELKController.start_elk_manager(emulation_env_config=emulation_env_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.elk_config.container.get_ips()[0]}:'
                f'{emulation_env_config.elk_config.elk_manager_port}') as channel:
            stub = csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub(channel)
            elk_dto = csle_collector.elk_manager.query_elk_server.start_kibana(stub)
            return elk_dto

    @staticmethod
    def start_logstash(emulation_env_config: EmulationEnvConfig) -> \
            csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Method for requesting the ELKManager to start Logstash

        :param emulation_env_config: the emulation env config
        :return: an ELKDTO with the status of the server
        """
        Logger.__call__().get_logger().info(
            f"Starting logstash on container: {emulation_env_config.elk_config.container.get_ips()[0]}")
        ELKController.start_elk_manager(emulation_env_config=emulation_env_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.elk_config.container.get_ips()[0]}:'
                f'{emulation_env_config.elk_config.elk_manager_port}') as channel:
            stub = csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub(channel)
            elk_dto = csle_collector.elk_manager.query_elk_server.start_logstash(stub)
            return elk_dto

    @staticmethod
    def stop_elastic(emulation_env_config: EmulationEnvConfig) -> \
            csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Method for requesting the ELKManager to start elasticsearch

        :param emulation_env_config: the emulation env config
        :return: an ELKDTO with the status of the server
        """
        Logger.__call__().get_logger().info(
            f"Starting elasticsearch on container: {emulation_env_config.elk_config.container.get_ips()[0]}")
        ELKController.start_elk_manager(emulation_env_config=emulation_env_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.elk_config.container.get_ips()[0]}:'
                f'{emulation_env_config.elk_config.elk_manager_port}') as channel:
            stub = csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub(channel)
            elk_dto = csle_collector.elk_manager.query_elk_server.stop_elastic(stub)
            return elk_dto

    @staticmethod
    def stop_kibana(emulation_env_config: EmulationEnvConfig) -> \
            csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Method for requesting the ELKManager to start kibana

        :param emulation_env_config: the emulation env config
        :return: an ELKDTO with the status of the server
        """
        Logger.__call__().get_logger().info(
            f"Starting kibana on container: {emulation_env_config.elk_config.container.get_ips()[0]}")
        ELKController.start_elk_manager(emulation_env_config=emulation_env_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.elk_config.container.get_ips()[0]}:'
                f'{emulation_env_config.elk_config.elk_manager_port}') as channel:
            stub = csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub(channel)
            elk_dto = csle_collector.elk_manager.query_elk_server.stop_kibana(stub)
            return elk_dto

    @staticmethod
    def stop_logstash(emulation_env_config: EmulationEnvConfig) -> \
            csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Method for requesting the ELKManager to start Logstash

        :param emulation_env_config: the emulation env config
        :return: an ELKDTO with the status of the server
        """
        Logger.__call__().get_logger().info(
            f"Starting logstash on container: {emulation_env_config.elk_config.container.get_ips()[0]}")
        ELKController.start_elk_manager(emulation_env_config=emulation_env_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.elk_config.container.get_ips()[0]}:'
                f'{emulation_env_config.elk_config.elk_manager_port}') as channel:
            stub = csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub(channel)
            elk_dto = csle_collector.elk_manager.query_elk_server.stop_logstash(stub)
            return elk_dto

    @staticmethod
    def get_elk_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the IPS of the ELK managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        return [emulation_env_config.elk_config.container.get_ips()[0]]

    @staticmethod
    def get_elk_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the Elk managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        return [emulation_env_config.elk_config.elk_manager_port]

    @staticmethod
    def get_elk_managers_info(emulation_env_config: EmulationEnvConfig, active_ips: List[str]) -> ELKManagersInfo:
        """
        Extracts the information of the ELK managers for a given emulation

        :param emulation_env_config: the configuration of the emulation
        :param active_ips: list of active IPs
        :return: a DTO with the status of the ELK managers
        """
        elk_managers_ips = ELKController.get_elk_managers_ips(emulation_env_config=emulation_env_config)
        elk_managers_ports = ELKController.get_elk_managers_ports(emulation_env_config=emulation_env_config)
        elk_managers_statuses = []
        elk_managers_running = []
        for ip in elk_managers_ips:
            if ip not in active_ips:
                continue
            status = None
            try:
                status = ELKController.get_elk_status_by_port_and_ip(
                    port=emulation_env_config.elk_config.elk_manager_port, ip=ip)
                running = True
            except Exception as e:
                running = False
                Logger.__call__().get_logger().debug(
                    f"Could not fetch Elk manager status on IP:{ip}, error: {str(e)}, {repr(e)}")
            if status is not None:
                elk_managers_statuses.append(status)
            else:
                elk_managers_statuses.append(csle_collector.elk_manager.elk_manager_util.ElkManagerUtil.elk_dto_empty())
            elk_managers_running.append(running)
        execution_id = emulation_env_config.execution_id
        emulation_name = emulation_env_config.name
        elk_manager_info_dto = ELKManagersInfo(
            elk_managers_running=elk_managers_running, ips=elk_managers_ips, execution_id=execution_id,
            emulation_name=emulation_name, elk_managers_statuses=elk_managers_statuses, ports=elk_managers_ports)
        return elk_manager_info_dto
