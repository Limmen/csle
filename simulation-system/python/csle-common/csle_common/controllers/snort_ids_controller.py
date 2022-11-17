from typing import List
import grpc
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.snort_managers_info import SnortManagersInfo
import csle_common.constants.constants as constants
import csle_collector.constants.constants as csle_collector_constants
import csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc
import csle_collector.snort_ids_manager.snort_ids_manager_pb2
import csle_collector.snort_ids_manager.query_snort_ids_manager
from csle_common.util.emulation_util import EmulationUtil
from csle_common.logging.log import Logger


class SnortIDSController:
    """
    Class managing operations related to Snort IDS Managers
    """

    @staticmethod
    def start_snort_ids(emulation_env_config: EmulationEnvConfig):
        """
        Utility function for starting the Snort IDS

        :param emulation_config: the emulation env configuration
        :return:
        """
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.SNORT_IDS_IMAGES:
                if ids_image in c.name:
                    EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=c.get_ips()[0])
                    cmd = constants.COMMANDS.CHANGE_PERMISSION_LOG_DIRS
                    o, e, _ = EmulationUtil.execute_ssh_cmd(
                        cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                    cmd = constants.COMMANDS.STOP_IDS
                    o, e, _ = EmulationUtil.execute_ssh_cmd(
                        cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                    time.sleep(2)
                    cmd = constants.COMMANDS.START_IDS
                    Logger.__call__().get_logger().info(f"Starting Snort IDS on {c.get_ips()[0]}")
                    o, e, _ = EmulationUtil.execute_ssh_cmd(
                        cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                    continue

    @staticmethod
    def _start_snort_ids_manager_if_not_running(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for checking if the snort ids manager is running and starting it if it is not running

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.SNORT_IDS_IMAGES:
                if ids_image in c.name:
                    # Connect
                    EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=c.get_ips()[0])

                    # Check if ids_manager is already running
                    cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
                          + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.SNORT_IDS_MANAGER_FILE_NAME
                    o, e, _ = EmulationUtil.execute_ssh_cmd(
                        cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                    t = constants.COMMANDS.SEARCH_SNORT_IDS_MANAGER

                    if not constants.COMMANDS.SEARCH_SNORT_IDS_MANAGER in str(o):

                        # Stop old background job if running
                        cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                              constants.COMMANDS.SPACE_DELIM \
                              + constants.TRAFFIC_COMMANDS.SNORT_IDS_MANAGER_FILE_NAME
                        o, e, _ = EmulationUtil.execute_ssh_cmd(
                            cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))

                        # Start the ids_manager
                        cmd = constants.COMMANDS.START_SNORT_IDS_MANAGER.format(
                            emulation_env_config.snort_ids_manager_config.snort_ids_manager_port)
                        o, e, _ = EmulationUtil.execute_ssh_cmd(
                            cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                        time.sleep(5)

    @staticmethod
    def start_snort_ids_monitor_thread(emulation_env_config: EmulationEnvConfig) -> None:
        """
        A method that sends a request to the SnortIDSManager on every container that runs
        an IDS to start the IDS manager and the monitor thread
n
        :param emulation_env_config: the emulation env config
        :return: None
        """
        SnortIDSController._start_snort_ids_manager_if_not_running(emulation_env_config=emulation_env_config)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.SNORT_IDS_IMAGES:
                if ids_image in c.name:
                    ids_monitor_dto = SnortIDSController.get_snort_ids_monitor_thread_status_by_ip_and_port(
                        port=emulation_env_config.snort_ids_manager_config.snort_ids_manager_port, ip=c.get_ips()[0])
                    if not ids_monitor_dto.running:
                        Logger.__call__().get_logger().info(
                            f"Snort IDS monitor thread is not running on {c.get_ips()[0]}, starting it.")
                        # Open a gRPC session
                        with grpc.insecure_channel(
                                f'{c.get_ips()[0]}:'
                                f'{emulation_env_config.snort_ids_manager_config.snort_ids_manager_port}') as channel:
                            stub = csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.SnortIdsManagerStub(channel)
                            csle_collector.snort_ids_manager.query_snort_ids_manager.start_snort_ids_monitor(
                                stub=stub, kafka_ip=emulation_env_config.kafka_config.container.get_ips()[0],
                                kafka_port=emulation_env_config.kafka_config.kafka_port,
                                log_file_path=csle_collector_constants.SNORT_IDS_ROUTER.SNORT_FAST_LOG_FILE,
                                time_step_len_seconds=
                                emulation_env_config.snort_ids_manager_config.time_step_len_seconds)


    @staticmethod
    def stop_snort_ids_monitor_thread(emulation_env_config: EmulationEnvConfig) -> None:
        """
        A method that sends a request to the SnortIDSManager on every container that runs
        an IDS to stop the monitor threads

        :param emulation_env_config: the emulation env config
        :return: None
        """
        SnortIDSController._start_snort_ids_manager_if_not_running(emulation_env_config=emulation_env_config)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.SNORT_IDS_IMAGES:
                if ids_image in c.name:
                    # Open a gRPC session
                    with grpc.insecure_channel(
                            f'{c.get_ips()[0]}:'
                            f'{emulation_env_config.snort_ids_manager_config.snort_ids_manager_port}') as channel:
                        stub = csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.SnortIdsManagerStub(channel)
                        Logger.__call__().get_logger().info(
                            f"Stopping the Snort IDS monitor thread on {c.get_ips()[0]}.")
                        csle_collector.snort_ids_manager.query_snort_ids_manager.stop_snort_ids_monitor(stub=stub)

    @staticmethod
    def get_snort_ids_monitor_thread_status(emulation_env_config: EmulationEnvConfig,
                                            start_if_stopped: bool = True) -> \
            List[csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO]:
        """
        A method that sends a request to the SnortIDSManager on every container to get the status of the IDS monitor thread

        :param emulation_env_config: the emulation config
        :param start_if_stopped: whether to start the IDS monitor if it is stopped
        :return: List of monitor thread statuses
        """
        statuses = []
        if start_if_stopped:
            SnortIDSController._start_snort_ids_manager_if_not_running(emulation_env_config=emulation_env_config)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.SNORT_IDS_IMAGES:
                if ids_image in c.name:
                    status = SnortIDSController.get_snort_ids_monitor_thread_status_by_ip_and_port(
                        port=emulation_env_config.snort_ids_manager_config.snort_ids_manager_port, ip=c.get_ips()[0])
                    statuses.append(status)
        return statuses

    @staticmethod
    def get_snort_ids_monitor_thread_status_by_ip_and_port(port: int, ip: str) \
            -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO:
        """
        A method that sends a request to the SnortIDSManager with a specific port and ip
        to get the status of the IDS monitor thread

        :param port: the port of the SnortIDSManager
        :param ip: the ip of the SnortIDSManager
        :return: the status of the SnortIDSManager
        """
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.SnortIdsManagerStub(channel)
            status = \
                csle_collector.snort_ids_manager.query_snort_ids_manager.get_snort_ids_monitor_status(
                    stub=stub)
            return status

    @staticmethod
    def get_snort_ids_log_data(emulation_env_config: EmulationEnvConfig, timestamp: float) \
            -> List[csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsLogDTO]:
        """
        A method that sends a request to the Snort IDSManager on every container to get contents of the IDS log from
        a given timestamp

        :param emulation_env_config: the emulation env config
        :param timestamp: the timestamp to read the IDS log from
        :return: List of monitor thread statuses
        """
        ids_log_data_list = []
        SnortIDSController._start_snort_ids_manager_if_not_running(emulation_env_config=emulation_env_config)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.SNORT_IDS_IMAGES:
                if ids_image in c.name:
                    # Open a gRPC session
                    with grpc.insecure_channel(
                            f'{c.get_ips()[0]}:'
                            f'{emulation_env_config.snort_ids_manager_config.snort_ids_manager_port}') as channel:
                        stub = csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.SnortIdsManagerStub(channel)
                        ids_log_data = csle_collector.snort_ids_manager.query_snort_ids_manager.get_snort_ids_alerts(
                            stub=stub, timestamp=timestamp,
                            log_file_path=csle_collector_constants.SNORT_IDS_ROUTER.SNORT_FAST_LOG_FILE)
                        ids_log_data_list.append(ids_log_data)
        return ids_log_data_list

    @staticmethod
    def get_snort_ids_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the IPs of the snort IDS managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        ips = []
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.SNORT_IDS_IMAGES:
                if ids_image in c.name:
                    try:
                        SnortIDSController.get_snort_ids_monitor_thread_status_by_ip_and_port(
                            port=emulation_env_config.snort_ids_manager_config.snort_ids_manager_port, ip=c.get_ips()[0])
                        ips.append(c.get_ips()[0])
                    except Exception as e:
                        pass
        return ips

    @staticmethod
    def get_snort_ids_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the snort IDS managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of ports
        """
        ports = []
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.SNORT_IDS_IMAGES:
                if ids_image in c.name:
                    try:
                        SnortIDSController.get_snort_ids_monitor_thread_status_by_ip_and_port(
                            port=emulation_env_config.snort_ids_manager_config.snort_ids_manager_port, ip=c.get_ips()[0])
                        ports.append(emulation_env_config.snort_ids_manager_config.snort_ids_manager_port)
                    except Exception as e:
                        pass
        return ports

    @staticmethod
    def get_snort_managers_info(emulation_env_config: EmulationEnvConfig) -> SnortManagersInfo:
        """
        Extracts the information of the Snort managers for a given emulation

        :param emulation_env_config: the configuration of the emulation
        :return: a DTO with the status of the Snort managers
        """
        snort_ids_managers_ips = SnortIDSController.get_snort_ids_managers_ips(emulation_env_config=emulation_env_config)
        snort_ids_managers_ports = \
            SnortIDSController.get_snort_ids_managers_ports(emulation_env_config=emulation_env_config)
        snort_statuses = []
        running = False
        status = None
        for ip in snort_ids_managers_ips:
            try:
                status = SnortIDSController.get_snort_ids_monitor_thread_status_by_ip_and_port(
                    port=emulation_env_config.snort_ids_manager_config.snort_ids_manager_port, ip=ip)
                if not running and status.running:
                    running = True
            except Exception as e:
                Logger.__call__().get_logger().warning(
                    f"Could not fetch Snort IDS manager status on IP:{ip}, error: {str(e)}, {repr(e)}")
            snort_statuses.append(status)
        execution_id = emulation_env_config.execution_id
        emulation_name = emulation_env_config.name
        snort_manager_info_dto = SnortManagersInfo(running=running, ips=snort_ids_managers_ips,
                                                   ports=snort_ids_managers_ports,
                                                   execution_id=execution_id,
                                                   emulation_name=emulation_name, snort_statuses=snort_statuses)
        return snort_manager_info_dto


