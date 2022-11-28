from typing import List
import grpc
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.kafka_managers_info import KafkaManagersInfo
import csle_common.constants.constants as constants
import csle_collector.kafka_manager.kafka_manager_pb2_grpc
import csle_collector.kafka_manager.kafka_manager_pb2
import csle_collector.kafka_manager.query_kafka_server
import csle_collector.kafka_manager.kafka_manager_util
from csle_common.util.emulation_util import EmulationUtil
from csle_common.logging.log import Logger


class KafkaController:

    @staticmethod
    def start_kafka_manager(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for starting the Kafka manager

        :param emulation_env_config: the emulation env config
        :return: None
        """

        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=emulation_env_config.kafka_config.container.get_ips()[0],
                                    create_producer=False)

        # Check if kafka_manager is already running
        cmd = (constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP + constants.COMMANDS.SPACE_DELIM +
               constants.TRAFFIC_COMMANDS.KAFKA_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd,
            conn=emulation_env_config.get_connection(ip=emulation_env_config.kafka_config.container.get_ips()[0]))

        if constants.COMMANDS.SEARCH_KAFKA_MANAGER not in str(o):
            Logger.__call__().get_logger().info(f"Starting the Kafka manager on node "
                                                f"{emulation_env_config.kafka_config.container.get_ips()[0]}")

            # Stop old background job if running
            cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
                   constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.KAFKA_MANAGER_FILE_NAME)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd,
                conn=emulation_env_config.get_connection(ip=emulation_env_config.kafka_config.container.get_ips()[0]))

            # Start the kafka_manager
            cmd = constants.COMMANDS.START_KAFKA_MANAGER.format(
                emulation_env_config.kafka_config.kafka_manager_port,
                emulation_env_config.kafka_config.kafka_manager_log_dir,
                emulation_env_config.kafka_config.kafka_manager_log_file,
                emulation_env_config.kafka_config.kafka_manager_max_workers)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd,
                conn=emulation_env_config.get_connection(ip=emulation_env_config.kafka_config.container.get_ips()[0]))
            time.sleep(2)

    @staticmethod
    def stop_kafka_manager(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for stopping the Kafka manager

        :param emulation_env_config: the emulation env config
        :return: None
        """

        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=emulation_env_config.kafka_config.container.get_ips()[0],
                                    create_producer=False)

        Logger.__call__().get_logger().info(f"Stopping the Kafka manager on node "
                                            f"{emulation_env_config.kafka_config.container.get_ips()[0]}")

        # Stop old background job if running
        cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
               constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.KAFKA_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd,
            conn=emulation_env_config.get_connection(ip=emulation_env_config.kafka_config.container.get_ips()[0]))
        time.sleep(2)

    @staticmethod
    def create_topics(emulation_env_config: EmulationEnvConfig) -> None:
        """
        A method that sends a request to the KafkaManager to create topics according to the given configuration

        :param emulation_env_config: the configuration of the emulation env
        :return: None
        """
        Logger.__call__().get_logger().info(
            f"creating kafka topics on container: {emulation_env_config.kafka_config.container.get_ips()[0]}")
        KafkaController.start_kafka_manager(emulation_env_config=emulation_env_config)
        kafka_dto = KafkaController.get_kafka_status_by_port_and_ip(
            ip=emulation_env_config.kafka_config.container.get_ips()[0],
            port=emulation_env_config.kafka_config.kafka_manager_port)
        with grpc.insecure_channel(
                f'{emulation_env_config.kafka_config.container.get_ips()[0]}:'
                f'{emulation_env_config.kafka_config.kafka_manager_port}') as channel:
            stub = csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub(channel)

            if not kafka_dto.running:
                # Open a gRPC session
                Logger.__call__().get_logger().info("Kafka server is not running, starting it.")

                csle_collector.kafka_manager.query_kafka_server.start_kafka(stub)
                time.sleep(20)

            for topic in emulation_env_config.kafka_config.topics:
                Logger.__call__().get_logger().info(f"Creating topic: {topic.name}")
                csle_collector.kafka_manager.query_kafka_server.create_topic(
                    stub, name=topic.name, partitions=topic.num_partitions, replicas=topic.num_replicas,
                    retention_time_hours=topic.retention_time_hours
                )

    @staticmethod
    def get_kafka_status(emulation_env_config: EmulationEnvConfig) -> \
            csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
        """
        Method for querying the KafkaManager about the status of the Kafka server

        :param emulation_env_config: the emulation config
        :return: a KafkaDTO with the status of the server
        """
        KafkaController.start_kafka_manager(emulation_env_config=emulation_env_config)
        kafka_dto = KafkaController.get_kafka_status_by_port_and_ip(
            ip=emulation_env_config.kafka_config.container.get_ips()[0],
            port=emulation_env_config.kafka_config.kafka_manager_port)
        return kafka_dto

    @staticmethod
    def get_kafka_status_by_port_and_ip(ip: str, port: int) -> \
            csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
        """
        Method for querying the KafkaManager about the status of the Kafka server

        :param ip: the ip where the KafkaManager is running
        :param port: the port the KafkaManager is listening to
        :return: a KafkaDTO with the status of the server
        """
        # Open a gRPC session
        with grpc.insecure_channel(
                f'{ip}:'
                f'{port}') as channel:
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
            f"Stopping kafka server on container: {emulation_env_config.kafka_config.container.get_ips()[0]}")
        KafkaController.start_kafka_manager(emulation_env_config=emulation_env_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.kafka_config.container.get_ips()[0]}:'
                f'{emulation_env_config.kafka_config.kafka_manager_port}') as channel:
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
            f"Starting kafka server on container: {emulation_env_config.kafka_config.container.get_ips()[0]}")
        KafkaController.start_kafka_manager(emulation_env_config=emulation_env_config)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.kafka_config.container.get_ips()[0]}:'
                f'{emulation_env_config.kafka_config.kafka_manager_port}') as channel:
            stub = csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub(channel)
            kafka_dto = csle_collector.kafka_manager.query_kafka_server.start_kafka(stub)
            return kafka_dto

    @staticmethod
    def get_kafka_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the IPS of the Kafka managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        return [emulation_env_config.kafka_config.container.get_ips()[0]]

    @staticmethod
    def get_kafka_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the IPS of the Kafka managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        return [emulation_env_config.kafka_config.kafka_manager_port]

    @staticmethod
    def get_kafka_managers_info(emulation_env_config: EmulationEnvConfig, active_ips: List[str]) -> KafkaManagersInfo:
        """
        Extracts the information of the Kafka managers for a given emulation

        :param emulation_env_config: the configuration of the emulation
        :return: a DTO with the status of the Kafka managers
        """
        kafka_managers_ips = KafkaController.get_kafka_managers_ips(emulation_env_config=emulation_env_config)
        kafka_managers_ports = KafkaController.get_kafka_managers_ports(emulation_env_config=emulation_env_config)
        kafka_managers_statuses = []
        kafka_managers_running = []
        for ip in kafka_managers_ips:
            if ip not in active_ips:
                continue
            running = False
            status = None
            try:
                status = KafkaController.get_kafka_status_by_port_and_ip(
                    port=emulation_env_config.kafka_config.kafka_manager_port, ip=ip)
                running = True
            except Exception as e:
                Logger.__call__().get_logger().debug(
                    f"Could not fetch Kafka manager status on IP:{ip}, error: {str(e)}, {repr(e)}")
            if status is not None:
                kafka_managers_statuses.append(status)
            else:
                kafka_managers_statuses.append(
                    csle_collector.kafka_manager.kafka_manager_util.KafkaManagerUtil.kafka_dto_empty())
            kafka_managers_running.append(running)
        execution_id = emulation_env_config.execution_id
        emulation_name = emulation_env_config.name
        kafka_manager_info_dto = KafkaManagersInfo(
            kafka_managers_running=kafka_managers_running, ips=kafka_managers_ips, execution_id=execution_id,
            emulation_name=emulation_name, kafka_managers_statuses=kafka_managers_statuses,
            ports=kafka_managers_ports)
        return kafka_manager_info_dto
