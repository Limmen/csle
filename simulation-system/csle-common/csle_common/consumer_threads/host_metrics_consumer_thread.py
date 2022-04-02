import threading
import time
from confluent_kafka import Consumer, KafkaError, KafkaException
import csle_collector.constants.constants as collector_constants
from csle_collector.host_manager.host_metrics import HostMetrics
from csle_common.logging.log import Logger


class HostMetricsConsumerThread(threading.Thread):
    """
    Thread that polls Kafka to get the latest metrics for a specific host
    """

    def __init__(self, host_ip: str, kafka_server_ip: str, kafka_port: int,
                 host_metrics: HostMetrics) -> None:
        """
        Initializes the thread

        :param host_ip: the ip of the host
        :param kafka_server_ip: the ip of the kafka server
        :param kafka_port: the port of the kafka server
        :param machine: the machine state to update
        """
        threading.Thread.__init__(self)
        self.running =True
        self.host_ip = host_ip
        self.kafka_server_ip = kafka_server_ip
        self.kafka_port = kafka_port
        self.ts = time.time()
        self.kafka_conf = {'bootstrap.servers': f"{self.kafka_server_ip}:{self.kafka_port}",
                           'group.id':  f"host_metrics_consumer_thread_{self.host_ip}_{self.ts}",
                           'auto.offset.reset': 'latest'}
        self.consumer = Consumer(**self.kafka_conf)
        self.consumer.subscribe([collector_constants.LOG_SINK.HOST_METRICS_TOPIC_NAME])
        self.host_metrics = host_metrics

    def run(self) -> None:
        """
        Runs the thread

        :return: None
        """
        while True:
            msg = self.consumer.poll(timeout=5.0)
            if msg is not None:
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        Logger.__call__().get_logger.warning(
                            f"reached end of partition: {msg.topic(), msg.partition(), msg.offset()}")
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    self.host_metrics.update_with_kafka_record(record=msg.value().decode(), ip=self.host_ip)
