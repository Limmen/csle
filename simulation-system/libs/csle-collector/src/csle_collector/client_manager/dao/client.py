import random
from typing import List, Dict, Any
import numpy as np
from scipy.stats import expon
from csle_collector.client_manager.dao.arrival_config import ArrivalConfig
from csle_collector.client_manager.dao.eptmp_arrival_config import EPTMPArrivalConfig
from csle_collector.client_manager.dao.spiking_arrival_config import SpikingArrivalConfig
from csle_collector.client_manager.dao.sine_arrival_config import SineArrivalConfig
from csle_collector.client_manager.dao.piece_wise_constant_arrival_config import PieceWiseConstantArrivalConfig
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
import csle_collector.client_manager.client_manager_pb2
from csle_base.json_serializable import JSONSerializable
from csle_base.grpc_serializable import GRPCSerializable


class Client(JSONSerializable, GRPCSerializable):
    """
    A client, which is characterized by its arrival process and its workflow distribution.
    """

    def __init__(self, id: int, workflow_distribution: List[float], arrival_config: ArrivalConfig, mu: float = 4,
                 exponential_service_time: bool = False) -> None:
        """
        Initializes the object

        :param id: the client id
        :param mu: the mean service time if exponential service times are used (otherwise MC is used)
        :param exponential_service_time: boolean flag indicating whether exponential service times should be used
        :param arrival_config: the arrival process configuration of the client
        :param workflow_distribution: the workflow distribution of the client
        """
        self.id = id
        self.mu = mu
        self.exponential_service_time = exponential_service_time
        self.arrival_config = arrival_config
        assert round(sum(workflow_distribution), 2) == 1
        assert self.arrival_config is not None
        self.workflow_distribution = workflow_distribution

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Client":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        if d["arrival_config"]["client_arrival_type"] == ClientArrivalType.CONSTANT.value:
            arrival_config = ConstantArrivalConfig.from_dict(d["arrival_config"])
        elif d["arrival_config"]["client_arrival_type"] == ClientArrivalType.EPTMP.value:
            arrival_config = EPTMPArrivalConfig.from_dict(d["arrival_config"])
        elif d["arrival_config"]["client_arrival_type"] == ClientArrivalType.SPIKING.value:
            arrival_config = SpikingArrivalConfig.from_dict(d["arrival_config"])
        elif d["arrival_config"]["client_arrival_type"] == ClientArrivalType.SINE_MODULATED.value:
            arrival_config = SineArrivalConfig.from_dict(d["arrival_config"])
        elif d["arrival_config"]["client_arrival_type"] == ClientArrivalType.PIECE_WISE_CONSTANT.value:
            arrival_config = PieceWiseConstantArrivalConfig.from_dict(d["arrival_config"])
        else:
            raise ValueError("Arrival config not recognized")
        obj = Client(
            arrival_config=arrival_config, id=d["id"], mu=d["mu"],
            exponential_service_time=d["exponential_service_time"], workflow_distribution=d["workflow_distribution"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["arrival_config"] = self.arrival_config.to_dict()
        d["id"] = self.id
        d["mu"] = self.mu
        d["exponential_service_time"] = self.exponential_service_time
        d["workflow_distribution"] = self.workflow_distribution
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "Client":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return Client.from_dict(json.loads(json_str))

    def copy(self) -> "Client":
        """
        :return: a copy of the DTO
        """
        return Client.from_dict(self.to_dict())

    def to_grpc_object(self) -> csle_collector.client_manager.client_manager_pb2.ClientDTO:
        """
        :return: a GRPC serializable version of the object
        """
        constant_arrival_config = None
        sine_arrival_config = None
        spiking_arrival_config = None
        piece_wise_constant_arrival_config = None
        eptmp_arrival_config = None
        if self.arrival_config.client_arrival_type == ClientArrivalType.CONSTANT:
            constant_arrival_config = self.arrival_config.to_grpc_object()
        elif self.arrival_config.client_arrival_type == ClientArrivalType.SINE_MODULATED:
            sine_arrival_config = self.arrival_config.to_grpc_object()
        elif self.arrival_config.client_arrival_type == ClientArrivalType.SPIKING:
            spiking_arrival_config = self.arrival_config.to_grpc_object()
        elif self.arrival_config.client_arrival_type == ClientArrivalType.PIECE_WISE_CONSTANT:
            piece_wise_constant_arrival_config = self.arrival_config.to_grpc_object()
        elif self.arrival_config.client_arrival_type == ClientArrivalType.EPTMP:
            eptmp_arrival_config = self.arrival_config.to_grpc_object()
        else:
            raise ValueError(f"Client arrival type: {self.arrival_config.client_arrival_type} not recognized")
        return csle_collector.client_manager.client_manager_pb2.ClientDTO(
            id=self.id, workflow_distribution=self.workflow_distribution, mu=self.mu,
            exponential_service_time=self.exponential_service_time, constant_arrival_config=constant_arrival_config,
            sine_arrival_config=sine_arrival_config, spiking_arrival_config=spiking_arrival_config,
            piece_wise_constant_arrival_config=piece_wise_constant_arrival_config,
            eptmp_arrival_config=eptmp_arrival_config, arrival_type=self.arrival_config.client_arrival_type.value)

    @staticmethod
    def from_grpc_object(obj: csle_collector.client_manager.client_manager_pb2.ClientDTO) -> "Client":
        """
        Instantiates the object from a GRPC DTO

        :param obj: the object to instantiate from
        :return: the instantiated object
        """
        arrival_type = ClientArrivalType(obj.arrival_type)
        if arrival_type.value == ClientArrivalType.EPTMP.value:
            arrival_config = EPTMPArrivalConfig.from_grpc_object(obj.eptmp_arrival_config)
        elif arrival_type.value == ClientArrivalType.SINE_MODULATED.value:
            arrival_config = SineArrivalConfig.from_grpc_object(obj.sine_arrival_config)
        elif arrival_type.value == ClientArrivalType.SPIKING.value:
            arrival_config = SpikingArrivalConfig.from_grpc_object(obj.spiking_arrival_config)
        elif arrival_type.value == ClientArrivalType.PIECE_WISE_CONSTANT.value:
            arrival_config = PieceWiseConstantArrivalConfig.from_grpc_object(obj.piece_wise_constant_arrival_config)
        elif arrival_type.value == ClientArrivalType.CONSTANT.value:
            arrival_config = ConstantArrivalConfig.from_grpc_object(obj.constant_arrival_config)
        else:
            raise ValueError(f"Client arrival type: {arrival_type} not recognized")
        workflow_distribution = list(map(lambda x: float(x), obj.workflow_distribution))
        return Client(id=obj.id, workflow_distribution=workflow_distribution, mu=obj.mu,
                      exponential_service_time=obj.exponential_service_time, arrival_config=arrival_config)

    def generate_commands(self, workflows_config: WorkflowsConfig) -> List[str]:
        """
        Generate the commands for the client

        :param workflows_config: the workflows configuration
        :return: sampled list of commands for the client
        """
        commands: List[str] = []
        w = np.random.choice(np.arange(0, len(workflows_config.workflow_services)), p=self.workflow_distribution)
        mc = workflows_config.get_workflow_mc(id=w)
        if mc is None:
            raise ValueError(f"Workflow not recognized: {w}")
        s = mc.initial_state
        service_time = 0
        if self.exponential_service_time:
            service_time = expon.rvs(scale=(self.mu), loc=0, size=1)[0]
        done = False
        while not done:
            if not self.exponential_service_time:
                done = s == len(workflows_config.workflow_services)
            else:
                done = len(commands) > service_time
            if not done:
                service = workflows_config.get_workflow_service(id=s)
                if service is None:
                    raise ValueError(f"Service with id: {s} not found, available service ids: "
                                     f"{list(map(lambda x: x.id, workflows_config.workflow_services))}")
                service_cmds = service.get_commands()
                commands.append(random.choice(service_cmds))
                s_prime = mc.step_forward()
                if not self.exponential_service_time or s_prime != len(workflows_config.workflow_services):
                    s = s_prime
        mc.reset()
        return commands

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"id: {self.id}, workflow distribution: {self.workflow_distribution}, mu: {self.mu}, " \
               f"exponential service time: {self.exponential_service_time}, arrival config: {str(self.arrival_config)}"
