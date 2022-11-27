from typing import List, Dict, Any
from csle_common.dao.simulation_config.env_parameter import EnvParameter


class EnvParametersConfig:
    """
    DTO representing the the configuration of custom environment parameters of a simulation
    """

    def __init__(self, parameters: List[EnvParameter]):
        """
        Initializes the DTO

        :param parameters: the list of parameters
        """
        self.parameters = parameters

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EnvParametersConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EnvParametersConfig(parameters=list(map(lambda x: EnvParameter.from_dict(x), d["parameters"])))
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the DTO
        """
        d = {}
        d["parameters"] = list(map(lambda x: x.to_dict(), self.parameters))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"parameters: {list(map(lambda x: str(x), self.parameters))}"
