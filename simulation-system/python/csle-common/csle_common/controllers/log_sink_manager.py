import grpc
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
import csle_common.constants.constants as constants
import csle_collector.kafka_manager.kafka_manager_pb2_grpc
import csle_collector.kafka_manager.kafka_manager_pb2
import csle_collector.kafka_manager.query_kafka_server
from csle_common.util.emulation_util import EmulationUtil
from csle_common.logging.log import Logger


class LogSinkManager:

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
    def _start_kafka_manager_if_not_running(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for checking if the kafka manager is running and starting it if it is not running

        :param emulation_env_config: the emulation env config
        :return: None
        """

        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=emulation_env_config.log_sink_config.container.get_ips()[0],
                                    create_producer=False)

        # Check if kafka_manager is already running
        cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
              + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.KAFKA_MANAGER_FILE_NAME
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd,
            conn=emulation_env_config.get_connection(ip=emulation_env_config.log_sink_config.container.get_ips()[0]))
        t = constants.COMMANDS.SEARCH_KAFKA_MANAGER

        if not constants.COMMANDS.SEARCH_KAFKA_MANAGER in str(o):

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                  constants.COMMANDS.SPACE_DELIM \
                  + constants.TRAFFIC_COMMANDS.KAFKA_MANAGER_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd,
                conn=
                emulation_env_config.get_connection(ip=emulation_env_config.log_sink_config.container.get_ips()[0]))

            # Start the kafka_manager
            cmd = constants.COMMANDS.START_KAFKA_MANAGER.format(
                emulation_env_config.log_sink_config.default_grpc_port)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd,
                conn=
                emulation_env_config.get_connection(ip=emulation_env_config.log_sink_config.container.get_ips()[0]))
            time.sleep(5)

    @staticmethod
    def create_topics(emulation_env_config: EmulationEnvConfig) -> None:
        """
        A method that sends a request to the KafkaManager to create topics according to the given configuration

        :param emulation_env_config: the configuration of the emulation env
        :return: None
        """
        Logger.__call__().get_logger().info(
            f"creating kafka topics on container: {emulation_env_config.log_sink_config.container.get_ips()[0]}")
        LogSinkManager._start_kafka_manager_if_not_running(emulation_env_config=emulation_env_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.log_sink_config.container.get_ips()[0]}:'
                f'{emulation_env_config.log_sink_config.default_grpc_port}') as channel:
            stub = csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub(channel)
            kafka_dto = csle_collector.kafka_manager.query_kafka_server.get_kafka_status(stub)
            if not kafka_dto.running:
                Logger.__call__().get_logger().info(f"Kafka server is not running, starting it.")
                csle_collector.kafka_manager.query_kafka_server.start_kafka(stub)
                time.sleep(15)

            for topic in emulation_env_config.log_sink_config.topics:
                Logger.__call__().get_logger().info(f"Creating topic: {topic.name}")
                csle_collector.kafka_manager.query_kafka_server.create_topic(
                    stub, name=topic.name, partitions=topic.num_partitions, replicas=topic.num_replicas
                )


    @staticmethod
    def get_kafka_status(emulation_env_config: EmulationEnvConfig) -> \
            csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
        """
        Method for querying the KafkaManager about the status of the Kafka server

        :param emulation_env_config: the emulation config
        :return: a KafkaDTO with the status of the server
        """
        LogSinkManager._start_kafka_manager_if_not_running(emulation_env_config=emulation_env_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.log_sink_config.container.get_ips()[0]}:'
                f'{emulation_env_config.log_sink_config.default_grpc_port}') as channel:
            stub = csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub(channel)
            kafka_dto = csle_collector.kafka_manager.query_kafka_server.get_kafka_status(stub)
            return kafka_dto


    @staticmethod
    def stop_kafka_server(emulation_env_config: EmulationEnvConfig) -> \
            csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
        """
        Method for requesting the KafkaManager to stop the Kafka server

        :param emulation_env_config: the emulation env config
        :return: a KafkaDTO with the status of the server
        """
        Logger.__call__().get_logger().info(
            f"Stopping kafka server on container: {emulation_env_config.log_sink_config.container.get_ips()[0]}")
        LogSinkManager._start_kafka_manager_if_not_running(emulation_env_config=emulation_env_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.log_sink_config.container.get_ips()[0]}:'
                f'{emulation_env_config.log_sink_config.default_grpc_port}') as channel:
            stub = csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub(channel)
            kafka_dto = csle_collector.kafka_manager.query_kafka_server.stop_kafka(stub)
            return kafka_dto


    @staticmethod
    def start_kafka_server(emulation_env_config: EmulationEnvConfig) -> \
            csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
        """
        Method for requesting the KafkaManager to start the Kafka server

        :param emulation_env_config: the emulation env config
        :return: a KafkaDTO with the status of the server
        """
        Logger.__call__().get_logger().info(
            f"Starting kafka server on container: {emulation_env_config.log_sink_config.container.get_ips()[0]}")
        LogSinkManager._start_kafka_manager_if_not_running(emulation_env_config=emulation_env_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.log_sink_config.container.get_ips()[0]}:'
                f'{emulation_env_config.log_sink_config.default_grpc_port}') as channel:
            stub = csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub(channel)
            kafka_dto = csle_collector.kafka_manager.query_kafka_server.start_kafka(stub)
            return kafka_dto