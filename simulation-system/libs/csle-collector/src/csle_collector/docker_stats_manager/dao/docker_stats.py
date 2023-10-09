from typing import List, Dict, Any, Tuple, Union
from datetime import datetime
import time
from csle_base.json_serializable import JSONSerializable
import csle_collector.constants.constants as constants


class DockerStats(JSONSerializable):
    """
    DTO class containing docker statistics
    """

    def __init__(self, pids: float = 0.0, timestamp: str = "", cpu_percent: float = 0.0, mem_current: float = 0.0,
                 mem_total: float = 0.0, mem_percent: float = 0.0, blk_read: float = 0.0, blk_write: float = 0.0,
                 net_rx: float = 0.0, net_tx: float = 0.0, container_name: str = "",
                 ip: Union[str, None] = None, ts: Union[None, float] = None):
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
        :param ip: the ip
        :param ts: the timestamp
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
        self.ip = ip
        self.ts = ts

    @staticmethod
    def from_dict(parsed_stats_dict: Dict[str, Any]) -> "DockerStats":
        """
        Parses a DockerStats object from a dict

        :param parsed_stats_dict: the dict to parse
        :return: the parsed DockerStats object
        """
        return DockerStats(pids=parsed_stats_dict[constants.DOCKER_STATS.PIDS],
                           timestamp=parsed_stats_dict[constants.DOCKER_STATS.TIMESTAMP],
                           cpu_percent=parsed_stats_dict[constants.DOCKER_STATS.CPU_PERCENT],
                           mem_current=parsed_stats_dict[constants.DOCKER_STATS.MEM_CURRENT],
                           mem_total=parsed_stats_dict[constants.DOCKER_STATS.MEM_TOTAL],
                           mem_percent=parsed_stats_dict[constants.DOCKER_STATS.MEM_PERCENT],
                           blk_read=parsed_stats_dict[constants.DOCKER_STATS.BLK_READ],
                           blk_write=parsed_stats_dict[constants.DOCKER_STATS.BLK_WRITE],
                           net_rx=parsed_stats_dict[constants.DOCKER_STATS.NET_RX],
                           net_tx=parsed_stats_dict[constants.DOCKER_STATS.NET_TX],
                           container_name=parsed_stats_dict[constants.DOCKER_STATS.CONTAINER_NAME])

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
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
        return f"pids: {self.pids}, timestamp: {self.timestamp}, cpu_percent: {self.cpu_percent}%, " \
               f"mem_current: {self.mem_current}MB, mem_total: {self.mem_total}MB, mem_percent: {self.mem_percent}%," \
               f"blk_read: {self.blk_read}MB, blk_write: {self.blk_write}MB, net_rx: {self.net_rx}MB, " \
               f"net_tx: {self.net_tx}MB, container_name: {self.container_name}"

    @staticmethod
    def compute_averages(stats_list: List["DockerStats"]) -> "DockerStats":
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
        sum_pids = 0.0
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

        avg_pids = float("{:.1f}".format(float(sum_pids / len(stats_list))))
        avg_cpu_percent = float("{:.1f}".format(float(sum_cpu_percent / len(stats_list))))
        avg_mem_current = float("{:.1f}".format(float(sum_mem_current / len(stats_list))))
        avg_mem_total = float("{:.1f}".format(float(sum_mem_total / len(stats_list))))
        avg_mem_percent = float("{:.1f}".format(float(sum_mem_percent / len(stats_list))))
        avg_blk_read = float("{:.1f}".format(float(sum_blk_read / len(stats_list))))
        avg_blk_write = float("{:.1f}".format(float(sum_blk_write / len(stats_list))))
        avg_net_rx = float("{:.1f}".format(float(sum_net_rx / len(stats_list))))
        avg_net_tx = float("{:.1f}".format(float(sum_net_tx / len(stats_list))))

        ts = stats_list[0].timestamp
        container_name = stats_list[0].container_name

        return DockerStats(pids=avg_pids, timestamp=ts, cpu_percent=avg_cpu_percent, mem_current=avg_mem_current,
                           mem_total=avg_mem_total, mem_percent=avg_mem_percent,
                           blk_read=avg_blk_read, blk_write=avg_blk_write, net_rx=avg_net_rx, net_tx=avg_net_tx,
                           container_name=container_name)

    @staticmethod
    def from_kafka_record(record: str) -> "DockerStats":
        """
        Converts a kafka record to a DTO

        :param record: the recordto convert
        :return: the created DTO
        """
        parts = record.split(",")
        obj = DockerStats(ts=float(parts[0]), ip=parts[1], cpu_percent=float(parts[2]), mem_current=float(parts[3]),
                          mem_total=float(parts[4]), mem_percent=float(parts[5]), blk_read=float(parts[6]),
                          blk_write=float(parts[7]), net_rx=float(parts[8]), net_tx=float(parts[9]), container_name="",
                          pids=int(round(float(parts[10]))), timestamp=str(parts[0]))
        return obj

    def update_with_kafka_record(self, record: str) -> None:
        """
        Updates the DTO with a given kafka record

        :param record: the record to update with
        :return: None
        """
        parts = record.split(",")
        self.ts = float(parts[0])
        self.ip = parts[1]
        self.cpu_percent = float(parts[2])
        self.mem_current = float(parts[3])
        self.mem_total = float(parts[4])
        self.mem_percent = float(parts[5])
        self.blk_read = float(parts[6])
        self.blk_write = float(parts[7])
        self.net_rx = float(parts[8])
        self.net_tx = float(parts[9])
        self.container_name = ""
        self.pids = int(round(float(parts[10])))
        self.timestamp = str(parts[0])

    def update_with_kafka_record_ip(self, record: str, ip: str) -> None:
        """
        Updates the DTO with a given kafka record

        :param record: the record to update with
        :param ip: the ip of the host
        :return: None
        """
        parts = record.split(",")
        if parts[1] == ip:
            self.ts = float(parts[0])
            self.ip = parts[1]
            self.cpu_percent = float(parts[2])
            self.mem_current = float(parts[3])
            self.mem_total = float(parts[4])
            self.mem_percent = float(parts[5])
            self.blk_read = float(parts[6])
            self.blk_write = float(parts[7])
            self.net_rx = float(parts[8])
            self.net_tx = float(parts[9])
            self.container_name = ""
            self.pids = int(round(float(parts[10])))
            self.timestamp = str(parts[0])

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO to a kafka record

        :param ip: the ip to add to the DTO
        :return: the Kafka record
        """
        ts = time.time()
        record = f"{ts},{ip},{self.cpu_percent},{self.mem_current}," \
                 f"{self.mem_total},{self.mem_percent}," \
                 f"{self.blk_read},{self.blk_write}," \
                 f"{self.net_rx},{self.net_tx},{self.pids}"
        return record

    def copy(self) -> "DockerStats":
        """
        :return: a copy of the object
        """
        c = DockerStats(
            pids=self.pids, timestamp=self.timestamp, cpu_percent=self.cpu_percent, mem_current=self.mem_current,
            mem_total=self.mem_total, mem_percent=self.mem_percent, blk_read=self.blk_read, blk_write=self.blk_write,
            net_rx=self.net_rx, net_tx=self.net_tx, container_name=self.container_name, ip=self.ip, ts=self.ts)
        return c

    def get_deltas(self, stats_prime: "DockerStats") -> Tuple[List[int], List[str]]:
        """
        Get the deltas between two stats objects

        :param stats_prime: the stats object to compare with
        :param max_counter: the maximum counter_value
        :return: the deltas and the labels
        """
        deltas = [
            int(round(stats_prime.cpu_percent - self.cpu_percent)),
            int(int(stats_prime.mem_current - self.mem_current)),
            int(int(stats_prime.mem_total - self.mem_total)),
            int(round(stats_prime.mem_percent - self.mem_percent)),
            int(int(stats_prime.blk_read - self.blk_read)),
            int(int(stats_prime.blk_write - self.blk_write)),
            int(int(stats_prime.net_rx - self.net_rx)),
            int(int(stats_prime.net_tx - self.net_tx)),
            int(int(stats_prime.pids - self.pids))
        ]
        labels = [
            "cpu_percent", "mem_current", "mem_total", "mem_percent", "blk_read", "blk_write", "net_rx",
            "net_tx", "pids"
        ]
        return deltas, labels

    def get_values(self) -> Tuple[List[int], List[str]]:
        """
        Get the current values

        :return: the values and the labels
        """
        values = [
            int(round(self.cpu_percent)), int(self.mem_current),
            int(self.mem_total),
            int(self.mem_percent),
            int(self.blk_read), int(self.blk_write),
            int(self.net_rx),
            int(self.net_tx), int(self.pids)
        ]
        labels = [
            "cpu_percent", "mem_current", "mem_total", "mem_percent", "blk_read", "blk_write", "net_rx",
            "net_tx", "pids"
        ]
        return values, labels

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 13

    @staticmethod
    def schema() -> "DockerStats":
        """
        :return: get the schema of the DTO
        """
        return DockerStats()

    @staticmethod
    def from_json_file(json_file_path: str) -> "DockerStats":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return DockerStats.from_dict(json.loads(json_str))
