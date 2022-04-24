import threading
import time
from confluent_kafka import Consumer, KafkaError, KafkaException
import csle_collector.constants.constants as collector_constants
from csle_collector.ids_manager.alert_counters import AlertCounters
from csle_common.logging.log import Logger


class IdsLogConsumerThread(threading.Thread):
    """
    Thread that polls the IDS log to get the latest metrics
    """

    def __init__(self, kafka_server_ip: str, kafka_port: int, ids_alert_counters : AlertCounters,
                 auto_offset_reset: str = "latest") -> None:
        """
        Initializes the thread

        :param kafka_server_ip: the ip of the kafka server
        :param kafka_port: the port of the kafka server
        :param ids_alert_counters: the alert counters to updaten
        :param auto_offset_reset: the offset for kafka to start reading from
        """
        threading.Thread.__init__(self)
        self.running =True
        self.kafka_server_ip = kafka_server_ip
        self.kafka_port = kafka_port
        self.ids_alert_counters = ids_alert_counters
        self.ids_alert_counters_list = []
        self.ts = time.time()
        self.kafka_conf = {
            collector_constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_server_ip}:{self.kafka_port}",
            collector_constants.KAFKA.GROUP_ID_PROPERTY:  f"ids_log_consumer_thread_{self.ts}",
            collector_constants.KAFKA.AUTO_OFFSET_RESET_PROPERTY: auto_offset_reset}
        self.consumer = Consumer(**self.kafka_conf)
        self.consumer.subscribe([collector_constants.LOG_SINK.IDS_LOG_TOPIC_NAME])

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
                    self.ids_alert_counters.update_with_kafka_record(record=msg.value().decode())
                    self.ids_alert_counters_list.append(self.ids_alert_counters.copy())
        self.consumer.close()

    def get_aggregated_ids_alert_counters(self) -> AlertCounters:
        """
        :return: aggregated alert counters from the list
        """
        if len(self.ids_alert_counters_list) == 0:
            return self.ids_alert_counters.copy()
        if len(self.ids_alert_counters_list) == 1:
            return self.ids_alert_counters_list[0].copy()
        alert_counters = self.ids_alert_counters_list[0].copy()
        for j in range(1, len(self.ids_alert_counters_list)):
            alert_counters.add(self.ids_alert_counters_list[j].copy())
        return alert_counters