from typing import List, Dict, Any
import csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc
import csle_collector.snort_ids_manager.snort_ids_manager_pb2
import csle_collector.snort_ids_manager.snort_ids_manager_util as snort_ids_manager_util
from csle_base.json_serializable import JSONSerializable


class SnortIdsManagersInfo(JSONSerializable):
    """
    DTO containing the status of the snort managers for a given emulation execution
    """

    def __init__(
            self, ips: List[str], ports: List[int], emulation_name: str, execution_id: int,
            snort_ids_managers_statuses: List[
                csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO],
            snort_ids_managers_running: List[bool]):
        """
        Initializes the DTO

        :param snort_ids_managers_running: list of booleans that indicate whether the snort managers are running or not
        :param ips: the list of IPs of the running snort managers
        :param ports: the list of ports of the running snort managers
        :param emulation_name: the name of the corresponding emulation
        :param execution_id: the ID of the corresponding emulation execution
        :param snort_ids_managers_statuses: a list of statuses of the Snort managers
        """
        self.snort_ids_managers_running = snort_ids_managers_running
        self.ips = ips
        self.ports = ports
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.snort_ids_managers_statuses = snort_ids_managers_statuses

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"snort_ids_managers_running: {self.snort_ids_managers_running}, " \
               f"ips: {list(map(lambda x: str(x), self.ips))}, " \
               f"emulation_name: {self.emulation_name}, " \
               f"execution_id: {self.execution_id}, " \
               f"snort_ids_managers_statuses: {list(map(lambda x: str(x), self.snort_ids_managers_statuses))}," \
               f" ports: {list(map(lambda x: str(x), self.ports))}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["snort_ids_managers_running"] = self.snort_ids_managers_running
        d["ips"] = self.ips
        d["ports"] = self.ports
        d["emulation_name"] = self.emulation_name
        d["execution_id"] = self.execution_id
        d["snort_ids_managers_statuses"] = list(map(
            lambda x: snort_ids_manager_util.SnortIdsManagerUtil.snort_ids_monitor_dto_to_dict(x),
            self.snort_ids_managers_statuses))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SnortIdsManagersInfo":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = SnortIdsManagersInfo(
            snort_ids_managers_running=d["snort_ids_managers_running"], ips=d["ips"], ports=d["ports"],
            emulation_name=d["emulation_name"], execution_id=d["execution_id"],
            snort_ids_managers_statuses=list(map(
                lambda x: snort_ids_manager_util.SnortIdsManagerUtil.snort_ids_monitor_dto_from_dict(x),
                d["snort_ids_managers_statuses"])))
        return dto

    @staticmethod
    def get_empty_dto() -> "SnortIdsManagersInfo":
        """
        :return: an empty version of the DTO
        """
        return SnortIdsManagersInfo(
            ips=[], ports=[], emulation_name="", execution_id=-1, snort_ids_managers_statuses=[],
            snort_ids_managers_running=[])

    @staticmethod
    def from_json_file(json_file_path: str) -> "SnortIdsManagersInfo":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SnortIdsManagersInfo.from_dict(json.loads(json_str))
