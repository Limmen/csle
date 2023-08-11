import csle_collector.kafka_manager.kafka_manager_pb2_grpc
import csle_collector.kafka_manager.kafka_manager_pb2
import csle_collector.constants.constants as constants


def get_kafka_status(stub: csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub,
                     timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
    """
    Queries the server for the kafka server status

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a KafkaDTO describing the status of the kafka server
    """
    get_kafka_status_msg = csle_collector.kafka_manager.kafka_manager_pb2.GetKafkaStatusMsg()
    kafka_dto: csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO = \
        stub.getKafkaStatus(get_kafka_status_msg, timeout=timeout)
    return kafka_dto


def create_topic(stub: csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub,
                 name: str, partitions: int, replicas: int, retention_time_hours: int,
                 timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
    """
    Sends a request to the KafkaManager to create a new Kafka topic

    :param stub: the stub to send the remote gRPC to the server
    :param name: the name of the Kafka topic
    :param partitions: the number of partitions of the Kafka topic
    :param replicas: the number of replicas of the Kafka topic
    :param retention_time_hours: the retention time for the topic
    :param timeout: the GRPC timeout (seconds)
    :return: a KafkaDTO describing the status of the kafka server
    """
    create_kafka_topic_msg = csle_collector.kafka_manager.kafka_manager_pb2.CreateTopicMsg(
        name=name, partitions=partitions, replicas=replicas, retention_time_hours=retention_time_hours)
    kafka_dto: csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO = \
        stub.createTopic(create_kafka_topic_msg, timeout=timeout)
    return kafka_dto


def stop_kafka(stub: csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub,
               timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
    """
    Sends a request to the Kafka server to stop the Kafka server

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a KafkaDTO describing the status of the kafka server
    """
    stop_kafka_msg = csle_collector.kafka_manager.kafka_manager_pb2.StopKafkaMsg()
    kafka_dto: csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO = \
        stub.stopKafka(stop_kafka_msg, timeout=timeout)
    return kafka_dto


def start_kafka(stub: csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub,
                timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
    """
    Sends a request to the Kafka server to start the Kafka server

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a KafkaDTO describing the status of the kafka server
    """
    start_kafka_msg = csle_collector.kafka_manager.kafka_manager_pb2.StartKafkaMsg()
    kafka_dto: csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO = \
        stub.startKafka(start_kafka_msg, timeout=timeout)
    return kafka_dto
