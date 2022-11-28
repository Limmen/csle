from typing import List, Tuple
import grpc
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.host_managers_info import HostManagersInfo
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
    def start_host_managers(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for checking if the host manager is running and starting it if it is not running

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            # Connect
            HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=c.get_ips()[0])

    @staticmethod
    def start_host_manager(emulation_env_config: EmulationEnvConfig, ip: str) -> None:
        """
        Utility method for starting the host manager on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
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
            Logger.__call__().get_logger().info(f"Starting host manager on node {ip}")

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
    def stop_host_managers(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for stopping host managers

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            HostController.stop_host_manager(emulation_env_config=emulation_env_config, ip=c.get_ips()[0])

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
    def start_host_monitor_threads(emulation_env_config: EmulationEnvConfig) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and the monitor thread

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            HostController.start_host_monitor_thread(emulation_env_config=emulation_env_config, ip=c.get_ips()[0])

    @staticmethod
    def start_host_monitor_thread(emulation_env_config: EmulationEnvConfig, ip: str) -> None:
        """
        A method that sends a request to the HostManager on a specific IP
        to start the Host manager and the monitor thread

        :param emulation_env_config: the emulation env config
        :param ip: IP of the container
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=ip)

        host_monitor_dto = HostController.get_host_monitor_thread_status_by_port_and_ip(
            ip=ip, port=emulation_env_config.host_manager_config.host_manager_port)
        if not host_monitor_dto.running:
            Logger.__call__().get_logger().info(
                f"Host monitor thread is not running on {ip}, starting it.")
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{ip}:{emulation_env_config.host_manager_config.host_manager_port}') as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                csle_collector.host_manager.query_host_manager.start_host_monitor(
                    stub=stub, kafka_ip=emulation_env_config.kafka_config.container.get_ips()[0],
                    kafka_port=emulation_env_config.kafka_config.kafka_port,
                    time_step_len_seconds=emulation_env_config.kafka_config.time_step_len_seconds)

    @staticmethod
    def stop_host_monitor_threads(emulation_env_config: EmulationEnvConfig) -> None:
        """
        A method that sends a request to the HostManager on every container to stop the monitor threads

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            HostController.stop_host_monitor_thread(emulation_env_config=emulation_env_config, ip=c.get_ips()[0])

    @staticmethod
    def stop_host_monitor_thread(emulation_env_config: EmulationEnvConfig, ip: str) -> None:
        """
        A method that sends a request to the HostManager on a specific container to stop the monitor threads

        :param emulation_env_config: the emulation env config
        :param ip: the IP of the container
        :return: None
        """
        HostController.start_host_manager(emulation_env_config=emulation_env_config, ip=ip)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{ip}:'
                f'{emulation_env_config.host_manager_config.host_manager_port}') as channel:
            stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
            Logger.__call__().get_logger().info(f"Stopping the Host monitor thread on {ip}.")
            csle_collector.host_manager.query_host_manager.stop_host_monitor(stub=stub)

    @staticmethod
    def get_host_monitor_thread_status(emulation_env_config: EmulationEnvConfig) -> \
            List[Tuple[csle_collector.host_manager.host_manager_pb2.HostMonitorDTO, str]]:
        """
        A method that sends a request to the HostManager on every container to get the status of the Host monitor thread

        :param emulation_env_config: the emulation config
        :return: List of monitor thread statuses
        """
        statuses = []
        HostController.start_host_managers(emulation_env_config=emulation_env_config)
        for c in emulation_env_config.containers_config.containers:
            status = HostController.get_host_monitor_thread_status_by_port_and_ip(
                ip=c.get_ips()[0], port=emulation_env_config.host_manager_config.host_manager_port)
            statuses.append((status, c.get_ips()[0]))
        return statuses

    @staticmethod
    def get_host_monitor_thread_status_by_port_and_ip(ip: str, port: int) -> \
            csle_collector.host_manager.host_manager_pb2.HostMonitorDTO:
        """
        A method that sends a request to the HostManager on a specific container
        to get the status of the Host monitor thread

        :param emulation_env_config: the emulation config
        :return: the status of the host manager
        """
        # Open a gRPC session
        with grpc.insecure_channel(
                f'{ip}:{port}') as channel:
            stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
            status = csle_collector.host_manager.query_host_manager.get_host_monitor_status(stub=stub)
            return status

    @staticmethod
    def get_hosts_log_data(emulation_env_config: EmulationEnvConfig, failed_auth_last_ts: float,
                           login_last_ts: float) \
            -> List[csle_collector.host_manager.host_manager_pb2.HostMetricsDTO]:
        """
        A method that sends a request to the HostManager on every container to get contents of the Hostmetrics
        given timestamps

        :param emulation_env_config: the emulation env config
        :param failed_auth_last_ts: the timestamp to read the last failed login attempts from
        :param login_last_ts: the timestamp to read the last successful login attempts from
        :return: List of monitor thread statuses
        """
        host_metrics_data_list = []
        HostController.start_host_managers(emulation_env_config=emulation_env_config)

        for c in emulation_env_config.containers_config.containers:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{c.get_ips()[0]}:'
                    f'{emulation_env_config.host_manager_config.host_manager_port}') as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                host_metrics_data = csle_collector.host_manager.query_host_manager.get_host_metrics(
                    stub=stub, failed_auth_last_ts=failed_auth_last_ts, login_last_ts=login_last_ts)
                host_metrics_data_list.append(host_metrics_data)
        return host_metrics_data_list

    @staticmethod
    def get_host_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the ips of the Host managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        ips = []
        for c in emulation_env_config.containers_config.containers:
            ips.append(c.get_ips()[0])
        return ips

    @staticmethod
    def get_host_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the Host managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of ports
        """
        ports = []
        for c in emulation_env_config.containers_config.containers:
            ports.append(emulation_env_config.host_manager_config.host_manager_port)
        return ports

    @staticmethod
    def get_host_managers_info(emulation_env_config: EmulationEnvConfig, active_ips: List[str]) -> HostManagersInfo:
        """
        Extracts the information of the Host managers for a given emulation

        :param emulation_env_config: the configuration of the emulation
        :param active_ips: list of active IPs
        :return: a DTO with the status of the Host managers
        """
        host_managers_ips = HostController.get_host_managers_ips(emulation_env_config=emulation_env_config)
        host_managers_ports = HostController.get_host_managers_ports(emulation_env_config=emulation_env_config)
        host_managers_statuses = []
        host_managers_running = []
        for ip in host_managers_ips:
            if ip not in active_ips:
                continue
            status = None
            running = False
            try:
                status = HostController.get_host_monitor_thread_status_by_port_and_ip(
                    port=emulation_env_config.host_manager_config.host_manager_port, ip=ip)
                running = True
            except Exception as e:
                Logger.__call__().get_logger().debug(
                    f"Could not fetch Host manager status on IP:{ip}, error: {str(e)}, {repr(e)}")
            if status is not None:
                host_managers_statuses.append(status)
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
