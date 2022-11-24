import threading
import time
from confluent_kafka import Consumer, KafkaError, KafkaException
import csle_collector.constants.constants as collector_constants
from csle_collector.docker_stats_manager.docker_stats import DockerStats
from csle_common.logging.log import Logger


class DockerHostStatsConsumerThread(threading.Thread):
    """
    Thread that polls the Kafka log to get the latest status of the docker statistics for a specific host
    """

    def __init__(self, kafka_server_ip: str, kafka_port: int, docker_stats: DockerStats, host_ip: str,
                 auto_offset_reset: str = "latest") -> None:
        """
        Initializes the thread

        :param kafka_server_ip: the ip of the kafka server
        :param kafka_port: the port of the kafka server
        :param docker_stats: the docker stats to update
        :param host_ip: the host ip
        :param auto_offset_reset: the offset for kafka to start reading from
        """
        threading.Thread.__init__(self)
        self.host_ip = host_ip
        self.running = True
        self.kafka_server_ip = kafka_server_ip
        self.kafka_port = kafka_port
        self.docker_stats = docker_stats
        self.ts = time.time()
        self.kafka_conf = {
            collector_constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_server_ip}:{self.kafka_port}",
            collector_constants.KAFKA.GROUP_ID_PROPERTY: f"docker_host_stats_consumer_thread_{self.host_ip}_{self.ts}",
            collector_constants.KAFKA.AUTO_OFFSET_RESET_PROPERTY: auto_offset_reset}
        self.consumer = Consumer(**self.kafka_conf)
        self.consumer.subscribe([collector_constants.KAFKA_CONFIG.DOCKER_HOST_STATS_TOPIC_NAME])

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
                    self.docker_stats.update_with_kafka_record_ip(record=msg.value().decode(), ip=self.host_ip)
        self.consumer.close()
