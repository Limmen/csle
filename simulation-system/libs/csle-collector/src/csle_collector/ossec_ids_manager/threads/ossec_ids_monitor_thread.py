import threading
import time
from confluent_kafka import Producer
import logging
from csle_collector.ossec_ids_manager.ossec_ids_manager_util import OSSecManagerUtil
import csle_collector.constants.constants as constants


class OSSecIdsMonitorThread(threading.Thread):
    """
    Thread that collects the OSSEC IDS statistics and pushes it to Kafka periodically
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
        logging.info("OSSEC IDSMonitor thread started successfully")

    def run(self) -> None:
        """
        Main loop of the thread. Parses the IDS log and pushes it to Kafka periodically

        :return: None
        """
        while self.running:
            time.sleep(self.time_step_len_seconds)
            alert_counters = OSSecManagerUtil.read_ossec_ids_data(self.latest_ts)
            record = alert_counters.to_kafka_record(ip=self.ip)
            self.producer.produce(constants.KAFKA_CONFIG.OSSEC_IDS_LOG_TOPIC_NAME, record)
            self.producer.poll(0)
            self.latest_ts = time.time()
