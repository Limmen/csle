import threading
import time
from confluent_kafka import Consumer, KafkaError, KafkaException
import csle_collector.constants.constants as collector_constants
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_common.logging.log import Logger


class OSSECIdsLogConsumerThread(threading.Thread):
    """
    Thread that polls the OSSEC IDS log to get the latest metrics
    """

    def __init__(self, host_ip: str, kafka_server_ip: str, kafka_port: int,
                 ossec_ids_alert_counters: OSSECIdsAlertCounters, auto_offset_reset: str = "latest") -> None:
        """
        Initializes the thread

        :param host_ip: the ip of the host
        :param kafka_server_ip: the ip of the kafka server
        :param kafka_port: the port of the kafka server
        :param ossec_ids_alert_counters: the alert counters to update
        :param auto_offset_reset: the offset for kafka to start reading from
        """
        threading.Thread.__init__(self)
        self.running = True
        self.host_ip = host_ip
        self.kafka_server_ip = kafka_server_ip
        self.kafka_port = kafka_port
        self.ossec_ids_alert_counters = ossec_ids_alert_counters
        self.ts = time.time()
        self.kafka_conf = {
            collector_constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_server_ip}:{self.kafka_port}",
            collector_constants.KAFKA.GROUP_ID_PROPERTY: f"ids_log_consumer_thread_{self.ts}",
            collector_constants.KAFKA.AUTO_OFFSET_RESET_PROPERTY: auto_offset_reset}
        self.consumer = Consumer(**self.kafka_conf)
        self.consumer.subscribe([collector_constants.KAFKA_CONFIG.OSSEC_IDS_LOG_TOPIC_NAME])

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
                    record = msg.value().decode()
                    if record.split(",")[1] == self.host_ip:
                        self.ossec_ids_alert_counters.update_with_kafka_record(record=msg.value().decode())
        self.consumer.close()
