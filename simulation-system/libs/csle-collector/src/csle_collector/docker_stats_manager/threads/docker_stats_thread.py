from typing import Dict, List, Tuple
import logging
import time
import threading
import socket
import docker
from confluent_kafka import Producer
from csle_collector.docker_stats_manager.docker_stats_manager_pb2 import ContainerIp
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.docker_stats_manager.docker_stats_util import DockerStatsUtil
import csle_collector.constants.constants as constants


class DockerStatsThread(threading.Thread):
    """
    Thread that collects performance statistics of Docker containers
    """

    def __init__(self, container_names_and_ips: List[ContainerIp], emulation: str, execution_first_ip_octet: int,
                 kafka_ip: str, stats_queue_maxsize: int, time_step_len_seconds: int, kafka_port: int) -> None:
        """
        Initializes the thread

        :param container_names_and_ips: list of container names and ips to monitor
        :param emulation: name of the emulation to monitor
        :param kafka_ip: the ip of the Kafka server to produce stats to
        :param kafka_port: the port of the Kafka server to produce stats to
        :param stats_queue_maxsize: max length of the queue before sending to Kafka
        :param time_step_len_seconds: the length of a time-step before sending stats to Kafka
        """
        threading.Thread.__init__(self)
        self.container_names_and_ips = container_names_and_ips
        self.emulation = emulation
        self.execution_first_ip_octet = execution_first_ip_octet
        self.client_1 = docker.from_env()
        self.client2 = docker.APIClient(base_url=constants.DOCKER_STATS.UNIX_DOCKER_SOCK_URL)
        self.containers = self.client_1.containers.list()
        self.container_names = list(map(lambda x: x.container, self.container_names_and_ips))
        self.containers = list(filter(lambda x: x.name in self.container_names, self.containers))
        streams = []
        for container in self.containers:
            stream = container.stats(decode=True, stream=True)
            streams.append((stream, container))
        self.stats_queue_maxsize = stats_queue_maxsize
        self.streams = streams
        self.stats_queues: Dict[str, List[DockerStats]] = {}
        self.time_step_len_seconds = time_step_len_seconds
        self.kafka_ip = kafka_ip
        self.kafka_port = kafka_port
        self.hostname = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ip = s.getsockname()[0]
        self.conf = {constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_ip}:{self.kafka_port}",
                     constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.producer = Producer(**self.conf)
        self.stopped = False
        logging.info(f"Producer thread starting, emulation:{self.emulation}, "
                     f"execution_first_ip_octet: {execution_first_ip_octet}, kafka ip: {self.kafka_ip}, "
                     f"kafka port:{self.kafka_port}, time_step_len_seconds: {self.time_step_len_seconds}, "
                     f"container and ips:{self.container_names_and_ips}")

    def run(self) -> None:
        """
        Main loop of the thread

        :return: None
        """
        start = time.time()
        while not self.stopped:
            time.sleep(5)
            try:
                if time.time() - start >= self.time_step_len_seconds:
                    aggregated_stats, avg_stats_dict = self.compute_averages()
                    record = aggregated_stats.to_kafka_record(ip=self.ip)
                    self.producer.produce(constants.KAFKA_CONFIG.DOCKER_STATS_TOPIC_NAME, record)
                    self.producer.poll(0)
                    for k, v in avg_stats_dict.items():
                        ip = self.get_ip(k)
                        record = v.to_kafka_record(ip=ip)
                        self.producer.produce(constants.KAFKA_CONFIG.DOCKER_HOST_STATS_TOPIC_NAME, record)
                        self.producer.poll(0)
                    self.stats_queues = {}
                    start = time.time()

                for stream, container in self.streams:
                    stats_dict = next(stream)
                    parsed_stats = DockerStatsUtil.parse_stats(stats_dict, container.name)
                    if parsed_stats.container_name not in self.stats_queues:
                        self.stats_queues[parsed_stats.container_name] = [parsed_stats]
                    else:
                        self.stats_queues[parsed_stats.container_name].append(parsed_stats)
            except BaseException as e:
                logging.warning(f"Exception in monitor thread for emulation: "
                                f"{self.emulation}, exception: {str(e)}, {repr(e)}")

    def get_ip(self, container_name: str) -> str:
        """
        Gets the ip of a given container name

        :param container_name: the name of the container
        :return: the ip of the container
        """
        for name_ip in self.container_names_and_ips:
            if name_ip.container == container_name:
                return name_ip.ip
        return "-"

    def compute_averages(self) -> Tuple[DockerStats, Dict[str, DockerStats]]:
        """
        Compute averages and aggregates of the list of metrics
        :return: the average and aggregate metrics
        """
        avg_stats = {}
        avg_stats_l = []
        for k, v in self.stats_queues.items():
            avg_stat = DockerStats.compute_averages(list(v))
            avg_stats[k] = avg_stat
            avg_stats_l.append(avg_stat)
        aggregated_stats = DockerStats.compute_averages(avg_stats_l)
        aggregated_stats.pids = float("{:.1f}".format(aggregated_stats.pids * len(avg_stats_l)))
        aggregated_stats.mem_current = float("{:.1f}".format(aggregated_stats.mem_current * len(avg_stats_l)))
        aggregated_stats.mem_total = float("{:.1f}".format(aggregated_stats.mem_total * len(avg_stats_l)))
        aggregated_stats.blk_read = float("{:.1f}".format(aggregated_stats.blk_read * len(avg_stats_l)))
        aggregated_stats.blk_write = float("{:.1f}".format(aggregated_stats.blk_write * len(avg_stats_l)))
        aggregated_stats.net_rx = float("{:.1f}".format(aggregated_stats.net_rx * len(avg_stats_l)))
        aggregated_stats.net_tx = float("{:.1f}".format(aggregated_stats.net_tx * len(avg_stats_l)))
        return aggregated_stats, avg_stats
