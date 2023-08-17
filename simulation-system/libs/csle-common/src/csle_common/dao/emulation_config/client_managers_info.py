from typing import List, Dict, Any
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
import csle_collector.client_manager.client_manager_util as client_manager_util
from csle_base.json_serializable import JSONSerializable


class ClientManagersInfo(JSONSerializable):
    """
    DTO containing the status of the Client managers for a given emulation execution
    """

    def __init__(self, ips: List[str], ports: List[int],
                 emulation_name: str, execution_id: int,
                 client_managers_statuses: List[csle_collector.client_manager.client_manager_pb2.ClientsDTO],
                 client_managers_running: List[bool]):
        """
        Initializes the DTO

        :param ips: the list of IPs of the running Client managers
        :param ports: the list of ports of the running Client managers
        :param emulation_name: the name of the corresponding emulation
        :param execution_id: the ID of the corresponding emulation execution
        :param client_managers_statuses: a list of statuses of the Client managers
        :param client_managers_running: a list of booleans indicating whether the client managers are running or not
        """
        self.client_managers_running = client_managers_running
        self.ips = ips
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.client_managers_statuses = client_managers_statuses
        self.ports = ports

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"client_managers_running: {self.client_managers_running}, " \
               f"ips: {list(map(lambda x: str(x), self.ips))}, " \
               f"ports: {list(map(lambda x: str(x), self.ports))}," \
               f"emulation_name: {self.emulation_name}, " \
               f"execution_id: {self.execution_id}, " \
               f"client_managers_statuses: {list(map(lambda x: str(x), self.client_managers_statuses))}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["client_managers_running"] = self.client_managers_running
        d["ips"] = self.ips
        d["ports"] = self.ports
        d["emulation_name"] = self.emulation_name
        d["execution_id"] = self.execution_id
        d["client_managers_statuses"] = list(map(
            lambda x: client_manager_util.ClientManagerUtil.client_dto_to_dict(x),
            self.client_managers_statuses))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ClientManagersInfo":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = ClientManagersInfo(
            client_managers_running=d["client_managers_running"], ips=d["ips"], ports=d["ports"],
            emulation_name=d["emulation_name"], execution_id=d["execution_id"],
            client_managers_statuses=list(map(lambda x: client_manager_util.ClientManagerUtil.clients_dto_from_dict(x),
                                              d["client_managers_statuses"])))
        return dto

    @staticmethod
    def from_json_file(json_file_path: str) -> "ClientManagersInfo":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ClientManagersInfo.from_dict(json.loads(json_str))
