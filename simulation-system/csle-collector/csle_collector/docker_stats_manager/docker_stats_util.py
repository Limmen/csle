from typing import Tuple, Union
import csle_collector.constants.constants as constants
from csle_collector.docker_stats_manager.docker_stats import DockerStats


class DockerStatsUtil:

    @staticmethod
    def calculate_cpu_percent(stats_dict : dict) -> float:
        """
        Calculates the CPU utilization percentage

        :param stats_dict: the stats dict from the Docker API
        :return: the CPU percentage
        """
        cpu_count = len(stats_dict[constants.DOCKER_STATS.CPU_STATS][constants.DOCKER_STATS.CPU_USAGE][
                            constants.DOCKER_STATS.PERCPU_USAGE])
        cpu_percent = 0.0
        cpu_delta = float(stats_dict[constants.DOCKER_STATS.CPU_STATS][constants.DOCKER_STATS.CPU_USAGE][
                              constants.DOCKER_STATS.TOTAL_USAGE]) - \
                    float(stats_dict[constants.DOCKER_STATS.PRECPU_STATS][constants.DOCKER_STATS.CPU_USAGE][
                              constants.DOCKER_STATS.TOTAL_USAGE])
        system_delta = float(stats_dict[constants.DOCKER_STATS.CPU_STATS][constants.DOCKER_STATS.SYSTEM_CPU_USAGE]) - \
                       float(stats_dict[constants.DOCKER_STATS.PRECPU_STATS][constants.DOCKER_STATS.SYSTEM_CPU_USAGE])
        if system_delta > 0.0:
            cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
        return cpu_percent

    @staticmethod
    def calculate_cpu_percent2(stats_dict: dict, previous_cpu :float, previous_system: float) \
            -> Tuple[Union[float, any], float, float]:
        """
        Calculates the CPU utilization percentage when precpu is broken in later versions of Docker

        :param stats_dict: the stats dict from the Docker API
        :param previous_cpu: previous cpu percentage
        :param previous_system: previous system percentage
        :return: the CPU percentage
        """
        cpu_percent = 0.0
        cpu_total = float(stats_dict[constants.DOCKER_STATS.CPU_STATS][constants.DOCKER_STATS.CPU_USAGE][
                              constants.DOCKER_STATS.TOTAL_USAGE])
        cpu_delta = cpu_total - previous_cpu
        cpu_system = float(stats_dict[constants.DOCKER_STATS.CPU_STATS][constants.DOCKER_STATS.SYSTEM_CPU_USAGE])
        system_delta = cpu_system - previous_system
        online_cpus = stats_dict[constants.DOCKER_STATS.CPU_STATS].get(
            constants.DOCKER_STATS.ONLINE_CPUS,
            len(stats_dict[constants.DOCKER_STATS.CPU_STATS][constants.DOCKER_STATS.CPU_USAGE][
                    constants.DOCKER_STATS.PERCPU_USAGE]))
        if system_delta > 0.0:
            cpu_percent = (cpu_delta / system_delta) * online_cpus * 100.0
        return cpu_percent, cpu_system, cpu_total

    @staticmethod
    def calculate_blkio_bytes(stats_dict):
        """
        :param stats_dict: the stats dict from the Docker API
        :return: (read_bytes, wrote_bytes), ints
        """
        bytes_stats = DockerStatsUtil.graceful_chain_get(stats_dict, constants.DOCKER_STATS.BLKIO_STATS,
                                                         constants.DOCKER_STATS.IO_SERVICE_BYTES_RECURSIVE)
        if not bytes_stats:
            return 0, 0
        r = 0
        w = 0
        for s in bytes_stats:
            if s[constants.DOCKER_STATS.OP] == constants.DOCKER_STATS.READ:
                r += s[constants.DOCKER_STATS.VALUE]
            elif s[constants.DOCKER_STATS.OP] == constants.DOCKER_STATS.WRITE:
                w += s[constants.DOCKER_STATS.VALUE]
        return r, w

    @staticmethod
    def calculate_network_bytes(stats_dict):
        """
        :param stats_dict: the stats dict from the Docker API
        :return: (received_bytes, transceived_bytes), ints
        """
        networks = DockerStatsUtil.graceful_chain_get(stats_dict, constants.DOCKER_STATS.NETWORKS)
        if not networks:
            return 0, 0
        r = 0
        t = 0
        for if_name, data in networks.items():
            r += data[constants.DOCKER_STATS.RX_BYTES]
            t += data[constants.DOCKER_STATS.TX_BYTES]
        return r, t

    @staticmethod
    def graceful_chain_get(stats_dict : dict, *args, default=None):
        """
        Wrapper to handle errors

        :param stats_dict: stats dict to handle
        :param args: extra arguments
        :param default: default return in case of errors
        :return: default or parsed value
        """
        t = stats_dict
        for a in args:
            try:
                t = t[a]
            except (KeyError, ValueError, TypeError) as ex:
                return default
        return t

    @staticmethod
    def parse_stats(stats_dict, container: str) -> DockerStats:
        """
        Parses a stats dict into a DockerStats object

        :param stats_dict: the dict to parse
        :param container: the container that the stats concerns
        :return: the parsed DockerStats object
        """
        cpu_total = 0.0
        cpu_system = 0.0
        blk_read, blk_write = DockerStatsUtil.calculate_blkio_bytes(stats_dict)
        net_r, net_w = DockerStatsUtil.calculate_network_bytes(stats_dict)
        mem_current = stats_dict[constants.DOCKER_STATS.MEMORY_STATS][constants.DOCKER_STATS.USAGE]
        mem_total = stats_dict[constants.DOCKER_STATS.MEMORY_STATS][constants.DOCKER_STATS.LIMIT]
        try:
            cpu_percent, cpu_system, cpu_total = DockerStatsUtil.calculate_cpu_percent2(stats_dict, cpu_total, cpu_system)
        except KeyError:
            cpu_percent = DockerStatsUtil.calculate_cpu_percent(stats_dict)

        parsed_stats_dict = {
            constants.DOCKER_STATS.PIDS: stats_dict[constants.DOCKER_STATS.PIDS_STATS][constants.DOCKER_STATS.CURRENT],
            constants.DOCKER_STATS.TIMESTAMP: stats_dict[constants.DOCKER_STATS.READ.lower()],
            constants.DOCKER_STATS.CPU_PERCENT: cpu_percent,
            constants.DOCKER_STATS.MEM_CURRENT: mem_current,
            constants.DOCKER_STATS.MEM_TOTAL: stats_dict[constants.DOCKER_STATS.MEMORY_STATS][
                constants.DOCKER_STATS.LIMIT],
            constants.DOCKER_STATS.MEM_PERCENT: (mem_current / mem_total) * 100.0,
            constants.DOCKER_STATS.BLK_READ: blk_read,
            constants.DOCKER_STATS.BLK_WRITE: blk_write,
            constants.DOCKER_STATS.NET_RX: net_r,
            constants.DOCKER_STATS.NET_TX: net_w,
            constants.DOCKER_STATS.CONTAINER_NAME: container
        }
        return DockerStats.from_dict(parsed_stats_dict)