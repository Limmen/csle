from typing import Dict, Any, List
from csle_collector.client_manager.dao.arrival_config import ArrivalConfig


class PieceWiseConstantArrivalConfig(ArrivalConfig):
    """
    DTO representing the configuration of a piece-wise constant
    poisson arrival process with exponential service times
    """

    def __init__(self, breakvalues: List[float], breakpoints: List[int]):
        """
        Initializes the object

        :param breakvalues: the constant rates at the different breakpoints
        :param breakpoints: the time steps where the rate changes
        """
        self.breakvalues = breakvalues
        self.breakpoints = breakpoints
        super(PieceWiseConstantArrivalConfig, self).__init__()

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"breakvalues: {self.breakvalues}, breakpoints: {self.breakpoints}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["breakvalues"] = self.breakvalues
        d["breakpoints"] = self.breakpoints
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PieceWiseConstantArrivalConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = PieceWiseConstantArrivalConfig(breakvalues=d["breakvalues"], breakpoints=d["breakpoints"])
        return obj