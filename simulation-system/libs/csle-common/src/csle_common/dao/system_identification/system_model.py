from typing import Dict, Any
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

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        # d_h = {}
        d["descr"] = self.descr
        d["model_type"] = self.model_type
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SystemModel":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the converted instance
        """
        obj = SystemModel(d["descr"], d["model_type"])
        return obj

    '''@abstractmethod
    def copy(self) -> "SystemModel":
        """
        :return: a copy of the object
        """
        pass'''

    @staticmethod
    def from_json_file(json_file_path: str) -> "SystemModel":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SystemModel(json.loads(json_str))
