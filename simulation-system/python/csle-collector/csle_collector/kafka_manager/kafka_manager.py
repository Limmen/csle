import time
from typing import Tuple, List
import logging
import subprocess
import os
from concurrent import futures
import grpc
import socket
import confluent_kafka
import confluent_kafka.admin
import csle_collector.kafka_manager.kafka_manager_pb2_grpc
import csle_collector.kafka_manager.kafka_manager_pb2
import csle_collector.constants.constants as constants


class KafkaManagerServicer(csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerServicer):
    """
    gRPC server for managing a Kafka server. Allows to start/stop the kafka server remotely and also to query the
    state of the server and create/delete topics.
    """

    def __init__(self, ip : str=None, hostname :str = None,) -> None:
        """
        Initializes the server

        :param ip: the ip of the kafka server
        :param hostname: the hostname of the kafka server
        """
        logging.basicConfig(filename=f"/{constants.LOG_FILES.KAFKA_MANAGER_LOG_FILE}", level=logging.INFO)
        self.ip = ip
        self.hostname = hostname
        if self.hostname is None:
            self.hostname = socket.gethostname()
        if self.ip is None:
            self.ip = socket.gethostbyname(self.hostname)
        self.conf = {constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.ip}:{constants.KAFKA.PORT}",
                constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        logging.info(f"Setting up KafkaManager hostname: {self.hostname} ip: {self.ip}")

    def _get_kafka_status_and_topics(self) -> Tuple[bool, List[str]]:
        """
        Utility method to get the status of Kafka and existing topics

        :return: status and list of topics
        """
        p = subprocess.Popen(constants.KAFKA.KAFKA_STATUS, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        status_output = output.decode()
        running = not ("not" in status_output)
        topics = []
        if running:
            client = confluent_kafka.admin.AdminClient(self.conf)
            try:
                cluster_metadata = client.list_topics(timeout=1)
                for k,v in cluster_metadata.topics.items():
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
        kafka_dto = csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO(
            running = running,
            topics = topics
        )
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
        return csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO(
            running = False,
            topics = []
        )

    def startKafka(self, request: csle_collector.kafka_manager.kafka_manager_pb2.StartKafkaMsg,
                     context: grpc.ServicerContext) -> csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
        """
        Starts the kafka server

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the kafka server
        """
        logging.info(f"Starting kafka")
        os.system(constants.KAFKA.KAFKA_START)
        kafka_dto = csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO(
            running = True,
            topics = []
        )
        return kafka_dto

    def hours_to_ms(self, hours: int) -> float:
        """
        Convert hours to ms

        :param hours: the hours to convert
        :return: the ms
        """
        return int((((hours*1000)*60)*60))

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
            constants.KAFKA.RETENTION_MS_CONFIG_PROPERTY: self.hours_to_ms(request.retention_time_hours)}
        new_topic = confluent_kafka.admin.NewTopic(
            request.name, request.partitions, request.replicas,
            config=config)
        client.create_topics([new_topic,])
        time.sleep(5)
        kafka_dto = csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO(
            running = True,
            topics = topics + [request.name]
        )
        return kafka_dto


def serve(port : int = 50051, ip=None, hostname=None) -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :return: None
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    csle_collector.kafka_manager.kafka_manager_pb2_grpc.add_KafkaManagerServicer_to_server(
        KafkaManagerServicer(hostname=hostname, ip=ip), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"KafkaManager Server Started, Listening on port: {port}")
    server.wait_for_termination()



# Program entrypoint
if __name__ == '__main__':
    serve(port=50051)