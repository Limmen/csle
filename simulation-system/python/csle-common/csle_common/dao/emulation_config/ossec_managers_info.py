from typing import List, Dict, Any
import csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc
import csle_collector.ossec_ids_manager.ossec_ids_manager_pb2
import csle_collector.ossec_ids_manager.ossec_ids_manager_util as ossec_ids_manager_util


class OSSECIDSManagersInfo:
    """
    DTO containing the status of the OSSEC IDS managers for a given emulation execution
    """

    def __init__(
            self, ips: List[str], ports: List[int], emulation_name: str, execution_id: int,
            ossec_ids_managers_statuses: List[
                csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO],
            ossec_ids_managers_running: List[bool]):
        """
        Initializes the DTO

        :param ossec_ids_managers_running: list of booleans that indicate whether OSSEC IDS managers are running or not
        :param ips: the list of IPs of the running OSSEC IDS managers
        :param ports: the list of ports of the running OSSEC IDS managers
        :param emulation_name: the name of the corresponding emulation
        :param execution_id: the ID of the corresponding emulation execution
        :param ossec_ids_managers_statuses: a list of statuses of the OSSEC IDS managers
        """
        self.ossec_ids_managers_running = ossec_ids_managers_running
        self.ips = ips
        self.ports = ports
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.ossec_ids_managers_statuses = ossec_ids_managers_statuses

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"ossec_ids_managers_running: {self.ossec_ids_managers_running}, " \
               f"ips: {list(map(lambda x: str(x), self.ips))}, " \
               f"emulation_name: {self.emulation_name}, " \
               f"execution_id: {self.execution_id}, " \
               f"ossec_ids_managers_statuses: {list(map(lambda x: str(x), self.ossec_ids_managers_statuses))}, " \
               f"ports: {list(map(lambda x: str(x), self.ports))},"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ossec_ids_managers_running"] = self.ossec_ids_managers_running
        d["ips"] = self.ips
        d["ports"] = self.ports
        d["emulation_name"] = self.emulation_name
        d["execution_id"] = self.execution_id
        d["ossec_ids_managers_statuses"] = list(map(
            lambda x: ossec_ids_manager_util.OSSecManagerUtil.ossec_ids_monitor_dto_to_dict(x),
            self.ossec_ids_managers_statuses))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OSSECIDSManagersInfo":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = OSSECIDSManagersInfo(
            ossec_ids_managers_running=d["ossec_ids_managers_running"], ips=d["ips"],
            emulation_name=d["emulation_name"], ports=d["ports"], execution_id=d["execution_id"],
            ossec_ids_managers_statuses=list(
                map(lambda x: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO.from_dict(x),
                    d["ossec_ids_managers_statuses"])))
        return dto
