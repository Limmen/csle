from typing import Dict, Any, List
from csle_collector.client_manager.dao.arrival_config import ArrivalConfig
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType
import csle_collector.client_manager.client_manager_pb2


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
        super(PieceWiseConstantArrivalConfig, self).__init__(client_arrival_type=ClientArrivalType.PIECE_WISE_CONSTANT)

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"Arrival type: Poisson process with piece-wise constant arrival rate, " \
               f"breakvalues: {self.breakvalues}, breakpoints: {self.breakpoints}, " \
               f"client_arrival_type: {self.client_arrival_type}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["breakvalues"] = self.breakvalues
        d["breakpoints"] = self.breakpoints
        d["client_arrival_type"] = self.client_arrival_type
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

    def to_grpc_object(self) -> csle_collector.client_manager.client_manager_pb2.PieceWiseConstantArrivalConfigDTO:
        """
        :return: a GRPC serializable version of the object
        """
        return csle_collector.client_manager.client_manager_pb2.PieceWiseConstantArrivalConfigDTO(
            breakvalues=self.breakvalues, breakpoints=self.breakpoints
        )

    @staticmethod
    def from_grpc_object(obj: csle_collector.client_manager.client_manager_pb2.PieceWiseConstantArrivalConfigDTO) \
            -> "PieceWiseConstantArrivalConfig":
        """
        Instantiates the object from a GRPC DTO

        :param obj: the object to instantiate from
        :return: the instantiated object
        """
        return PieceWiseConstantArrivalConfig(breakvalues=list(obj.breakvalues), breakpoints=list(obj.breakpoints))

    @staticmethod
    def from_json_file(json_file_path: str) -> "PieceWiseConstantArrivalConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return PieceWiseConstantArrivalConfig.from_dict(json.loads(json_str))
