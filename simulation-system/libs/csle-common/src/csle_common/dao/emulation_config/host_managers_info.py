from typing import List, Dict, Any
import csle_collector.host_manager.host_manager_pb2_grpc
import csle_collector.host_manager.host_manager_pb2
import csle_collector.host_manager.host_manager_util as host_manager_util
from csle_base.json_serializable import JSONSerializable


class HostManagersInfo(JSONSerializable):
    """
    DTO containing the status of the Host managers for a given emulation execution
    """

    def __init__(self, ips: List[str], ports: List[int],
                 emulation_name: str, execution_id: int,
                 host_managers_statuses: List[csle_collector.host_manager.host_manager_pb2.HostStatusDTO],
                 host_managers_running: List[bool]):
        """
        Initializes the DTO

        :param host_managers_running: list of booleans indicating whether the host managers are running or not
        :param ips: the list of IPs of the running Host managers
        :param ports: the list of ports of the running Host managers
        :param emulation_name: the name of the corresponding emulation
        :param execution_id: the ID of the corresponding emulation execution
        :param host_managers_statuses: a list of statuses of the Host managers
        """
        self.host_managers_running = host_managers_running
        self.ips = ips
        self.ports = ports
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.host_managers_statuses = host_managers_statuses

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"host_managers_running: {self.host_managers_running}, " \
               f"ips: {list(map(lambda x: str(x), self.ips))}, " \
               f"ports: {list(map(lambda x: str(x), self.ports))}," \
               f"emulation_name: {self.emulation_name}, " \
               f"execution_id: {self.execution_id}, " \
               f"host_managers_statuses: {list(map(lambda x: str(x), self.host_managers_statuses))}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["host_managers_running"] = self.host_managers_running
        d["ips"] = self.ips
        d["emulation_name"] = self.emulation_name
        d["execution_id"] = self.execution_id
        d["ports"] = self.ports
        d["host_managers_statuses"] = list(map(
            lambda x: host_manager_util.HostManagerUtil.host_monitor_dto_to_dict(x),
            self.host_managers_statuses))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "HostManagersInfo":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = HostManagersInfo(
            host_managers_running=d["host_managers_running"], ips=d["ips"], ports=d["ports"],
            emulation_name=d["emulation_name"], execution_id=d["execution_id"],
            host_managers_statuses=list(
                map(lambda x: host_manager_util.HostManagerUtil.host_monitor_dto_from_dict(x),
                    d["host_managers_statuses"])))
        return dto

    @staticmethod
    def from_json_file(json_file_path: str) -> "HostManagersInfo":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return HostManagersInfo.from_dict(json.loads(json_str))
