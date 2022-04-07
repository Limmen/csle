from typing import List
import grpc
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
import csle_common.constants.constants as constants
import csle_collector.constants.constants as csle_collector_constants
import csle_collector.ids_manager.ids_manager_pb2_grpc
import csle_collector.ids_manager.ids_manager_pb2
import csle_collector.ids_manager.query_ids_manager
from csle_common.util.emulation_util import EmulationUtil
from csle_common.logging.log import Logger


class IDSManager:

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
    def start_ids(emulation_env_config: EmulationEnvConfig):
        """
        Utility function for starting the IDS

        :param emulation_config: the emulation env configuration
        :return:
        """
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.IDS_IMAGES:
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
                    Logger.__call__().get_logger().info(f"Starting Snort IDS on {c.get_ips()[0]}")
                    o, e, _ = EmulationUtil.execute_ssh_cmd(
                        cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                    continue

    @staticmethod
    def _start_ids_manager_if_not_running(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for checking if the ids manager is running and starting it if it is not running

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.IDS_IMAGES:
                if ids_image in c.name:
                    # Connect
                    EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=c.get_ips()[0])

                    # Check if ids_manager is already running
                    cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
                          + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.IDS_MANAGER_FILE_NAME
                    o, e, _ = EmulationUtil.execute_ssh_cmd(
                        cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                    t = constants.COMMANDS.SEARCH_IDS_MANAGER

                    if not constants.COMMANDS.SEARCH_IDS_MANAGER in str(o):

                        # Stop old background job if running
                        cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                              constants.COMMANDS.SPACE_DELIM \
                              + constants.TRAFFIC_COMMANDS.IDS_MANAGER_FILE_NAME
                        o, e, _ = EmulationUtil.execute_ssh_cmd(
                            cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))

                        # Start the ids_manager
                        cmd = constants.COMMANDS.START_IDS_MANAGER.format(
                            emulation_env_config.log_sink_config.default_grpc_port)
                        o, e, _ = EmulationUtil.execute_ssh_cmd(
                            cmd=cmd, conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                        time.sleep(5)

    @staticmethod
    def start_ids_monitor_thread(emulation_env_config: EmulationEnvConfig) -> None:
        """
        A method that sends a request to the IDSManager on every container that runs
        an IDS to start the IDS manager and the monitor thread
n
        :param emulation_env_config: the emulation env config
        :return: None
        """
        IDSManager._start_ids_manager_if_not_running(emulation_env_config=emulation_env_config)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.IDS_IMAGES:
                if ids_image in c.name:
                    # Open a gRPC session
                    with grpc.insecure_channel(
                            f'{c.get_ips()[0]}:'
                            f'{emulation_env_config.log_sink_config.default_grpc_port}') as channel:
                        stub = csle_collector.ids_manager.ids_manager_pb2_grpc.IdsManagerStub(channel)
                        ids_monitor_dto = csle_collector.ids_manager.query_ids_manager.get_ids_monitor_status(stub)
                        if not ids_monitor_dto.running:
                            Logger.__call__().get_logger().info(
                                f"IDS monitor thread is not running on {c.get_ips()[0]}, starting it.")
                            csle_collector.ids_manager.query_ids_manager.start_ids_monitor(
                                stub=stub, kafka_ip=emulation_env_config.log_sink_config.container.get_ips()[0],
                                kafka_port=emulation_env_config.log_sink_config.kafka_port,
                                log_file_path=csle_collector_constants.IDS_ROUTER.FAST_LOG_FILE,
                                time_step_len_seconds=emulation_env_config.log_sink_config.time_step_len_seconds)


    @staticmethod
    def stop_ids_monitor_thread(emulation_env_config: EmulationEnvConfig) -> None:
        """
        A method that sends a request to the IDSManager on every container that runs
        an IDS to stop the monitor threads

        :param emulation_env_config: the emulation env config
        :return: None
        """
        IDSManager._start_ids_manager_if_not_running(emulation_env_config=emulation_env_config)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.IDS_IMAGES:
                if ids_image in c.name:
                    # Open a gRPC session
                    with grpc.insecure_channel(
                            f'{c.get_ips()[0]}:'
                            f'{emulation_env_config.log_sink_config.default_grpc_port}') as channel:
                        stub = csle_collector.ids_manager.ids_manager_pb2_grpc.IdsManagerStub(channel)
                        ids_monitor_dto = csle_collector.ids_manager.query_ids_manager.get_ids_monitor_status(stub)
                        Logger.__call__().get_logger().info(
                            f"Stopping the IDS monitor thread on {c.get_ips()[0]}.")
                        csle_collector.ids_manager.query_ids_manager.stop_ids_monitor(stub=stub)

    @staticmethod
    def get_ids_monitor_thread_status(emulation_env_config: EmulationEnvConfig) -> \
            List[csle_collector.ids_manager.ids_manager_pb2.IdsMonitorDTO]:
        """
        A method that sends a request to the IDSManager on every container to get the status of the IDS monitor thread

        :param emulation_env_config: the emulation config
        :return: List of monitor thread statuses
        """
        statuses = []
        IDSManager._start_ids_manager_if_not_running(emulation_env_config=emulation_env_config)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.IDS_IMAGES:
                if ids_image in c.name:
                    # Open a gRPC session
                    with grpc.insecure_channel(
                            f'{c.get_ips()[0]}:'
                            f'{emulation_env_config.log_sink_config.default_grpc_port}') as channel:
                        stub = csle_collector.ids_manager.ids_manager_pb2_grpc.IdsManagerStub(channel)
                        status = csle_collector.ids_manager.query_ids_manager.get_ids_monitor_status(stub=stub)
                        statuses.append(status)
        return statuses

    @staticmethod
    def get_ids_log_data(emulation_env_config: EmulationEnvConfig, timestamp: float) \
            -> List[csle_collector.ids_manager.ids_manager_pb2.IdsLogDTO]:
        """
        A method that sends a request to the IDSManager on every container to get contents of the IDS log from
        a given timestamp

        :param emulation_env_config: the emulation env config
        :param timestamp: the timestamp to read the IDS log from
        :return: List of monitor thread statuses
        """
        ids_log_data_list = []
        IDSManager._start_ids_manager_if_not_running(emulation_env_config=emulation_env_config)

        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.IDS_IMAGES:
                if ids_image in c.name:
                    # Open a gRPC session
                    with grpc.insecure_channel(
                            f'{c.get_ips()[0]}:'
                            f'{emulation_env_config.log_sink_config.default_grpc_port}') as channel:
                        stub = csle_collector.ids_manager.ids_manager_pb2_grpc.IdsManagerStub(channel)
                        ids_log_data = csle_collector.ids_manager.query_ids_manager.get_ids_alerts(
                            stub=stub, timestamp=timestamp,
                            log_file_path=csle_collector_constants.IDS_ROUTER.FAST_LOG_FILE)
                        ids_log_data_list.append(ids_log_data)
        return ids_log_data_list
