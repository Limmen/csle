import socket
import netifaces
import threading
import logging
import time
from confluent_kafka import Producer
import csle_collector.constants.constants as constants
from csle_collector.client_manager.threads.arrival_thread import ArrivalThread


class ProducerThread(threading.Thread):
    """
    Thread that pushes statistics to Kafka
    """

    def __init__(self, arrival_thread: ArrivalThread, time_step_len_seconds: int, ip: str, port: int):
        """
        Initializes the thread

        :param arrival_thread: the thread that manages the client arrivals, used to extract statistics
        :param time_step_len_seconds: the length between pushing statistics to Kafka
        :param ip: the ip of the Kafka server
        :param port: the port of the Kafka server
        """
        threading.Thread.__init__(self)
        self.arrival_thread = arrival_thread
        self.time_step_len_seconds = time_step_len_seconds
        self.stopped = False
        self.kafka_ip = ip
        self.port = port
        self.hostname = socket.gethostname()
        try:
            self.ip = netifaces.ifaddresses(constants.INTERFACES.ETH0)[netifaces.AF_INET][0][constants.INTERFACES.ADDR]
        except Exception:
            self.ip = socket.gethostbyname(self.hostname)
        self.conf = {
            constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_ip}:{self.port}",
            constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.producer = Producer(**self.conf)
        logging.info(f"Starting producer thread, ip:{self.ip}, kafka port:{self.port}, "
                     f"time_step_len:{self.time_step_len_seconds}, kafka_ip:{self.kafka_ip}")

    def run(self) -> None:
        """
        Main loop of the thread, pushes data to Kafka periodically

        :return: None
        """
        while not self.stopped and self.arrival_thread is not None:
            time.sleep(self.time_step_len_seconds)
            if self.arrival_thread is not None:
                ts = time.time()
                num_clients = len(self.arrival_thread.client_threads)
                rate = self.arrival_thread.rate
                mu = 4
                self.producer.produce(constants.KAFKA_CONFIG.CLIENT_POPULATION_TOPIC_NAME,
                                      f"{ts},{self.ip},{num_clients},{rate},{mu}")
                self.producer.poll(0)
