from typing import Dict, Any
from abc import abstractmethod
from csle_common.dao.system_identification.system_model_type import SystemModelType
from csle_base.json_serializable import JSONSerializable


class SystemModel(JSONSerializable):
    """
    Abstract system model
    """

    def __init__(self, descr: str, model_type: SystemModelType):
        """
        Abstract constructor

        :param descr: the description of the system model
        :param model_type: the type of the system model
        """
        self.descr = descr
        self.model_type = model_type

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        pass

    @staticmethod
    @abstractmethod
    def from_dict(d: Dict[str, Any]) -> "SystemModel":
        """
        Converts a dict representation of the object to an instance
        """
        pass

    @abstractmethod
    def copy(self) -> "SystemModel":
        """
        :return: a copy of the object
        """
        pass

    @staticmethod
    @abstractmethod
    def from_json_file(json_file_path: str) -> "SystemModel":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        pass
