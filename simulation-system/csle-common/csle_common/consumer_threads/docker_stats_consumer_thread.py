import threading
import time
from confluent_kafka import Consumer, KafkaError, KafkaException
import csle_collector.constants.constants as collector_constants
from csle_collector.docker_stats_manager.docker_stats import DockerStats
from csle_common.logging.log import Logger


class DockerStatsConsumerThread(threading.Thread):
    """
    Thread that polls the Kafka log to get the latest status of the docker statistics
    """

    def __init__(self, kafka_server_ip: str, kafka_port: int, docker_stats: DockerStats,
                 auto_offset_reset: str = "latest") -> None:
        """
        Initializes the thread

        :param kafka_server_ip: the ip of the kafka server
        :param kafka_port: the port of the kafka server
        :param docker_stats: the docker stats to update
        :param auto_offset_reset: the kafka offset to start reading from
        """
        threading.Thread.__init__(self)
        self.running =True
        self.kafka_server_ip = kafka_server_ip
        self.kafka_port = kafka_port
        self.docker_stats = docker_stats
        self.auto_offset_reset = auto_offset_reset
        self.ts = time.time()
        self.kafka_conf = {'bootstrap.servers': f"{self.kafka_server_ip}:{self.kafka_port}",
                           'group.id':  f"docker_stats_consumer_thread_{self.ts}",
                           'auto.offset.reset': auto_offset_reset}
        self.consumer = Consumer(**self.kafka_conf)
        self.consumer.subscribe([collector_constants.LOG_SINK.DOCKER_STATS_TOPIC_NAME])

    def run(self) -> None:
        """
        Runs the thread

        :return: None
        """
        while self.running:
            msg = self.consumer.poll(timeout=5.0)
            if msg is not None:
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        Logger.__call__().get_logger.warning(
                            f"reached end of partition: {msg.topic(), msg.partition(), msg.offset()}")
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    self.docker_stats.update_with_kafka_record(record=msg.value().decode())
