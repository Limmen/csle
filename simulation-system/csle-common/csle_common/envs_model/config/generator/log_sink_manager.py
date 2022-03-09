import grpc
import time
from csle_common.dao.container_config.log_sink_config import LogSinkConfig
import csle_common.constants.constants as constants
import csle_collector.kafka_manager.kafka_manager_pb2_grpc
import csle_collector.kafka_manager.kafka_manager_pb2
import csle_collector.kafka_manager.query_kafka_server
from csle_common.envs_model.config.generator.generator_util import GeneratorUtil
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil


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
    def _start_kafka_manager_if_not_running(log_sink_config: LogSinkConfig, emulation_config: EmulationConfig) -> None:
        """
        Utility method for checking if the kafka manager is running and starting it if it is not running

        :param log_sink_config: the configuration of the log sink
        :param emulation_config: the emulation config
        :return: None
        """

        # Connect
        GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=log_sink_config.container.get_ips()[0])

        # Check if kafka_manager is already running
        cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
              + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.KAFKA_MANAGER_FILE_NAME
        o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
        t = constants.COMMANDS.SEARCH_KAFKA_MANAGER

        if not constants.COMMANDS.SEARCH_KAFKA_MANAGER in str(o):

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                  constants.COMMANDS.SPACE_DELIM \
                  + constants.TRAFFIC_COMMANDS.KAFKA_MANAGER_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            # Start the kafka_manager
            cmd = constants.COMMANDS.START_KAFKA_MANAGER.format(
                log_sink_config.kafka_manager_port)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            time.sleep(5)

    @staticmethod
    def create_topics(log_sink_config: LogSinkConfig, emulation_config: EmulationConfig) -> None:
        """
        A method that sends a request to the KafkaManager to create topics according to the given configuration

        :param log_sink_config: the configuration of the Kafka server
        :param emulation_config: the configuration of the emulation
        :return: None
        """
        print(f"creating kafka topics on container: {log_sink_config.container.get_ips()[0]}")

        LogSinkManager._start_kafka_manager_if_not_running(log_sink_config=log_sink_config,
                                                           emulation_config=emulation_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{log_sink_config.container.get_ips()[0]}:'
                f'{log_sink_config.kafka_manager_port}') as channel:
            stub = csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub(channel)
            kafka_dto = csle_collector.kafka_manager.query_kafka_server.get_kafka_status(stub)
            if not kafka_dto.running:
                print(f"Kafka server is not running, starting it.")
                csle_collector.kafka_manager.query_kafka_server.start_kafka(stub)
                time.sleep(15)

            for topic in log_sink_config.topics:
                print(f"Creating topic: {topic.name}")
                csle_collector.kafka_manager.query_kafka_server.create_topic(
                    stub, name=topic.name, partitions=topic.num_partitions, replicas=topic.num_replicas
                )


    @staticmethod
    def get_kafka_status(log_sink_config: LogSinkConfig, emulation_config: EmulationConfig) -> \
            csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
        """
        Method for querying the KafkaManager about the status of the Kafka server

        :param log_sink_config: the configuration of the Kafka server
        :param emulation_config: the emulation config
        :return: a KafkaDTO with the status of the server
        """
        LogSinkManager._start_kafka_manager_if_not_running(log_sink_config=log_sink_config,
                                                           emulation_config=emulation_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{log_sink_config.container.get_ips()[0]}:'
                f'{log_sink_config.kafka_manager_port}') as channel:
            stub = csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub(channel)
            kafka_dto = csle_collector.kafka_manager.query_kafka_server.get_kafka_status(stub)
            return kafka_dto