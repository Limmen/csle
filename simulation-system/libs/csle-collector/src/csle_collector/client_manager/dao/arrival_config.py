from typing import Dict
from abc import abstractmethod
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType
from csle_base.json_serializable import JSONSerializable
from csle_base.grpc_serializable import GRPCSerializable


class ArrivalConfig(GRPCSerializable):
    """
    Abstract arrival configuration class
    """

    def __init__(self, client_arrival_type: ClientArrivalType) -> None:
        """
        Initializes the object

        :param client_arrival_type: the type of the arrival configuration
        """
        self.client_arrival_type = client_arrival_type

    @abstractmethod
    def to_dict(self) -> Dict:
        """
        :return: a dict representation of the object
        """
        pass

    @staticmethod
    @abstractmethod
    def from_dict(d: Dict) -> "ArrivalConfig":
        """
        Instantiates the object from a dict representation

        :param d: the dict to instantiate the object from
        :return: the instantiated object
        """
        pass

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
