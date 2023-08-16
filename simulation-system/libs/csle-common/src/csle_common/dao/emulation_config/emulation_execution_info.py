from typing import Dict, Any, List, Union
from csle_common.dao.emulation_config.snort_managers_info import SnortIdsManagersInfo
from csle_common.dao.emulation_config.ossec_managers_info import OSSECIDSManagersInfo
from csle_common.dao.emulation_config.kafka_managers_info import KafkaManagersInfo
from csle_common.dao.emulation_config.host_managers_info import HostManagersInfo
from csle_common.dao.emulation_config.client_managers_info import ClientManagersInfo
from csle_common.dao.emulation_config.docker_stats_managers_info import DockerStatsManagersInfo
from csle_common.dao.emulation_config.elk_managers_info import ELKManagersInfo
from csle_common.dao.emulation_config.traffic_managers_info import TrafficManagersInfo
from csle_common.dao.emulation_config.ryu_managers_info import RyuManagersInfo
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_base.json_serializable import JSONSerializable


class EmulationExecutionInfo(JSONSerializable):
    """
    DTO containing the runtime status of an emulation execution
    """

    def __init__(self, emulation_name: str, execution_id: int, snort_ids_managers_info: SnortIdsManagersInfo,
                 ossec_ids_managers_info: OSSECIDSManagersInfo, kafka_managers_info: KafkaManagersInfo,
                 host_managers_info: HostManagersInfo, client_managers_info: ClientManagersInfo,
                 docker_stats_managers_info: DockerStatsManagersInfo, running_containers: List[NodeContainerConfig],
                 stopped_containers: List[NodeContainerConfig], traffic_managers_info: TrafficManagersInfo,
                 active_networks: List[ContainerNetwork],
                 inactive_networks: List[ContainerNetwork], elk_managers_info: ELKManagersInfo,
                 ryu_managers_info: Union[None, RyuManagersInfo]):
        """
        Initializes the DTO

        :param emulation_name: the name of the emulation
        :param execution_id: the execution ID
        :param snort_ids_managers_info: information about the snort managers
        :param ossec_ids_managers_info: information about the OSSEC managers
        :param kafka_managers_info: information about the Kafka managers
        :param host_managers_info: information about the Host managers
        :param traffic_managers_info: information about the traffic managers
        :param client_managers_info: information about the client managers
        :param docker_stats_managers_info: information about the docker stats managers
        :param running_containers: information about the running containers
        :param stopped_containers: information about the stopped containers
        :param active_networks: information about the active networks
        :param inactive_networks: information about the inactive networks
        :param elk_managers_info: information about the ELK managers
        :param ryu_managers_info: information about the Ryu managers
        """
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.snort_ids_managers_info = snort_ids_managers_info
        self.ossec_ids_managers_info = ossec_ids_managers_info
        self.kafka_managers_info = kafka_managers_info
        self.host_managers_info = host_managers_info
        self.client_managers_info = client_managers_info
        self.docker_stats_managers_info = docker_stats_managers_info
        self.running_containers = running_containers
        self.stopped_containers = stopped_containers
        self.active_networks = active_networks
        self.inactive_networks = inactive_networks
        self.elk_managers_info = elk_managers_info
        self.traffic_managers_info = traffic_managers_info
        self.ryu_managers_info = ryu_managers_info

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"emulation_name: {self.emulation_name}, execution id: {self.execution_id}, " \
               f"snort_ids_managers_info: {self.snort_ids_managers_info}, " \
               f"ossec_ids_managers_info: {self.ossec_ids_managers_info}," \
               f"kafka_managers_info: {self.kafka_managers_info}, host_managers_info: {self.host_managers_info}," \
               f"client_managers_info: {self.client_managers_info}, " \
               f"docker_stats_managers_info: {self.docker_stats_managers_info}, " \
               f"elk_managers_info: {self.elk_managers_info}, traffic_managers_info: {self.traffic_managers_info}" \
               f"running_containers: {list(map(lambda x: str(x), self.running_containers))}, " \
               f"stopped_containers: {list(map(lambda x: str(x), self.stopped_containers))}, " \
               f"active_networks : {list(map(lambda x: str(x), self.active_networks))}, " \
               f"inactive_networks : {list(map(lambda x: str(x), self.inactive_networks))}," \
               f"ryu_managers_info: {self.ryu_managers_info}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dictionary representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["emulation_name"] = self.emulation_name
        d["execution_id"] = self.execution_id
        d["snort_ids_managers_info"] = self.snort_ids_managers_info.to_dict()
        d["ossec_ids_managers_info"] = self.ossec_ids_managers_info.to_dict()
        d["kafka_managers_info"] = self.kafka_managers_info.to_dict()
        d["host_managers_info"] = self.host_managers_info.to_dict()
        d["elk_managers_info"] = self.elk_managers_info.to_dict()
        d["traffic_managers_info"] = self.traffic_managers_info.to_dict()
        d["client_managers_info"] = self.client_managers_info.to_dict()
        d["docker_stats_managers_info"] = self.docker_stats_managers_info.to_dict()
        d["running_containers"] = list(map(lambda x: x.to_dict(), self.running_containers))
        d["stopped_containers"] = list(map(lambda x: x.to_dict(), self.stopped_containers))
        d["active_networks"] = list(map(lambda x: x.to_dict(), self.active_networks))
        d["inactive_networks"] = list(map(lambda x: x.to_dict(), self.inactive_networks))
        if self.ryu_managers_info is not None:
            d["ryu_managers_info"] = self.ryu_managers_info.to_dict()
        else:
            d["ryu_managers_info"] = None
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationExecutionInfo":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
    
        dto = EmulationExecutionInfo(
            emulation_name=d["emulation_name"], execution_id=d["execution_id"],
            snort_ids_managers_info=SnortIdsManagersInfo.from_dict(d["snort_ids_managers_info"]),
            ossec_ids_managers_info=OSSECIDSManagersInfo.from_dict(d["ossec_ids_managers_info"]),
            kafka_managers_info=KafkaManagersInfo.from_dict(d["kafka_managers_info"]),
            elk_managers_info=ELKManagersInfo.from_dict(d["elk_managers_info"]),
            traffic_managers_info=TrafficManagersInfo.from_dict(d["traffic_managers_info"]),
            host_managers_info=HostManagersInfo.from_dict(d["host_managers_info"]),
            client_managers_info=ClientManagersInfo.from_dict(d["client_managers_info"]),
            docker_stats_managers_info=DockerStatsManagersInfo.from_dict(d["docker_stats_managers_info"]),
            running_containers=list(map(lambda x: NodeContainerConfig.from_dict(x), d["running_containers"])),
            stopped_containers=list(map(lambda x: NodeContainerConfig.from_dict(x), d["stopped_containers"])),
            active_networks=list(map(lambda x: ContainerNetwork.from_dict(x), d["active_networks"])),
            inactive_networks=list(map(lambda x: ContainerNetwork.from_dict(x), d["inactive_networks"])),
            ryu_managers_info=RyuManagersInfo.from_dict(d["ryu_managers_info"]))
        return dto

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationExecutionInfo":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmulationExecutionInfo.from_dict(json.loads(json_str))
