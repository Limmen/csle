from typing import List, Dict, Any
import csle_collector.host_manager.host_manager_pb2_grpc
import csle_collector.host_manager.host_manager_pb2
import csle_collector.host_manager.host_manager_util as host_manager_util


class HostManagersInfo:
    """
    DTO containing the status of the Host managers for a given emulation execution
    """

    def __init__(self, running: bool, ips: List[str], ports: List[int],
                 emulation_name: str, execution_id: int,
                 host_managers_statuses: List[csle_collector.host_manager.host_manager_pb2.HostMonitorDTO]):
        """
        Initializes the DTO

        :param running: boolean that indicates whether the at least one Host manager is running or not
        :param ips: the list of IPs of the running Host managers
        :param ports: the list of ports of the running Host managers
        :param emulation_name: the name of the corresponding emulation
        :param execution_id: the ID of the corresponding emulation execution
        :param host_managers_statuses: a list of statuses of the Host managers
        """
        self.running = running
        self.ips = ips
        self.ports = ports
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.host_managers_statuses = host_managers_statuses

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"running: {self.running}, ips: {list(map(lambda x: str(x), self.ips))}, " \
               f"ports: {list(map(lambda x: str(x), self.ports))}," \
               f"emulation_name: {self.emulation_name}, " \
               f"execution_id: {self.execution_id}, " \
               f"host_managers_statuses: {list(map(lambda x: str(x), self.host_managers_statuses))}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["running"] = self.running
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
        dto = HostManagersInfo(running=d["running"], ips=d["ips"], ports = d["ports"],
                               emulation_name=d["emulation_name"],
                               execution_id=d["execution_id"], host_managers_statuses=list(map(
                lambda x: host_manager_util.HostManagerUtil.host_monitor_dto_from_dict(x),
                d["host_managers_statuses"])))
        return dto