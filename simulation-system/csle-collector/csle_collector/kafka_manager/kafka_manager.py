import time
from typing import Tuple, List
import logging
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
        logging.basicConfig(filename="/kafka_manager.log", level=logging.INFO)
        self.ip = ip
        self.hostname = hostname
        if self.hostname is None:
            self.hostname = socket.gethostname()
        if self.ip is None:
            self.ip = socket.gethostbyname(self.hostname)
        self.conf = {'bootstrap.servers': f"{self.ip}:9092",
                'client.id': self.hostname}
        logging.info(f"Setting up KafkaManager hostname: {self.hostname} ip: {self.ip}")

    def _get_kafka_status_and_topics(self) -> Tuple[bool, List[str]]:
        """
        Utility method to get the status of Kafka and existing topics

        :return: status and list of topics
        """
        stat = os.system(constants.KAFKA_COMMANDS.KAFKA_STATUS)
        running = (stat == 0)
        client = confluent_kafka.admin.AdminClient(self.conf)
        cluster_metadata = client.list_topics()
        topics = []
        for k,v in cluster_metadata.topics.items():
            topics.append(k)
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
        os.system(constants.KAFKA_COMMANDS.KAFKA_STOP)
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
        os.system(constants.KAFKA_COMMANDS.KAFKA_START)
        kafka_dto = csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO(
            running = True,
            topics = []
        )
        return kafka_dto

    def createTopic(self, request: csle_collector.kafka_manager.kafka_manager_pb2.CreateTopicMsg,
                   context: grpc.ServicerContext) -> csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
        """
        Starts/Restarts the Poisson process that generates clients

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the kafka server
        """
        logging.info(f"Creating topic: {request.name}")
        running, topics = self._get_kafka_status_and_topics()
        client = confluent_kafka.admin.AdminClient(self.conf)
        new_topic = confluent_kafka.admin.NewTopic(request.name, request.partitions, request.replicas)
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