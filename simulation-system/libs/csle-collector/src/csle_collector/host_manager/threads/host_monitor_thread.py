import time
import logging
import threading
from confluent_kafka import Producer
from csle_collector.host_manager.host_manager_util import HostManagerUtil
import csle_collector.constants.constants as constants


class HostMonitorThread(threading.Thread):
    """
    Thread that collects the Host statistics and pushes it to Kafka periodically
    """

    def __init__(self, kafka_ip: str, kafka_port: int, ip: str, hostname: str, time_step_len_seconds: int) -> None:
        """
        Initializes the thread

        :param kafka_ip: IP of the Kafka server to push to
        :param kafka_port: port of the Kafka server to push to
        :param ip: ip of the server we are pushing from
        :param hostname: hostname of the server we are pushing from
        :param time_step_len_seconds: the length of a timestep
        """
        threading.Thread.__init__(self)
        self.kafka_ip = kafka_ip
        self.kafka_port = kafka_port
        self.ip = ip
        self.hostname = hostname
        self.latest_ts = time.time()
        self.failed_auth_last_ts = HostManagerUtil.read_latest_ts_auth()
        self.login_last_ts = HostManagerUtil.read_latest_ts_login()
        self.time_step_len_seconds = time_step_len_seconds
        self.conf = {
            constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_ip}:{self.kafka_port}",
            constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.producer = Producer(**self.conf)
        self.running = True
        logging.info("HostMonitor thread started successfully")

    def run(self) -> None:
        """
        Main loop of the thread. Parses log files and metrics on the host and pushes it to Kafka periodically

        :return: None
        """
        logging.info("HostMonitor [Running]")
        while self.running:
            time.sleep(self.time_step_len_seconds)
            try:
                host_metrics = HostManagerUtil.read_host_metrics(failed_auth_last_ts=self.failed_auth_last_ts,
                                                                 login_last_ts=self.login_last_ts)
                record = host_metrics.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.HOST_METRICS_TOPIC_NAME, record)
                self.producer.poll(0)
                self.failed_auth_last_ts = HostManagerUtil.read_latest_ts_auth()
                self.login_last_ts = HostManagerUtil.read_latest_ts_login()
            except Exception as e:
                logging.info(f"[Monitor thread], "
                             f"There was an exception reading host metrics and producing to kafka: "
                             f"{str(e)}, {repr(e)}")
