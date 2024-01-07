from typing import List
import threading
import time
from confluent_kafka import Consumer, KafkaError, KafkaException
import csle_collector.constants.constants as collector_constants
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_common.logging.log import Logger


class ClientPopulationConsumerThread(threading.Thread):
    """
    Thread that polls the Kafka log to get the latest status of the client population
    """

    def __init__(self, kafka_server_ip: str, kafka_port: int,
                 client_population_metrics: ClientPopulationMetrics, auto_offset_reset: str = "latest") -> None:
        """
        Initialzes the thread

        :param kafka_server_ip: the ip of the kafka server
        :param kafka_port: the port of the kafka server
        :param client_population_metrics: the client population metrics to update
        :param auto_offset_reset: the offset for kafka to start reading from
        """
        threading.Thread.__init__(self)
        self.running = True
        self.kafka_server_ip = kafka_server_ip
        self.kafka_port = kafka_port
        self.client_population_metrics = client_population_metrics
        self.client_population_metrics_list: List[ClientPopulationMetrics] = []
        self.ts = time.time()
        self.auto_offset_reset = auto_offset_reset
        self.kafka_conf = {
            collector_constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_server_ip}:{self.kafka_port}",
            collector_constants.KAFKA.GROUP_ID_PROPERTY: f"client_population_consumer_thread_{self.ts}",
            collector_constants.KAFKA.AUTO_OFFSET_RESET_PROPERTY: auto_offset_reset}
        self.consumer = Consumer(**self.kafka_conf)
        self.consumer.subscribe([collector_constants.KAFKA_CONFIG.CLIENT_POPULATION_TOPIC_NAME])

    def run(self) -> None:
        """
        Run thread

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
                    self.client_population_metrics.update_with_kafka_record(record=msg.value().decode())
                    self.client_population_metrics_list.append(self.client_population_metrics.copy())
        self.consumer.close()

    def get_average_client_population_metrics(self) -> ClientPopulationMetrics:
        """
        :return: average of the list of client population metrics
        """
        if len(self.client_population_metrics_list) == 0:
            return self.client_population_metrics.copy()
        if len(self.client_population_metrics_list) == 1:
            return self.client_population_metrics_list[0].copy()
        avg_client_population_metrics = ClientPopulationMetrics(num_clients=0, rate=0)

        for i in range(len(self.client_population_metrics_list)):
            avg_client_population_metrics.num_clients = (avg_client_population_metrics.num_clients +
                                                         self.client_population_metrics_list[i].num_clients)
            avg_client_population_metrics.rate = (avg_client_population_metrics.rate +
                                                  self.client_population_metrics_list[i].rate)

        avg_client_population_metrics.num_clients = int(round(
            avg_client_population_metrics.num_clients / len(self.client_population_metrics_list)))
        avg_client_population_metrics.rate = float(round(
            avg_client_population_metrics.rate / len(self.client_population_metrics_list)))
        return avg_client_population_metrics
