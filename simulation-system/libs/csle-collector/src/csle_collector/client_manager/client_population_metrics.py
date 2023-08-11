from typing import Dict, Any, Tuple, List
import time


class ClientPopulationMetrics:
    """
    DTO representing information about the client population
    """

    def __init__(self, ip: str = "", ts: float = time.time(), num_clients: int = 0, rate: float = 20,
                 service_time: float = 4):
        """
        Initializes the DTO

        :param ip: the ip address
        :param ts: the timestamp
        :param num_clients: the number of clients currently
        :param rate: the client arrival rate
        :param mean_service_time: the average service time (in terms of time-steps)
        """
        self.ip = ip
        self.ts = ts
        self.num_clients = num_clients
        self.rate = rate
        self.service_time = service_time

    @staticmethod
    def from_kafka_record(record: str) -> "ClientPopulationMetrics":
        """
        Converts a kafka record to a DTO

        :param record: the kafka record
        :return: the DTO
        """
        parts = record.split(",")
        obj = ClientPopulationMetrics(ts=float(parts[0]), ip=parts[1], num_clients=int(parts[2]),
                                      rate=float(parts[3]), service_time=float(parts[4]))
        return obj

    def update_with_kafka_record(self, record: str) -> None:
        """
        Updates the DTO with a new kafka record

        :param record: the kafka record
        :return: None
        """
        parts = record.split(",")
        self.ts = float(parts[0])
        self.ip = parts[1]
        self.num_clients = int(parts[2])
        self.rate = float(parts[3])
        self.service_time = float(parts[4])

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ClientPopulationMetrics":
        """
        Converts a dict representation of the object into an instance
        :param d: the dict representation
        :return: the created instance
        """
        rate = 0
        if "rate" in d:
            rate = d["rate"]
        if "service_time" in d:
            service_time = d["service_time"]
        else:
            service_time = -1
        obj = ClientPopulationMetrics(
            ts=d["ts"], ip=d["ip"], num_clients=d["num_clients"], rate=rate, service_time=service_time)
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["ip"] = self.ip
        d["ts"] = self.ts
        d["num_clients"] = self.num_clients
        d["rate"] = self.rate
        d["service_time"] = self.service_time
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"ip: {self.ip}, ts: {self.ts}, num_clients: {self.num_clients}, rate: {self.rate}, " \
               f"avg service time: {self.service_time}"

    def copy(self) -> "ClientPopulationMetrics":
        """
        :return: a copy of the object
        """
        c = ClientPopulationMetrics(ip=self.ip, ts=self.ts, num_clients=self.num_clients, rate=self.rate,
                                    service_time=self.service_time)
        return c

    def get_values(self) -> Tuple[List[float], List[str]]:
        """
        Get the current values

        :return: the values and the labels
        """
        deltas = [int(self.num_clients), float(self.rate), float(self.service_time)]
        labels = ["num_clients", "rate", "service_time"]
        return deltas, labels

    def get_deltas(self, stats_prime: "ClientPopulationMetrics") -> Tuple[List[float], List[str]]:
        """
        Get the deltas between two stats objects

        :param stats_prime: the stats object to compare with
        :return: the deltas and the labels
        """
        deltas = [int(stats_prime.num_clients - self.num_clients), float(stats_prime.rate - self.rate),
                  float(stats_prime.service_time - self.service_time)]
        labels = ["num_clients", "rate", "service_time"]
        return deltas, labels

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 5

    @staticmethod
    def schema() -> "ClientPopulationMetrics":
        """
        :return: get the schema of the DTO
        """
        return ClientPopulationMetrics()
