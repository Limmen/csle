from typing import Dict, Any, List
from csle_collector.client_manager.dao.arrival_config import ArrivalConfig
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType


class SpikingArrivalConfig(ArrivalConfig):
    """
    DTO representing the configuration of a poisson arrival process with spiking arrivals
    """

    def __init__(self, exponents: List[float], factors: List[float], mu: float):
        """
        Initializes the object

        :param mu: expected service time
        :param exponents: exponents for the spiking arrival rate
        :param factors: factors for the spiking arrival rate
        """
        self.mu = mu
        self.exponents = exponents
        self.factors = factors
        super(SpikingArrivalConfig, self).__init__(client_arrival_type=ClientArrivalType.SPIKING)

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"exponents: {self.exponents}, factors: {self.factors}, client_arrival_type: {self.client_arrival_type}, " \
               f"mu: {self.mu}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["mu"] = self.mu
        d["exponents"] = self.exponents
        d["factors"] = self.factors
        d["client_arrival_type"] = self.client_arrival_type
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SpikingArrivalConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = SpikingArrivalConfig(exponents=d["exponents"], factors=d["factors"], mu=d["mu"])
        return obj