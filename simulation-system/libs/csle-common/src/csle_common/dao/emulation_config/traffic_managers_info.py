from typing import List, Dict, Any
import csle_collector.traffic_manager.traffic_manager_pb2_grpc
import csle_collector.traffic_manager.traffic_manager_pb2
import csle_collector.traffic_manager.traffic_manager_util as traffic_manager_util
from csle_base.json_serializable import JSONSerializable


class TrafficManagersInfo(JSONSerializable):
    """
    DTO containing the status of the Traffic managers for a given emulation execution
    """

    def __init__(self, ips: List[str], ports: List[int],
                 emulation_name: str, execution_id: int,
                 traffic_managers_statuses: List[csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO],
                 traffic_managers_running: List[bool]):
        """
        Initializes the DTO

        :param ips: the list of IPs of the running traffic managers
        :param ports: the list of ports of the running traffic managers
        :param emulation_name: the name of the corresponding emulation
        :param execution_id: the ID of the corresponding emulation execution
        :param traffic_managers_statuses: a list of statuses of the traffic managers
        :param traffic_managers_running: a list of booleans indicating whether the traffic managers are running
        """
        self.traffic_managers_running = traffic_managers_running
        self.ips = ips
        self.ports = ports
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.traffic_managers_statuses = traffic_managers_statuses

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"traffic_managers_running: {self.traffic_managers_running}, " \
               f"ips: {list(map(lambda x: str(x), self.ips))}, " \
               f"ports: {list(map(lambda x: str(x), self.ports))}," \
               f"emulation_name: {self.emulation_name}, " \
               f"execution_id: {self.execution_id}, " \
               f"traffic_managers_statuses: {list(map(lambda x: str(x), self.traffic_managers_statuses))}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["traffic_managers_running"] = self.traffic_managers_running
        d["ips"] = self.ips
        d["emulation_name"] = self.emulation_name
        d["execution_id"] = self.execution_id
        d["ports"] = self.ports
        d["traffic_managers_statuses"] = list(map(
            lambda x: traffic_manager_util.TrafficManagerUtil.traffic_dto_to_dict(x),
            self.traffic_managers_statuses))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TrafficManagersInfo":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = TrafficManagersInfo(
            traffic_managers_running=d["traffic_managers_running"], ips=d["ips"], ports=d["ports"],
            emulation_name=d["emulation_name"], execution_id=d["execution_id"],
            traffic_managers_statuses=list(map(lambda x:
                                               traffic_manager_util.TrafficManagerUtil.traffic_dto_from_dict(x),
                                               d["traffic_managers_statuses"])))
        return dto

    @staticmethod
    def from_json_file(json_file_path: str) -> "TrafficManagersInfo":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return TrafficManagersInfo.from_dict(json.loads(json_str))
