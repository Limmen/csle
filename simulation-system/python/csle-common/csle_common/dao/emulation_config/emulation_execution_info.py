from typing import Dict, Any, List
from csle_common.dao.emulation_config.snort_managers_info import SnortManagersInfo
from csle_common.dao.emulation_config.ossec_managers_info import OSSECIDSManagersInfo
from csle_common.dao.emulation_config.kafka_managers_info import KafkaManagersInfo
from csle_common.dao.emulation_config.host_managers_info import HostManagersInfo
from csle_common.dao.emulation_config.client_managers_info import ClientManagersInfo
from csle_common.dao.emulation_config.docker_stats_managers_info import DockerStatsManagersInfo
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.container_network import ContainerNetwork


class EmulationExecutionInfo:
    """
    DTO containing the runtime status of an emulation execution
    """

    def __init__(self, emulation_name: str, execution_id: int, snort_managers_info: SnortManagersInfo,
                 ossec_managers_info: OSSECIDSManagersInfo, kafka_managers_info: KafkaManagersInfo,
                 host_managers_info: HostManagersInfo, client_managers_info: ClientManagersInfo,
                 docker_stats_managers_info: DockerStatsManagersInfo, running_containers: List[NodeContainerConfig],
                 stopped_containers: List[NodeContainerConfig], active_networks: List[ContainerNetwork],
                 inactive_networks: List[ContainerNetwork]):
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.snort_managers_info = snort_managers_info
        self.ossec_managers_info = ossec_managers_info
        self.kafka_managers_info = kafka_managers_info
        self.host_managers_info = host_managers_info
        self.client_managers_info = client_managers_info
        self.docker_stats_managers_info = docker_stats_managers_info
        self.running_containers = running_containers
        self.stopped_containers = stopped_containers
        self.active_networks = active_networks
        self.inactive_networks = inactive_networks

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"emulation_name: {self.emulation_name}, execution id: {self.execution_id}, " \
               f"snort_managers_info: {self.snort_managers_info}, ossec_managers_info: {self.ossec_managers_info}," \
               f"kafka_managers_info: {self.kafka_managers_info}, host_managers_info: {self.host_managers_info}," \
               f"client_managers_info: {self.client_managers_info}, " \
               f"docker_stats_managers_info: {self.docker_stats_managers_info}, " \
               f"running_containers: {list(map(lambda x: str(x), self.running_containers))}, " \
               f"stopped_containers: {list(map(lambda x: str(x), self.stopped_containers))}, " \
               f"active_networks : {list(map(lambda x: str(x), self.active_networks))}, " \
               f"inactive_networks : {list(map(lambda x: str(x), self.inactive_networks))}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["emulation_name"] = self.emulation_name
        d["execution_id"] = self.execution_id
        d["snort_managers_info"] = self.snort_managers_info.to_dict()
        d["ossec_managers_info"] = self.ossec_managers_info.to_dict()
        d["kafka_managers_info"] = self.kafka_managers_info.to_dict()
        d["host_managers_info"] = self.host_managers_info.to_dict()
        d["client_managers_info"] = self.client_managers_info.to_dict()
        d["docker_stats_managers_info"] = self.docker_stats_managers_info.to_dict()
        d["running_containers"] = list(map(lambda x: x.to_dict(), self.running_containers))
        d["stopped_containers"] = list(map(lambda x: x.to_dict(), self.stopped_containers))
        d["active_networks"] = list(map(lambda x: x.to_dict(), self.active_networks))
        d["inactive_networks"] = list(map(lambda x: x.to_dict(), self.inactive_networks))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationExecutionInfo":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = EmulationExecutionInfo(emulation_name=d["emulation_name"], execution_id=d["execution_id"],
                                     snort_managers_info=SnortManagersInfo.from_dict(d["snort_managers_info"]),
                                     ossec_managers_info=OSSECIDSManagersInfo.from_dict(d["ossec_managers_info"]),
                                     kafka_managers_info=d["kafka_managers_info"],
                                     host_managers_info=d["host_managers_info"],
                                     client_managers_info=d["client_managers_info"],
                                     docker_stats_managers_info=d["docker_stats_managers_info"],
                                     running_containers=list(map(lambda x: x.from_dict(), d["running_containers"])),
                                     stopped_containers=list(map(lambda x: x.from_dict(), d["stopped_containers"])),
                                     active_networks=list(map(lambda x: x.from_dict(), d["active_networks"])),
                                     inactive_networks=list(map(lambda x: x.from_dict(), d["inactive_networks"])))
        return dto