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
                    cmd = constants.COMMANDS.STOP_SNORT_IDS
                    o, e, _ = EmulationUtil.execute_ssh_cmd(
                        cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                    time.sleep(1)
                    cmd = constants.COMMANDS.START_SNORT_IDS
                    Logger.__call__().get_logger().info(f"Starting OSSEC IDS on {c.get_ips()[0]}")
                    o, e, _ = EmulationUtil.execute_ssh_cmd(
                        cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                    continue

    @staticmethod
    def start_ossec_idses_managers(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for starting OSSEC IDS managers

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    OSSECIDSController.start_ossec_ids_manager(emulation_env_config=emulation_env_config,
                                                               ip=c.get_ips()[0])

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
        cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
              + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.OSSEC_IDS_MANAGER_FILE_NAME
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
        t = constants.COMMANDS.SEARCH_OSSEC_IDS_MANAGER

        if not constants.COMMANDS.SEARCH_OSSEC_IDS_MANAGER in str(o):

            Logger.__call__().get_logger().info(f"Starting OSSEC IDS manager on node {ip}")

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                  constants.COMMANDS.SPACE_DELIM \
                  + constants.TRAFFIC_COMMANDS.OSSEC_IDS_MANAGER_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))

            # Start the OSSEC ids_manager
            cmd = constants.COMMANDS.START_OSSEC_IDS_MANAGER.format(
                emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            time.sleep(5)

    @staticmethod
    def stop_ossec_idses_managers(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for stopping ossec ids managers

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    OSSECIDSController.stop_ossec_ids_manager(emulation_env_config=emulation_env_config,
                                                              ip=c.get_ips()[0])

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

        cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
              constants.COMMANDS.SPACE_DELIM \
              + constants.TRAFFIC_COMMANDS.OSSEC_IDS_MANAGER_FILE_NAME
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))

        time.sleep(5)

    @staticmethod
    def start_ossec_idses_monitor_threads(emulation_env_config: EmulationEnvConfig) -> None:
        """
        A method that sends a request to the OSSECIDSManager on every container that runs
        an IDS to start the IDS manager and the monitor thread

        :param emulation_env_config: the emulation env config
        :return: None
        """
        OSSECIDSController.start_ossec_idses_managers(emulation_env_config=emulation_env_config)
        time.sleep(10)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    OSSECIDSController.start_ossec_ids_monitor_thread(emulation_env_config=emulation_env_config,
                                                                      ip=c.get_ips()[0])

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
            port=emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port, ip = ip)
        if not ids_monitor_dto.running:
            Logger.__call__().get_logger().info(
                f"OSSEC IDS monitor thread is not running on {ip}, starting it.")
            with grpc.insecure_channel(
                    f'{ip}:'
                    f'{emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port}') as channel:
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
                f'{emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port}') as channel:
            stub = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub(channel)
            Logger.__call__().get_logger().info(
                f"Stopping the OSSEC IDS monitor thread on {ip}.")
            csle_collector.ossec_ids_manager.query_ossec_ids_manager.stop_ossec_ids_monitor(stub=stub)

    @staticmethod
    def stop_ossec_idses_monitor_threads(emulation_env_config: EmulationEnvConfig) -> None:
        """
        A method that sends a request to the OSSECIDSManager on every container that runs
        an IDS to stop the monitor threads

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    OSSECIDSController.stop_ossec_ids_monitor_thread(emulation_env_config=emulation_env_config,
                                                                     ip=c.get_ips()[0])

    @staticmethod
    def get_ossec_idses_monitor_threads_statuses(emulation_env_config: EmulationEnvConfig) -> \
            List[csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO]:
        """
        A method that sends a request to the OSSECIDSManager on every container to get the status of the IDS monitor thread

        :param emulation_env_config: the emulation config
        :return: List of monitor thread statuses
        """
        statuses = []
        OSSECIDSController.start_ossec_idses_managers(emulation_env_config=emulation_env_config)
        time.sleep(10)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    status = OSSECIDSController.get_ossec_ids_monitor_thread_status_by_ip_and_port(
                        port=emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port, ip = c.get_ips()[0])
                    statuses.append(status)
        return statuses

    @staticmethod
    def get_ossec_idses_log_data(emulation_env_config: EmulationEnvConfig, timestamp: float) \
            -> List[csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsLogDTO]:
        """
        A method that sends a request to the OSSEC IDSManager on every container to get contents of the IDS log from
        a given timestamp

        :param emulation_env_config: the emulation env config
        :param timestamp: the timestamp to read the IDS log from
        :return: List of monitor thread statuses
        """
        ids_log_data_list = []
        OSSECIDSController.start_ossec_idses_managers(emulation_env_config=emulation_env_config)
        time.sleep(10)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES:
                if ids_image in c.name:
                    # Open a gRPC session
                    with grpc.insecure_channel(
                            f'{c.get_ips()[0]}:'
                            f'{emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port}') as channel:
                        stub = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub(channel)
                        ids_log_data = csle_collector.ossec_ids_manager.query_ossec_ids_manager.get_ossec_ids_alerts(
                            stub=stub, timestamp=timestamp,
                            log_file_path=csle_collector_constants.OSSEC.OSSEC_ALERTS_FILE)
                        ids_log_data_list.append(ids_log_data)
        return ids_log_data_list

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
                    try:
                        OSSECIDSController.get_ossec_ids_monitor_thread_status_by_ip_and_port(
                            port=emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port, ip = c.get_ips()[0])
                        ips.append(c.get_ips()[0])
                    except Exception as e:
                        pass
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
                    try:
                        OSSECIDSController.get_ossec_ids_monitor_thread_status_by_ip_and_port(
                            port=emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port, ip = c.get_ips()[0])
                        ports.append(emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port)
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
        ossec_ids_managers_ips = OSSECIDSController.get_ossec_idses_managers_ips(emulation_env_config=emulation_env_config)
        ossec_ids_managers_ports = \
            OSSECIDSController.get_ossec_idses_managers_ports(emulation_env_config=emulation_env_config)
        ossec_statuses = []
        running = False
        status = None
        for ip in ossec_ids_managers_ips:
            try:
                status = OSSECIDSController.get_ossec_ids_monitor_thread_status_by_ip_and_port(
                    port=emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port, ip=ip)
                running = True
            except Exception as e:
                Logger.__call__().get_logger().debug(
                    f"Could not fetch OSSEC IDS manager status on IP:{ip}, error: {str(e)}, {repr(e)}")
            if status is not None:
                ossec_statuses.append(status)
            else:
                ossec_statuses.append(
                    csle_collector.ossec_ids_manager.ossec_ids_manager_util.OSSecManagerUtil.ossec_ids_log_dto_empty())
        execution_id = emulation_env_config.execution_id
        emulation_name = emulation_env_config.name
        ossec_manager_info_dto = OSSECIDSManagersInfo(
            running=running, ips=ossec_ids_managers_ips, execution_id=execution_id,
            emulation_name=emulation_name, ossec_ids_statuses=ossec_statuses, ports=ossec_ids_managers_ports)
        return ossec_manager_info_dto
