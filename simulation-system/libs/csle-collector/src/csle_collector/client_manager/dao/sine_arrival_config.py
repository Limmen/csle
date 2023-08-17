from typing import Dict, Any
from csle_collector.client_manager.dao.arrival_config import ArrivalConfig
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType
import csle_collector.client_manager.client_manager_pb2


class SineArrivalConfig(ArrivalConfig):
    """
    DTO representing the configuration of a sine-modulated poisson arrival process with exponential service times
    """

    def __init__(self, lamb: float, time_scaling_factor: float, period_scaling_factor: float):
        """
        Initializes the object

        :param lamb: the static arrival rate
        :param time_scaling_factor: the time-scaling factor for sine-modulated arrival processes
        :param period_scaling_factor: the period-scaling factor for sine-modulated arrival processes
        """
        self.lamb = lamb
        self.time_scaling_factor = time_scaling_factor
        self.period_scaling_factor = period_scaling_factor
        super(SineArrivalConfig, self).__init__(client_arrival_type=ClientArrivalType.SINE_MODULATED)

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"Arrival type: Sine-modulated Poisson process, " \
               f"lamb: {self.lamb}, time_scaling_factor: {self.time_scaling_factor}, " \
               f"period_scaling_factor: {self.period_scaling_factor}, client_arrival_type: {self.client_arrival_type}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d = {}
        d["lamb"] = self.lamb
        d["time_scaling_factor"] = self.time_scaling_factor
        d["period_scaling_factor"] = self.period_scaling_factor
        d["client_arrival_type"] = self.client_arrival_type
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SineArrivalConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = SineArrivalConfig(lamb=d["lamb"], time_scaling_factor=d["time_scaling_factor"],
                                period_scaling_factor=d["period_scaling_factor"])
        return obj

    def to_grpc_object(self) -> csle_collector.client_manager.client_manager_pb2.SineArrivalConfigDTO:
        """
        :return: a GRPC serializable version of the object
        """
        return csle_collector.client_manager.client_manager_pb2.SineArrivalConfigDTO(
            lamb=self.lamb, time_scaling_factor=self.time_scaling_factor,
            period_scaling_factor=self.period_scaling_factor
        )

    @staticmethod
    def from_grpc_object(obj: csle_collector.client_manager.client_manager_pb2.SineArrivalConfigDTO) \
            -> "SineArrivalConfig":
        """
        Instantiates the object from a GRPC DTO

        :param obj: the object to instantiate from
        :return: the instantiated object
        """
        return SineArrivalConfig(lamb=obj.lamb, time_scaling_factor=obj.time_scaling_factor,
                                 period_scaling_factor=obj.period_scaling_factor)

    @staticmethod
    def from_json_file(json_file_path: str) -> "SineArrivalConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SineArrivalConfig.from_dict(json.loads(json_str))
