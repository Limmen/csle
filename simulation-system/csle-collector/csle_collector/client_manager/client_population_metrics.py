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

    @staticmethod
    def from_dict(d: dict) -> "ClientPopulationMetrics":
        """
        Converts a dict representation of the object into an instance
        :param d: the dict representation
        :return: the created instance
        """
        obj = ClientPopulationMetrics(
            ts=d["ts"], ip=d["ip"], num_clients=d["num_clients"]
        )
        return obj

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["ts"] = self.ts
        d["num_clients"] = self.num_clients
        return d