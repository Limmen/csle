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
from csle_common.util.emulation_util import EmulationUtil
from csle_common.logging.log import Logger


class OSSECIDSManager:

    @staticmethod
    def grpc_server_on(channel) -> bool:
        """
        Utility function to test if a given gRPC channel is working or not

        :param channel: the channel to test
        :return: True if working, False if timeout
        """
        try:
            grpc.channel_ready_future(channel).result(timeout=15)
            return True
        except grpc.FutureTimeoutError:
            return False

    @staticmethod
    def start_ossec_ids(emulation_env_config: EmulationEnvConfig):
        """
        Utility function for starting the OSSEC IDS

        :param emulation_config: the emulation env configuration
        :return:
        """
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=c.get_ips()[0])
                    cmd = constants.COMMANDS.CHANGE_PERMISSION_LOG_DIRS
                    o, e, _ = EmulationUtil.execute_ssh_cmd(
                        cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                    cmd = constants.COMMANDS.STOP_IDS
                    o, e, _ = EmulationUtil.execute_ssh_cmd(
                        cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                    time.sleep(1)
                    cmd = constants.COMMANDS.START_IDS
                    Logger.__call__().get_logger().info(f"Starting OSSEC IDS on {c.get_ips()[0]}")
                    o, e, _ = EmulationUtil.execute_ssh_cmd(
                        cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                    continue

    @staticmethod
    def _start_ossec_ids_manager_if_not_running(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for checking if the ossec ids manager is running and starting it if it is not running

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    # Connect
                    EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=c.get_ips()[0])

                    # Check if ids_manager is already running
                    cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
                          + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.OSSEC_IDS_MANAGER_FILE_NAME
                    o, e, _ = EmulationUtil.execute_ssh_cmd(
                        cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                    t = constants.COMMANDS.SEARCH_OSSEC_IDS_MANAGER

                    if not constants.COMMANDS.SEARCH_OSSEC_IDS_MANAGER in str(o):

                        # Stop old background job if running
                        cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                              constants.COMMANDS.SPACE_DELIM \
                              + constants.TRAFFIC_COMMANDS.OSSEC_IDS_MANAGER_FILE_NAME
                        o, e, _ = EmulationUtil.execute_ssh_cmd(
                            cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))

                        # Start the OSSEC ids_manager
                        cmd = constants.COMMANDS.START_OSSEC_IDS_MANAGER.format(
                            emulation_env_config.log_sink_config.third_grpc_port)
                        o, e, _ = EmulationUtil.execute_ssh_cmd(
                            cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                        time.sleep(5)

    @staticmethod
    def start_ossec_ids_monitor_thread(emulation_env_config: EmulationEnvConfig) -> None:
        """
        A method that sends a request to the OSSECIDSManager on every container that runs
        an IDS to start the IDS manager and the monitor thread
n
        :param emulation_env_config: the emulation env config
        :return: None
        """
        OSSECIDSManager._start_ossec_ids_manager_if_not_running(emulation_env_config=emulation_env_config)
        time.sleep(10)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    ids_monitor_dto = OSSECIDSManager.get_ossec_ids_monitor_thread_status_by_ip_and_port(
                        port=emulation_env_config.log_sink_config.third_grpc_port, ip = c.get_ips()[0])
                    if not ids_monitor_dto.running:
                        Logger.__call__().get_logger().info(
                            f"OSSEC IDS monitor thread is not running on {c.get_ips()[0]}, starting it.")
                        with grpc.insecure_channel(
                                f'{c.get_ips()[0]}:'
                                f'{emulation_env_config.log_sink_config.third_grpc_port}') as channel:
                            stub = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub(channel)
                            csle_collector.ossec_ids_manager.query_ossec_ids_manager.start_ossec_ids_monitor(
                                stub=stub, kafka_ip=emulation_env_config.log_sink_config.container.get_ips()[0],
                                kafka_port=emulation_env_config.log_sink_config.kafka_port,
                                log_file_path=csle_collector_constants.OSSEC.OSSEC_ALERTS_FILE,
                                time_step_len_seconds=emulation_env_config.log_sink_config.time_step_len_seconds)


    @staticmethod
    def stop_ossec_ids_monitor_thread(emulation_env_config: EmulationEnvConfig) -> None:
        """
        A method that sends a request to the OSSECIDSManager on every container that runs
        an IDS to stop the monitor threads

        :param emulation_env_config: the emulation env config
        :return: None
        """
        OSSECIDSManager._start_ossec_ids_manager_if_not_running(emulation_env_config=emulation_env_config)
        time.sleep(10)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    # Open a gRPC session
                    with grpc.insecure_channel(
                            f'{c.get_ips()[0]}:'
                            f'{emulation_env_config.log_sink_config.third_grpc_port}') as channel:
                        stub = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub(channel)
                        Logger.__call__().get_logger().info(
                            f"Stopping the OSSEC IDS monitor thread on {c.get_ips()[0]}.")
                        csle_collector.ossec_ids_manager.query_ossec_ids_manager.stop_ossec_ids_monitor(stub=stub)

    @staticmethod
    def get_ossec_ids_monitor_thread_status(emulation_env_config: EmulationEnvConfig) -> \
            List[csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO]:
        """
        A method that sends a request to the OSSECIDSManager on every container to get the status of the IDS monitor thread

        :param emulation_env_config: the emulation config
        :return: List of monitor thread statuses
        """
        statuses = []
        OSSECIDSManager._start_ossec_ids_manager_if_not_running(emulation_env_config=emulation_env_config)
        time.sleep(10)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    status = OSSECIDSManager.get_ossec_ids_monitor_thread_status_by_ip_and_port(
                        port=emulation_env_config.log_sink_config.third_grpc_port, ip = c.get_ips()[0])
                    statuses.append(status)
        return statuses

    @staticmethod
    def get_ossec_ids_log_data(emulation_env_config: EmulationEnvConfig, timestamp: float) \
            -> List[csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsLogDTO]:
        """
        A method that sends a request to the OSSEC IDSManager on every container to get contents of the IDS log from
        a given timestamp

        :param emulation_env_config: the emulation env config
        :param timestamp: the timestamp to read the IDS log from
        :return: List of monitor thread statuses
        """
        ids_log_data_list = []
        OSSECIDSManager._start_ossec_ids_manager_if_not_running(emulation_env_config=emulation_env_config)
        time.sleep(10)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    # Open a gRPC session
                    with grpc.insecure_channel(
                            f'{c.get_ips()[0]}:'
                            f'{emulation_env_config.log_sink_config.third_grpc_port}') as channel:
                        stub = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub(channel)
                        ids_log_data = csle_collector.ossec_ids_manager.query_ossec_ids_manager.get_ossec_ids_alerts(
                            stub=stub, timestamp=timestamp,
                            log_file_path=csle_collector_constants.OSSEC.OSSEC_ALERTS_FILE)
                        ids_log_data_list.append(ids_log_data)
        return ids_log_data_list

    @staticmethod
    def get_ossec_ids_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the IPS of the OSSEC IDS managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        ips = []
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    try:
                        OSSECIDSManager.get_ossec_ids_monitor_thread_status_by_ip_and_port(
                            port=emulation_env_config.log_sink_config.third_grpc_port, ip = c.get_ips()[0])
                        ips.append(c.get_ips()[0])
                    except Exception as e:
                        pass
        return ips

    @staticmethod
    def get_ossec_ids_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the OSSEC IDS managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of ports
        """
        ports = []
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    try:
                        OSSECIDSManager.get_ossec_ids_monitor_thread_status_by_ip_and_port(
                            port=emulation_env_config.log_sink_config.third_grpc_port, ip = c.get_ips()[0])
                        ports.append(emulation_env_config.log_sink_config.third_grpc_port)
                    except Exception as e:
                        pass
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
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub(channel)
            status = \
                csle_collector.ossec_ids_manager.query_ossec_ids_manager.get_ossec_ids_monitor_status(stub=stub)
            return status

    @staticmethod
    def get_ossec_managers_info(emulation_env_config: EmulationEnvConfig) -> OSSECIDSManagersInfo:
        """
        Extracts the information of the OSSEC IDS managers for a given emulation

        :param emulation_env_config: the configuration of the emulation
        :return: a DTO with the status of the OSSEC IDS managers
        """
        ossec_ids_managers_ips = OSSECIDSManager.get_ossec_ids_managers_ips(emulation_env_config=emulation_env_config)
        ossec_ids_managers_ports = \
            OSSECIDSManager.get_ossec_ids_managers_ports(emulation_env_config=emulation_env_config)
        ossec_statuses = []
        running = False

        for ip in ossec_ids_managers_ips:
            status = OSSECIDSManager.get_ossec_ids_monitor_thread_status_by_ip_and_port(
                port=emulation_env_config.log_sink_config.third_grpc_port, ip=ip)
            if not running and status.running:
                running = True
            ossec_statuses.append(status)
        execution_id = emulation_env_config.execution_id
        emulation_name = emulation_env_config.name
        ossec_manager_info_dto = OSSECIDSManagersInfo(
            running=running, ips=ossec_ids_managers_ips, execution_id=execution_id,
            emulation_name=emulation_name, ossec_ids_statuses=ossec_statuses, ports=ossec_ids_managers_ports)
        return ossec_manager_info_dto
