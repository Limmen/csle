from typing import Tuple
import threading
import docker
from collections import deque
from csle_common.envs_model.config.generator.env_info import EnvInfo
from csle_common.envs_model.logic.emulation.util.common.docker_stats_util import DockerStatsUtil
from csle_common.dao.env_info.docker_stats import DockerStats
import csle_common.constants.constants as constants


class DockerStatsThread(threading.Thread):
    """
    Thread that collects performance statistics of Docker containers
    """

    def __init__(self, jumphost_ip: str = None, stats_queue_maxsize = 100):
        """
        Initializes the thread

        :param jumphost_ip: IP to the server where the docker daemon is running, if None assume localhost
        :param stats_queue_maxsize: maximum size of the queue of stats objects
        """
        threading.Thread.__init__(self)
        self.jumphost_ip = jumphost_ip
        if jumphost_ip is not None:
            self.client1 = docker.DockerClient(base_url=constants.DOCKER.SSH_PREFIX + jumphost_ip)
            self.client2 = docker.APIClient(base_url=constants.DOCKER.SSH_PREFIX + jumphost_ip)
        else:
            self.client1 = docker.from_env()
            self.client2 = docker.APIClient(base_url=constants.DOCKER.UNIX_DOCKER_SOCK_URL)

        self.containers = EnvInfo.parse_running_containers(client1=self.client1, client2=self.client2)

        streams = []
        for container in self.containers:
            stream = container.container_handle.stats(decode=True, stream=True)
            streams.append((stream, container))
        self.streams = streams
        self.stats_queue_maxsize = stats_queue_maxsize
        self.stats_queues = {}

    def run(self) -> None:
        """
        Main loop of the thread

        :return: None
        """
        while True:
            for stream, container in self.streams:
                stats_dict = next(stream)
                parsed_stats = DockerStatsUtil.parse_stats(stats_dict, container)
                if parsed_stats.container_ip not in self.stats_queues:
                    self.stats_queues[parsed_stats.container_ip] = deque([], maxlen=self.stats_queue_maxsize)
                self.stats_queues[parsed_stats.container_ip].append(parsed_stats)


    def compute_averages(self) -> Tuple[DockerStats, dict]:
        """
        Compute averages and aggregates of the list of metrics
        :return: the average and aggregate metrics
        """
        avg_stats = {}
        avg_stats_l = []
        for k,v in self.stats_queues.items():
            avg_stat = DockerStats.compute_averages(list(v))
            avg_stats[k] = avg_stat
            avg_stats_l.append(avg_stat)
        aggregated_stats = DockerStats.compute_averages(avg_stats_l)
        aggregated_stats.pids = float("{:.1f}".format(aggregated_stats.pids*len(avg_stats_l)))
        aggregated_stats.mem_current = float("{:.1f}".format(aggregated_stats.mem_current * len(avg_stats_l)))
        aggregated_stats.mem_total = float("{:.1f}".format(aggregated_stats.mem_total * len(avg_stats_l)))
        aggregated_stats.blk_read = float("{:.1f}".format(aggregated_stats.blk_read * len(avg_stats_l)))
        aggregated_stats.blk_write = float("{:.1f}".format(aggregated_stats.blk_write * len(avg_stats_l)))
        aggregated_stats.net_rx = float("{:.1f}".format(aggregated_stats.net_rx * len(avg_stats_l)))
        aggregated_stats.net_tx = float("{:.1f}".format(aggregated_stats.net_tx * len(avg_stats_l)))
        return aggregated_stats, avg_stats




