from typing import List, Dict, Any
import csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc
import csle_collector.snort_ids_manager.snort_ids_manager_pb2
import csle_collector.snort_ids_manager.snort_ids_manager_util as snort_ids_manager_util


class SnortManagersInfo:
    """
    DTO containing the status of the snort managers for a given emulation execution
    """

    def __init__(self, running: bool, ips: List[str], emulation_name: str, execution_id: int,
                 snort_statuses: List[csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO]):
        """
        Initializes the DTO

        :param running: boolean that indicates whether the at least one snort manager is running or not
        :param ips: the list of IPs of the running snort managers
        :param emulation_name: the name of the corresponding emulation
        :param execution_id: the ID of the corresponding emulation execution
        :param snort_statuses: a list of statuses of the Snort managers
        """
        self.running = running
        self.ips = ips
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.snort_statuses = snort_statuses

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"running: {self.running}, ips: {list(map(lambda x: str(x), self.ips))}, " \
               f"emulation_name: {self.emulation_name}, " \
               f"execution_id: {self.execution_id}, " \
               f"snort_statuses: {list(map(lambda x: str(x), self.snort_statuses))}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["running"] = self.running
        d["ips"] = self.ips
        d["emulation_name"] = self.emulation_name
        d["execution_id"] = self.execution_id
        d["snort_statuses"] = list(map(
            lambda x: snort_ids_manager_util.SnortIdsManagerUtil.snort_ids_monitor_dto_to_dict(x),
            self.snort_statuses))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SnortManagersInfo":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = SnortManagersInfo(running=d["running"], ips=d["ips"], emulation_name=d["emulation_name"],
                                execution_id=d["execution_id"], snort_statuses=list(map(
                lambda x: snort_ids_manager_util.SnortIdsManagerUtil.snort_ids_monitor_dto_from_dict(x),
                d["snort_statuses"])))
        return dto