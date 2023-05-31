from typing import Dict
from abc import ABC, abstractmethod
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType


class ArrivalConfig(ABC):
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

    @abstractmethod
    def to_grpc_object(self):
        """
        :return: a grpc serializable version of the object
        """
        pass

    @staticmethod
    @abstractmethod
    def from_grpc_object(obj):
        """
        Instantiate the object from a GRPC object

        :param obj: the objet to instantiate from
        :return: the instantiated grpc object
        """
        pass

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

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

