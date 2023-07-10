from typing import Dict, Any
from abc import abstractmethod
from csle_base.json_serializable import JSONSerializable


class SimulationEnvInputConfig(JSONSerializable):
    """
    Abstract class representing the input to a simulation
    """

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        pass

    @staticmethod
    @abstractmethod
    def from_dict(d: Dict[str, Any]) -> "SimulationEnvInputConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the converted instance
        """
        pass

    @staticmethod
    @abstractmethod
    def from_json_file(json_file_path: str) -> "SimulationEnvInputConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        pass
