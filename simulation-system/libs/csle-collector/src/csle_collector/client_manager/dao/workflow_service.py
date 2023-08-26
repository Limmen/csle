from typing import List, Dict, Any, Tuple, Union
import csle_collector.client_manager.client_manager_pb2
from csle_base.json_serializable import JSONSerializable
from csle_base.grpc_serializable import GRPCSerializable


class WorkflowService(JSONSerializable, GRPCSerializable):
    """
    A service of the network.
    The service might be distributed across several network nodes.
    The service is defined by the series of commands that a client executes to make use of the service.
    """

    def __init__(self, ips_and_commands: List[Tuple[str, List[str]]], id: int) -> None:
        """
        Initializes the object

        :param id: the id of the service
        :param ips_and_commands: the list of commands
        """
        self.ips_and_commands = ips_and_commands
        self.id = id

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "WorkflowService":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = WorkflowService(ips_and_commands=list(map(lambda x: (x[0], x[1]),
                                                        d["ips_and_commands"])), id=d["id"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Union[int, List[Tuple[str, List[str]]]]] = {}
        d["ips_and_commands"] = self.ips_and_commands
        d["id"] = self.id
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "WorkflowService":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return WorkflowService.from_dict(json.loads(json_str))

    def copy(self) -> "WorkflowService":
        """
        :return: a copy of the DTO
        """
        return WorkflowService.from_dict(self.to_dict())

    @staticmethod
    def replace_first_octet_of_ip(ip: str, ip_first_octet: int) -> str:
        """
        Utility function for changing the first octet in an IP address

        :param ip: the IP to modify
        :param ip_first_octet: the first octet to insert
        :return: the new IP
        """
        index_of_first_octet_end = ip.find(".")
        return str(ip_first_octet) + ip[index_of_first_octet_end:]

    def create_execution_config(self, ip_first_octet: int) -> "WorkflowService":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        for i in range(len(config.ips_and_commands)):
            config.ips_and_commands[i] = \
                (WorkflowService.replace_first_octet_of_ip(ip=config.ips_and_commands[i][0],
                                                           ip_first_octet=ip_first_octet),
                 config.ips_and_commands[i][1])
        return config

    def to_grpc_object(self) -> csle_collector.client_manager.client_manager_pb2.WorkflowServiceDTO:
        """
        :return: a GRPC serializable version of the object
        """
        ips = []
        commands = []
        for i in range(len(self.ips_and_commands)):
            ips.append(self.ips_and_commands[i][0])
            commands.append(csle_collector.client_manager.client_manager_pb2.NodeCommandsDTO(
                commands=self.ips_and_commands[i][1]))
        return csle_collector.client_manager.client_manager_pb2.WorkflowServiceDTO(
            id=self.id, ips=ips, commands=commands)

    @staticmethod
    def from_grpc_object(obj: csle_collector.client_manager.client_manager_pb2.WorkflowServiceDTO) \
            -> "WorkflowService":
        """
        Instantiates the object from a GRPC DTO

        :param obj: the object to instantiate from
        :return: the instantiated object
        """
        ips_and_commands = []
        ips = list(obj.ips)
        commands = list(obj.commands)
        for i in range(len(list(ips))):
            ips_and_commands.append((ips[i], list(commands[i].commands)))
        return WorkflowService(id=obj.id, ips_and_commands=ips_and_commands)

    def get_commands(self) -> List[str]:
        """
        :return: the list of commands for the service
        """
        commands = []
        for i in range(len(self.ips_and_commands)):
            for j in range(len(self.ips_and_commands[i][1])):
                commands.append(self.ips_and_commands[i][1][j].format(self.ips_and_commands[i][0]))
        return commands

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"Workflow service, id: {self.id}, ips and commands: {self.ips_and_commands}"
