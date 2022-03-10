from typing import List
from datetime import datetime
import csle_collector.constants.constants as constants


class DockerStats:
    """
    DTO class containing docker statistics
    """

    def __init__(self, pids: float, timestamp: str, cpu_percent: float, mem_current: float, mem_total: float,
                 mem_percent: float, blk_read: float, blk_write: float, net_rx: float, net_tx: float,
                 container_name: str):
        """
        Class constructor, creates a DockerStats object

        :param pids: the number of pids in the container
        :param timestamp: the timestamp that the stats were read
        :param cpu_percent: the CPU utilization percentage
        :param mem_current: the current memory usage
        :param mem_total: the memory limit
        :param mem_percent: the memory utilization
        :param blk_read: the number of read IO bytes
        :param blk_write: the number of written IO bytes
        :param net_rx: the number of receives network bytes
        :param net_tx: the number of sent network bytes
        :param container_name: the name of the container
        """
        self.pids = pids
        self.timestamp = timestamp
        self.cpu_percent = cpu_percent
        self.mem_current = mem_current
        self.mem_total = mem_total
        self.mem_percent = mem_percent
        self.blk_read = blk_read
        self.blk_write = blk_write
        self.net_rx = net_rx
        self.net_tx = net_tx
        self.container_name = container_name

    @staticmethod
    def from_dict(parsed_stats_dict: dict) -> "DockerStats":
        """
        Parses a DockerStats object from a dict

        :param parsed_stats_dict: the dict to parse
        :return: the parsed DockerStats object
        """
        return DockerStats(
            pids = parsed_stats_dict[constants.DOCKER_STATS.PIDS],
            timestamp=parsed_stats_dict[constants.DOCKER_STATS.TIMESTAMP],
            cpu_percent=parsed_stats_dict[constants.DOCKER_STATS.CPU_PERCENT],
            mem_current=parsed_stats_dict[constants.DOCKER_STATS.MEM_CURRENT],
            mem_total=parsed_stats_dict[constants.DOCKER_STATS.MEM_TOTAL],
            mem_percent=parsed_stats_dict[constants.DOCKER_STATS.MEM_PERCENT],
            blk_read=parsed_stats_dict[constants.DOCKER_STATS.BLK_READ],
            blk_write=parsed_stats_dict[constants.DOCKER_STATS.BLK_WRITE],
            net_rx=parsed_stats_dict[constants.DOCKER_STATS.NET_RX],
            net_tx=parsed_stats_dict[constants.DOCKER_STATS.NET_TX],
            container_name = parsed_stats_dict[constants.DOCKER_STATS.CONTAINER_NAME]
        )

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        return {
            constants.DOCKER_STATS.PIDS: self.pids,
            constants.DOCKER_STATS.TIMESTAMP: self.timestamp,
            constants.DOCKER_STATS.CPU_PERCENT: self.cpu_percent,
            constants.DOCKER_STATS.MEM_CURRENT: self.mem_current,
            constants.DOCKER_STATS.MEM_TOTAL: self.mem_total,
            constants.DOCKER_STATS.MEM_PERCENT: self.mem_percent,
            constants.DOCKER_STATS.BLK_READ: self.blk_read,
            constants.DOCKER_STATS.BLK_WRITE: self.blk_write,
            constants.DOCKER_STATS.NET_RX: self.net_rx,
            constants.DOCKER_STATS.NET_TX: self.net_tx,
            constants.DOCKER_STATS.CONTAINER_NAME: self.container_name
        }

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"pids: {self.pids}, timestamp: {self.timestamp}, cpu_percent: {self.cpu_percent}, " \
               f"mem_current: {self.mem_current}, mem_total: {self.mem_total}, mem_percent: {self.mem_percent}," \
               f"blk_read: {self.blk_read}, blk_write: {self.blk_write}, net_rx: {self.net_rx}, " \
               f"net_tx: {self.net_tx}, container_name: {self.container_name}"


    @staticmethod
    def compute_averages(stats_list : List["DockerStats"]) -> "DockerStats":
        """
        Compute average stats from a list

        :param stats_list: the list to use to compute averages
        :return: a new DockerStats object with the averages
        """
        if len(stats_list) == 0:
            now = datetime.now()
            ts = now.strftime("%m/%d/%Y, %H:%M:%S")
            return DockerStats(pids=0.0, timestamp=ts, cpu_percent=0.0, mem_current=0.0, mem_total=0.0, mem_percent=0.0,
                               blk_read=0.0, blk_write=0.0, net_rx=0.0, net_tx=0.0, container_name="-")
        sum_pids = 0
        sum_cpu_percent = 0.0
        sum_mem_current = 0.0
        sum_mem_total = 0.0
        sum_mem_percent = 0.0
        sum_blk_read = 0.0
        sum_blk_write = 0.0
        sum_net_rx = 0.0
        sum_net_tx = 0.0
        for i in range(len(stats_list)):
            sum_pids = sum_pids + stats_list[i].pids
            sum_cpu_percent = sum_cpu_percent + stats_list[i].cpu_percent
            sum_mem_current = sum_mem_current + stats_list[i].mem_current
            sum_mem_total = sum_mem_total + stats_list[i].mem_total
            sum_mem_percent = sum_mem_percent + stats_list[i].mem_percent
            sum_blk_read = sum_blk_read + stats_list[i].blk_read
            sum_blk_write = sum_blk_write + stats_list[i].blk_write
            sum_net_rx = sum_net_rx + stats_list[i].net_rx
            sum_net_tx = sum_net_tx + stats_list[i].net_tx

        avg_pids = float("{:.1f}".format(float(sum_pids/len(stats_list))))
        avg_cpu_percent = float("{:.1f}".format(float(sum_cpu_percent / len(stats_list))))
        avg_mem_current = float("{:.1f}".format(float(sum_mem_current / len(stats_list))))
        avg_mem_total = float("{:.1f}".format(float(sum_mem_total / len(stats_list))))
        avg_mem_percent = float("{:.1f}".format(float(sum_mem_percent / len(stats_list))))
        avg_blk_read = float("{:.1f}".format(float(sum_blk_read / len(stats_list))))
        avg_blk_write = float("{:.1f}".format(float(sum_blk_write / len(stats_list))))
        avg_net_rx = float("{:.1f}".format(float(sum_net_rx / len(stats_list))))
        avg_net_tx = float("{:.1f}".format(float(sum_net_tx / len(stats_list))))

        ts = stats_list[0].timestamp
        container_name=stats_list[0].container_name

        return DockerStats(pids=avg_pids, timestamp=ts, cpu_percent=avg_cpu_percent, mem_current=avg_mem_current,
                           mem_total=avg_mem_total, mem_percent=avg_mem_percent,
                           blk_read=avg_blk_read, blk_write=avg_blk_write, net_rx=avg_net_rx, net_tx=avg_net_tx,
                           container_name=container_name)

