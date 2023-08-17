from typing import Dict, Any, List
from csle_collector.client_manager.dao.arrival_config import ArrivalConfig
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType
import csle_collector.client_manager.client_manager_pb2


class SpikingArrivalConfig(ArrivalConfig):
    """
    DTO representing the configuration of a poisson arrival process with spiking arrivals
    """

    def __init__(self, exponents: List[float], factors: List[float]):
        """
        Initializes the object

        :param exponents: exponents for the spiking arrival rate
        :param factors: factors for the spiking arrival rate
        """
        self.exponents = exponents
        self.factors = factors
        super(SpikingArrivalConfig, self).__init__(client_arrival_type=ClientArrivalType.SPIKING)

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"Arrival type: Poisson process with spiking rate, " \
               f"exponents: {self.exponents}, factors: {self.factors}, client_arrival_type: {self.client_arrival_type}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
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
        obj = SpikingArrivalConfig(exponents=d["exponents"], factors=d["factors"])
        return obj

    def to_grpc_object(self) -> csle_collector.client_manager.client_manager_pb2.SpikingArrivalConfigDTO:
        """
        :return: a GRPC serializable version of the object
        """
        return csle_collector.client_manager.client_manager_pb2.SpikingArrivalConfigDTO(
            exponents=self.exponents, factors=self.factors
        )

    @staticmethod
    def from_grpc_object(obj: csle_collector.client_manager.client_manager_pb2.SpikingArrivalConfigDTO) \
            -> "SpikingArrivalConfig":
        """
        Instantiates the object from a GRPC DTO

        :param obj: the object to instantiate from
        :return: the instantiated object
        """
        return SpikingArrivalConfig(exponents=list(obj.exponents), factors=list(obj.factors))

    @staticmethod
    def from_json_file(json_file_path: str) -> "SpikingArrivalConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SpikingArrivalConfig.from_dict(json.loads(json_str))
