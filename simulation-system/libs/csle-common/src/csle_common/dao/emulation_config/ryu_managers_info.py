from typing import List, Dict, Any
import csle_collector.ryu_manager.ryu_manager_pb2_grpc
import csle_collector.ryu_manager.ryu_manager_pb2
import csle_collector.ryu_manager.ryu_manager_util as ryu_manager_util
from csle_base.json_serializable import JSONSerializable


class RyuManagersInfo(JSONSerializable):
    """
    DTO containing the status of the Ryu managers for a given emulation execution
    """

    def __init__(self, ips: List[str], ports: List[int],
                 emulation_name: str, execution_id: int,
                 ryu_managers_statuses: List[csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO],
                 ryu_managers_running: List[bool], local_controller_web_port: int = -1,
                 physical_server_ip: str = ""):
        """
        Initializes the DTO

        :param ryu_managers_running: boolean list that indicate whether the Ryu managers are running
        :param ips: the list of IPs of the running Ryu managers
        :param ports: the list of ports of the running Ryu managers
        :param emulation_name: the name of the corresponding emulation
        :param execution_id: the ID of the corresponding emulation execution
        :param ryu_managers_statuses: a list of statuses of the Ryu managers
        :param local_controller_web_port: the local port that is forwarded to the SDN controller's web api
        :param physical_server_ip: the ip of the physical server where Ryu is running
        """
        self.ryu_managers_running = ryu_managers_running
        self.ips = ips
        self.ports = ports
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.ryu_managers_statuses = ryu_managers_statuses
        self.local_controller_web_port = local_controller_web_port
        self.physical_server_ip = physical_server_ip

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"ryu_managers_running: {self.ryu_managers_running}, ips: {list(map(lambda x: str(x), self.ips))}, " \
               f"emulation_name: {self.emulation_name}, " \
               f"execution_id: {self.execution_id}, " \
               f"ryu_managers_statuses: {list(map(lambda x: str(x), self.ryu_managers_statuses))}, " \
               f"ports: {list(map(lambda x: str(x), self.ports))}," \
               f"local_controller_web_port: {self.local_controller_web_port}, " \
               f"physical_server_ip: {self.physical_server_ip}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["ryu_managers_running"] = self.ryu_managers_running
        d["ips"] = self.ips
        d["ports"] = self.ports
        d["emulation_name"] = self.emulation_name
        d["execution_id"] = self.execution_id
        d["local_controller_web_port"] = self.local_controller_web_port
        d["physical_server_ip"] = self.physical_server_ip
        d["ryu_managers_statuses"] = list(map(
            lambda x: ryu_manager_util.RyuManagerUtil.ryu_dto_to_dict(x), self.ryu_managers_statuses))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RyuManagersInfo":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = RyuManagersInfo(ryu_managers_running=d["ryu_managers_running"], ips=d["ips"], ports=d["ports"],
                              emulation_name=d["emulation_name"], execution_id=d["execution_id"],
                              ryu_managers_statuses=list(map(
                                  lambda x: ryu_manager_util.RyuManagerUtil.ryu_dto_from_dict(x),
                                  d["ryu_managers_statuses"])),
                              local_controller_web_port=d["local_controller_web_port"],
                              physical_server_ip=d["physical_server_ip"])
        return dto

    @staticmethod
    def from_json_file(json_file_path: str) -> "RyuManagersInfo":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return RyuManagersInfo.from_dict(json.loads(json_str))
