import pycr_common.constants.constants as constants

class DockerStats:

    def __init__(self, pids: int, timestamp: str, cpu_percent: float, mem_current: float, mem_total: float,
                 mem_percent: float, blk_read: int, blk_write: int, net_rx: int, net_tx: int, container_name: str,
                 container_id):
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
        :param container_id: the id of the container
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
        self.container_id = container_id


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
            container_name = parsed_stats_dict[constants.DOCKER_STATS.CONTAINER_NAME],
            container_id=parsed_stats_dict[constants.DOCKER_STATS.CONTAINER_ID]
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
            constants.DOCKER_STATS.CONTAINER_NAME: self.container_name,
            constants.DOCKER_STATS.CONTAINER_ID: self.container_id
        }


    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"pids: {self.pids}, timestamp: {self.timestamp}, cpu_percent: {self.cpu_percent}, " \
               f"mem_current: {self.mem_current}, mem_total: {self.mem_total}, mem_percent: {self.mem_percent}," \
               f"blk_read: {self.blk_read}, blk_write: {self.blk_write}, net_rx: {self.net_rx}, " \
               f"net_tx: {self.net_tx}, container_name: {self.container_name}, container_id: {self.container_id}"
