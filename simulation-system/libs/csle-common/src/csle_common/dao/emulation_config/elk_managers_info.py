from typing import List, Dict, Any
import csle_collector.elk_manager.elk_manager_pb2_grpc
import csle_collector.elk_manager.elk_manager_pb2
import csle_collector.elk_manager.elk_manager_util as elk_manager_util
from csle_base.json_serializable import JSONSerializable


class ELKManagersInfo(JSONSerializable):
    """
    DTO containing the status of the ELK managers for a given emulation execution
    """

    def __init__(self, ips: List[str], ports: List[int],
                 emulation_name: str, execution_id: int,
                 elk_managers_statuses: List[csle_collector.elk_manager.elk_manager_pb2.ElkDTO],
                 elk_managers_running: List[bool], local_kibana_port: int = -1,
                 physical_server_ip=""):
        """
        Initializes the DTO

        :param elk_managers_running: boolean list that indicate whether the elk managers are running
        :param ips: the list of IPs of the running ELK managers
        :param ports: the list of ports of the running ELK managers
        :param emulation_name: the name of the corresponding emulation
        :param execution_id: the ID of the corresponding emulation execution
        :param elk_managers_statuses: a list of statuses of the ELK managers
        :param local_kibana_port: the local port that is forwarded to Kibana
        :param physical_server_ip: the physical server where the ELK stack is running
        """
        self.elk_managers_running = elk_managers_running
        self.ips = ips
        self.ports = ports
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.elk_managers_statuses = elk_managers_statuses
        self.local_kibana_port = local_kibana_port
        self.physical_server_ip = physical_server_ip

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"elk_managers_running: {self.elk_managers_running}, ips: {list(map(lambda x: str(x), self.ips))}, " \
               f"emulation_name: {self.emulation_name}, " \
               f"execution_id: {self.execution_id}, " \
               f"elk_managers_statuses: {list(map(lambda x: str(x), self.elk_managers_statuses))}, " \
               f"ports: {list(map(lambda x: str(x), self.ports))}," \
               f"local_kibana_port: {self.local_kibana_port}, physical_server_ip: {self.physical_server_ip}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["elk_managers_running"] = self.elk_managers_running
        d["ips"] = self.ips
        d["ports"] = self.ports
        d["emulation_name"] = self.emulation_name
        d["execution_id"] = self.execution_id
        d["physical_server_ip"] = self.physical_server_ip
        d["local_kibana_port"] = self.local_kibana_port
        d["elk_managers_statuses"] = list(map(
            lambda x: elk_manager_util.ElkManagerUtil.elk_dto_to_dict(x), self.elk_managers_statuses))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ELKManagersInfo":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = ELKManagersInfo(elk_managers_running=d["elk_managers_running"], ips=d["ips"], ports=d["ports"],
                              emulation_name=d["emulation_name"], execution_id=d["execution_id"],
                              elk_managers_statuses=list(map(
                                  lambda x: elk_manager_util.ElkManagerUtil.elk_dto_from_dict(x),
                                  d["elk_managers_statuses"])), local_kibana_port=d["local_kibana_port"],
                              physical_server_ip=d["physical_server_ip"])
        return dto

    @staticmethod
    def from_json_file(json_file_path: str) -> "ELKManagersInfo":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ELKManagersInfo.from_dict(json.loads(json_str))
