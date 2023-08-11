from typing import Tuple, List
import time
import logging
import subprocess
import os
from concurrent import futures
import grpc
import socket
import netifaces
import confluent_kafka
import confluent_kafka.admin
import csle_collector.kafka_manager.kafka_manager_pb2_grpc
import csle_collector.kafka_manager.kafka_manager_pb2
import csle_collector.constants.constants as constants
from csle_collector.kafka_manager.kafka_manager_util import KafkaManagerUtil


class KafkaManagerServicer(csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerServicer):
    """
    gRPC server for managing a Kafka server. Allows to start/stop the kafka server remotely and also to query the
    state of the server and create/delete topics.
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        logging.basicConfig(filename=f"{constants.LOG_FILES.KAFKA_MANAGER_LOG_DIR}"
                                     f"{constants.LOG_FILES.KAFKA_MANAGER_LOG_FILE}", level=logging.INFO)
        self.hostname = socket.gethostname()
        try:
            self.ip = netifaces.ifaddresses(constants.INTERFACES.ETH0)[netifaces.AF_INET][0][constants.INTERFACES.ADDR]
        except Exception:
            self.ip = socket.gethostbyname(self.hostname)
        self.conf = {constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.ip}:{constants.KAFKA.PORT}",
                     constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        logging.info(f"Setting up KafkaManager hostname: {self.hostname} ip: {self.ip}")

    def _get_kafka_status_and_topics(self) -> Tuple[bool, List[str]]:
        """
        Utility method to get the status of Kafka and existing topics

        :return: status and list of topics
        """
        status_output = subprocess.run(constants.KAFKA.KAFKA_STATUS.split(" "), capture_output=True, text=True).stdout
        running = not ("not" in status_output)
        topics = []
        if running:
            client = confluent_kafka.admin.AdminClient(self.conf)
            try:
                cluster_metadata = client.list_topics(timeout=1)
                for k, v in cluster_metadata.topics.items():
                    topics.append(k)
            except Exception as e:
                logging.info(f"There was an exception listing the Kafka topics: {str(e)}, {repr(e)}")
        return running, topics

    def getKafkaStatus(self, request: csle_collector.kafka_manager.kafka_manager_pb2.GetKafkaStatusMsg,
                       context: grpc.ServicerContext) \
            -> csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
        """
        Gets the state of the kafka server

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the kafka server
        """
        running, topics = self._get_kafka_status_and_topics()
        kafka_dto = csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO(running=running, topics=topics)
        return kafka_dto

    def stopKafka(self, request: csle_collector.kafka_manager.kafka_manager_pb2.StopKafkaMsg,
                  context: grpc.ServicerContext):
        """
        Stops the kafka server

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the kafka server
        """
        logging.info("Stopping kafka")
        os.system(constants.KAFKA.KAFKA_STOP)
        return csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO(running=False, topics=[])

    def startKafka(self, request: csle_collector.kafka_manager.kafka_manager_pb2.StartKafkaMsg,
                   context: grpc.ServicerContext) -> csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
        """
        Starts the kafka server

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the kafka server
        """
        logging.info("Starting kafka")
        os.system(constants.KAFKA.KAFKA_START)
        kafka_dto = csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO(running=True, topics=[])
        return kafka_dto

    def createTopic(self, request: csle_collector.kafka_manager.kafka_manager_pb2.CreateTopicMsg,
                    context: grpc.ServicerContext) -> csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
        """
        Creates a new Kafka topic

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the kafka server
        """
        logging.info(f"Creating topic: {request.name}, partitions:{request.partitions}, replicas:{request.replicas}, "
                     f"retention hours: {request.retention_time_hours}")
        running, topics = self._get_kafka_status_and_topics()
        client = confluent_kafka.admin.AdminClient(self.conf)
        config = {
            constants.KAFKA.RETENTION_MS_CONFIG_PROPERTY: KafkaManagerUtil.hours_to_ms(request.retention_time_hours)}
        new_topic = confluent_kafka.admin.NewTopic(
            request.name, request.partitions, request.replicas,
            config=config)
        client.create_topics([new_topic])
        time.sleep(5)
        kafka_dto = csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO(running=True,
                                                                            topics=topics + [request.name])
        return kafka_dto


def serve(port: int = 50051, log_dir: str = "/", max_workers: int = 10,
          log_file_name: str = "kafka_manager.log") -> None:
    """
    Starts the gRPC server for managing the kafka server

    :param port: the port that the server will listen to
    :param log_dir: the directory to write the log file
    :param log_file_name: the file name of the log
    :param max_workers: the maximum number of GRPC workers
    :return: None
    """
    constants.LOG_FILES.KAFKA_MANAGER_LOG_DIR = log_dir
    constants.LOG_FILES.KAFKA_MANAGER_LOG_FILE = log_file_name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    csle_collector.kafka_manager.kafka_manager_pb2_grpc.add_KafkaManagerServicer_to_server(
        KafkaManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"KafkaManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
