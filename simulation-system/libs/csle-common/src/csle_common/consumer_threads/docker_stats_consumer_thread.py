from typing import List
import threading
import time
from confluent_kafka import Consumer, KafkaError, KafkaException
import csle_collector.constants.constants as collector_constants
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
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
        self.running = True
        self.kafka_server_ip = kafka_server_ip
        self.kafka_port = kafka_port
        self.docker_stats = docker_stats
        self.docker_stats_list: List[DockerStats] = []
        self.auto_offset_reset = auto_offset_reset
        self.ts = time.time()
        self.kafka_conf = {
            collector_constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_server_ip}:{self.kafka_port}",
            collector_constants.KAFKA.GROUP_ID_PROPERTY: f"docker_stats_consumer_thread_{self.ts}",
            collector_constants.KAFKA.AUTO_OFFSET_RESET_PROPERTY: auto_offset_reset}
        self.consumer = Consumer(**self.kafka_conf)
        self.consumer.subscribe([collector_constants.KAFKA_CONFIG.DOCKER_STATS_TOPIC_NAME])

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
                    self.docker_stats_list.append(self.docker_stats.copy())
        self.consumer.close()

    def get_average_docker_stats(self) -> DockerStats:
        """
        :return: the average of the list of docker stats
        """
        if len(self.docker_stats_list) == 0:
            return self.docker_stats.copy()
        if len(self.docker_stats_list) == 1:
            return self.docker_stats_list[0].copy()
        avg_docker_stats = DockerStats()
        for i in range(len(self.docker_stats_list)):
            avg_docker_stats.pids = avg_docker_stats.pids + self.docker_stats_list[i].pids
            avg_docker_stats.cpu_percent = avg_docker_stats.cpu_percent + self.docker_stats_list[i].cpu_percent
            avg_docker_stats.mem_current = avg_docker_stats.mem_current + self.docker_stats_list[i].mem_current
            avg_docker_stats.mem_total = avg_docker_stats.mem_total + self.docker_stats_list[i].mem_total
            avg_docker_stats.mem_percent = avg_docker_stats.mem_percent + self.docker_stats_list[i].mem_percent
            avg_docker_stats.blk_read = avg_docker_stats.blk_read + self.docker_stats_list[i].blk_read
            avg_docker_stats.blk_write = avg_docker_stats.blk_write + self.docker_stats_list[i].blk_write
            avg_docker_stats.net_rx = avg_docker_stats.net_rx + self.docker_stats_list[i].net_rx
            avg_docker_stats.net_tx = avg_docker_stats.pids + self.docker_stats_list[i].net_tx

        avg_docker_stats.pids = int(round(avg_docker_stats.pids / len(self.docker_stats_list)))
        avg_docker_stats.cpu_percent = int(round(avg_docker_stats.cpu_percent / len(self.docker_stats_list)))
        avg_docker_stats.mem_current = int(round(avg_docker_stats.mem_current / len(self.docker_stats_list)))
        avg_docker_stats.mem_total = int(round(avg_docker_stats.mem_total / len(self.docker_stats_list)))
        avg_docker_stats.mem_percent = int(round(avg_docker_stats.mem_percent / len(self.docker_stats_list)))
        avg_docker_stats.blk_read = int(round(avg_docker_stats.blk_read / len(self.docker_stats_list)))
        avg_docker_stats.blk_write = int(round(avg_docker_stats.blk_write / len(self.docker_stats_list)))
        avg_docker_stats.net_rx = int(round(avg_docker_stats.net_rx / len(self.docker_stats_list)))
        avg_docker_stats.net_tx = int(round(avg_docker_stats.net_tx / len(self.docker_stats_list)))
        return avg_docker_stats
