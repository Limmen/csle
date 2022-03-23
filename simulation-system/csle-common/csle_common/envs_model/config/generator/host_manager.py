from typing import List
import grpc
import time
from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.dao.container_config.log_sink_config import LogSinkConfig
from csle_common.dao.container_config.emulation_env_config import EmulationEnvConfig
import csle_common.constants.constants as constants
import csle_collector.host_manager.host_manager_pb2_grpc
import csle_collector.host_manager.host_manager_pb2
import csle_collector.host_manager.query_host_manager
from csle_common.envs_model.config.generator.generator_util import GeneratorUtil
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil


class HostManager:

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
    def _start_host_managers_if_not_running(emulation_config: EmulationConfig, containers_cfg: ContainersConfig,
                                            log_sink_config: LogSinkConfig) -> None:
        """
        Utility method for checking if the host manager is running and starting it if it is not running

        :param log_sink_config: the configuration of the log sink
        :param containers_cfg: the container configurations
        :param emulation_config: the emulation config
        :return: None
        """
        for c in containers_cfg.containers:
            # Connect
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=c.get_ips()[0])

            # Check if host_manager is already running
            cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
                  + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.HOST_MANAGER_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            if not constants.COMMANDS.SEARCH_HOST_MANAGER in str(o):

                print(f"Starting host manager on node {c.get_ips()[0]}")

                # Stop old background job if running
                cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                      constants.COMMANDS.SPACE_DELIM \
                      + constants.TRAFFIC_COMMANDS.HOST_MANAGER_FILE_NAME
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

                # Start the host_manager
                cmd = constants.COMMANDS.START_HOST_MANAGER.format(log_sink_config.secondary_grpc_port)
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
                time.sleep(5)

    @staticmethod
    def start_host_monitor_thread(containers_cfg: ContainersConfig, emulation_config: EmulationConfig,
                                 log_sink_config: LogSinkConfig) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and the monitor thread

        :param log_sink_config: the configuration of the log sink
        :param containers_cfg: the container configurations
        :param emulation_config: the emulation config
        :return: None
        """
        HostManager._start_host_managers_if_not_running(
            log_sink_config=log_sink_config, emulation_config=emulation_config, containers_cfg=containers_cfg)

        for c in containers_cfg.containers:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{c.get_ips()[0]}:{log_sink_config.secondary_grpc_port}') as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                host_monitor_dto = csle_collector.host_manager.query_host_manager.get_host_monitor_status(stub)
                if not host_monitor_dto.running:
                    print(f"Host monitor thread is not running on {c.get_ips()[0]}, starting it.")
                    csle_collector.host_manager.query_host_manager.start_host_monitor(
                        stub=stub, kafka_ip=log_sink_config.container.get_ips()[0],
                        kafka_port=log_sink_config.kafka_port,
                        time_step_len_seconds=log_sink_config.time_step_len_seconds)


    @staticmethod
    def stop_host_monitor_thread(containers_cfg: ContainersConfig, emulation_config: EmulationConfig,
                                log_sink_config: LogSinkConfig) -> None:
        """
        A method that sends a request to the HostManager on every container to stop the monitor threads

        :param log_sink_config: the configuration of the log sink
        :param containers_cfg: the container configurations
        :param emulation_config: the emulation config
        :return: None
        """
        HostManager._start_host_managers_if_not_running(
            log_sink_config=log_sink_config, emulation_config=emulation_config, containers_cfg=containers_cfg)

        for c in containers_cfg.containers:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{c.get_ips()[0]}:'
                    f'{log_sink_config.secondary_grpc_port}') as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                host_monitor_dto = csle_collector.host_manager.query_host_manager.get_host_monitor_status(stub)
                print(f"Stopping the Host monitor thread on {c.get_ips()[0]}.")
                csle_collector.host_manager.query_host_manager.stop_host_monitor(stub=stub)

    @staticmethod
    def get_host_monitor_thread_status(emulation_env_config: EmulationEnvConfig) -> \
            List[csle_collector.host_manager.host_manager_pb2.HostMonitorDTO]:
        """
        A method that sends a request to the HostManager on every container to get the status of the Host monitor thread

        :param emulation_env_config: the emulation config
        :return: List of monitor thread statuses
        """
        emulation_config = EmulationConfig(agent_ip=emulation_env_config.containers_config.agent_ip,
                                           agent_username=constants.CSLE_ADMIN.USER,
                                           agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)

        statuses = []
        HostManager._start_host_managers_if_not_running(
            log_sink_config=emulation_env_config.log_sink_config,
            emulation_config=emulation_config, containers_cfg=emulation_env_config.containers_config)

        for c in emulation_env_config.containers_config.containers:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{c.get_ips()[0]}:'
                    f'{emulation_env_config.log_sink_config.secondary_grpc_port}') as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                status = csle_collector.host_manager.query_host_manager.get_host_monitor_status(stub=stub)
                statuses.append(status)
        return statuses


    @staticmethod
    def get_host_log_data(containers_cfg: ContainersConfig, emulation_config: EmulationConfig,
                         log_sink_config: LogSinkConfig, failed_auth_last_ts: float,
                          login_last_ts: float) \
            -> List[csle_collector.host_manager.host_manager_pb2.HostMetricsDTO]:
        """
        A method that sends a request to the HostManager on every container to get contents of the Hostmetrics
        given timestamps

        :param log_sink_config: the configuration of the log sink
        :param containers_cfg: the container configurations
        :param emulation_config: the emulation config
        :param failed_auth_last_ts: the timestamp to read the last failed login attempts from
        :param login_last_ts: the timestamp to read the last successful login attempts from
        :return: List of monitor thread statuses
        """
        host_metrics_data_list = []
        HostManager._start_host_managers_if_not_running(
            log_sink_config=log_sink_config, emulation_config=emulation_config, containers_cfg=containers_cfg)

        for c in containers_cfg.containers:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{c.get_ips()[0]}:'
                    f'{log_sink_config.secondary_grpc_port}') as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                host_metrics_data = csle_collector.host_manager.query_host_manager.get_host_metrics(
                    stub=stub, failed_auth_last_ts=failed_auth_last_ts, login_last_ts=login_last_ts)
                host_metrics_data_list.append(host_metrics_data)
        return host_metrics_data_list
