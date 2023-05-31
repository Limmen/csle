from typing import Dict, Any
from csle_collector.client_manager.dao.arrival_config import ArrivalConfig
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType
import csle_collector.client_manager.client_manager_pb2


class ConstantArrivalConfig(ArrivalConfig):
    """
    DTO representing the configuration of a stationary poisson arrival process with exponential service times
    """

    def __init__(self, lamb: float):
        """
        Initializes the object

        :param lamb: the static arrival rate
        """
        self.lamb = lamb
        super(ConstantArrivalConfig, self).__init__(client_arrival_type=ClientArrivalType.CONSTANT)

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"lamb: {self.lamb}, client_arrival_type: {self.client_arrival_type}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["lamb"] = self.lamb
        d["client_arrival_type"] = self.client_arrival_type
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ConstantArrivalConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ConstantArrivalConfig(lamb=d["lamb"])
        return obj

    def to_grpc_object(self) -> csle_collector.client_manager.client_manager_pb2.ConstantArrivalConfigDTO:
        """
        :return: a GRPC serializable version of the object
        """
        return csle_collector.client_manager.client_manager_pb2.ConstantArrivalConfigDTO(
            lamb=self.lamb
        )

    @staticmethod
    def from_grpc_object(obj: csle_collector.client_manager.client_manager_pb2.ConstantArrivalConfigDTO) \
            -> "ConstantArrivalConfig":
        """
        Instantiates the object from a GRPC DTO

        :param obj: the object to instantiate from
        :return: the instantiated object
        """
        return ConstantArrivalConfig(lamb=obj.lamb)