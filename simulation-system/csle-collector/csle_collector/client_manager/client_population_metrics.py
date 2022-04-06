from typing import Dict, Any, Tuple, List
import time


class ClientPopulationMetrics:

    """
    DTO representing information about the client population
    """

    def __init__(self, ip: str= "", ts: float = time.time(), num_clients: int = 0):
        """
        Initializes the DTO

        :param ip: the ip address
        :param ts: the timestamp
        :param num_clients: the number of clients currently
        """
        self.ip = ip
        self.ts = ts
        self.num_clients = num_clients

    @staticmethod
    def from_kafka_record(record: str) -> "ClientPopulationMetrics":
        """
        Converts a kafka record to a DTO

        :param record: the kafka record
        :return: the DTO
        """
        parts = record.split(",")
        obj = ClientPopulationMetrics(ts = float(parts[0]), ip=parts[1], num_clients=int(parts[2]))
        return obj

    def update_with_kafka_record(self, record: str) -> None:
        """
        Updates the DTO with a new kafka record

        :param record: the kafka record
        :return: None
        """
        parts = record.split(",")
        self.ts = float(parts[0])
        self.ip=parts[1]
        self.num_clients=int(parts[2])

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ClientPopulationMetrics":
        """
        Converts a dict representation of the object into an instance
        :param d: the dict representation
        :return: the created instance
        """
        obj = ClientPopulationMetrics(
            ts=d["ts"], ip=d["ip"], num_clients=d["num_clients"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["ts"] = self.ts
        d["num_clients"] = self.num_clients
        return d


    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"ip: {self.ip}, ts: {self.ts}, num_clients: {self.num_clients}"


    def copy(self) -> "ClientPopulationMetrics":
        """
        :return: a copy of the object
        """
        c = ClientPopulationMetrics(ip=self.ip, ts=self.ts, num_clients=self.num_clients)
        return c


    def get_deltas(self, stats_prime: "ClientPopulationMetrics", max_counter: int) -> Tuple[List[float], List[str]]:
        """
        Get the deltas between two stats objects

        :param stats_prime: the stats object to compare with
        :param max_counter: the maximum counter_value
        :return: the deltas and the labels
        """
        deltas = [min(max_counter, max(-max_counter, int(stats_prime.num_clients - self.num_clients)))]
        labels = ["num_clients"]
        return deltas, labels