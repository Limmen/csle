from typing import Dict, Any
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType
from csle_base.json_serializable import JSONSerializable


class ArrivalConfig(JSONSerializable):
    """
    Abstract arrival configuration class
    """

    def __init__(self, client_arrival_type: ClientArrivalType) -> None:
        """
        Initializes the object

        :param client_arrival_type: the type of the arrival configuration
        """
        self.client_arrival_type = client_arrival_type

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d = {}
        d["client_arrival_type"] = self.client_arrival_type
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ArrivalConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ArrivalConfig(client_arrival_type=d["client_arrival_type"])
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "ArrivalConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ArrivalConfig.from_dict(json.loads(json_str))
