from typing import List, Dict, Any
import csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc
import csle_collector.snort_ids_manager.snort_ids_manager_pb2
import csle_collector.snort_ids_manager.snort_ids_manager_util as snort_ids_manager_util


class SnortIdsManagersInfo:
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
        :return: a dict representation of the object
        """
        d = {}
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
