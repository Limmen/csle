from typing import List, Dict, Any, Union
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.workflow_service import WorkflowService
import csle_collector.client_manager.client_manager_pb2
from csle_base.json_serializable import JSONSerializable
from csle_base.grpc_serializable import GRPCSerializable


class WorkflowsConfig(JSONSerializable, GRPCSerializable):
    """
    Workflows configuration
    """

    def __init__(self, workflow_markov_chains: List[WorkflowMarkovChain], workflow_services: List[WorkflowService]) \
            -> None:
        """
        Initializes the object

        :param workflow_markov_chains: the workflow Markov chains
        :param workflow_services: the workflow services
        """
        self.workflow_markov_chains = workflow_markov_chains
        self.workflow_services = workflow_services

    def get_workflow_service(self, id: int) -> Union[WorkflowService, None]:
        """
        Gets the workflow service with a specific id

        :param id: the id of the service
        :return: the service or None
        """
        for service in self.workflow_services:
            if service.id == id:
                return service
        return None

    def get_workflow_mc(self, id: int) -> Union[WorkflowMarkovChain, None]:
        """
        Gets the workflow Markov chain with a specific id

        :param id: the id of the MC
        :return: the MC or None
        """
        for mc in self.workflow_markov_chains:
            if mc.id == id:
                return mc
        return None

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "WorkflowsConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = WorkflowsConfig(
            workflow_services=list(map(lambda x: WorkflowService.from_dict(x), d["workflow_services"])),
            workflow_markov_chains=list(map(lambda x: WorkflowMarkovChain.from_dict(x), d["workflow_markov_chains"]))
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d = {}
        d["workflow_services"] = list(map(lambda x: x.to_dict(), self.workflow_services))
        d["workflow_markov_chains"] = list(map(lambda x: x.to_dict(), self.workflow_markov_chains))
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "WorkflowsConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return WorkflowsConfig.from_dict(json.loads(json_str))

    def copy(self) -> "WorkflowsConfig":
        """
        :return: a copy of the DTO
        """
        return WorkflowsConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "WorkflowsConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.workflow_services = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet),
                                            config.workflow_services))
        return config

    def to_grpc_object(self) -> csle_collector.client_manager.client_manager_pb2.WorkflowsConfigDTO:
        """
        :return: a GRPC serializable version of the object
        """
        mcs = list(map(lambda x: x.to_grpc_object(), self.workflow_markov_chains))
        services = list(map(lambda x: x.to_grpc_object(), self.workflow_services))
        return csle_collector.client_manager.client_manager_pb2.WorkflowsConfigDTO(
            workflow_markov_chains=mcs, workflow_services=services)

    @staticmethod
    def from_grpc_object(obj: csle_collector.client_manager.client_manager_pb2.WorkflowsConfigDTO) \
            -> "WorkflowsConfig":
        """
        Instantiates the object from a GRPC DTO

        :param obj: the object to instantiate from
        :return: the instantiated object
        """
        mcs = list(map(lambda x: WorkflowMarkovChain.from_grpc_object(x), obj.workflow_markov_chains))
        services = list(map(lambda x: WorkflowService.from_grpc_object(x), obj.workflow_services))
        return WorkflowsConfig(workflow_markov_chains=mcs, workflow_services=services)

    def commands(self) -> List[str]:
        """
        Gets the list of all commands across all services

        :return: the list of commands
        """
        commands: List[str] = []
        for w in self.workflow_services:
            commands = commands + w.get_commands()
        return commands

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"Workflows configuration; markov chains: {list(map(lambda x: str(x), self.workflow_markov_chains))}, " \
               f"workflow services: {list(map(lambda x: str(x), self.workflow_services))}"
