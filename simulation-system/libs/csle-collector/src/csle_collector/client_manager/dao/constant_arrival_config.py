from typing import Dict, Any
from csle_collector.client_manager.dao.arrival_config import ArrivalConfig


class ConstantArrivalConfig(ArrivalConfig):
    """
    DTO representing the configuration of a stationary poisson arrival process with exponential service times
    """

    def __init__(self, lamb: float, mu: float):
        """
        Initializes the object

        :param lamb: the static arrival rate
        :param mu: the mean service time
        """
        self.lamb = lamb
        self.mu = mu
        super(ConstantArrivalConfig, self).__init__()

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"lamb: {self.lamb}, mu: {self.mu}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["lamb"] = self.lamb
        d["mu"] = self.mu
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ConstantArrivalConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ConstantArrivalConfig(lamb=d["lamb"], mu=d["mu"])
        return obj