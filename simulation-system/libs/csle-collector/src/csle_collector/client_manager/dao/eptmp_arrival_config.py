from typing import Dict, Any, List
from csle_collector.client_manager.dao.arrival_config import ArrivalConfig
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType
import csle_collector.client_manager.client_manager_pb2


class EPTMPArrivalConfig(ArrivalConfig):
    """
    DTO representing the configuration of a homogenous poisson arrival process with an
    Exponential-Polynomial-Trigonometric rate function having Multiple Periodicities
    """

    def __init__(self, thetas: List[float], gammas: List[float], phis: List[float], omegas: List[float]):
        """
        Initializes the object

        :param thetas: represent the overall trend in frequency of events over a long time frame
        :param gammas: amplitudes
        :param phis: period shifts
        :param omegas: frequencies
        """
        self.thetas = thetas
        self.gammas = gammas
        self.phis = phis
        self.omegas = omegas
        super(EPTMPArrivalConfig, self).__init__(client_arrival_type=ClientArrivalType.EPTMP)

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"Arrival type: Poisson process with EPTMP rate function, " \
               f"thetas: {self.thetas}, gammas: {self.gammas}, phis: {self.phis}, omegas: {self.omegas}, " \
               f"client_arrival_type: {self.client_arrival_type}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["thetas"] = self.thetas
        d["gammas"] = self.gammas
        d["phis"] = self.phis
        d["omegas"] = self.omegas
        d["client_arrival_type"] = self.client_arrival_type
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EPTMPArrivalConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EPTMPArrivalConfig(thetas=d["thetas"], gammas=d["gammas"], phis=d["phis"], omegas=d["omegas"])
        return obj

    def to_grpc_object(self) -> csle_collector.client_manager.client_manager_pb2.EPTMPArrivalConfigDTO:
        """
        :return: a GRPC serializable version of the object
        """
        return csle_collector.client_manager.client_manager_pb2.EPTMPArrivalConfigDTO(
            thetas=self.thetas, gammas=self.gammas, phis=self.phis, omegas=self.omegas
        )

    @staticmethod
    def from_grpc_object(obj: csle_collector.client_manager.client_manager_pb2.EPTMPArrivalConfigDTO) \
            -> "EPTMPArrivalConfig":
        """
        Instantiates the object from a GRPC DTO

        :param obj: the object to instantiate from
        :return: the instantiated object
        """
        return EPTMPArrivalConfig(thetas=list(obj.thetas), gammas=list(obj.gammas), phis=list(obj.phis),
                                  omegas=list(obj.omegas))

    @staticmethod
    def from_json_file(json_file_path: str) -> "EPTMPArrivalConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EPTMPArrivalConfig.from_dict(json.loads(json_str))
