import threading
from confluent_kafka import Producer
import time
import logging
import csle_collector.constants.constants as constants
from csle_collector.snort_ids_manager.snort_ids_manager_util import SnortIdsManagerUtil


class SnortIDSMonitorThread(threading.Thread):
    """
    Thread that collects the Snort IDS statistics and pushes it to Kafka periodically
    """

    def __init__(self, kafka_ip: str, kafka_port: int, ip: str, hostname: str, log_file_path: str,
                 time_step_len_seconds: int):
        """
        Initializes the thread

        :param kafka_ip: IP of the Kafka server to push to
        :param kafka_port: port of the Kafka server to push to
        :param ip: ip of the server we are pushing from
        :param hostname: hostname of the server we are pushing from
        :param log_file_path: path to the IDS log
        :param time_step_len_seconds: the length of a timestep
        """
        threading.Thread.__init__(self)
        self.kafka_ip = kafka_ip
        self.kafka_port = kafka_port
        self.ip = ip
        self.hostname = hostname
        self.log_file_path = log_file_path
        self.latest_ts = time.time()
        self.time_step_len_seconds = time_step_len_seconds
        self.conf = {constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_ip}:{self.kafka_port}",
                     constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.producer = Producer(**self.conf)
        self.running = True
        logging.info("SnortIDSMonitor thread started successfully")

    def run(self) -> None:
        """
        Main loop of the thread. Parses the IDS log and pushes it to Kafka periodically

        :return: None
        """
        while self.running:
            time.sleep(self.time_step_len_seconds)
            try:
                agg_alert_counters, rule_alert_counters, ip_alert_counters = \
                    SnortIdsManagerUtil.read_snort_ids_data(self.latest_ts)
                record = agg_alert_counters.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.SNORT_IDS_LOG_TOPIC_NAME, record)
                self.producer.poll(0)
                record = rule_alert_counters.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.SNORT_IDS_RULE_LOG_TOPIC_NAME, record)
                self.producer.poll(0)
                for ip_alert_counter in ip_alert_counters:
                    record = ip_alert_counter.to_kafka_record(ip=self.ip)
                    self.producer.produce(constants.KAFKA_CONFIG.SNORT_IDS_IP_LOG_TOPIC_NAME, record)
                    self.producer.poll(0)
            except Exception as e:
                logging.info(f"There was an exception parsing the Snort logs: {str(e)}, {repr(e)}")
            self.latest_ts = time.time()
