from typing import Dict, Any, List, Union
import logging
from requests import get
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.controllers.container_controller import ContainerController
from csle_common.dao.emulation_config.snort_managers_info import SnortIdsManagersInfo
from csle_common.dao.emulation_config.ossec_managers_info import OSSECIDSManagersInfo
from csle_common.dao.emulation_config.host_managers_info import HostManagersInfo
from csle_common.dao.emulation_config.kafka_managers_info import KafkaManagersInfo
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.client_managers_info import ClientManagersInfo
from csle_common.dao.emulation_config.traffic_managers_info import TrafficManagersInfo
from csle_common.dao.emulation_config.elk_managers_info import ELKManagersInfo
from csle_common.dao.emulation_config.ryu_managers_info import RyuManagersInfo
from csle_common.dao.emulation_config.docker_stats_managers_info import DockerStatsManagersInfo
from csle_common.dao.emulation_config.emulation_execution_info import EmulationExecutionInfo
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.emulation_env_controller import EmulationEnvController
from csle_common.util.general_util import GeneralUtil
from csle_common.util.emulation_util import EmulationUtil
from csle_common.dao.emulation_config.emulation_metrics_time_series import EmulationMetricsTimeSeries
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_collector.snort_ids_manager.dao.snort_ids_ip_alert_counters import SnortIdsIPAlertCounters
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.host_manager.dao.host_metrics import HostMetrics
import csle_collector.client_manager.client_manager_pb2
import csle_collector.traffic_manager.traffic_manager_pb2
import csle_collector.docker_stats_manager.docker_stats_manager_pb2
import csle_collector.elk_manager.elk_manager_pb2
import csle_collector.snort_ids_manager.snort_ids_manager_pb2
import csle_collector.ossec_ids_manager.ossec_ids_manager_pb2
import csle_collector.kafka_manager.kafka_manager_pb2
import csle_collector.ryu_manager.ryu_manager_pb2
import csle_collector.host_manager.host_manager_pb2
from csle_ryu.dao.avg_port_statistic import AvgPortStatistic
from csle_ryu.dao.avg_flow_statistic import AvgFlowStatistic
from csle_ryu.dao.flow_statistic import FlowStatistic
from csle_ryu.dao.port_statistic import PortStatistic
from csle_ryu.dao.agg_flow_statistic import AggFlowStatistic
import csle_cluster.cluster_manager.cluster_manager_pb2 as cluster_manager_pb2
import csle_cluster.constants.constants as cluster_constants


class ClusterManagerUtil:
    """
    Class with utility functions related to the cluster manager
    """

    @staticmethod
    def convert_traffic_dto_to_traffic_manager_info_dto(
            traffic_dto: csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO) -> \
            cluster_manager_pb2.TrafficManagerInfoDTO:
        """
        Converts a TrafficDTO to a TrafficManagerInfoDTO

        :param traffic_dto: the DTO to convert
        :return: the converted DTO
        """
        if traffic_dto is None:
            return ClusterManagerUtil.get_empty_traffic_manager_info_dto()
        else:
            return cluster_manager_pb2.TrafficManagerInfoDTO(running=traffic_dto.running, script=traffic_dto.script)

    @staticmethod
    def convert_traffic_dto_to_traffic_manager_info_dto_reverse(
            traffic_dto: Union[cluster_manager_pb2.TrafficManagerInfoDTO, None]) -> \
            csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO:
        """
        Converts a TrafficManagerInfoDTO to a TrafficDTO

        :param traffic_dto: the DTO to convert
        :return: the converted DTO
        """
        if traffic_dto is None:
            return ClusterManagerUtil.convert_traffic_dto_to_traffic_manager_info_dto_reverse(
                ClusterManagerUtil.get_empty_traffic_manager_info_dto())
        else:
            return csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO(
                running=traffic_dto.running, script=traffic_dto.script)

    @staticmethod
    def get_empty_traffic_manager_info_dto() -> cluster_manager_pb2.TrafficManagerInfoDTO:
        """
        Gets an empty TrafficManagersInfoDTO

        :return: an empty TrafficManagersInfoDTO
        """
        return cluster_manager_pb2.TrafficManagerInfoDTO(running=False, script="")

    @staticmethod
    def get_empty_traffic_managers_info_dto() -> cluster_manager_pb2.TrafficManagersInfoDTO:
        """
        Gets an empty TrafficManagersInfoDTO

        :return: an empty TrafficManagersInfoDTO
        """
        return cluster_manager_pb2.TrafficManagersInfoDTO(ips=[], ports=[], emulationName="", executionId=-1,
                                                          trafficManagersRunning=[], trafficManagersStatuses=[])

    @staticmethod
    def get_empty_client_managers_info_dto() -> cluster_manager_pb2.ClientManagersInfoDTO:
        """
        Gets an empty ClientManagersInfoDTO

        :return: an empty ClientManagersInfoDTO
        """
        return cluster_manager_pb2.ClientManagersInfoDTO(
            ips=[], ports=[], emulationName="", executionId=-1, clientManagersRunning=[],
            clientManagersStatuses=[])

    @staticmethod
    def get_empty_get_num_clients_dto() -> cluster_manager_pb2.GetNumClientsDTO:
        """
        Gets an empty GetNumClientsDTO

        :return: an empty GetNumClientsDTO
        """
        return cluster_manager_pb2.GetNumClientsDTO(num_clients=0, client_process_active=False, producer_active=False,
                                                    clients_time_step_len_seconds=0, producer_time_step_len_seconds=0)

    @staticmethod
    def convert_client_dto_to_get_num_clients_dto(
            clients_dto: csle_collector.client_manager.client_manager_pb2.ClientsDTO) -> \
            cluster_manager_pb2.GetNumClientsDTO:
        """
        Converts a clients DTO to a GetNumClientsDTO

        :param clients_dto: the clients DTO to convert
        :return: the converted DTO
        """
        if clients_dto is None:
            return ClusterManagerUtil.get_empty_num_clients_dto()
        return cluster_manager_pb2.GetNumClientsDTO(
            num_clients=clients_dto.num_clients,
            client_process_active=clients_dto.client_process_active,
            producer_active=clients_dto.producer_active,
            clients_time_step_len_seconds=clients_dto.clients_time_step_len_seconds,
            producer_time_step_len_seconds=clients_dto.producer_time_step_len_seconds
        )

    @staticmethod
    def convert_client_dto_to_get_num_clients_dto_reverse(
            clients_dto: Union[cluster_manager_pb2.GetNumClientsDTO, None]) -> \
            csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Converts a clients DTO to a GetNumClientsDTO

        :param clients_dto: the clients DTO to convert
        :return: the converted DTO
        """
        if clients_dto is None:
            return ClusterManagerUtil.convert_client_dto_to_get_num_clients_dto_reverse(
                ClusterManagerUtil.get_empty_num_clients_dto())
        return csle_collector.client_manager.client_manager_pb2.ClientsDTO(
            num_clients=clients_dto.num_clients,
            client_process_active=clients_dto.client_process_active,
            producer_active=clients_dto.producer_active,
            clients_time_step_len_seconds=clients_dto.clients_time_step_len_seconds,
            producer_time_step_len_seconds=clients_dto.producer_time_step_len_seconds
        )

    @staticmethod
    def node_status_dto_to_dict(node_status_dto: cluster_manager_pb2.NodeStatusDTO) -> Dict[str, Any]:
        """
        Converts a NodeStatusDTO to a dict

        :param node_status_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Union[str, bool]] = {}
        d["ip"] = node_status_dto.ip
        d["leader"] = node_status_dto.leader
        d["cAdvisorRunning"] = node_status_dto.cAdvisorRunning
        d["prometheusRunning"] = node_status_dto.prometheusRunning
        d["grafanaRunning"] = node_status_dto.grafanaRunning
        d["pgAdminRunning"] = node_status_dto.pgAdminRunning
        d["nginxRunning"] = node_status_dto.nginxRunning
        d["flaskRunning"] = node_status_dto.flaskRunning
        d["dockerStatsManagerRunning"] = node_status_dto.dockerStatsManagerRunning
        d["nodeExporterRunning"] = node_status_dto.nodeExporterRunning
        d["postgreSQLRunning"] = node_status_dto.postgreSQLRunning
        d["dockerEngineRunning"] = node_status_dto.dockerEngineRunning
        return d

    @staticmethod
    def service_status_dto_to_dict(node_status_dto: cluster_manager_pb2.ServiceStatusDTO) -> Dict[str, Any]:
        """
        Converts a ServiceStatusDTO to a dict

        :param node_status_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, bool] = {}
        d["running"] = node_status_dto.running
        return d

    @staticmethod
    def logs_dto_to_dict(logs_dto: cluster_manager_pb2.LogsDTO) -> Dict[str, Any]:
        """
        Converts a LogsDTO to a dict

        :param logs_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, List[str]] = {}
        d["logs"] = list(logs_dto.logs)
        return d

    @staticmethod
    def get_num_clients_dto_to_dict(get_num_clients_dto: cluster_manager_pb2.GetNumClientsDTO) -> Dict[str, Any]:
        """
        Converts a GetNumClientsDTO to a dict

        :param get_num_clients_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["num_clients"] = get_num_clients_dto.num_clients
        d["client_process_active"] = get_num_clients_dto.client_process_active
        d["producer_active"] = get_num_clients_dto.producer_active
        d["clients_time_step_len_seconds"] = get_num_clients_dto.clients_time_step_len_seconds
        d["producer_time_step_len_seconds"] = get_num_clients_dto.producer_time_step_len_seconds
        return d

    @staticmethod
    def get_active_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        Gets the locally active ips for a given emulation

        :param emulation_env_config: the emulation configuration
        :return: the list of Ips
        """
        running_containers, stopped_containers = ContainerController.list_all_running_containers_in_emulation(
            emulation_env_config=emulation_env_config)
        active_ips: List[str] = []
        for container in running_containers:
            active_ips = active_ips + container.get_ips()
            active_ips.append(container.docker_gw_bridge_ip)
        active_ips.append(constants.COMMON.LOCALHOST)
        active_ips.append(constants.COMMON.LOCALHOST_127_0_0_1)
        active_ips.append(constants.COMMON.LOCALHOST_127_0_1_1)
        return active_ips

    @staticmethod
    def client_managers_info_dto_to_dict(clients_managers_info_dto: cluster_manager_pb2.ClientManagersInfoDTO) \
            -> Dict[str, Any]:
        """
        Converts a ClientManagersInfoDTO to a dict

        :param clients_managers_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ips"] = list(clients_managers_info_dto.ips)
        d["ports"] = list(clients_managers_info_dto.ports)
        d["emulationName"] = clients_managers_info_dto.emulationName
        d["executionId"] = clients_managers_info_dto.executionId
        d["clientManagersRunning"] = list(clients_managers_info_dto.clientManagersRunning)
        d["clientManagersStatuses"] = list(map(lambda x: ClusterManagerUtil.get_num_clients_dto_to_dict(x),
                                               list(clients_managers_info_dto.clientManagersStatuses)))
        return d

    @staticmethod
    def traffic_manager_info_dto_to_dict(traffic_manager_info_dto: cluster_manager_pb2.TrafficManagerInfoDTO) \
            -> Dict[str, Any]:
        """
        Converts a TrafficManagerInfoDTO to a dict

        :param traffic_manager_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Union[str, bool]] = {}
        d["running"] = traffic_manager_info_dto.running
        d["script"] = traffic_manager_info_dto.script
        return d

    @staticmethod
    def traffic_managers_info_dto_to_dict(traffic_managers_info_dto: cluster_manager_pb2.TrafficManagersInfoDTO) \
            -> Dict[str, Any]:
        """
        Converts a TrafficManagersInfoDTO to a dict

        :param traffic_managers_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ips"] = list(traffic_managers_info_dto.ips)
        d["ports"] = list(traffic_managers_info_dto.ports)
        d["trafficManagersRunning"] = list(traffic_managers_info_dto.trafficManagersRunning)
        d["trafficManagersStatuses"] = list(map(lambda x: ClusterManagerUtil.traffic_manager_info_dto_to_dict(x),
                                                list(traffic_managers_info_dto.trafficManagersStatuses)))
        d["emulationName"] = traffic_managers_info_dto.emulationName
        d["executionId"] = traffic_managers_info_dto.executionId
        return d

    @staticmethod
    def docker_stats_monitor_status_dto_to_dict(
            docker_stats_managers_info_dto: cluster_manager_pb2.DockerStatsMonitorStatusDTO) -> Dict[str, Any]:
        """
        Converts a DockerStatsMonitorStatusDTO to a dict

        :param docker_stats_managers_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["num_monitors"] = docker_stats_managers_info_dto.num_monitors
        d["emulations"] = list(docker_stats_managers_info_dto.emulations)
        d["emulation_executions"] = list(docker_stats_managers_info_dto.emulation_executions)
        return d

    @staticmethod
    def docker_stats_managers_info_dto_to_dict(
            docker_stats_managers_info_dto: cluster_manager_pb2.DockerStatsManagersInfoDTO) -> Dict[str, Any]:
        """
        Converts a DockerStatsManagersInfoDTO to a dict

        :param docker_stats_managers_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ips"] = list(docker_stats_managers_info_dto.ips)
        d["ports"] = list(docker_stats_managers_info_dto.ports)
        d["dockerStatsManagersRunning"] = list(docker_stats_managers_info_dto.dockerStatsManagersRunning)
        d["dockerStatsManagersStatuses"] = list(map(lambda x:
                                                    ClusterManagerUtil.docker_stats_monitor_status_dto_to_dict(x),
                                                    list(docker_stats_managers_info_dto.dockerStatsManagersStatuses)))
        d["emulationName"] = docker_stats_managers_info_dto.emulationName
        d["executionId"] = docker_stats_managers_info_dto.executionId
        return d

    @staticmethod
    def stopped_containers_dto_to_dict(stopped_containers_dto_to_dict: cluster_manager_pb2.StoppedContainersDTO) \
            -> Dict[str, Any]:
        """
        Converts a StoppedContainersDTO to a dict

        :param stopped_containers_dto_to_dict: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["stoppedContainers"] = list(map(lambda x: ClusterManagerUtil.docker_container_dto_to_dict(x),
                                          list(stopped_containers_dto_to_dict.stoppedContainers)))
        return d

    @staticmethod
    def docker_container_dto_to_dict(docker_container_dto_to_dict: cluster_manager_pb2.DockerContainerDTO) \
            -> Dict[str, Any]:
        """
        Converts a DockerContainerDTO to a dict

        :param docker_container_dto_to_dict: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["name"] = docker_container_dto_to_dict.name
        d["image"] = docker_container_dto_to_dict.image
        d["ip"] = docker_container_dto_to_dict.ip
        return d

    @staticmethod
    def running_emulations_dto_to_dict(running_emulations_dto: cluster_manager_pb2.RunningEmulationsDTO) \
            -> Dict[str, Any]:
        """
        Converts a RunningEmulationsDTO to a dict

        :param running_emulations_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["runningEmulations"] = list(running_emulations_dto.runningEmulations)
        return d

    @staticmethod
    def running_containers_dto_to_dict(running_containers_dto_to_dict: cluster_manager_pb2.RunningContainersDTO) \
            -> Dict[str, List[Dict[str, Any]]]:
        """
        Converts a RunningContainersDTO to a dict

        :param running_containers_dto_to_dict: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["runningContainers"] = list(map(lambda x: ClusterManagerUtil.docker_container_dto_to_dict(x),
                                          list(running_containers_dto_to_dict.runningContainers)))
        return d

    @staticmethod
    def docker_networks_dto_to_dict(docker_networks_dto: cluster_manager_pb2.DockerNetworksDTO) -> Dict[str, Any]:
        """
        Converts a DockerNetworksDTO to a dict

        :param docker_networks_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["networks"] = list(docker_networks_dto.networks)
        d["network_ids"] = list(docker_networks_dto.network_ids)
        return d

    @staticmethod
    def container_image_dto_to_dict(container_image_dto: cluster_manager_pb2.ContainerImageDTO) -> Dict[str, Any]:
        """
        Converts a ContainerImageDTO to a dict

        :param container_image_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["repoTags"] = list(container_image_dto.repoTags)
        d["created"] = list(container_image_dto.created)
        d["os"] = list(container_image_dto.os)
        d["architecture"] = list(container_image_dto.architecture)
        d["size"] = container_image_dto.size
        return d

    @staticmethod
    def container_images_dtos_to_dict(container_images_dtos: cluster_manager_pb2.ContainerImagesDTO) -> Dict[str, Any]:
        """
        Converts a ContainerImagesDTO to a dict

        :param container_images_dtos: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["images"] = list(map(lambda x: ClusterManagerUtil.container_image_dto_to_dict(x),
                               list(container_images_dtos.images)))
        return d

    @staticmethod
    def convert_docker_stats_monitor_dto(
            monitor_dto: csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO) -> \
            cluster_manager_pb2.DockerStatsMonitorStatusDTO:
        """
        Converts a DockerStatsMonitorDTO to a DockerStatsMonitorStatusDTO

        :param monitor_dto: the DTO to convert
        :return: the converted DTO
        """
        if monitor_dto is None:
            return ClusterManagerUtil.get_empty_docker_stats_monitor_status_dto()
        return cluster_manager_pb2.DockerStatsMonitorStatusDTO(
            num_monitors=monitor_dto.num_monitors, emulations=monitor_dto.emulations,
            emulation_executions=monitor_dto.emulation_executions
        )

    @staticmethod
    def convert_docker_stats_monitor_dto_reverse(
            monitor_dto: Union[cluster_manager_pb2.DockerStatsMonitorStatusDTO, None]) -> \
            csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO:
        """
        Converts a DockerStatsMonitorStatusDTO to a DockerStatsMonitorDTO

        :param monitor_dto: the DTO to convert
        :return: the converted DTO
        """
        if monitor_dto is None:
            return ClusterManagerUtil.convert_docker_stats_monitor_dto_reverse(
                ClusterManagerUtil.get_empty_docker_stats_monitor_status_dto())
        return csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO(
            num_monitors=monitor_dto.num_monitors, emulations=monitor_dto.emulations,
            emulation_executions=monitor_dto.emulation_executions
        )

    @staticmethod
    def elk_status_dto_to_dict(elk_status_dto: cluster_manager_pb2.ElkStatusDTO) -> Dict[str, Any]:
        """
        Converts a ElkStatusDTO to a dict

        :param elk_status_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, bool] = {}
        d["elasticRunning"] = elk_status_dto.elasticRunning
        d["kibanaRunning"] = elk_status_dto.kibanaRunning
        d["logstashRunning"] = elk_status_dto.logstashRunning
        return d

    @staticmethod
    def elk_managers_info_dto_to_dict(elk_managers_info_dto: cluster_manager_pb2.ElkManagersInfoDTO) -> Dict[str, Any]:
        """
        Converts a ElkManagersInfoDTO to a dict

        :param elk_managers_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ips"] = list(elk_managers_info_dto.ips)
        d["ports"] = list(elk_managers_info_dto.ports)
        d["elkManagersRunning"] = list(elk_managers_info_dto.elkManagersRunning)
        d["elkManagersStatuses"] = list(map(lambda x: ClusterManagerUtil.elk_status_dto_to_dict(x),
                                            list(elk_managers_info_dto.elkManagersStatuses)))
        d["emulationName"] = elk_managers_info_dto.emulationName
        d["executionId"] = elk_managers_info_dto.executionId
        d["localKibanaPort"] = elk_managers_info_dto.localKibanaPort
        return d

    @staticmethod
    def convert_elk_dto(
            elk_dto: csle_collector.elk_manager.elk_manager_pb2.ElkDTO) -> cluster_manager_pb2.ElkStatusDTO:
        """
        Converts an ElkDTO to a ElkStatusDTO

        :param elk_dto: the DTO to convert
        :return: the converted DTO
        """
        if elk_dto is None:
            return ClusterManagerUtil.get_empty_elk_status_dto()
        return cluster_manager_pb2.ElkStatusDTO(
            elasticRunning=elk_dto.elasticRunning, kibanaRunning=elk_dto.kibanaRunning,
            logstashRunning=elk_dto.logstashRunning
        )

    @staticmethod
    def convert_elk_dto_reverse(elk_dto: Union[cluster_manager_pb2.ElkStatusDTO, None]) \
            -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Converts an ElkStatusDTO to an ElkDTO

        :param elk_dto: the DTO to convert
        :return: the converted DTO
        """
        if elk_dto is None:
            return ClusterManagerUtil.convert_elk_dto_reverse(ClusterManagerUtil.get_empty_elk_status_dto())
        return csle_collector.elk_manager.elk_manager_pb2.ElkDTO(
            elasticRunning=elk_dto.elasticRunning, kibanaRunning=elk_dto.kibanaRunning,
            logstashRunning=elk_dto.logstashRunning
        )

    @staticmethod
    def convert_snort_ids_monitor_dto_to_snort_ids_status_dto(
            snort_dto: Union[csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO, None]) -> \
            cluster_manager_pb2.SnortIdsStatusDTO:
        """
        Converts a SnortIdsMonitorDTO to a SnortIdsStatusDTO

        :param snort_dto: the DTO to convert
        :return: the converted DTO
        """
        if snort_dto is None:
            return ClusterManagerUtil.get_empty_snort_ids_status_dto()
        return cluster_manager_pb2.SnortIdsStatusDTO(monitor_running=snort_dto.monitor_running,
                                                     snort_ids_running=snort_dto.snort_ids_running)

    @staticmethod
    def convert_snort_ids_monitor_dto_to_snort_ids_status_dto_reverse(
            snort_dto: Union[cluster_manager_pb2.SnortIdsStatusDTO, None]) -> \
            csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO:
        """
        Converts a SnortIdsStatusDTO to a SnortIdsMonitorDTO

        :param snort_dto: the DTO to convert
        :return: the converted DTO
        """
        if snort_dto is None:
            return ClusterManagerUtil.convert_snort_ids_monitor_dto_to_snort_ids_status_dto_reverse(
                ClusterManagerUtil.get_empty_snort_ids_status_dto())
        return csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO(
            monitor_running=snort_dto.monitor_running, snort_ids_running=snort_dto.snort_ids_running)

    @staticmethod
    def convert_ossec_ids_monitor_dto_to_ossec_ids_status_dto(
            ossec_dto: Union[None, csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO]) -> \
            cluster_manager_pb2.OSSECIdsStatusDTO:
        """
        Converts a OSSECIdsMonitorDTO to a OSSECIdsStatusDTO

        :param ossec_dto: the DTO to convert
        :return: the converted DTO
        """
        if ossec_dto is None:
            return ClusterManagerUtil.get_empty_ossec_ids_status_dto()
        return cluster_manager_pb2.OSSECIdsStatusDTO(monitor_running=ossec_dto.monitor_running,
                                                     ossec_ids_running=ossec_dto.ossec_ids_running)

    @staticmethod
    def convert_ossec_ids_monitor_dto_to_ossec_ids_status_dto_reverse(
            ossec_dto: Union[None, cluster_manager_pb2.OSSECIdsStatusDTO]) -> \
            csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO:
        """
        Converts a OSSECIdsStatusDTO to a OSSECIdsMonitorDTO

        :param ossec_dto: the DTO to convert
        :return: the converted DTO
        """
        if ossec_dto is None:
            return ClusterManagerUtil.convert_ossec_ids_monitor_dto_to_ossec_ids_status_dto_reverse(
                ClusterManagerUtil.get_empty_ossec_ids_status_dto())
        return csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO(
            monitor_running=ossec_dto.monitor_running, ossec_ids_running=ossec_dto.ossec_ids_running)

    @staticmethod
    def convert_kafka_dto_to_kafka_status_dto(
            kafka_dto: Union[None, csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO]) \
            -> cluster_manager_pb2.KafkaStatusDTO:
        """
        Converts a KafkaDTO to a KafkaStatusDTO

        :param kafka_dto: the DTO to convert
        :return: the converted DTO
        """
        if kafka_dto is None:
            return ClusterManagerUtil.get_empty_kafka_dto()
        return cluster_manager_pb2.KafkaStatusDTO(running=kafka_dto.running, topics=kafka_dto.topics)

    @staticmethod
    def convert_kafka_dto_to_kafka_status_dto_reverse(
            kafka_dto: Union[None, cluster_manager_pb2.KafkaStatusDTO]) \
            -> csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
        """
        Converts a KafkaStatusDTO to a KafkaDTO

        :param kafka_dto: the DTO to convert
        :return: the converted DTO
        """
        if kafka_dto is None:
            return ClusterManagerUtil.convert_kafka_dto_to_kafka_status_dto_reverse(
                ClusterManagerUtil.get_empty_kafka_dto())
        return csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO(
            running=kafka_dto.running, topics=kafka_dto.topics)

    @staticmethod
    def convert_ryu_dto_to_ryu_status_dto(
            ryu_dto: Union[None, csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO]) \
            -> cluster_manager_pb2.RyuManagerStatusDTO:
        """
        Converts a RyuDTO to a RyuManagerStatusDTO

        :param ryu_dto: the DTO to convert
        :return: the converted DTO
        """
        if ryu_dto is None:
            return ClusterManagerUtil.get_empty_ryu_manager_status_dto()
        return cluster_manager_pb2.RyuManagerStatusDTO(
            ryu_running=ryu_dto.ryu_running, monitor_running=ryu_dto.monitor_running, port=ryu_dto.port,
            web_port=ryu_dto.web_port, controller=ryu_dto.controller, kafka_ip=ryu_dto.kafka_ip,
            kafka_port=ryu_dto.kafka_port, time_step_len=ryu_dto.time_step_len)

    @staticmethod
    def convert_ryu_dto_to_ryu_status_dto_reverse(
            ryu_dto: Union[None, cluster_manager_pb2.RyuManagerStatusDTO]) \
            -> csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
        """
        Converts a RyuManagerStatusDTO to a RyuDTO

        :param ryu_dto: the DTO to convert
        :return: the converted DTO
        """
        if ryu_dto is None:
            return ClusterManagerUtil.convert_ryu_dto_to_ryu_status_dto_reverse(
                ClusterManagerUtil.get_empty_ryu_manager_status_dto())
        return csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO(
            ryu_running=ryu_dto.ryu_running, monitor_running=ryu_dto.monitor_running, port=ryu_dto.port,
            web_port=ryu_dto.web_port, controller=ryu_dto.controller, kafka_ip=ryu_dto.kafka_ip,
            kafka_port=ryu_dto.kafka_port, time_step_len=ryu_dto.time_step_len)

    @staticmethod
    def snort_ids_status_dto_to_dict(snort_ids_status_dto: cluster_manager_pb2.SnortIdsStatusDTO) -> Dict[str, Any]:
        """
        Converts a SnortIdsStatusDTO to a dict

        :param snort_ids_status_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, bool] = {}
        d["monitor_running"] = snort_ids_status_dto.monitor_running
        d["snort_ids_running"] = snort_ids_status_dto.snort_ids_running
        return d

    @staticmethod
    def ossec_ids_status_dto_to_dict(ossec_ids_status_dto: cluster_manager_pb2.OSSECIdsStatusDTO) -> Dict[str, Any]:
        """
        Converts a OSSECIdsStatusDTO to a dict

        :param ossec_ids_status_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, bool] = {}
        d["monitor_running"] = ossec_ids_status_dto.monitor_running
        d["ossec_ids_running"] = ossec_ids_status_dto.ossec_ids_running
        return d

    @staticmethod
    def snort_ids_monitor_thread_statuses_dto_to_dict(
            snort_ids_monitor_thread_statuses_dto: cluster_manager_pb2.SnortIdsMonitorThreadStatusesDTO) \
            -> Dict[str, Any]:
        """
        Converts a SnortIdsMonitorThreadStatusesDTO to a dict

        :param snort_ids_monitor_thread_statuses_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["snortIDSStatuses"] = list(map(lambda x: ClusterManagerUtil.snort_ids_status_dto_to_dict(x),
                                         snort_ids_monitor_thread_statuses_dto.snortIDSStatuses))
        return d

    @staticmethod
    def ossec_ids_monitor_thread_statuses_dto_to_dict(
            ossec_ids_monitor_thread_statuses_dto: cluster_manager_pb2.OSSECIdsMonitorThreadStatusesDTO) \
            -> Dict[str, Any]:
        """
        Converts a OSSECIdsMonitorThreadStatusesDTO to a dict

        :param ossec_ids_monitor_thread_statuses_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ossecIDSStatuses"] = list(map(lambda x: ClusterManagerUtil.ossec_ids_status_dto_to_dict(x),
                                         ossec_ids_monitor_thread_statuses_dto.ossecIDSStatuses))
        return d

    @staticmethod
    def ryu_manager_status_dto_to_dict(
            ryu_manager_status_dto_to_dict: cluster_manager_pb2.RyuManagerStatusDTO) -> Dict[str, Any]:
        """
        Converts a RyuManagerStatusDTO to a dict

        :param ryu_manager_status_dto_to_dict: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ryu_running"] = ryu_manager_status_dto_to_dict.ryu_running
        d["monitor_running"] = ryu_manager_status_dto_to_dict.monitor_running
        d["port"] = ryu_manager_status_dto_to_dict.port
        d["web_port"] = ryu_manager_status_dto_to_dict.web_port
        d["controller"] = ryu_manager_status_dto_to_dict.controller
        d["kafka_ip"] = ryu_manager_status_dto_to_dict.kafka_ip
        d["kafka_port"] = ryu_manager_status_dto_to_dict.kafka_port
        d["time_step_len"] = ryu_manager_status_dto_to_dict.time_step_len
        return d

    @staticmethod
    def host_manager_status_dto_to_dict(host_manager_status_dto: cluster_manager_pb2.HostManagerStatusDTO) \
            -> Dict[str, Any]:
        """
        Converts a HostManagerStatusDTO to a dict

        :param host_manager_status_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["monitor_running"] = host_manager_status_dto.monitor_running
        d["filebeat_running"] = host_manager_status_dto.filebeat_running
        d["packetbeat_running"] = host_manager_status_dto.packetbeat_running
        d["metricbeat_running"] = host_manager_status_dto.metricbeat_running
        d["heartbeat_running"] = host_manager_status_dto.heartbeat_running
        return d

    @staticmethod
    def kafka_status_dto_to_dict(kafka_status_dto: cluster_manager_pb2.KafkaStatusDTO) -> Dict[str, Any]:
        """
        Converts a KafkaStatusDTO to a dict

        :param kafka_status_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["running"] = kafka_status_dto.running
        d["topics"] = kafka_status_dto.topics
        return d

    @staticmethod
    def snort_managers_info_dto_to_dict(snort_managers_info_dto: cluster_manager_pb2.SnortIdsManagersInfoDTO) \
            -> Dict[str, Any]:
        """
        Converts a SnortIdsManagersInfoDTO to a dict

        :param snort_managers_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ips"] = list(snort_managers_info_dto.ips)
        d["ports"] = list(snort_managers_info_dto.ports)
        d["snortIdsManagersRunning"] = list(snort_managers_info_dto.snortIdsManagersRunning)
        d["snortIdsManagersStatuses"] = list(map(lambda x: ClusterManagerUtil.snort_ids_status_dto_to_dict(x),
                                                 list(snort_managers_info_dto.snortIdsManagersStatuses)))
        d["emulationName"] = snort_managers_info_dto.emulationName
        d["executionId"] = snort_managers_info_dto.executionId
        return d

    @staticmethod
    def ossec_managers_info_dto_to_dict(ossec_managers_info_dto: cluster_manager_pb2.OSSECIdsManagersInfoDTO) \
            -> Dict[str, Any]:
        """
        Converts a OSSECIdsManagersInfoDTO to a dict

        :param ossec_managers_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ips"] = list(ossec_managers_info_dto.ips)
        d["ports"] = list(ossec_managers_info_dto.ports)
        d["ossecIdsManagersRunning"] = list(ossec_managers_info_dto.ossecIdsManagersRunning)
        d["ossecIdsManagersStatuses"] = list(map(lambda x: ClusterManagerUtil.ossec_ids_status_dto_to_dict(x),
                                                 list(ossec_managers_info_dto.ossecIdsManagersStatuses)))
        d["emulationName"] = ossec_managers_info_dto.emulationName
        d["executionId"] = ossec_managers_info_dto.executionId
        return d

    @staticmethod
    def kafka_managers_info_dto_to_dict(kafka_managers_info_dto: cluster_manager_pb2.KafkaManagersInfoDTO) \
            -> Dict[str, Any]:
        """
        Converts a KafkaManagersInfoDTO to a dict

        :param kafka_managers_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ips"] = list(kafka_managers_info_dto.ips)
        d["ports"] = list(kafka_managers_info_dto.ports)
        d["kafkaManagersRunning"] = list(kafka_managers_info_dto.kafkaManagersRunning)
        d["kafkaManagersStatuses"] = list(map(lambda x: ClusterManagerUtil.kafka_status_dto_to_dict(x),
                                              list(kafka_managers_info_dto.kafkaManagersStatuses)))
        d["emulationName"] = kafka_managers_info_dto.emulationName
        d["executionId"] = kafka_managers_info_dto.executionId
        return d

    @staticmethod
    def host_managers_info_dto_to_dict(host_managers_info_dto: cluster_manager_pb2.HostManagersInfoDTO) \
            -> Dict[str, Any]:
        """
        Converts a HostManagersInfoDTO to a dict

        :param host_managers_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ips"] = list(host_managers_info_dto.ips)
        d["ports"] = list(host_managers_info_dto.ports)
        d["hostManagersRunning"] = list(host_managers_info_dto.hostManagersRunning)
        d["hostManagersStatuses"] = list(map(lambda x: ClusterManagerUtil.host_manager_status_dto_to_dict(x),
                                             list(host_managers_info_dto.hostManagersStatuses)))
        d["emulationName"] = host_managers_info_dto.emulationName
        d["executionId"] = host_managers_info_dto.executionId
        return d

    @staticmethod
    def ryu_managers_info_dto_to_dict(ryu_managers_info_dto: cluster_manager_pb2.RyuManagersInfoDTO) -> Dict[str, Any]:
        """
        Converts a RyuManagersInfoDTO to a dict

        :param ryu_managers_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ips"] = list(ryu_managers_info_dto.ips)
        d["ports"] = list(ryu_managers_info_dto.ports)
        d["ryuManagersRunning"] = list(ryu_managers_info_dto.ryuManagersRunning)
        d["ryuManagersStatuses"] = list(map(lambda x: ClusterManagerUtil.ryu_manager_status_dto_to_dict(x),
                                            list(ryu_managers_info_dto.ryuManagersStatuses)))
        d["emulationName"] = ryu_managers_info_dto.emulationName
        d["executionId"] = ryu_managers_info_dto.executionId
        return d

    @staticmethod
    def convert_host_status_to_host_manager_status_dto(
            host_status_dto: csle_collector.host_manager.host_manager_pb2.HostStatusDTO) -> \
            cluster_manager_pb2.HostManagerStatusDTO:
        """
        Converts a HostStatusDTO to a HostManagerStatusDTO

        :param host_status_dto: the DTO to convert
        :return: the converted DTO
        """
        if host_status_dto is None:
            return ClusterManagerUtil.get_empty_host_manager_status_dto()
        return cluster_manager_pb2.HostManagerStatusDTO(
            monitor_running=host_status_dto.monitor_running,
            filebeat_running=host_status_dto.filebeat_running,
            packetbeat_running=host_status_dto.packetbeat_running,
            metricbeat_running=host_status_dto.metricbeat_running,
            heartbeat_running=host_status_dto.heartbeat_running,
            ip=host_status_dto.ip
        )

    @staticmethod
    def convert_host_status_to_host_manager_status_dto_reverse(
            host_status_dto: Union[None, cluster_manager_pb2.HostManagerStatusDTO]) \
            -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Converts a HostManagerStatusDTO to a HostStatusDTO

        :param host_status_dto: the DTO to convert
        :return: the converted DTO
        """
        if host_status_dto is None:
            return ClusterManagerUtil.convert_host_status_to_host_manager_status_dto_reverse(
                ClusterManagerUtil.get_empty_host_manager_status_dto())
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(
            monitor_running=host_status_dto.monitor_running,
            filebeat_running=host_status_dto.filebeat_running,
            packetbeat_running=host_status_dto.packetbeat_running,
            metricbeat_running=host_status_dto.metricbeat_running,
            heartbeat_running=host_status_dto.heartbeat_running)

    @staticmethod
    def convert_snort_info_dto(snort_ids_managers_info_dto: Union[None, SnortIdsManagersInfo]) -> \
            cluster_manager_pb2.SnortIdsManagersInfoDTO:
        """
        Converts a SnortIdsManagersInfo into a SnortIdsManagersInfoDTO

        :param snort_ids_managers_info_dto: the DTO to convert
        :return: the converted DTO
        """
        if snort_ids_managers_info_dto is None:
            return ClusterManagerUtil.get_empty_snort_managers_info_dto()
        return cluster_manager_pb2.SnortIdsManagersInfoDTO(
            ips=snort_ids_managers_info_dto.ips,
            ports=snort_ids_managers_info_dto.ports,
            emulationName=snort_ids_managers_info_dto.emulation_name,
            executionId=snort_ids_managers_info_dto.execution_id,
            snortIdsManagersRunning=snort_ids_managers_info_dto.snort_ids_managers_running,
            snortIdsManagersStatuses=list(
                map(lambda x: ClusterManagerUtil.convert_snort_ids_monitor_dto_to_snort_ids_status_dto(x),
                    snort_ids_managers_info_dto.snort_ids_managers_statuses))
        )

    @staticmethod
    def convert_snort_info_dto_reverse(
            snort_ids_managers_info_dto: Union[None, cluster_manager_pb2.SnortIdsManagersInfoDTO]) \
            -> SnortIdsManagersInfo:
        """
        Converts a SnortIdsManagersInfo into a SnortIdsManagersInfoDTO

        :param snort_ids_managers_info_dto: the DTO to convert
        :return: the converted DTO
        """
        if snort_ids_managers_info_dto is None:
            return ClusterManagerUtil.convert_snort_info_dto_reverse(
                ClusterManagerUtil.get_empty_snort_managers_info_dto())
        return SnortIdsManagersInfo(
            ips=snort_ids_managers_info_dto.ips,
            ports=snort_ids_managers_info_dto.ports,
            emulation_name=snort_ids_managers_info_dto.emulationName,
            execution_id=snort_ids_managers_info_dto.executionId,
            snort_ids_managers_running=snort_ids_managers_info_dto.snortIdsManagersRunning,
            snort_ids_managers_statuses=list(
                map(lambda x: ClusterManagerUtil.convert_snort_ids_monitor_dto_to_snort_ids_status_dto_reverse(x),
                    snort_ids_managers_info_dto.snortIdsManagersStatuses))
        )

    @staticmethod
    def convert_ossec_info_dto(ossec_ids_managers_info_dto: Union[OSSECIDSManagersInfo, None]) \
            -> cluster_manager_pb2.OSSECIdsManagersInfoDTO:
        """
        Converts a OSSECIDSManagersInfo into a OSSECIdsManagersInfoDTO

        :param ossec_ids_managers_info_dto: the DTO to convert
        :return: the converted DTO
        """
        if ossec_ids_managers_info_dto is None:
            return ClusterManagerUtil.get_empty_ossec_managers_info_dto()
        return cluster_manager_pb2.OSSECIdsManagersInfoDTO(
            ips=ossec_ids_managers_info_dto.ips,
            ports=ossec_ids_managers_info_dto.ports,
            emulationName=ossec_ids_managers_info_dto.emulation_name,
            executionId=ossec_ids_managers_info_dto.execution_id,
            ossecIdsManagersRunning=ossec_ids_managers_info_dto.ossec_ids_managers_running,
            ossecIdsManagersStatuses=list(map(
                lambda x: ClusterManagerUtil.convert_ossec_ids_monitor_dto_to_ossec_ids_status_dto(x),
                ossec_ids_managers_info_dto.ossec_ids_managers_statuses))
        )

    @staticmethod
    def convert_ossec_info_dto_reverse(
            ossec_ids_managers_info_dto: Union[None, cluster_manager_pb2.OSSECIdsManagersInfoDTO]) \
            -> OSSECIDSManagersInfo:
        """
        Converts a OSSECIdsManagersInfoDTO into a OSSECIDSManagersInfo

        :param ossec_ids_managers_info_dto: the DTO to convert
        :return: the converted DTO
        """
        if ossec_ids_managers_info_dto is None:
            return ClusterManagerUtil.convert_ossec_info_dto_reverse(
                ClusterManagerUtil.get_empty_ossec_managers_info_dto())
        return OSSECIDSManagersInfo(
            ips=ossec_ids_managers_info_dto.ips,
            ports=ossec_ids_managers_info_dto.ports,
            emulation_name=ossec_ids_managers_info_dto.emulationName,
            execution_id=ossec_ids_managers_info_dto.executionId,
            ossec_ids_managers_running=ossec_ids_managers_info_dto.ossecIdsManagersRunning,
            ossec_ids_managers_statuses=list(map(
                lambda x: ClusterManagerUtil.convert_ossec_ids_monitor_dto_to_ossec_ids_status_dto_reverse(x),
                ossec_ids_managers_info_dto.ossecIdsManagersStatuses))
        )

    @staticmethod
    def convert_elk_info_dto(elk_managers_dto: Union[None, ELKManagersInfo]) \
            -> cluster_manager_pb2.ElkManagersInfoDTO:
        """
        Converts a ELKManagersInfo into a ElkManagersInfoDTO

        :param elk_managers_dto: the DTO to convert
        :return: the converted DTO
        """
        if elk_managers_dto is None:
            return ClusterManagerUtil.get_empty_elk_managers_info_dto()
        return cluster_manager_pb2.ElkManagersInfoDTO(
            ips=elk_managers_dto.ips,
            ports=elk_managers_dto.ports,
            emulationName=elk_managers_dto.emulation_name,
            executionId=elk_managers_dto.execution_id,
            elkManagersRunning=elk_managers_dto.elk_managers_running,
            elkManagersStatuses=list(map(
                lambda x: ClusterManagerUtil.convert_elk_dto(x), elk_managers_dto.elk_managers_statuses)),
            localKibanaPort=elk_managers_dto.local_kibana_port, physicalServerIp=elk_managers_dto.physical_server_ip
        )

    @staticmethod
    def convert_elk_info_dto_reverse(elk_managers_dto: Union[None, cluster_manager_pb2.ElkManagersInfoDTO]) \
            -> ELKManagersInfo:
        """
        Converts a ELKManagersInfo into a ElkManagersInfoDTO

        :param elk_managers_dto: the DTO to convert
        :return: the converted DTO
        """
        if elk_managers_dto is None:
            return ClusterManagerUtil.convert_elk_info_dto_reverse(ClusterManagerUtil.get_empty_elk_managers_info_dto())
        return ELKManagersInfo(
            ips=elk_managers_dto.ips,
            ports=elk_managers_dto.ports,
            emulation_name=elk_managers_dto.emulationName,
            execution_id=elk_managers_dto.executionId,
            elk_managers_running=elk_managers_dto.elkManagersRunning,
            elk_managers_statuses=list(map(
                lambda x: ClusterManagerUtil.convert_elk_dto_reverse(x), elk_managers_dto.elkManagersStatuses)),
            local_kibana_port=elk_managers_dto.localKibanaPort,
            physical_server_ip=elk_managers_dto.physicalServerIp
        )

    @staticmethod
    def convert_ryu_info_dto(ryu_managers_info_dto: Union[None, RyuManagersInfo]) \
            -> cluster_manager_pb2.RyuManagersInfoDTO:
        """
        Converts a RyuManagersInfo into a RyuManagersInfoDTO

        :param ryu_managers_info_dto: the DTO to convert
        :return: the converted DTO
        """
        if ryu_managers_info_dto is None:
            return ClusterManagerUtil.get_empty_ryu_managers_info_dto()
        return cluster_manager_pb2.RyuManagersInfoDTO(
            ips=ryu_managers_info_dto.ips,
            ports=ryu_managers_info_dto.ports,
            emulationName=ryu_managers_info_dto.emulation_name,
            executionId=ryu_managers_info_dto.execution_id,
            ryuManagersRunning=ryu_managers_info_dto.ryu_managers_running,
            ryuManagersStatuses=list(
                map(lambda x: ClusterManagerUtil.convert_ryu_dto_to_ryu_status_dto(x),
                    ryu_managers_info_dto.ryu_managers_statuses)),
            physicalServerIp=ryu_managers_info_dto.physical_server_ip,
            localControllerWebPort=ryu_managers_info_dto.local_controller_web_port
        )

    @staticmethod
    def convert_ryu_info_dto_reverse(ryu_managers_info_dto: Union[None, cluster_manager_pb2.RyuManagersInfoDTO]) \
            -> RyuManagersInfo:
        """
        Converts a RyuManagersInfoDTO into a RyuManagersInfo

        :param ryu_managers_info_dto: the DTO to convert
        :return: the converted DTO
        """
        if ryu_managers_info_dto is None:
            return ClusterManagerUtil.convert_ryu_info_dto_reverse(ClusterManagerUtil.get_empty_ryu_managers_info_dto())
        return RyuManagersInfo(
            ips=ryu_managers_info_dto.ips,
            ports=ryu_managers_info_dto.ports,
            emulation_name=ryu_managers_info_dto.emulationName,
            execution_id=ryu_managers_info_dto.executionId,
            ryu_managers_running=ryu_managers_info_dto.ryuManagersRunning,
            ryu_managers_statuses=list(
                map(lambda x: ClusterManagerUtil.convert_ryu_dto_to_ryu_status_dto_reverse(x),
                    ryu_managers_info_dto.ryuManagersStatuses)),
            physical_server_ip=ryu_managers_info_dto.physicalServerIp,
            local_controller_web_port=ryu_managers_info_dto.localControllerWebPort
        )

    @staticmethod
    def convert_host_info_dto(host_managers_dto: Union[None, HostManagersInfo]) \
            -> cluster_manager_pb2.HostManagersInfoDTO:
        """
        Converts a HostManagersInfo into a HostManagersInfoDTO

        :param host_managers_dto: the DTO to convert
        :return: the converted DTO
        """
        if host_managers_dto is None:
            return ClusterManagerUtil.get_empty_host_managers_info_dto()
        return cluster_manager_pb2.HostManagersInfoDTO(
            ips=host_managers_dto.ips,
            ports=host_managers_dto.ports,
            emulationName=host_managers_dto.emulation_name,
            executionId=host_managers_dto.execution_id,
            hostManagersRunning=host_managers_dto.host_managers_running,
            hostManagersStatuses=list(
                map(lambda x: ClusterManagerUtil.convert_host_status_to_host_manager_status_dto(x),
                    host_managers_dto.host_managers_statuses))
        )

    @staticmethod
    def convert_host_info_dto_reverse(host_managers_dto: Union[None, cluster_manager_pb2.HostManagersInfoDTO]) \
            -> HostManagersInfo:
        """
        Converts a HostManagersInfoDTO into a HostManagersInfo

        :param host_managers_dto: the DTO to convert
        :return: the converted DTO
        """
        if host_managers_dto is None:
            return ClusterManagerUtil.convert_host_info_dto_reverse(
                ClusterManagerUtil.get_empty_host_managers_info_dto())
        return HostManagersInfo(
            ips=host_managers_dto.ips,
            ports=host_managers_dto.ports,
            emulation_name=host_managers_dto.emulationName,
            execution_id=host_managers_dto.executionId,
            host_managers_running=host_managers_dto.hostManagersRunning,
            host_managers_statuses=list(
                map(lambda x: ClusterManagerUtil.convert_host_status_to_host_manager_status_dto_reverse(x),
                    host_managers_dto.hostManagersStatuses))
        )

    @staticmethod
    def convert_kafka_info_dto(kafka_managers_info_dto: Union[None, KafkaManagersInfo]) \
            -> cluster_manager_pb2.KafkaManagersInfoDTO:
        """
        Converts a KafkaManagersInfo into a KafkaManagersInfoDTO

        :param kafka_managers_info_dto: the DTO to convert
        :return: the converted DTO
        """
        if kafka_managers_info_dto is None:
            return ClusterManagerUtil.get_empty_kafka_managers_info_dto()
        return cluster_manager_pb2.KafkaManagersInfoDTO(
            ips=kafka_managers_info_dto.ips,
            ports=kafka_managers_info_dto.ports,
            emulationName=kafka_managers_info_dto.emulation_name,
            executionId=kafka_managers_info_dto.execution_id,
            kafkaManagersRunning=kafka_managers_info_dto.kafka_managers_running,
            kafkaManagersStatuses=list(map(lambda x: ClusterManagerUtil.convert_kafka_dto_to_kafka_status_dto(x),
                                           kafka_managers_info_dto.kafka_managers_statuses))
        )

    @staticmethod
    def convert_kafka_info_dto_reverse(
            kafka_managers_info_dto: Union[None, cluster_manager_pb2.KafkaManagersInfoDTO]) -> KafkaManagersInfo:
        """
        Converts a KafkaManagersInfoDTO into a KafkaManagersInfo

        :param kafka_managers_info_dto: the DTO to convert
        :return: the converted DTO
        """
        if kafka_managers_info_dto is None:
            return ClusterManagerUtil.convert_kafka_info_dto_reverse(
                ClusterManagerUtil.get_empty_kafka_managers_info_dto())
        return KafkaManagersInfo(
            ips=kafka_managers_info_dto.ips,
            ports=kafka_managers_info_dto.ports,
            emulation_name=kafka_managers_info_dto.emulationName,
            execution_id=kafka_managers_info_dto.executionId,
            kafka_managers_running=kafka_managers_info_dto.kafkaManagersRunning,
            kafka_managers_statuses=list(
                map(lambda x: ClusterManagerUtil.convert_kafka_dto_to_kafka_status_dto_reverse(x),
                    kafka_managers_info_dto.kafkaManagersStatuses))
        )

    @staticmethod
    def convert_client_info_dto(client_managers_dto: Union[None, ClientManagersInfo]) \
            -> cluster_manager_pb2.ClientManagersInfoDTO:
        """
        Converts a ClientManagersInfo into a ClientManagersInfoDTO

        :param client_managers_dto: the DTO to convert
        :return: the converted DTO
        """
        if client_managers_dto is None:
            return ClusterManagerUtil.get_empty_client_managers_info_dto()
        return cluster_manager_pb2.ClientManagersInfoDTO(
            ips=client_managers_dto.ips,
            ports=client_managers_dto.ports,
            emulationName=client_managers_dto.emulation_name,
            executionId=client_managers_dto.execution_id,
            clientManagersRunning=client_managers_dto.client_managers_running,
            clientManagersStatuses=list(map(lambda x: ClusterManagerUtil.convert_client_dto_to_get_num_clients_dto(x),
                                            client_managers_dto.client_managers_statuses))
        )

    @staticmethod
    def convert_client_info_dto_reverse(client_managers_dto: Union[None, cluster_manager_pb2.ClientManagersInfoDTO]) \
            -> ClientManagersInfo:
        """
        Converts a ClientManagersInfoDTO into a ClientManagersInfo

        :param client_managers_dto: the DTO to convert
        :return: the converted DTO
        """
        if client_managers_dto is None:
            return ClusterManagerUtil.convert_client_info_dto_reverse(
                ClusterManagerUtil.get_empty_client_managers_info_dto())
        return ClientManagersInfo(
            ips=client_managers_dto.ips,
            ports=client_managers_dto.ports,
            emulation_name=client_managers_dto.emulationName,
            execution_id=client_managers_dto.executionId,
            client_managers_running=client_managers_dto.clientManagersRunning,
            client_managers_statuses=list(
                map(lambda x: ClusterManagerUtil.convert_client_dto_to_get_num_clients_dto_reverse(x),
                    client_managers_dto.clientManagersStatuses))
        )

    @staticmethod
    def convert_traffic_info_dto(traffic_managers_dto: Union[None, TrafficManagersInfo]) \
            -> cluster_manager_pb2.TrafficManagersInfoDTO:
        """
        Converts a TrafficManagersInfo into a TrafficManagerInfoDTO

        :param traffic_managers_dto: the DTO to convert
        :return: the converted DTO
        """

        if traffic_managers_dto is None:
            return ClusterManagerUtil.get_empty_traffic_managers_info_dto()
        return cluster_manager_pb2.TrafficManagersInfoDTO(
            ips=traffic_managers_dto.ips,
            ports=traffic_managers_dto.ports,
            emulationName=traffic_managers_dto.emulation_name,
            executionId=traffic_managers_dto.execution_id,
            trafficManagersRunning=traffic_managers_dto.traffic_managers_running,
            trafficManagersStatuses=list(map(
                lambda x: ClusterManagerUtil.convert_traffic_dto_to_traffic_manager_info_dto(x),
                traffic_managers_dto.traffic_managers_statuses))
        )

    @staticmethod
    def convert_traffic_info_dto_reverse(
            traffic_managers_dto: Union[None, cluster_manager_pb2.TrafficManagersInfoDTO]) -> TrafficManagersInfo:
        """
        Converts a TrafficManagerInfoDTO into a TrafficManagersInfo

        :param traffic_managers_dto: the DTO to convert
        :return: the converted DTO
        """
        if traffic_managers_dto is None:
            return ClusterManagerUtil.convert_traffic_info_dto_reverse(
                ClusterManagerUtil.get_empty_traffic_managers_info_dto())
        return TrafficManagersInfo(
            ips=traffic_managers_dto.ips,
            ports=traffic_managers_dto.ports,
            emulation_name=traffic_managers_dto.emulationName,
            execution_id=traffic_managers_dto.executionId,
            traffic_managers_running=traffic_managers_dto.trafficManagersRunning,
            traffic_managers_statuses=list(map(
                lambda x: ClusterManagerUtil.convert_traffic_dto_to_traffic_manager_info_dto_reverse(x),
                traffic_managers_dto.trafficManagersStatuses))
        )

    @staticmethod
    def convert_docker_info_dto(docker_stats_managers_dto: Union[None, DockerStatsManagersInfo]) \
            -> cluster_manager_pb2.DockerStatsManagersInfoDTO:
        """
        Converts a DockerStatsManagersInfo into a DockerStatsManagersInfoDTO

        :param docker_stats_managers_dto: the DTO to convert
        :return: the converted DTO
        """
        if docker_stats_managers_dto is None:
            return ClusterManagerUtil.get_empty_docker_managers_info_dto()
        return cluster_manager_pb2.DockerStatsManagersInfoDTO(
            ips=docker_stats_managers_dto.ips,
            ports=docker_stats_managers_dto.ports,
            emulationName=docker_stats_managers_dto.emulation_name,
            executionId=docker_stats_managers_dto.execution_id,
            dockerStatsManagersRunning=docker_stats_managers_dto.docker_stats_managers_running,
            dockerStatsManagersStatuses=list(map(lambda x: ClusterManagerUtil.convert_docker_stats_monitor_dto(x),
                                                 docker_stats_managers_dto.docker_stats_managers_statuses))
        )

    @staticmethod
    def convert_docker_info_dto_reverse(
            docker_stats_managers_dto: Union[None, cluster_manager_pb2.DockerStatsManagersInfoDTO]) \
            -> DockerStatsManagersInfo:
        """
        Converts a DockerStatsManagersInfoDTO into a DockerStatsManagersInfo

        :param docker_stats_managers_dto: the DTO to convert
        :return: the converted DTO
        """
        if docker_stats_managers_dto is None:
            return ClusterManagerUtil.convert_docker_info_dto_reverse(
                ClusterManagerUtil.get_empty_docker_managers_info_dto())
        return DockerStatsManagersInfo(
            ips=docker_stats_managers_dto.ips,
            ports=docker_stats_managers_dto.ports,
            emulation_name=docker_stats_managers_dto.emulationName,
            execution_id=docker_stats_managers_dto.executionId,
            docker_stats_managers_running=docker_stats_managers_dto.dockerStatsManagersRunning,
            docker_stats_managers_statuses=list(
                map(lambda x: ClusterManagerUtil.convert_docker_stats_monitor_dto_reverse(x),
                    docker_stats_managers_dto.dockerStatsManagersStatuses))
        )

    @staticmethod
    def convert_execution_info_dto(execution_info_dto: Union[None, EmulationExecutionInfo]) \
            -> cluster_manager_pb2.ExecutionInfoDTO:
        """
        Converts a EmulationExecutionInfo into a ExecutionInfoDTO

        :param execution_info_dto: the DTO to convert
        :return: the converted DTO
        """
        if execution_info_dto is None:
            return ClusterManagerUtil.get_empty_execution_info_dto()
        running_containers = []
        for container in execution_info_dto.running_containers:
            running_containers.append(
                cluster_manager_pb2.DockerContainerDTO(
                    name=container.name, image=container.full_name_str, ip=container.get_ips()[0]
                )
            )
        stopped_containers = []
        for container in execution_info_dto.stopped_containers:
            stopped_containers.append(
                cluster_manager_pb2.DockerContainerDTO(
                    name=container.name, image=container.full_name_str, ip=container.get_ips()[0]
                )
            )
        network_names = []
        network_ids = []
        for net in execution_info_dto.active_networks:
            network_names.append(net.name)
            network_ids.append(-1)
        stopped_container_dtos = cluster_manager_pb2.StoppedContainersDTO(stoppedContainers=stopped_containers)
        running_container_dtos = cluster_manager_pb2.RunningContainersDTO(runningContainers=running_containers)
        activeNetworks = cluster_manager_pb2.DockerNetworksDTO(networks=network_names, network_ids=network_ids)
        return cluster_manager_pb2.ExecutionInfoDTO(
            emulationName=execution_info_dto.emulation_name,
            executionId=execution_info_dto.execution_id,
            snortIdsManagersInfo=ClusterManagerUtil.convert_snort_info_dto(execution_info_dto.snort_ids_managers_info),
            ossecIdsManagersInfo=ClusterManagerUtil.convert_ossec_info_dto(execution_info_dto.ossec_ids_managers_info),
            kafkaManagersInfo=ClusterManagerUtil.convert_kafka_info_dto(execution_info_dto.kafka_managers_info),
            hostManagersInfo=ClusterManagerUtil.convert_host_info_dto(execution_info_dto.host_managers_info),
            clientManagersInfo=ClusterManagerUtil.convert_client_info_dto(execution_info_dto.client_managers_info),
            dockerStatsManagersInfo=ClusterManagerUtil.convert_docker_info_dto(
                execution_info_dto.docker_stats_managers_info),
            runningContainers=running_container_dtos, stoppedContainers=stopped_container_dtos,
            trafficManagersInfoDTO=ClusterManagerUtil.convert_traffic_info_dto(
                execution_info_dto.traffic_managers_info),
            activeNetworks=activeNetworks,
            elkManagersInfoDTO=ClusterManagerUtil.convert_elk_info_dto(execution_info_dto.elk_managers_info),
            ryuManagersInfoDTO=ClusterManagerUtil.convert_ryu_info_dto(execution_info_dto.ryu_managers_info),
        )

    @staticmethod
    def get_empty_kafka_dto() -> cluster_manager_pb2.KafkaStatusDTO:
        """
        Gets an empty KafkaStatusDTO

        :return: an empty KafkaStatusDTO
        """
        return cluster_manager_pb2.KafkaStatusDTO(running=False, topics=[])

    @staticmethod
    def get_empty_ryu_manager_status_dto() -> cluster_manager_pb2.RyuManagerStatusDTO:
        """
        Gets an empty RyuManagerStatusDTO

        :return: an empty RyuManagerStatusDTO
        """
        return cluster_manager_pb2.RyuManagerStatusDTO(
            ryu_running=False, monitor_running=False, port=-1, web_port=-1, controller="", kafka_ip="",
            kafka_port=-1, time_step_len=-1
        )

    @staticmethod
    def get_empty_docker_stats_monitor_status_dto() -> cluster_manager_pb2.DockerStatsMonitorStatusDTO:
        """
        Gets an empty DockerStatsMonitorStatusDTO

        :return: an empty DockerStatsMonitorStatusDTO
        """
        return cluster_manager_pb2.DockerStatsMonitorStatusDTO(num_monitors=0, emulations=[], emulation_executions=[])

    @staticmethod
    def get_empty_num_clients_dto() -> cluster_manager_pb2.GetNumClientsDTO:
        """
        Gets an empty GetNumClientsDTO

        :return: an empty GetNumClientsDTO
        """
        return cluster_manager_pb2.GetNumClientsDTO(
            num_clients=0, client_process_active=False, producer_active=False, clients_time_step_len_seconds=-1,
            producer_time_step_len_seconds=-1)

    @staticmethod
    def get_empty_elk_status_dto() -> cluster_manager_pb2.ElkStatusDTO:
        """
        Gets an empty ElkStatusDTO

        :return: an empty ElkStatusDTO
        """
        return cluster_manager_pb2.ElkStatusDTO(elasticRunning=False, kibanaRunning=False, logstashRunning=False)

    @staticmethod
    def get_empty_snort_ids_status_dto() -> cluster_manager_pb2.SnortIdsStatusDTO:
        """
        Gets an empty SnortIdsStatusDTO

        :return: an empty SnortIdsStatusDTO
        """
        return cluster_manager_pb2.SnortIdsStatusDTO(monitor_running=False, snort_ids_running=False)

    @staticmethod
    def get_empty_ossec_ids_status_dto() -> cluster_manager_pb2.OSSECIdsStatusDTO:
        """
        Gets an empty OSSECIdsStatusDTO

        :return: an empty OSSECIdsStatusDTO
        """
        return cluster_manager_pb2.OSSECIdsStatusDTO(monitor_running=False, ossec_ids_running=False)

    @staticmethod
    def get_empty_ossec_ids_monitor_dto() -> cluster_manager_pb2.OSSECIdsStatusDTO:
        """
        Gets an empty OSSECIdsMonitorDTO

        :return: an empty OSSECIdsMonitorDTO
        """
        return cluster_manager_pb2.OSSECIdsStatusDTO(monitor_running=False, ossec_ids_running=False)

    @staticmethod
    def get_empty_host_manager_status_dto() -> cluster_manager_pb2.HostManagerStatusDTO:
        """
        Gets an empty HostManagerStatusDTO

        :return: an empty HostManagerStatusDTO
        """
        return cluster_manager_pb2.HostManagerStatusDTO(
            monitor_running=False, filebeat_running=False, packetbeat_running=False, metricbeat_running=False,
            heartbeat_running=False, ip="")

    @staticmethod
    def get_empty_snort_managers_info_dto() -> cluster_manager_pb2.SnortIdsManagersInfoDTO:
        """
        Gets an empty SnortIdsManagersInfoDTO

        :return: an empty SnortIdsManagersInfoDTO
        """
        return cluster_manager_pb2.SnortIdsManagersInfoDTO(
            ips=[], ports=[], emulationName="", executionId=-1, snortIdsManagersRunning=[], snortIdsManagersStatuses=[])

    @staticmethod
    def get_empty_ossec_managers_info_dto() -> cluster_manager_pb2.OSSECIdsManagersInfoDTO:
        """
        Gets an empty OSSECIdsManagersInfoDTO

        :return: an empty OSSECIdsManagersInfoDTO
        """
        return cluster_manager_pb2.OSSECIdsManagersInfoDTO(
            ips=[], ports=[], emulationName="", executionId=-1, ossecIdsManagersRunning=[], ossecIdsManagersStatuses=[]
        )

    @staticmethod
    def get_empty_elk_managers_info_dto() -> cluster_manager_pb2.ElkManagersInfoDTO:
        """
        Gets an empty ElkManagersInfoDTO

        :return: an empty ElkManagersInfoDTO
        """
        return cluster_manager_pb2.ElkManagersInfoDTO(
            ips=[], ports=[], emulationName="", executionId=-1, elkManagersRunning=[], elkManagersStatuses=[],
            localKibanaPort=-1, physicalServerIp=""
        )

    @staticmethod
    def get_empty_ryu_managers_info_dto() -> cluster_manager_pb2.RyuManagersInfoDTO:
        """
        Gets an empty RyuManagersInfoDTO

        :return: an empty RyuManagersInfoDTO
        """
        return cluster_manager_pb2.RyuManagersInfoDTO(
            ips=[], ports=[], emulationName="", executionId=-1, ryuManagersRunning=[], ryuManagersStatuses=[],
            physicalServerIp="", localControllerWebPort=-1
        )

    @staticmethod
    def get_empty_host_managers_info_dto() -> cluster_manager_pb2.HostManagersInfoDTO:
        """
        Gets an empty HostManagersInfoDTO

        :return: an empty HostManagersInfoDTO
        """
        return cluster_manager_pb2.HostManagersInfoDTO(
            ips=[], ports=[], emulationName="", executionId=-1, hostManagersRunning=[], hostManagersStatuses=[]
        )

    @staticmethod
    def get_empty_kafka_managers_info_dto() -> cluster_manager_pb2.KafkaManagersInfoDTO:
        """
        Gets an empty KafkaManagersInfoDTO

        :return: an empty KafkaManagersInfoDTO
        """
        return cluster_manager_pb2.KafkaManagersInfoDTO(
            ips=[], ports=[], emulationName="", executionId=-1, kafkaManagersRunning=[], kafkaManagersStatuses=[])

    @staticmethod
    def get_empty_docker_managers_info_dto() -> cluster_manager_pb2.DockerStatsManagersInfoDTO:
        """
        Gets an empty DockerStatsManagersInfoDTO

        :return: an empty DockerStatsManagersInfoDTO
        """
        return cluster_manager_pb2.DockerStatsManagersInfoDTO(
            ips=[], ports=[], emulationName="", executionId=-1, dockerStatsManagersRunning=[],
            dockerStatsManagersStatuses=[]
        )

    @staticmethod
    def get_empty_execution_info_dto() -> cluster_manager_pb2.ExecutionInfoDTO:
        """
        Gets an empty ExecutionInfoDTO

        :return: an empty ExecutionInfoDTO
        """
        return cluster_manager_pb2.ExecutionInfoDTO(
            emulationName="", executionId=-1, snortIdsManagersInfo=None, ossecIdsManagersInfo=None,
            kafkaManagersInfo=None, hostManagersInfo=None, clientManagersInfo=None, dockerStatsManagersInfo=None,
            runningContainers=None, elkManagersInfoDTO=None, ryuManagersInfoDTO=None, trafficManagersInfoDTO=None,
            stoppedContainers=None, activeNetworks=None
        )

    @staticmethod
    def get_empty_kibana_tunnel_dto() -> cluster_manager_pb2.KibanaTunnelDTO:
        """
        Gets an empty KibanaTunnelDTO

        :return: an empty KibanaTunnelDTO
        """
        return cluster_manager_pb2.KibanaTunnelDTO(port=1, ip="", emulation="", ipFirstOctet=-1)

    @staticmethod
    def get_empty_kibana_tunnels_dto() -> cluster_manager_pb2.KibanaTunnelsDTO:
        """
        Gets an empty KibanaTunnelsDTO

        :return: an empty KibanaTunnelsDTO
        """
        return cluster_manager_pb2.KibanaTunnelsDTO(tunnels=[])

    @staticmethod
    def kibana_tunnel_dto_to_dict(kibana_tunnel_dto: cluster_manager_pb2.KibanaTunnelDTO) -> Dict[str, Any]:
        """
        Converts a KibanaTunnelDTO to a dict

        :param kibana_tunnel_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ip"] = kibana_tunnel_dto.ip
        d["port"] = kibana_tunnel_dto.port
        d["emulation"] = kibana_tunnel_dto.emulation
        d["ipFirstOctet"] = kibana_tunnel_dto.ipFirstOctet
        return d

    @staticmethod
    def kibana_tunnels_dto_to_dict(kibana_tunnels_dto: cluster_manager_pb2.KibanaTunnelsDTO) -> Dict[str, Any]:
        """
        Converts a KibanaTunnelsDTO to a dict

        :param kibana_tunnels_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["tunnels"] = list(map(lambda x: ClusterManagerUtil.kibana_tunnel_dto_to_dict(kibana_tunnel_dto=x),
                                kibana_tunnels_dto.tunnels))
        return d

    @staticmethod
    def get_empty_ryu_tunnel_dto() -> cluster_manager_pb2.RyuTunnelDTO:
        """
        Gets an empty RyuTunnelDTO

        :return: an empty RyuTunnelDTO
        """
        return cluster_manager_pb2.RyuTunnelDTO(port=1, ip="", emulation="", ipFirstOctet=-1)

    @staticmethod
    def get_empty_ryu_tunnels_dto() -> cluster_manager_pb2.RyuTunnelsDTO:
        """
        :return: an empty RyuTunnelsDTO
        """
        return cluster_manager_pb2.RyuTunnelsDTO(tunnels=[])

    @staticmethod
    def ryu_tunnel_dto_to_dict(ryu_tunnel_dto: cluster_manager_pb2.RyuTunnelDTO) -> Dict[str, Any]:
        """
        Converts a RyuTunnelDTO to a dict

        :param ryu_tunnel_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ip"] = ryu_tunnel_dto.ip
        d["port"] = ryu_tunnel_dto.port
        d["emulation"] = ryu_tunnel_dto.emulation
        d["ipFirstOctet"] = ryu_tunnel_dto.ipFirstOctet
        return d

    @staticmethod
    def ryu_tunnels_dto_to_dict(ryu_tunnels_dto: cluster_manager_pb2.RyuTunnelsDTO) -> Dict[str, Any]:
        """
        Converts a RyuTunnelsDTO to a dict

        :param ryu_tunnels_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["tunnels"] = list(map(lambda x: ClusterManagerUtil.ryu_tunnel_dto_to_dict(ryu_tunnel_dto=x),
                                ryu_tunnels_dto.tunnels))
        return d

    @staticmethod
    def create_kibana_tunnel(execution: EmulationExecution, logger: logging.Logger) -> int:
        """
        Utility method for creating a Kibana tunnel.

        :param execution: the execution to create the tunnel for
        :param logger: the logger to use for logging
        :return: the port of the tunnel
        """
        ip = GeneralUtil.get_host_ip()
        if ip != execution.emulation_env_config.elk_config.container.physical_host_ip:
            return -1
        try:
            local_kibana_port = cluster_constants.KIBANA_TUNNELS.KIBANA_TUNNEL_BASE_PORT + execution.ip_first_octet
            if execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip \
                    not in cluster_constants.KIBANA_TUNNELS.KIBANA_TUNNELS_DICT:
                try:
                    EmulationEnvController.create_ssh_tunnel(
                        tunnels_dict=cluster_constants.KIBANA_TUNNELS.KIBANA_TUNNELS_DICT,
                        local_port=local_kibana_port,
                        remote_port=execution.emulation_env_config.elk_config.kibana_port,
                        remote_ip=execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip,
                        emulation=execution.emulation_name, execution_id=execution.ip_first_octet)
                except Exception:
                    local_kibana_port = local_kibana_port + 100
                    EmulationEnvController.create_ssh_tunnel(
                        tunnels_dict=cluster_constants.KIBANA_TUNNELS.KIBANA_TUNNELS_DICT,
                        local_port=local_kibana_port,
                        remote_port=execution.emulation_env_config.elk_config.kibana_port,
                        remote_ip=execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip,
                        emulation=execution.emulation_name, execution_id=execution.ip_first_octet)
            else:
                tunnel_thread_dict = cluster_constants.KIBANA_TUNNELS.KIBANA_TUNNELS_DICT[
                    execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip]
                try:
                    response = get(f'{constants.HTTP.HTTP_PROTOCOL_PREFIX}{constants.COMMON.LOCALHOST}:'
                                   f'{local_kibana_port}', timeout=constants.HTTP.DEFAULT_TIMEOUT)
                    if response.status_code != constants.HTTPS.OK_STATUS_CODE:
                        tunnel_thread_dict[cluster_constants.KIBANA_TUNNELS.THREAD_PROPERTY].shutdown()
                        del cluster_constants.KIBANA_TUNNELS.KIBANA_TUNNELS_DICT[
                            execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip]
                        EmulationEnvController.create_ssh_tunnel(
                            tunnels_dict=cluster_constants.KIBANA_TUNNELS.KIBANA_TUNNELS_DICT,
                            local_port=local_kibana_port,
                            remote_port=execution.emulation_env_config.elk_config.kibana_port,
                            remote_ip=execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip,
                            emulation=execution.emulation_name, execution_id=execution.ip_first_octet)
                except Exception:
                    tunnel_thread_dict[cluster_constants.KIBANA_TUNNELS.THREAD_PROPERTY].shutdown()
                    if execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip in \
                            cluster_constants.KIBANA_TUNNELS.KIBANA_TUNNELS_DICT:
                        del cluster_constants.KIBANA_TUNNELS.KIBANA_TUNNELS_DICT[
                            execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip]
                    local_kibana_port = local_kibana_port + 100
                    EmulationEnvController.create_ssh_tunnel(
                        tunnels_dict=cluster_constants.KIBANA_TUNNELS.KIBANA_TUNNELS_DICT,
                        local_port=local_kibana_port, remote_port=execution.emulation_env_config.elk_config.kibana_port,
                        remote_ip=execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip,
                        emulation=execution.emulation_name, execution_id=execution.ip_first_octet)
            return int(local_kibana_port)
        except Exception as e:
            logger.warning(f"There was an exception creating the Kibana tunnel: {str(e)}, {repr(e)}")
            return -1

    @staticmethod
    def remove_kibana_tunnel(execution: EmulationExecution) -> None:
        """
        Utility function for removing the kibana tunnel of a given execution

        :param execution: the execution to remove the tunnel for
        :return: None
        """
        if execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip in \
                cluster_constants.KIBANA_TUNNELS.KIBANA_TUNNELS_DICT:
            tunnel_thread_dict = cluster_constants.KIBANA_TUNNELS.KIBANA_TUNNELS_DICT[
                execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip]
            tunnel_thread_dict[cluster_constants.KIBANA_TUNNELS.THREAD_PROPERTY].shutdown()
            del cluster_constants.KIBANA_TUNNELS.KIBANA_TUNNELS_DICT[
                execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip]

    @staticmethod
    def create_ryu_tunnel(execution: EmulationExecution, logger: logging.Logger) -> int:
        """
        Utility function for creating a Ryu tunnel

        :param execution: the execution to create the tunnel for
        :param logger: the logger to use for logging
        :return: the port of the tunnel
        """
        try:
            local_ryu_port = cluster_constants.RYU_TUNNELS.RYU_TUNNEL_BASE_PORT + execution.ip_first_octet
            if execution.emulation_env_config.sdn_controller_config is not None:
                if execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip \
                        not in cluster_constants.RYU_TUNNELS.RYU_TUNNELS_DICT:
                    try:
                        EmulationEnvController.create_ssh_tunnel(
                            tunnels_dict=cluster_constants.RYU_TUNNELS.RYU_TUNNELS_DICT,
                            local_port=local_ryu_port,
                            remote_port=execution.emulation_env_config.sdn_controller_config.controller_web_api_port,
                            remote_ip=(
                                execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip),
                            emulation=execution.emulation_name, execution_id=execution.ip_first_octet)
                    except Exception:
                        local_ryu_port = local_ryu_port + 100
                        EmulationEnvController.create_ssh_tunnel(
                            tunnels_dict=cluster_constants.RYU_TUNNELS.RYU_TUNNELS_DICT,
                            local_port=local_ryu_port,
                            remote_port=execution.emulation_env_config.sdn_controller_config.controller_web_api_port,
                            remote_ip=(
                                execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip),
                            emulation=execution.emulation_name, execution_id=execution.ip_first_octet)
                else:
                    tunnel_thread_dict = cluster_constants.RYU_TUNNELS.RYU_TUNNELS_DICT[
                        execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip]
                    try:
                        response = get(f'{constants.HTTP.HTTP_PROTOCOL_PREFIX}{constants.COMMON.LOCALHOST}:'
                                       f'{local_ryu_port}', timeout=constants.HTTP.DEFAULT_TIMEOUT)
                        if response.status_code != constants.HTTPS.OK_STATUS_CODE:
                            tunnel_thread_dict[cluster_constants.RYU_TUNNELS.THREAD_PROPERTY].shutdown()
                            del cluster_constants.RYU_TUNNELS.RYU_TUNNELS_DICT[
                                execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip]
                            EmulationEnvController.create_ssh_tunnel(
                                tunnels_dict=cluster_constants.RYU_TUNNELS.RYU_TUNNELS_DICT,
                                local_port=local_ryu_port,
                                remote_port=(
                                    execution.emulation_env_config.sdn_controller_config.controller_web_api_port),
                                remote_ip=(
                                    execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip),
                                emulation=execution.emulation_name, execution_id=execution.ip_first_octet)
                    except Exception:
                        tunnel_thread_dict[cluster_constants.RYU_TUNNELS.THREAD_PROPERTY].shutdown()
                        if execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip in \
                                cluster_constants.RYU_TUNNELS.RYU_TUNNELS_DICT:
                            del cluster_constants.RYU_TUNNELS.RYU_TUNNELS_DICT[
                                execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip]
                        local_ryu_port = local_ryu_port + 100
                        EmulationEnvController.create_ssh_tunnel(
                            tunnels_dict=cluster_constants.RYU_TUNNELS.RYU_TUNNELS_DICT,
                            local_port=local_ryu_port,
                            remote_port=execution.emulation_env_config.sdn_controller_config.controller_web_api_port,
                            remote_ip=(
                                execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip),
                            emulation=execution.emulation_name, execution_id=execution.ip_first_octet)
            return int(local_ryu_port)
        except Exception as e:
            logger.warning(
                f"There was an exception creating the Ryu tunnel: {str(e)}, {repr(e)}")
            return -1

    @staticmethod
    def remove_ryu_tunnel(execution: EmulationExecution) -> None:
        """
        Utility function for removing a Ryu tunnel for a given execution

        :param execution: the execution to remove the tunnel for
        :return: None
        """
        if execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip \
                in cluster_constants.RYU_TUNNELS.RYU_TUNNELS_DICT:
            tunnel_thread_dict = cluster_constants.RYU_TUNNELS.RYU_TUNNELS_DICT[
                execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip]
            tunnel_thread_dict[cluster_constants.RYU_TUNNELS.THREAD_PROPERTY].shutdown()
            del cluster_constants.RYU_TUNNELS.RYU_TUNNELS_DICT[
                execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip]

    @staticmethod
    def create_kibana_tunnels_dto_from_dict(dict: Dict[str, Any]) -> cluster_manager_pb2.KibanaTunnelsDTO:
        """
        Utility function for creating a kibana tunnels DTO from a dict with Kibana tunnels

        :param dict: the dict with the tunnels
        :return: the DTO
        """
        kibana_tunnels = []
        for k, v in dict.items():
            kibana_tunnels.append(cluster_manager_pb2.KibanaTunnelDTO(
                ip=k, port=v[constants.GENERAL.PORT_PROPERTY], emulation=v[constants.GENERAL.EMULATION_PROPERTY],
                ipFirstOctet=v[constants.GENERAL.EXECUTION_ID_PROPERTY]
            ))
        return cluster_manager_pb2.KibanaTunnelsDTO(tunnels=kibana_tunnels)

    @staticmethod
    def create_ryu_tunnels_dto_from_dict(dict: Dict[str, Any]) -> cluster_manager_pb2.RyuTunnelsDTO:
        """
        Utility function for creating a ryu tunnels DTO from a dict with Ryu tunnels

        :param dict: the dict with the tunnels
        :return: the DTO
        """
        ryu_tunnels = []
        for k, v in dict.items():
            ryu_tunnels.append(cluster_manager_pb2.RyuTunnelDTO(
                ip=k, port=v[constants.GENERAL.PORT_PROPERTY], emulation=v[constants.GENERAL.EMULATION_PROPERTY],
                ipFirstOctet=v[constants.GENERAL.EXECUTION_ID_PROPERTY]
            ))
        return cluster_manager_pb2.RyuTunnelsDTO(tunnels=ryu_tunnels)

    @staticmethod
    def merge_execution_infos(execution_infos: List[cluster_manager_pb2.ExecutionInfoDTO]) -> EmulationExecutionInfo:
        """
        Function that merges a list of execution infos into one

        :param execution_infos: the list of execution infos to merge
        :return: the merged info
        """
        assert len(execution_infos) > 0
        emulation_name = execution_infos[0].emulationName
        execution_id = execution_infos[0].executionId
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation_name)
        snort_ids_managers_info = []
        ossec_ids_managers_info = []
        kafka_managers_info = []
        host_managers_info = []
        client_managers_info = []
        docker_stats_managers_info = []
        running_containers = []
        running_container_names = []
        stopped_containers = []
        traffic_managers_info = []
        active_networks = []
        active_network_names = []
        inactive_networks = []
        elk_managers_info = []
        ryu_managers_info = []
        for exec_info in execution_infos:
            snort_ids_managers_info.append(ClusterManagerUtil.convert_snort_info_dto_reverse(
                exec_info.snortIdsManagersInfo))
            ossec_ids_managers_info.append(ClusterManagerUtil.convert_ossec_info_dto_reverse(
                exec_info.ossecIdsManagersInfo))
            kafka_managers_info.append(ClusterManagerUtil.convert_kafka_info_dto_reverse(
                exec_info.kafkaManagersInfo))
            host_managers_info.append(ClusterManagerUtil.convert_host_info_dto_reverse(
                exec_info.hostManagersInfo))
            client_managers_info.append(ClusterManagerUtil.convert_client_info_dto_reverse(
                exec_info.clientManagersInfo))
            docker_stats_managers_info.append(ClusterManagerUtil.convert_docker_info_dto_reverse(
                exec_info.dockerStatsManagersInfo))
            for running_c in exec_info.runningContainers.runningContainers:
                container_dto = execution.emulation_env_config.containers_config.get_container_from_ip(ip=running_c.ip)
                if container_dto is not None:
                    running_containers.append(container_dto)
                    running_container_names.append(container_dto.name)
                elif running_c.ip in execution.emulation_env_config.kafka_config.container.get_ips() or \
                        running_c.ip == execution.emulation_env_config.kafka_config.container.docker_gw_bridge_ip:
                    running_containers.append(execution.emulation_env_config.kafka_config.container)
                    running_container_names.append(execution.emulation_env_config.kafka_config.container.name)
                elif running_c.ip in execution.emulation_env_config.elk_config.container.get_ips() or \
                        running_c.ip == execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip:
                    running_containers.append(execution.emulation_env_config.elk_config.container)
                    running_container_names.append(execution.emulation_env_config.elk_config.container.name)
                elif execution.emulation_env_config.sdn_controller_config is not None and \
                        (running_c.ip in execution.emulation_env_config.sdn_controller_config.container.get_ips() or
                         running_c.ip ==
                         execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip):
                    running_containers.append(execution.emulation_env_config.sdn_controller_config.container)
                    running_container_names.append(execution.emulation_env_config.sdn_controller_config.container.name)
            for stopped_c in exec_info.stoppedContainers.stoppedContainers:
                container_dto = execution.emulation_env_config.containers_config.get_container_from_ip(ip=stopped_c.ip)
                if container_dto is not None:
                    stopped_containers.append(container_dto)
                elif stopped_c.ip in execution.emulation_env_config.kafka_config.container.get_ips() or \
                        stopped_c.ip == execution.emulation_env_config.kafka_config.container.docker_gw_bridge_ip:
                    stopped_containers.append(execution.emulation_env_config.kafka_config.container)
                elif stopped_c.ip in execution.emulation_env_config.elk_config.container.get_ips() or \
                        stopped_c.ip == execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip:
                    stopped_containers.append(execution.emulation_env_config.elk_config.container)
                elif execution.emulation_env_config.sdn_controller_config is not None and \
                        (stopped_c.ip in execution.emulation_env_config.sdn_controller_config.container.get_ips() or
                         stopped_c.ip ==
                         execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip):
                    stopped_containers.append(execution.emulation_env_config.sdn_controller_config.container)
            traffic_managers_info.append(ClusterManagerUtil.convert_traffic_info_dto_reverse(
                exec_info.trafficManagersInfoDTO))
            for net in exec_info.activeNetworks.networks:
                if net not in active_network_names:
                    active_network_names.append(net)
                    active_networks.append(execution.emulation_env_config.get_network_by_name(net_name=net))
            elk_managers_info.append(ClusterManagerUtil.convert_elk_info_dto_reverse(exec_info.elkManagersInfoDTO))
            ryu_managers_info.append(ClusterManagerUtil.convert_ryu_info_dto_reverse(exec_info.ryuManagersInfoDTO))

        for network in execution.emulation_env_config.containers_config.networks:
            if network.name not in active_network_names:
                inactive_networks.append(network)

        stopped_containers = list(filter(lambda x: x.name not in running_container_names, stopped_containers))
        merged_snort_ids_managers_info = snort_ids_managers_info[0]
        for snort_ids_manager_info in snort_ids_managers_info[1:]:
            merged_snort_ids_managers_info.ips = (list(merged_snort_ids_managers_info.ips) +
                                                  list(snort_ids_manager_info.ips))
            merged_snort_ids_managers_info.ports = (list(merged_snort_ids_managers_info.ports) +
                                                    list(snort_ids_manager_info.ports))
            merged_snort_ids_managers_info.snort_ids_managers_running = \
                list(merged_snort_ids_managers_info.snort_ids_managers_running) + \
                list(snort_ids_manager_info.snort_ids_managers_running)
            merged_snort_ids_managers_info.snort_ids_managers_statuses = \
                (list(merged_snort_ids_managers_info.snort_ids_managers_statuses) +
                 list(snort_ids_manager_info.snort_ids_managers_statuses))

        merged_ossec_ids_managers_info = ossec_ids_managers_info[0]
        for ossec_ids_manager_info in ossec_ids_managers_info[1:]:
            merged_ossec_ids_managers_info.ips = (list(merged_ossec_ids_managers_info.ips) +
                                                  list(ossec_ids_manager_info.ips))
            merged_ossec_ids_managers_info.ports = (list(merged_ossec_ids_managers_info.ports) +
                                                    list(ossec_ids_manager_info.ports))
            merged_ossec_ids_managers_info.ossec_ids_managers_running = \
                list(merged_ossec_ids_managers_info.ossec_ids_managers_running) + \
                list(ossec_ids_manager_info.ossec_ids_managers_running)
            merged_ossec_ids_managers_info.ossec_ids_managers_statuses = \
                list(merged_ossec_ids_managers_info.ossec_ids_managers_statuses) + \
                list(ossec_ids_manager_info.ossec_ids_managers_statuses)

        merged_kafka_managers_info = kafka_managers_info[0]
        for kafka_manager_info in kafka_managers_info[1:]:
            merged_kafka_managers_info.ips = list(merged_kafka_managers_info.ips) + list(kafka_manager_info.ips)
            merged_kafka_managers_info.ports = list(merged_kafka_managers_info.ports) + list(kafka_manager_info.ports)
            merged_kafka_managers_info.kafka_managers_running = \
                list(merged_kafka_managers_info.kafka_managers_running) + \
                list(kafka_manager_info.kafka_managers_running)
            merged_kafka_managers_info.kafka_managers_statuses = \
                list(merged_kafka_managers_info.kafka_managers_statuses) + \
                list(kafka_manager_info.kafka_managers_statuses)

        merged_host_managers_info = host_managers_info[0]
        for host_manager_info in host_managers_info[1:]:
            merged_host_managers_info.ips = list(merged_host_managers_info.ips) + list(host_manager_info.ips)
            merged_host_managers_info.ports = list(merged_host_managers_info.ports) + list(host_manager_info.ports)
            merged_host_managers_info.host_managers_running = (list(merged_host_managers_info.host_managers_running) +
                                                               list(host_manager_info.host_managers_running))
            merged_host_managers_info.host_managers_statuses = \
                (list(merged_host_managers_info.host_managers_statuses) +
                 list(host_manager_info.host_managers_statuses))

        merged_client_managers_info = client_managers_info[0]
        for client_manager_info in client_managers_info[1:]:
            merged_client_managers_info.ips = list(merged_client_managers_info.ips) + list(client_manager_info.ips)
            merged_client_managers_info.ports = (list(merged_client_managers_info.ports) +
                                                 list(client_manager_info.ports))
            merged_client_managers_info.client_managers_running = \
                list(merged_client_managers_info.client_managers_running) + \
                list(client_manager_info.client_managers_running)
            merged_client_managers_info.client_managers_statuses = \
                list(merged_client_managers_info.client_managers_statuses) + \
                list(client_manager_info.client_managers_statuses)

        merged_docker_stats_managers_info = docker_stats_managers_info[0]
        for docker_stats_manager_info in docker_stats_managers_info[1:]:
            merged_docker_stats_managers_info.ips = (list(merged_docker_stats_managers_info.ips) +
                                                     list(docker_stats_manager_info.ips))
            merged_docker_stats_managers_info.ports = (list(merged_docker_stats_managers_info.ports) +
                                                       list(docker_stats_manager_info.ports))
            merged_docker_stats_managers_info.docker_stats_managers_running = \
                list(merged_docker_stats_managers_info.docker_stats_managers_running) + \
                list(docker_stats_manager_info.docker_stats_managers_running)
            merged_docker_stats_managers_info.docker_stats_managers_statuses = \
                list(merged_docker_stats_managers_info.docker_stats_managers_statuses) + \
                list(docker_stats_manager_info.docker_stats_managers_statuses)

        merged_traffic_managers_info = traffic_managers_info[0]
        for traffic_manager_info in traffic_managers_info[1:]:
            merged_traffic_managers_info.ips = list(merged_traffic_managers_info.ips) + list(traffic_manager_info.ips)
            merged_traffic_managers_info.ports = (list(merged_traffic_managers_info.ports)
                                                  + list(traffic_manager_info.ports))
            merged_traffic_managers_info.traffic_managers_running = \
                list(merged_traffic_managers_info.traffic_managers_running) + \
                list(traffic_manager_info.traffic_managers_running)
            merged_traffic_managers_info.traffic_managers_statuses = \
                list(merged_traffic_managers_info.traffic_managers_statuses) + \
                list(traffic_manager_info.traffic_managers_statuses)

        merged_elk_managers_info = elk_managers_info[0]
        for elk_manager_info in elk_managers_info[1:]:
            merged_elk_managers_info.ips = list(merged_elk_managers_info.ips) + list(elk_manager_info.ips)
            merged_elk_managers_info.ports = list(merged_elk_managers_info.ports) + list(elk_manager_info.ports)
            merged_elk_managers_info.elk_managers_running = \
                list(merged_elk_managers_info.elk_managers_running) + \
                list(elk_manager_info.elk_managers_running)
            merged_elk_managers_info.elk_managers_statuses = \
                list(merged_elk_managers_info.elk_managers_statuses) + \
                list(elk_manager_info.elk_managers_statuses)

        merged_ryu_managers_info = ryu_managers_info[0]
        for ryu_manager_info in ryu_managers_info[1:]:
            merged_ryu_managers_info.ips = list(merged_ryu_managers_info.ips) + list(ryu_manager_info.ips)
            merged_ryu_managers_info.ports = list(merged_ryu_managers_info.ports) + list(ryu_manager_info.ports)
            merged_ryu_managers_info.ryu_managers_running = \
                list(merged_ryu_managers_info.ryu_managers_running) + \
                list(ryu_manager_info.ryu_managers_running)
            merged_ryu_managers_info.ryu_managers_statuses = \
                list(merged_ryu_managers_info.ryu_managers_statuses) + \
                list(ryu_manager_info.ryu_managers_statuses)

        merged_execution_info = EmulationExecutionInfo(
            emulation_name=emulation_name, execution_id=execution_id,
            snort_ids_managers_info=merged_snort_ids_managers_info,
            ossec_ids_managers_info=merged_ossec_ids_managers_info,
            kafka_managers_info=merged_kafka_managers_info,
            host_managers_info=merged_host_managers_info, client_managers_info=merged_client_managers_info,
            docker_stats_managers_info=merged_docker_stats_managers_info, running_containers=running_containers,
            stopped_containers=stopped_containers, active_networks=active_networks, inactive_networks=inactive_networks,
            elk_managers_info=merged_elk_managers_info, ryu_managers_info=merged_ryu_managers_info,
            traffic_managers_info=merged_traffic_managers_info
        )
        return merged_execution_info

    @staticmethod
    def get_container_config(execution: EmulationExecution, ip: str) -> Union[NodeContainerConfig, None]:
        """
        Utility method for checking if a given IP matches som container IP in a given execution and then returns
        the corresponding configuration

        :param execution: the execution to check
        :param ip: the ip to check
        :return: the IP if it matches, otherwise None
        """
        node_container_config = execution.emulation_env_config.containers_config.get_container_from_ip(ip=ip)
        if node_container_config is not None and node_container_config.physical_host_ip == GeneralUtil.get_host_ip():
            return node_container_config
        elif (ip in execution.emulation_env_config.kafka_config.container.get_ips() or
              ip == execution.emulation_env_config.kafka_config.container.docker_gw_bridge_ip) \
                and execution.emulation_env_config.kafka_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            return execution.emulation_env_config.kafka_config.container
        elif (ip in execution.emulation_env_config.elk_config.container.get_ips() or
              ip == execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip) \
                and execution.emulation_env_config.elk_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            return execution.emulation_env_config.elk_config.container
        elif execution.emulation_env_config.sdn_controller_config is not None and \
                (ip in execution.emulation_env_config.sdn_controller_config.container.get_ips() or
                 ip == execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip) \
                and execution.emulation_env_config.sdn_controller_config.container.physical_host_ip == \
                GeneralUtil.get_host_ip():
            return execution.emulation_env_config.sdn_controller_config.container
        return None

    @staticmethod
    def get_logs(execution: EmulationExecution, ip: str, path: str) -> cluster_manager_pb2.LogsDTO:
        """
        Utility method for getting the logs of a specific container in a specific execution and with a specific
        path

        :param execution: the execution
        :param ip: the IP of the container
        :return: the parsed logs
        """
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=execution.emulation_env_config, ip=ip)
        sftp_client = execution.emulation_env_config.get_connection(ip=ip).open_sftp()
        remote_file = sftp_client.open(path)
        try:
            data = remote_file.read(constants.SSH.MAX_FILE_READ_BYTES)
            if isinstance(data, bytes):
                data = data.decode()
                data = data.split("\n")
                data = data[-100:]
            else:
                raise Exception("Could not read remote file")
        finally:
            remote_file.close()
        return cluster_manager_pb2.LogsDTO(logs=data)

    @staticmethod
    def tail(f, window=1) -> str:
        """
        Returns the last `window` lines of file `f` as a list of bytes.

        :param f: the file object
        :param window: the window size
        :return: the parsed lines
        """
        if window == 0:
            return ''
        BUFSIZE = 1024
        f.seek(0, 2)
        end = f.tell()
        nlines = window + 1
        data = []
        while nlines > 0 and end > 0:
            i = max(0, end - BUFSIZE)
            nread = min(end, BUFSIZE)

            f.seek(i)
            chunk = f.read(nread)
            data.append(chunk)
            nlines -= chunk.count("\n")
            end -= nread
        return '\n'.join(''.join(reversed(data)).splitlines()[-window:])

    @staticmethod
    def convert_client_population_metrics_dto(client_population_metrics: ClientPopulationMetrics) -> \
            cluster_manager_pb2.ClientPopulationMetricsDTO:
        """
        Converts a ClientPopulationMetrics object to a ClientPopulationMetricsDTO

        :param client_population_metrics: the object to convert
        :return: the converted objected
        """
        if client_population_metrics is None:
            return ClusterManagerUtil.get_empty_client_population_metrics_dto()
        else:
            return cluster_manager_pb2.ClientPopulationMetricsDTO(
                ip=client_population_metrics.ip, ts=client_population_metrics.ts,
                num_clients=client_population_metrics.num_clients, rate=client_population_metrics.rate,
                service_time=client_population_metrics.service_time)

    @staticmethod
    def convert_client_population_metrics_dto_reverse(
            client_population_metrics_dto: Union[None, cluster_manager_pb2.ClientPopulationMetricsDTO]) \
            -> ClientPopulationMetrics:
        """
        Converts a ClientPopulationMetricsDTO to a ClientPopulationMetrics

        :param client_population_metrics_dto: the DTO to convert
        :return: the converted DTO
        """
        if client_population_metrics_dto is None:
            return ClusterManagerUtil.convert_client_population_metrics_dto_reverse(
                ClusterManagerUtil.get_empty_client_population_metrics_dto())
        else:
            return ClientPopulationMetrics(
                ip=client_population_metrics_dto.ip, ts=client_population_metrics_dto.ts,
                num_clients=client_population_metrics_dto.num_clients, rate=client_population_metrics_dto.rate,
                service_time=client_population_metrics_dto.service_time
            )

    @staticmethod
    def get_empty_client_population_metrics_dto() -> cluster_manager_pb2.ClientPopulationMetricsDTO:
        """
        Gets an empty ClientPopulationMetricsDTO

        :return: an empty ClientPopulationMetricsDTO
        """
        return cluster_manager_pb2.ClientPopulationMetricsDTO(ip="", ts=-1., num_clients=0, rate=0., service_time=0.)

    @staticmethod
    def client_population_metrics_dto_to_dict(
            client_population_metrics_dto: cluster_manager_pb2.ClientPopulationMetricsDTO) -> Dict[str, Any]:
        """
        Converts a ClientPopulationMetricsDTO to a dict

        :param client_population_metrics_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ip"] = client_population_metrics_dto.ip
        d["ts"] = client_population_metrics_dto.ts
        d["num_clients"] = client_population_metrics_dto.num_clients
        d["rate"] = client_population_metrics_dto.rate
        d["service_time"] = client_population_metrics_dto.service_time
        return d

    @staticmethod
    def convert_docker_stats_dto(docker_stats: Union[None, DockerStats]) -> cluster_manager_pb2.DockerStatsDTO:
        """
        Converts a DockerStats object to a DockerStatsDTO

        :param docker_stats: the object to convert
        :return: the converted objected
        """
        if docker_stats is None:
            return ClusterManagerUtil.get_empty_docker_stats_dto()
        else:
            return cluster_manager_pb2.DockerStatsDTO(
                pids=docker_stats.pids, timestamp=docker_stats.timestamp, cpu_percent=docker_stats.cpu_percent,
                mem_current=docker_stats.mem_current, mem_total=docker_stats.mem_total,
                mem_percent=docker_stats.mem_percent, blk_read=docker_stats.blk_read, blk_write=docker_stats.blk_write,
                net_rx=docker_stats.net_rx, net_tx=docker_stats.net_tx, container_name=docker_stats.container_name,
                ip=docker_stats.ip, ts=docker_stats.ts)

    @staticmethod
    def convert_docker_stats_dto_reverse(docker_stats_dto: Union[None, cluster_manager_pb2.DockerStatsDTO]) \
            -> DockerStats:
        """
        Converts a DockerStatsDTO to a DockerStats

        :param docker_stats_dto: the DTO to convert
        :return: the converted DTO
        """
        if docker_stats_dto is None:
            return ClusterManagerUtil.convert_docker_stats_dto_reverse(ClusterManagerUtil.get_empty_docker_stats_dto())
        else:
            return DockerStats(
                pids=docker_stats_dto.pids, timestamp=docker_stats_dto.timestamp,
                cpu_percent=docker_stats_dto.cpu_percent,
                mem_current=docker_stats_dto.mem_current, mem_total=docker_stats_dto.mem_total,
                mem_percent=docker_stats_dto.mem_percent, blk_read=docker_stats_dto.blk_read,
                blk_write=docker_stats_dto.blk_write,
                net_rx=docker_stats_dto.net_rx, net_tx=docker_stats_dto.net_tx,
                container_name=docker_stats_dto.container_name,
                ip=docker_stats_dto.ip, ts=docker_stats_dto.ts)

    @staticmethod
    def get_empty_docker_stats_dto() -> cluster_manager_pb2.DockerStatsDTO:
        """
        :return: an empty ClientPopulationMetricsDTO
        """
        return cluster_manager_pb2.DockerStatsDTO(
            pids=0.0, timestamp="", cpu_percent=0.0, mem_current=0.0, mem_total=0.0, mem_percent=0.0,
            blk_read=0.0, blk_write=0.0, net_rx=0.0, net_tx=0.0, container_name="", ip="", ts=0.0)

    @staticmethod
    def docker_stats_dto_to_dict(docker_stats_dto: cluster_manager_pb2.DockerStatsDTO) -> Dict[str, Any]:
        """
        Converts a DockerStatsDTO to a dict

        :param docker_stats_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["pids"] = docker_stats_dto.pids
        d["timestamp"] = docker_stats_dto.timestamp
        d["cpu_percent"] = docker_stats_dto.cpu_percent
        d["mem_current"] = docker_stats_dto.mem_current
        d["mem_total"] = docker_stats_dto.mem_total
        d["mem_percent"] = docker_stats_dto.mem_percent
        d["blk_read"] = docker_stats_dto.blk_read
        d["blk_write"] = docker_stats_dto.blk_write
        d["net_rx"] = docker_stats_dto.net_rx
        d["net_tx"] = docker_stats_dto.net_tx
        d["container_name"] = docker_stats_dto.container_name
        d["ip"] = docker_stats_dto.ip
        d["ts"] = docker_stats_dto.ts
        return d

    @staticmethod
    def convert_host_metrics_dto(host_metrics: Union[None, HostMetrics]) -> cluster_manager_pb2.HostMetricsDataDTO:
        """
        Converts a HostMetrics object to a HostMetricsDataDTO

        :param host_metrics: the object to convert
        :return: the converted objected
        """
        if host_metrics is None:
            return ClusterManagerUtil.get_empty_host_metrics_dto()
        else:
            return cluster_manager_pb2.HostMetricsDataDTO(
                num_logged_in_users=host_metrics.num_logged_in_users,
                num_failed_login_attempts=host_metrics.num_failed_login_attempts,
                num_open_connections=host_metrics.num_open_connections,
                num_login_events=host_metrics.num_login_events, num_processes=host_metrics.num_processes,
                num_users=host_metrics.num_users, ip=host_metrics.ip, ts=host_metrics.ts)

    @staticmethod
    def convert_host_metrics_dto_reverse(host_metrics_dto: Union[None, cluster_manager_pb2.HostMetricsDataDTO]) \
            -> HostMetrics:
        """
        Converts a HostMetricsDataDTO to a HostMetrics

        :param host_metrics_dto: the DTO to convert
        :return: the converted DTO
        """
        if host_metrics_dto is None:
            return ClusterManagerUtil.convert_host_metrics_dto_reverse(ClusterManagerUtil.get_empty_host_metrics_dto())
        else:
            return HostMetrics(
                num_logged_in_users=host_metrics_dto.num_logged_in_users,
                num_failed_login_attempts=host_metrics_dto.num_failed_login_attempts,
                num_open_connections=host_metrics_dto.num_open_connections,
                num_login_events=host_metrics_dto.num_login_events, num_processes=host_metrics_dto.num_processes,
                num_users=host_metrics_dto.num_users, ip=host_metrics_dto.ip, ts=host_metrics_dto.ts)

    @staticmethod
    def get_empty_host_metrics_dto() -> cluster_manager_pb2.HostMetricsDataDTO:
        """
        Gets an empty HostMetricsDataDTO

        :return: an empty HostMetricsDataDTO
        """
        return cluster_manager_pb2.HostMetricsDataDTO(num_logged_in_users=0, num_failed_login_attempts=0,
                                                      num_open_connections=0, num_login_events=0, num_processes=0,
                                                      num_users=0, ip="", ts=0.0)

    @staticmethod
    def host_metrics_dto_to_dict(host_metrics_dto: cluster_manager_pb2.HostMetricsDataDTO) -> Dict[str, Any]:
        """
        Converts a HostMetricsDataDTO to a dict

        :param host_metrics_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["num_logged_in_users"] = host_metrics_dto.num_logged_in_users
        d["num_failed_login_attempts"] = host_metrics_dto.num_failed_login_attempts
        d["num_open_connections"] = host_metrics_dto.num_open_connections
        d["num_login_events"] = host_metrics_dto.num_login_events
        d["num_processes"] = host_metrics_dto.num_processes
        d["num_users"] = host_metrics_dto.num_users
        d["ts"] = host_metrics_dto.ts
        d["ip"] = host_metrics_dto.ip
        return d

    @staticmethod
    def convert_emulation_defender_action_dto(emulation_defender_action: Union[None, EmulationDefenderAction]) \
            -> cluster_manager_pb2.EmulationDefenderActionDTO:
        """
        Converts a EmulationDefenderAction object to a EmulationDefenderActionDTO

        :param emulation_defender_action: the object to convert
        :return: the converted objected
        """
        if emulation_defender_action is None:
            return ClusterManagerUtil.get_empty_emulation_defender_action_dto()
        else:
            return cluster_manager_pb2.EmulationDefenderActionDTO(
                id=emulation_defender_action.id, name=emulation_defender_action.name,
                cmds=emulation_defender_action.cmds, type=emulation_defender_action.type,
                descr=emulation_defender_action.descr, index=emulation_defender_action.index,
                ips=emulation_defender_action.ips, action_outcome=emulation_defender_action.action_outcome,
                alt_cmds=emulation_defender_action.alt_cmds, execution_time=emulation_defender_action.execution_time,
                ts=emulation_defender_action.ts)

    @staticmethod
    def convert_emulation_defender_action_dto_reverse(
            emulation_defender_action_dto: Union[None, cluster_manager_pb2.EmulationDefenderActionDTO]) \
            -> EmulationDefenderAction:
        """
        Converts a EmulationDefenderActionDTO to an EmulationDefenderAction

        :param emulation_defender_action_dto: the DTO to convert
        :return: the converted DTO
        """
        if emulation_defender_action_dto is None:
            return ClusterManagerUtil.convert_emulation_defender_action_dto_reverse(
                ClusterManagerUtil.get_empty_emulation_defender_action_dto())
        else:
            return EmulationDefenderAction(
                id=emulation_defender_action_dto.id, name=emulation_defender_action_dto.name,
                cmds=emulation_defender_action_dto.cmds, type=emulation_defender_action_dto.type,
                descr=emulation_defender_action_dto.descr, index=emulation_defender_action_dto.index,
                ips=emulation_defender_action_dto.ips, action_outcome=emulation_defender_action_dto.action_outcome,
                alt_cmds=emulation_defender_action_dto.alt_cmds,
                execution_time=emulation_defender_action_dto.execution_time,
                ts=emulation_defender_action_dto.ts)

    @staticmethod
    def get_empty_emulation_defender_action_dto() -> cluster_manager_pb2.EmulationDefenderActionDTO:
        """
        Gets an empty EmulationDefenderActionDTO

        :return: an empty EmulationDefenderActionDTO
        """
        return cluster_manager_pb2.EmulationDefenderActionDTO(id=-1, name="", cmds=[], type=-1, descr="", ips=[],
                                                              index=-1, action_outcome=-1, alt_cmds=[],
                                                              execution_time=-1, ts=-1)

    @staticmethod
    def emulation_defender_action_dto_to_dict(
            emulation_defender_action_dto: cluster_manager_pb2.EmulationDefenderActionDTO) -> Dict[str, Any]:
        """
        Converts a EmulationDefenderActionDTO to a dict

        :param emulation_defender_action_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["id"] = emulation_defender_action_dto.id
        d["name"] = emulation_defender_action_dto.name
        d["cmds"] = emulation_defender_action_dto.cmds
        d["type"] = emulation_defender_action_dto.type
        d["descr"] = emulation_defender_action_dto.descr
        d["ips"] = emulation_defender_action_dto.ips
        d["index"] = emulation_defender_action_dto.index
        d["action_outcome"] = emulation_defender_action_dto.action_outcome
        d["alt_cmds"] = emulation_defender_action_dto.alt_cmds
        d["execution_time"] = emulation_defender_action_dto.execution_time
        d["ts"] = emulation_defender_action_dto.ts
        return d

    @staticmethod
    def convert_emulation_attacker_action_dto(emulation_attacker_action: Union[None, EmulationAttackerAction]) \
            -> cluster_manager_pb2.EmulationAttackerActionDTO:
        """
        Converts a EmulationAttackerAction object to a EmulationAttackerActionDTO

        :param emulation_attacker_action: the object to convert
        :return: the converted objected
        """
        if emulation_attacker_action is None:
            return ClusterManagerUtil.get_empty_emulation_attacker_action_dto()
        else:
            return cluster_manager_pb2.EmulationAttackerActionDTO(
                id=emulation_attacker_action.id, name=emulation_attacker_action.name,
                cmds=emulation_attacker_action.cmds, type=emulation_attacker_action.type,
                descr=emulation_attacker_action.descr, index=emulation_attacker_action.index,
                ips=emulation_attacker_action.ips, action_outcome=emulation_attacker_action.action_outcome,
                alt_cmds=emulation_attacker_action.alt_cmds, execution_time=emulation_attacker_action.execution_time,
                ts=emulation_attacker_action.ts, backdoor=emulation_attacker_action.backdoor,
                vulnerability=emulation_attacker_action.vulnerability
            )

    @staticmethod
    def convert_emulation_attacker_action_dto_reverse(
            emulation_attacker_action_dto: Union[None, cluster_manager_pb2.EmulationAttackerActionDTO]) \
            -> EmulationAttackerAction:
        """
        Converts a EmulationAttackerActionDTO to an EmulationAttackerAction

        :param emulation_attacker_action_dto: the DTO to convert
        :return: the converted DTO
        """
        if emulation_attacker_action_dto is None:
            return ClusterManagerUtil.convert_emulation_attacker_action_dto_reverse(
                ClusterManagerUtil.get_empty_emulation_attacker_action_dto())
        else:
            return EmulationAttackerAction(
                id=emulation_attacker_action_dto.id, name=emulation_attacker_action_dto.name,
                cmds=emulation_attacker_action_dto.cmds, type=emulation_attacker_action_dto.type,
                descr=emulation_attacker_action_dto.descr, index=emulation_attacker_action_dto.index,
                ips=emulation_attacker_action_dto.ips, action_outcome=emulation_attacker_action_dto.action_outcome,
                alt_cmds=emulation_attacker_action_dto.alt_cmds,
                execution_time=emulation_attacker_action_dto.execution_time,
                ts=emulation_attacker_action_dto.ts, backdoor=emulation_attacker_action_dto.backdoor,
                vulnerability=emulation_attacker_action_dto.vulnerability)

    @staticmethod
    def get_empty_emulation_attacker_action_dto() -> cluster_manager_pb2.EmulationAttackerActionDTO:
        """
        Gets an empty EmulationAttackerActionDTO

        :return: an empty EmulationAttackerActionDTO
        """
        return cluster_manager_pb2.EmulationAttackerActionDTO(id=-1, name="", cmds=[], type=-1, descr="", ips=[],
                                                              index=-1, action_outcome=-1, alt_cmds=[],
                                                              execution_time=-1, ts=-1, backdoor=False,
                                                              vulnerability="")

    @staticmethod
    def emulation_attacker_action_dto_to_dict(
            emulation_attacker_action_dto: cluster_manager_pb2.EmulationAttackerActionDTO) -> Dict[str, Any]:
        """
        Converts a EmulationAttackerActionDTO to a dict

        :param emulation_attacker_action_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["id"] = emulation_attacker_action_dto.id
        d["name"] = emulation_attacker_action_dto.name
        d["cmds"] = emulation_attacker_action_dto.cmds
        d["type"] = emulation_attacker_action_dto.type
        d["descr"] = emulation_attacker_action_dto.descr
        d["ips"] = emulation_attacker_action_dto.ips
        d["index"] = emulation_attacker_action_dto.index
        d["action_outcome"] = emulation_attacker_action_dto.action_outcome
        d["alt_cmds"] = emulation_attacker_action_dto.alt_cmds
        d["execution_time"] = emulation_attacker_action_dto.execution_time
        d["ts"] = emulation_attacker_action_dto.ts
        return d

    @staticmethod
    def convert_snort_ids_alert_counters_dto(snort_ids_alert_counters: Union[None, SnortIdsAlertCounters]) \
            -> cluster_manager_pb2.SnortIdsAlertCountersDTO:
        """
        Converts a SnortIdsAlertCounters object to a SnortIdsAlertCountersDTO

        :param snort_ids_alert_counters: the object to convert
        :return: the converted objected
        """
        if snort_ids_alert_counters is None:
            return ClusterManagerUtil.get_empty_snort_ids_alert_counters_dto()
        else:
            return cluster_manager_pb2.SnortIdsAlertCountersDTO(
                priority_alerts=list(map(lambda x: int(x), snort_ids_alert_counters.priority_alerts)),
                class_alerts=list(map(lambda x: int(x), snort_ids_alert_counters.class_alerts)),
                severe_alerts=int(snort_ids_alert_counters.severe_alerts),
                warning_alerts=int(snort_ids_alert_counters.warning_alerts),
                alerts_weighted_by_priority=snort_ids_alert_counters.alerts_weighted_by_priority,
                ip=snort_ids_alert_counters.ip, ts=snort_ids_alert_counters.ts
            )

    @staticmethod
    def convert_snort_ids_alert_counters_dto_reverse(
            snort_ids_alert_counters_dto: Union[None, cluster_manager_pb2.SnortIdsAlertCountersDTO]) \
            -> SnortIdsAlertCounters:
        """
        Converts a SnortIdsAlertCountersDTO to a SnortIdsAlertCounters

        :param snort_ids_alert_counters_dto: the DTO to convert
        :return: the converted DTO
        """
        if snort_ids_alert_counters_dto is None:
            return ClusterManagerUtil.convert_snort_ids_alert_counters_dto_reverse(
                ClusterManagerUtil.get_empty_snort_ids_alert_counters_dto())
        else:
            dto = SnortIdsAlertCounters()
            dto.priority_alerts = snort_ids_alert_counters_dto.priority_alerts
            dto.class_alerts = snort_ids_alert_counters_dto.class_alerts
            dto.severe_alerts = snort_ids_alert_counters_dto.severe_alerts
            dto.warning_alerts = snort_ids_alert_counters_dto.warning_alerts
            dto.alerts_weighted_by_priority = snort_ids_alert_counters_dto.alerts_weighted_by_priority
            dto.ip = snort_ids_alert_counters_dto.ip
            dto.ts = snort_ids_alert_counters_dto.ts
            return dto

    @staticmethod
    def get_empty_snort_ids_alert_counters_dto() -> cluster_manager_pb2.SnortIdsAlertCountersDTO:
        """
        Gets an empty SnortIdsAlertCountersDTO

        :return: an empty SnortIdsAlertCountersDTO
        """
        return cluster_manager_pb2.SnortIdsAlertCountersDTO(
            priority_alerts=[], class_alerts=[], severe_alerts=0, warning_alerts=0, alerts_weighted_by_priority=0.0,
            ip="", ts=0.0)

    @staticmethod
    def snort_ids_alert_counters_dto_to_dict(
            snort_ids_alert_counters_dto: cluster_manager_pb2.SnortIdsAlertCountersDTO) -> Dict[str, Any]:
        """
        Converts a SnortIdsAlertCountersDTO to a dict

        :param snort_ids_alert_counters_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ip"] = snort_ids_alert_counters_dto.ip
        d["ts"] = snort_ids_alert_counters_dto.ts
        d["class_alerts"] = snort_ids_alert_counters_dto.class_alerts
        d["priority_alerts"] = snort_ids_alert_counters_dto.priority_alerts
        d["warning_alerts"] = snort_ids_alert_counters_dto.warning_alerts
        d["severe_alerts"] = snort_ids_alert_counters_dto.severe_alerts
        d["alerts_weighted_by_priority"] = snort_ids_alert_counters_dto.alerts_weighted_by_priority
        return d

    @staticmethod
    def convert_snort_ids_rule_counters_dto(snort_ids_rule_counters: Union[SnortIdsRuleCounters, None]) \
            -> cluster_manager_pb2.SnortIdsRuleCountersDTO:
        """
        Converts a SnortIdsRuleCounters object to a SnortIdsRuleCountersDTO

        :param snort_ids_rule_counters: the object to convert
        :return: the converted objected
        """
        if snort_ids_rule_counters is None:
            return ClusterManagerUtil.get_empty_snort_ids_rule_counters_dto()
        else:
            rule_ids = list(snort_ids_rule_counters.rule_alerts.keys())
            rule_counters = list(snort_ids_rule_counters.rule_alerts.values())
            return cluster_manager_pb2.SnortIdsRuleCountersDTO(
                rule_ids=rule_ids, rule_alert_counts=rule_counters, ip=snort_ids_rule_counters.ip,
                ts=snort_ids_rule_counters.ts)

    @staticmethod
    def convert_snort_ids_rule_counters_dto_reverse(
            snort_ids_rule_counters_dto: Union[None, cluster_manager_pb2.SnortIdsRuleCountersDTO]) \
            -> SnortIdsRuleCounters:
        """
        Converts a SnortIdsRuleCountersDTO to a SnortIdsRuleCounters

        :param snort_ids_rule_counters_dto: the DTO to convert
        :return: the converted DTO
        """
        if snort_ids_rule_counters_dto is None:
            return ClusterManagerUtil.convert_snort_ids_rule_counters_dto_reverse(
                ClusterManagerUtil.get_empty_snort_ids_rule_counters_dto())
        else:
            dto = SnortIdsRuleCounters()
            rule_alerts = {}
            for i in range(len(snort_ids_rule_counters_dto.rule_ids)):
                rule_alerts[snort_ids_rule_counters_dto.rule_ids[i]] = snort_ids_rule_counters_dto.rule_alert_counts[i]
            dto.rule_alerts = rule_alerts
            dto.ip = snort_ids_rule_counters_dto.ip
            dto.ts = snort_ids_rule_counters_dto.ts
            return dto

    @staticmethod
    def get_empty_snort_ids_rule_counters_dto() -> cluster_manager_pb2.SnortIdsRuleCountersDTO:
        """
        Gets an empty SnortIdsAlertCountersDTO

        :return: an empty SnortIdsAlertCountersDTO
        """
        return cluster_manager_pb2.SnortIdsRuleCountersDTO(ip="", ts=0.0, rule_ids=[], rule_alert_counts=[])

    @staticmethod
    def snort_ids_rule_counters_dto_to_dict(
            snort_ids_rule_counters_dto: cluster_manager_pb2.SnortIdsRuleCountersDTO) -> Dict[str, Any]:
        """
        Converts a SnortIdsRuleCountersDTO to a dict

        :param snort_ids_rule_counters_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ip"] = snort_ids_rule_counters_dto.ip
        d["ts"] = snort_ids_rule_counters_dto.ts
        d["rule_ids"] = list(snort_ids_rule_counters_dto.rule_ids)
        d["rule_alert_counts"] = list(snort_ids_rule_counters_dto.rule_alert_counts)
        return d

    @staticmethod
    def convert_snort_ids_ip_alert_counters_dto(snort_ids_ip_alert_counters: Union[None, SnortIdsIPAlertCounters]) \
            -> cluster_manager_pb2.SnortIdsIpAlertCountersDTO:
        """
        Converts a SnortIdsIPAlertCounters object to a SnortIdsIpAlertCountersDTO

        :param snort_ids_ip_alert_counters: the object to convert
        :return: the converted objected
        """
        if snort_ids_ip_alert_counters is None:
            return ClusterManagerUtil.get_empty_snort_ids_ip_alert_counters_dto()
        else:
            return cluster_manager_pb2.SnortIdsIpAlertCountersDTO(
                priority_alerts=snort_ids_ip_alert_counters.priority_alerts,
                class_alerts=snort_ids_ip_alert_counters.class_alerts,
                severe_alerts=snort_ids_ip_alert_counters.severe_alerts,
                warning_alerts=snort_ids_ip_alert_counters.warning_alerts,
                alerts_weighted_by_priority=snort_ids_ip_alert_counters.alerts_weighted_by_priority,
                ip=snort_ids_ip_alert_counters.ip, ts=snort_ids_ip_alert_counters.ts,
                alert_ip=snort_ids_ip_alert_counters.alert_ip
            )

    @staticmethod
    def convert_snort_ids_ip_alert_counters_dto_reverse(
            snort_ids_ip_alert_counters_dto: Union[None, cluster_manager_pb2.SnortIdsIpAlertCountersDTO]) \
            -> SnortIdsIPAlertCounters:
        """
        Converts a SnortIdsIpAlertCountersDTO to a SnortIdsIPAlertCounters

        :param snort_ids_ip_alert_counters_dto: the DTO to convert
        :return: the converted DTO
        """
        if snort_ids_ip_alert_counters_dto is None:
            return ClusterManagerUtil.convert_snort_ids_ip_alert_counters_dto_reverse(
                ClusterManagerUtil.get_empty_snort_ids_ip_alert_counters_dto())
        else:
            dto = SnortIdsIPAlertCounters()
            dto.priority_alerts = snort_ids_ip_alert_counters_dto.priority_alerts
            dto.class_alerts = snort_ids_ip_alert_counters_dto.class_alerts
            dto.severe_alerts = snort_ids_ip_alert_counters_dto.severe_alerts
            dto.warning_alerts = snort_ids_ip_alert_counters_dto.warning_alerts
            dto.alerts_weighted_by_priority = snort_ids_ip_alert_counters_dto.alerts_weighted_by_priority
            dto.ip = snort_ids_ip_alert_counters_dto.ip
            dto.ts = snort_ids_ip_alert_counters_dto.ts
            dto.alert_ip = snort_ids_ip_alert_counters_dto.alert_ip
            return dto

    @staticmethod
    def get_empty_snort_ids_ip_alert_counters_dto() -> cluster_manager_pb2.SnortIdsIpAlertCountersDTO:
        """
        Gets an empty SnortIdsAlertCountersDTO

        :return: an empty SnortIdsAlertCountersDTO
        """
        return cluster_manager_pb2.SnortIdsIpAlertCountersDTO(
            priority_alerts=[], class_alerts=[], severe_alerts=0, warning_alerts=0, alerts_weighted_by_priority=0.0,
            ip="", ts=0.0, alert_ip="")

    @staticmethod
    def snort_ids_ip_alert_counters_dto_to_dict(
            snort_ids_alert_counters_dto: cluster_manager_pb2.SnortIdsIpAlertCountersDTO) -> Dict[str, Any]:
        """
        Converts a SnortIdsAlertCountersDTO to a dict

        :param snort_ids_alert_counters_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ip"] = snort_ids_alert_counters_dto.ip
        d["alert_ip"] = snort_ids_alert_counters_dto.alert_ip
        d["ts"] = snort_ids_alert_counters_dto.ts
        d["class_alerts"] = snort_ids_alert_counters_dto.class_alerts
        d["priority_alerts"] = snort_ids_alert_counters_dto.priority_alerts
        d["warning_alerts"] = snort_ids_alert_counters_dto.warning_alerts
        d["severe_alerts"] = snort_ids_alert_counters_dto.severe_alerts
        d["alerts_weighted_by_priority"] = snort_ids_alert_counters_dto.alerts_weighted_by_priority
        return d

    @staticmethod
    def convert_ossec_ids_alert_counters_dto(ossec_ids_alert_counters: Union[None, OSSECIdsAlertCounters]) \
            -> cluster_manager_pb2.OSSECIdsAlertCountersDTO:
        """
        Converts a OSSECIdsAlertCounters object to a OSSECIdsAlertCountersDTO

        :param ossec_ids_alert_counters: the object to convert
        :return: the converted objected
        """
        if ossec_ids_alert_counters is None:
            return ClusterManagerUtil.get_empty_ossec_ids_alert_counters_dto()
        else:
            return cluster_manager_pb2.OSSECIdsAlertCountersDTO(
                level_alerts=list(map(lambda x: int(x), ossec_ids_alert_counters.level_alerts)),
                group_alerts=list(map(lambda x: int(x), ossec_ids_alert_counters.group_alerts)),
                severe_alerts=int(ossec_ids_alert_counters.severe_alerts),
                warning_alerts=int(ossec_ids_alert_counters.warning_alerts),
                total_alerts=int(ossec_ids_alert_counters.total_alerts),
                alerts_weighted_by_level=float(ossec_ids_alert_counters.alerts_weighted_by_level),
                ip=ossec_ids_alert_counters.ip,
                ts=float(ossec_ids_alert_counters.ts))

    @staticmethod
    def convert_ossec_ids_alert_counters_dto_reverse(
            ossec_ids_alert_counters_dto: Union[None, cluster_manager_pb2.OSSECIdsAlertCountersDTO]) \
            -> OSSECIdsAlertCounters:
        """
        Converts a OSSECIdsAlertCountersDTO to a OSSECIdsAlertCounters

        :param ossec_ids_alert_counters_dto: the DTO to convert
        :return: the converted DTO
        """
        if ossec_ids_alert_counters_dto is None:
            return ClusterManagerUtil.convert_ossec_ids_alert_counters_dto_reverse(
                ClusterManagerUtil.get_empty_ossec_ids_alert_counters_dto())
        else:
            dto = OSSECIdsAlertCounters()
            dto.level_alerts = ossec_ids_alert_counters_dto.level_alerts
            dto.group_alerts = ossec_ids_alert_counters_dto.group_alerts
            dto.severe_alerts = ossec_ids_alert_counters_dto.severe_alerts
            dto.warning_alerts = ossec_ids_alert_counters_dto.warning_alerts
            dto.total_alerts = ossec_ids_alert_counters_dto.total_alerts
            dto.alerts_weighted_by_level = ossec_ids_alert_counters_dto.alerts_weighted_by_level
            dto.ip = ossec_ids_alert_counters_dto.ip
            dto.ts = ossec_ids_alert_counters_dto.ts
            return dto

    @staticmethod
    def get_empty_ossec_ids_alert_counters_dto() -> cluster_manager_pb2.OSSECIdsAlertCountersDTO:
        """
        Gets an empty OSSECIdsAlertCountersDTO

        :return: an empty OSSECIdsAlertCountersDTO
        """
        return cluster_manager_pb2.OSSECIdsAlertCountersDTO(
            level_alerts=[], group_alerts=[], severe_alerts=0, warning_alerts=0, total_alerts=0,
            alerts_weighted_by_level=0, ip="", ts=0.0)

    @staticmethod
    def ossec_ids_alert_counters_dto_to_dict(
            ossec_ids_alert_counters_dto: cluster_manager_pb2.OSSECIdsAlertCountersDTO) -> Dict[str, Any]:
        """
        Converts a OSSECIdsAlertCountersDTO to a dict

        :param ossec_ids_alert_counters_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["level_alerts"] = ossec_ids_alert_counters_dto.level_alerts
        d["group_alerts"] = ossec_ids_alert_counters_dto.group_alerts
        d["severe_alerts"] = ossec_ids_alert_counters_dto.severe_alerts
        d["warning_alerts"] = ossec_ids_alert_counters_dto.warning_alerts
        d["total_alerts"] = ossec_ids_alert_counters_dto.total_alerts
        d["alerts_weighted_by_level"] = ossec_ids_alert_counters_dto.alerts_weighted_by_level
        d["ip"] = ossec_ids_alert_counters_dto.ip
        d["ts"] = ossec_ids_alert_counters_dto.ts
        return d

    @staticmethod
    def convert_flow_statistics_dto(flow_statistic: Union[None, FlowStatistic]) -> cluster_manager_pb2.FlowStatisticDTO:
        """
        Converts a FlowStatistic object to a FlowStatisticDTO

        :param flow_statistic: the object to convert
        :return: the converted objected
        """
        if flow_statistic is None:
            return ClusterManagerUtil.get_empty_flow_statistic_dto()
        else:
            return cluster_manager_pb2.FlowStatisticDTO(
                timestamp=flow_statistic.timestamp, datapath_id=flow_statistic.datapath_id,
                in_port=flow_statistic.in_port, out_port=flow_statistic.out_port,
                dst_mac_address=flow_statistic.dst_mac_address, num_packets=flow_statistic.num_packets,
                num_bytes=flow_statistic.num_bytes, duration_nanoseconds=flow_statistic.duration_nanoseconds,
                duration_seconds=flow_statistic.duration_seconds, hard_timeout=flow_statistic.hard_timeout,
                idle_timeout=flow_statistic.idle_timeout, priority=flow_statistic.priority,
                cookie=flow_statistic.cookie)

    @staticmethod
    def convert_flow_statistic_dto_reverse(flow_statistic_dto: Union[None, cluster_manager_pb2.FlowStatisticDTO]) \
            -> FlowStatistic:
        """
        Converts a FlowStatisticDTO to a FlowStatistic

        :param flow_statistic_dto: the DTO to convert
        :return: the converted DTO
        """
        if flow_statistic_dto is None:
            return ClusterManagerUtil.convert_flow_statistic_dto_reverse(
                ClusterManagerUtil.get_empty_flow_statistic_dto())
        else:
            return FlowStatistic(
                timestamp=flow_statistic_dto.timestamp, datapath_id=flow_statistic_dto.datapath_id,
                in_port=flow_statistic_dto.in_port, out_port=flow_statistic_dto.out_port,
                dst_mac_address=flow_statistic_dto.dst_mac_address, num_packets=flow_statistic_dto.num_packets,
                num_bytes=flow_statistic_dto.num_bytes, duration_nanoseconds=flow_statistic_dto.duration_nanoseconds,
                duration_seconds=flow_statistic_dto.duration_seconds, hard_timeout=flow_statistic_dto.hard_timeout,
                idle_timeout=flow_statistic_dto.idle_timeout, priority=flow_statistic_dto.priority,
                cookie=flow_statistic_dto.cookie
            )

    @staticmethod
    def get_empty_flow_statistic_dto() -> cluster_manager_pb2.FlowStatisticDTO:
        """
        Gets an empty FlowStatisticDTO

        :return: an empty FlowStatisticDTO
        """
        return cluster_manager_pb2.FlowStatisticDTO(
            timestamp=0.0, datapath_id="", in_port="", out_port="", dst_mac_address="", num_packets=-1,
            num_bytes=-1, duration_nanoseconds=-1, duration_seconds=-1, hard_timeout=-1, idle_timeout=-1,
            priority=-1, cookie=-1)

    @staticmethod
    def flow_statistic_dto_to_dict(flow_statistic_dto: cluster_manager_pb2.FlowStatisticDTO) -> Dict[str, Any]:
        """
        Converts a FlowStatisticDTO to a dict

        :param flow_statistic_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["timestamp"] = flow_statistic_dto.timestamp
        d["datapath_id"] = flow_statistic_dto.datapath_id
        d["in_port"] = flow_statistic_dto.in_port
        d["out_port"] = flow_statistic_dto.out_port
        d["dst_mac_address"] = flow_statistic_dto.dst_mac_address
        d["num_packets"] = flow_statistic_dto.num_packets
        d["num_bytes"] = flow_statistic_dto.num_bytes
        d["duration_nanoseconds"] = flow_statistic_dto.duration_nanoseconds
        d["duration_seconds"] = flow_statistic_dto.duration_seconds
        d["hard_timeout"] = flow_statistic_dto.hard_timeout
        d["idle_timeout"] = flow_statistic_dto.idle_timeout
        d["priority"] = flow_statistic_dto.priority
        d["cookie"] = flow_statistic_dto.cookie
        return d

    @staticmethod
    def convert_port_statistics_dto(port_statistic: Union[None, PortStatistic]) -> cluster_manager_pb2.PortStatisticDTO:
        """
        Converts a PortStatistic object to a PortStatisticDTO

        :param port_statistic: the object to convert
        :return: the converted objected
        """
        if port_statistic is None:
            return ClusterManagerUtil.get_empty_port_statistic_dto()
        else:
            return cluster_manager_pb2.PortStatisticDTO(
                timestamp=port_statistic.timestamp, datapath_id=port_statistic.datapath_id,
                port=port_statistic.port, num_received_packets=port_statistic.num_received_packets,
                num_received_bytes=port_statistic.num_received_bytes,
                num_received_errors=port_statistic.num_received_errors,
                num_transmitted_packets=port_statistic.num_transmitted_packets,
                num_transmitted_bytes=port_statistic.num_transmitted_bytes,
                num_transmitted_errors=port_statistic.num_transmitted_errors,
                num_received_dropped=port_statistic.num_received_dropped,
                num_transmitted_dropped=port_statistic.num_transmitted_dropped,
                num_received_frame_errors=port_statistic.num_received_frame_errors,
                num_received_overrun_errors=port_statistic.num_received_overrun_errors,
                num_received_crc_errors=port_statistic.num_received_crc_errors,
                num_collisions=port_statistic.num_collisions,
                duration_nanoseconds=port_statistic.duration_nanoseconds,
                duration_seconds=port_statistic.duration_seconds)

    @staticmethod
    def convert_port_statistic_dto_reverse(port_statistic_dto: Union[None, cluster_manager_pb2.PortStatisticDTO]) \
            -> PortStatistic:
        """
        Converts a PortStatisticDTO to a PortStatistic

        :param port_statistic_dto: the DTO to convert
        :return: the converted DTO
        """
        if port_statistic_dto is None:
            return ClusterManagerUtil.convert_port_statistic_dto_reverse(
                ClusterManagerUtil.get_empty_port_statistic_dto())
        else:
            return PortStatistic(
                timestamp=port_statistic_dto.timestamp, datapath_id=port_statistic_dto.datapath_id,
                port=port_statistic_dto.port, num_received_packets=port_statistic_dto.num_received_packets,
                num_received_bytes=port_statistic_dto.num_received_bytes,
                num_received_errors=port_statistic_dto.num_received_errors,
                num_transmitted_packets=port_statistic_dto.num_transmitted_packets,
                num_transmitted_bytes=port_statistic_dto.num_transmitted_bytes,
                num_transmitted_errors=port_statistic_dto.num_transmitted_errors,
                num_received_dropped=port_statistic_dto.num_received_dropped,
                num_transmitted_dropped=port_statistic_dto.num_transmitted_dropped,
                num_received_frame_errors=port_statistic_dto.num_received_frame_errors,
                num_received_overrun_errors=port_statistic_dto.num_received_overrun_errors,
                num_received_crc_errors=port_statistic_dto.num_received_crc_errors,
                num_collisions=port_statistic_dto.num_collisions,
                duration_nanoseconds=port_statistic_dto.duration_nanoseconds,
                duration_seconds=port_statistic_dto.duration_seconds
            )

    @staticmethod
    def get_empty_port_statistic_dto() -> cluster_manager_pb2.PortStatisticDTO:
        """
        Gets an empty PortStatisticDTO

        :return: an empty PortStatisticDTO
        """
        return cluster_manager_pb2.PortStatisticDTO(
            timestamp=0.0, datapath_id="", port=-1, num_received_packets=-1, num_received_bytes=-1,
            num_received_errors=-1, num_transmitted_packets=-1, num_transmitted_bytes=-1, num_transmitted_errors=-1,
            num_received_dropped=-1, num_transmitted_dropped=-1, num_received_frame_errors=-1,
            num_received_overrun_errors=-1, num_received_crc_errors=-1, num_collisions=-1, duration_nanoseconds=-1,
            duration_seconds=-1)

    @staticmethod
    def port_statistic_dto_to_dict(port_statistic_dto: cluster_manager_pb2.PortStatisticDTO) -> Dict[str, Any]:
        """
        Converts a PortStatisticDTO to a dict

        :param port_statistic_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["timestamp"] = port_statistic_dto.timestamp
        d["datapath_id"] = port_statistic_dto.datapath_id
        d["port"] = port_statistic_dto.port
        d["num_received_packets"] = port_statistic_dto.num_received_packets
        d["num_received_bytes"] = port_statistic_dto.num_received_bytes
        d["num_received_errors"] = port_statistic_dto.num_received_errors
        d["num_transmitted_packets"] = port_statistic_dto.num_transmitted_packets
        d["num_transmitted_bytes"] = port_statistic_dto.num_transmitted_bytes
        d["num_transmitted_errors"] = port_statistic_dto.num_transmitted_errors
        d["num_received_dropped"] = port_statistic_dto.num_received_dropped
        d["num_transmitted_dropped"] = port_statistic_dto.num_transmitted_dropped
        d["num_received_frame_errors"] = port_statistic_dto.num_received_frame_errors
        d["num_received_overrun_errors"] = port_statistic_dto.num_received_overrun_errors
        d["num_received_crc_errors"] = port_statistic_dto.num_received_crc_errors
        d["num_collisions"] = port_statistic_dto.num_collisions
        d["duration_nanoseconds"] = port_statistic_dto.duration_nanoseconds
        d["duration_seconds"] = port_statistic_dto.duration_seconds
        return d

    @staticmethod
    def convert_agg_flow_statistic_dto(agg_flow_statistic: Union[None, AggFlowStatistic]) \
            -> cluster_manager_pb2.AggFlowStatisticDTO:
        """
        Converts a AggFlowStatistic object to a AggFlowStatisticDTO

        :param agg_flow_statistic: the object to convert
        :return: the converted objected
        """
        if agg_flow_statistic is None:
            return ClusterManagerUtil.get_empty_agg_flow_statistic_dto()
        else:
            return cluster_manager_pb2.AggFlowStatisticDTO(
                timestamp=agg_flow_statistic.timestamp, datapath_id=agg_flow_statistic.datapath_id,
                total_num_packets=agg_flow_statistic.total_num_packets,
                total_num_bytes=agg_flow_statistic.total_num_bytes,
                total_num_flows=agg_flow_statistic.total_num_flows)

    @staticmethod
    def convert_agg_flow_statistic_dto_reverse(
            agg_flow_statistic_dto: Union[None, cluster_manager_pb2.AggFlowStatisticDTO]) -> AggFlowStatistic:
        """
        Converts a AggFlowStatisticDTO to a AggFlowStatistic

        :param agg_flow_statistic_dto: the DTO to convert
        :return: the converted DTO
        """
        if agg_flow_statistic_dto is None:
            return ClusterManagerUtil.convert_agg_flow_statistic_dto_reverse(
                ClusterManagerUtil.get_empty_agg_flow_statistic_dto())
        else:
            return AggFlowStatistic(
                timestamp=agg_flow_statistic_dto.timestamp, datapath_id=agg_flow_statistic_dto.datapath_id,
                total_num_packets=agg_flow_statistic_dto.total_num_packets,
                total_num_bytes=agg_flow_statistic_dto.total_num_bytes,
                total_num_flows=agg_flow_statistic_dto.total_num_flows)

    @staticmethod
    def get_empty_agg_flow_statistic_dto() -> cluster_manager_pb2.AggFlowStatisticDTO:
        """
        Gets an empty AggFlowStatisticDTO

        :return: an empty AggFlowStatisticDTO
        """
        return cluster_manager_pb2.AggFlowStatisticDTO(
            timestamp=0.0, datapath_id="", total_num_packets=-1, total_num_bytes=-1, total_num_flows=-1)

    @staticmethod
    def agg_flow_statistic_dto_to_dict(agg_flow_statistic_dto: cluster_manager_pb2.AggFlowStatisticDTO) \
            -> Dict[str, Any]:
        """
        Converts a AggFlowStatisticDTO to a dict

        :param agg_flow_statistic_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["timestamp"] = agg_flow_statistic_dto.timestamp
        d["datapath_id"] = agg_flow_statistic_dto.datapath_id
        d["total_num_packets"] = agg_flow_statistic_dto.total_num_packets
        d["total_num_bytes"] = agg_flow_statistic_dto.total_num_bytes
        d["total_num_flows"] = agg_flow_statistic_dto.total_num_flows
        return d

    @staticmethod
    def convert_avg_flow_statistic_dto(avg_flow_statistic: Union[None, AvgFlowStatistic]) \
            -> cluster_manager_pb2.AvgFlowStatisticDTO:
        """
        Converts a AvgFlowStatistic object to a AvgFlowStatisticDTO

        :param avg_flow_statistic: the object to convert
        :return: the converted objected
        """
        if avg_flow_statistic is None:
            return ClusterManagerUtil.get_empty_avg_flow_statistic_dto()
        else:
            return cluster_manager_pb2.AvgFlowStatisticDTO(
                timestamp=avg_flow_statistic.timestamp, datapath_id=avg_flow_statistic.datapath_id,
                total_num_packets=avg_flow_statistic.total_num_packets,
                total_num_bytes=avg_flow_statistic.total_num_bytes,
                avg_duration_nanoseconds=avg_flow_statistic.avg_duration_nanoseconds,
                avg_duration_seconds=avg_flow_statistic.avg_duration_seconds,
                avg_hard_timeout=avg_flow_statistic.avg_hard_timeout,
                avg_idle_timeout=avg_flow_statistic.avg_idle_timeout,
                avg_priority=avg_flow_statistic.avg_priority,
                avg_cookie=avg_flow_statistic.avg_cookie)

    @staticmethod
    def convert_avg_flow_statistic_dto_reverse(
            avg_flow_statistic_dto: Union[None, cluster_manager_pb2.AvgFlowStatisticDTO]) -> AvgFlowStatistic:
        """
        Converts a AvgFlowStatisticDTO to a AvgFlowStatistic

        :param avg_flow_statistic_dto: the DTO to convert
        :return: the converted DTO
        """
        if avg_flow_statistic_dto is None:
            return ClusterManagerUtil.convert_avg_flow_statistic_dto_reverse(
                ClusterManagerUtil.get_empty_avg_flow_statistic_dto())
        else:
            return AvgFlowStatistic(
                timestamp=avg_flow_statistic_dto.timestamp, datapath_id=avg_flow_statistic_dto.datapath_id,
                total_num_packets=avg_flow_statistic_dto.total_num_packets,
                total_num_bytes=avg_flow_statistic_dto.total_num_bytes,
                avg_duration_nanoseconds=avg_flow_statistic_dto.avg_duration_nanoseconds,
                avg_duration_seconds=avg_flow_statistic_dto.avg_duration_seconds,
                avg_hard_timeout=avg_flow_statistic_dto.avg_hard_timeout,
                avg_idle_timeout=avg_flow_statistic_dto.avg_idle_timeout,
                avg_priority=avg_flow_statistic_dto.avg_priority,
                avg_cookie=avg_flow_statistic_dto.avg_cookie)

    @staticmethod
    def get_empty_avg_flow_statistic_dto() -> cluster_manager_pb2.AvgFlowStatisticDTO:
        """
        Gets an empty AvgFlowStatisticDTO

        :return: an empty AvgFlowStatisticDTO
        """
        return cluster_manager_pb2.AvgFlowStatisticDTO(
            timestamp=0.0, datapath_id="", total_num_packets=-1, total_num_bytes=-1,
            avg_duration_nanoseconds=-1, avg_duration_seconds=-1, avg_hard_timeout=-1, avg_idle_timeout=-1,
            avg_priority=-1, avg_cookie=-1)

    @staticmethod
    def avg_flow_statistic_dto_to_dict(avg_flow_statistic_dto: cluster_manager_pb2.AvgFlowStatisticDTO) \
            -> Dict[str, Any]:
        """
        Converts a AvgFlowStatisticDTO to a dict

        :param avg_flow_statistic_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["timestamp"] = avg_flow_statistic_dto.timestamp
        d["datapath_id"] = avg_flow_statistic_dto.datapath_id
        d["total_num_packets"] = avg_flow_statistic_dto.total_num_packets
        d["total_num_bytes"] = avg_flow_statistic_dto.total_num_bytes
        d["avg_duration_nanoseconds"] = avg_flow_statistic_dto.avg_duration_nanoseconds
        d["avg_duration_seconds"] = avg_flow_statistic_dto.avg_duration_seconds
        d["avg_hard_timeout"] = avg_flow_statistic_dto.avg_hard_timeout
        d["avg_idle_timeout"] = avg_flow_statistic_dto.avg_idle_timeout
        d["avg_priority"] = avg_flow_statistic_dto.avg_priority
        d["avg_cookie"] = avg_flow_statistic_dto.avg_cookie
        return d

    @staticmethod
    def convert_avg_port_statistic_dto(avg_port_statistic: Union[None, AvgPortStatistic]) \
            -> cluster_manager_pb2.AvgPortStatisticDTO:
        """
        Converts a AvgPortStatistic object to a AvgPortStatisticDTO

        :param avg_port_statistic: the object to convert
        :return: the converted objected
        """
        if avg_port_statistic is None:
            return ClusterManagerUtil.get_empty_avg_port_statistic_dto()
        else:
            return cluster_manager_pb2.AvgPortStatisticDTO(
                timestamp=avg_port_statistic.timestamp, datapath_id=avg_port_statistic.datapath_id,
                total_num_received_packets=avg_port_statistic.total_num_received_packets,
                total_num_received_bytes=avg_port_statistic.total_num_received_bytes,
                total_num_received_errors=avg_port_statistic.total_num_received_errors,
                total_num_transmitted_packets=avg_port_statistic.total_num_transmitted_packets,
                total_num_transmitted_bytes=avg_port_statistic.total_num_transmitted_bytes,
                total_num_transmitted_errors=avg_port_statistic.total_num_transmitted_errors,
                total_num_received_dropped=avg_port_statistic.total_num_received_dropped,
                total_num_transmitted_dropped=avg_port_statistic.total_num_transmitted_dropped,
                total_num_received_frame_errors=avg_port_statistic.total_num_received_frame_errors,
                total_num_received_overrun_errors=avg_port_statistic.total_num_received_overrun_errors,
                total_num_received_crc_errors=avg_port_statistic.total_num_received_crc_errors,
                total_num_collisions=avg_port_statistic.total_num_collisions,
                avg_duration_nanoseconds=avg_port_statistic.avg_duration_nanoseconds,
                avg_duration_seconds=avg_port_statistic.avg_duration_seconds)

    @staticmethod
    def convert_avg_port_statistic_dto_reverse(
            avg_port_statistic_dto: Union[None, cluster_manager_pb2.AvgPortStatisticDTO]) -> AvgPortStatistic:
        """
        Converts a AvgPortStatisticDTO to a AvgPortStatistic

        :param avg_port_statistic_dto: the DTO to convert
        :return: the converted DTO
        """
        if avg_port_statistic_dto is None:
            return ClusterManagerUtil.convert_avg_port_statistic_dto_reverse(
                ClusterManagerUtil.get_empty_avg_port_statistic_dto())
        else:
            return AvgPortStatistic(
                timestamp=avg_port_statistic_dto.timestamp, datapath_id=avg_port_statistic_dto.datapath_id,
                total_num_received_packets=avg_port_statistic_dto.total_num_received_packets,
                total_num_received_bytes=avg_port_statistic_dto.total_num_received_bytes,
                total_num_received_errors=avg_port_statistic_dto.total_num_received_errors,
                total_num_transmitted_packets=avg_port_statistic_dto.total_num_transmitted_packets,
                total_num_transmitted_bytes=avg_port_statistic_dto.total_num_transmitted_bytes,
                total_num_transmitted_errors=avg_port_statistic_dto.total_num_transmitted_errors,
                total_num_received_dropped=avg_port_statistic_dto.total_num_received_dropped,
                total_num_transmitted_dropped=avg_port_statistic_dto.total_num_transmitted_dropped,
                total_num_received_frame_errors=avg_port_statistic_dto.total_num_received_frame_errors,
                total_num_received_overrun_errors=avg_port_statistic_dto.total_num_received_overrun_errors,
                total_num_received_crc_errors=avg_port_statistic_dto.total_num_received_crc_errors,
                total_num_collisions=avg_port_statistic_dto.total_num_collisions,
                avg_duration_nanoseconds=avg_port_statistic_dto.avg_duration_nanoseconds,
                avg_duration_seconds=avg_port_statistic_dto.avg_duration_seconds)

    @staticmethod
    def get_empty_avg_port_statistic_dto() -> cluster_manager_pb2.AvgPortStatisticDTO:
        """
        Gets an empty AvgPortStatisticDTO

        :return: an empty AvgPortStatisticDTO
        """
        return cluster_manager_pb2.AvgPortStatisticDTO(
            timestamp=0.0, datapath_id="", total_num_received_packets=0, total_num_received_bytes=0,
            total_num_received_errors=0, total_num_transmitted_packets=0, total_num_transmitted_bytes=0,
            total_num_transmitted_errors=0, total_num_received_dropped=0, total_num_transmitted_dropped=0,
            total_num_received_frame_errors=0, total_num_received_overrun_errors=0,
            total_num_received_crc_errors=0,
            total_num_collisions=0, avg_duration_nanoseconds=0, avg_duration_seconds=0)

    @staticmethod
    def avg_port_statistic_dto_to_dict(avg_port_statistic_dto: cluster_manager_pb2.AvgPortStatisticDTO) \
            -> Dict[str, Any]:
        """
        Converts a AvgPortStatisticDTO to a dict

        :param avg_port_statistic_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["timestamp"] = avg_port_statistic_dto.timestamp
        d["datapath_id"] = avg_port_statistic_dto.datapath_id
        d["total_num_received_packets"] = avg_port_statistic_dto.total_num_received_packets
        d["total_num_received_bytes"] = avg_port_statistic_dto.total_num_received_bytes
        d["total_num_received_errors"] = avg_port_statistic_dto.total_num_received_errors
        d["total_num_transmitted_packets"] = avg_port_statistic_dto.total_num_transmitted_packets
        d["total_num_transmitted_bytes"] = avg_port_statistic_dto.total_num_transmitted_bytes
        d["total_num_transmitted_errors"] = avg_port_statistic_dto.total_num_transmitted_errors
        d["total_num_received_dropped"] = avg_port_statistic_dto.total_num_received_dropped
        d["total_num_transmitted_dropped"] = avg_port_statistic_dto.total_num_transmitted_dropped
        d["total_num_received_frame_errors"] = avg_port_statistic_dto.total_num_received_frame_errors
        d["total_num_received_overrun_errors"] = avg_port_statistic_dto.total_num_received_overrun_errors
        d["total_num_received_crc_errors"] = avg_port_statistic_dto.total_num_received_crc_errors
        d["total_num_collisions"] = avg_port_statistic_dto.total_num_collisions
        d["avg_duration_nanoseconds"] = avg_port_statistic_dto.avg_duration_nanoseconds
        d["avg_duration_seconds"] = avg_port_statistic_dto.avg_duration_seconds
        return d

    @staticmethod
    def convert_docker_stats_dict(docker_stats_d: Union[Dict[str, List[DockerStats]], None]) \
            -> List[cluster_manager_pb2.DockerStatsDict]:
        """
        Converts a dict to list of DockerStatsDict

        :param docker_stats_d: the dict to convert
        :return: the converted objected
        """
        if docker_stats_d is None:
            return ClusterManagerUtil.get_empty_docker_stats_dict()
        else:
            docker_stats_dict_list = []
            for k, v in docker_stats_d.items():
                docker_stats_dict_list.append(cluster_manager_pb2.DockerStatsDict(
                    key=k, dtos=list(map(lambda x: ClusterManagerUtil.convert_docker_stats_dto(x), v))))
            return docker_stats_dict_list

    @staticmethod
    def convert_docker_stats_dict_reverse(docker_stats_dict: Union[List[cluster_manager_pb2.DockerStatsDict], None]) \
            -> Dict[str, List[DockerStats]]:
        """
        Converts a list of DockerStatsDict to a dict

        :param docker_stats_dict: the list to convert
        :return: the converted DTO
        """
        if docker_stats_dict is None:
            return ClusterManagerUtil.convert_docker_stats_dict_reverse(
                ClusterManagerUtil.get_empty_docker_stats_dict())
        else:
            d: Dict[str, Any] = {}
            for ds in docker_stats_dict:
                d[ds.key] = list(map(lambda x: ClusterManagerUtil.convert_docker_stats_dto_reverse(x), ds.dtos))
            return d

    @staticmethod
    def get_empty_docker_stats_dict() -> List[cluster_manager_pb2.DockerStatsDict]:
        """
        Gets an empty list of DockerStatsDict

        :return: an empty list of DockerStatsDict
        """
        return []

    @staticmethod
    def docker_stats_dict_to_dict(docker_stats_dict: cluster_manager_pb2.DockerStatsDict) \
            -> Dict[str, Any]:
        """
        Converts a DTO to a dict

        :param docker_stats_dict: the DTO to convert
        :return: the dict
        """
        d: Dict[str, Any] = {}
        d["key"] = docker_stats_dict.key
        dtos = []
        for dto in docker_stats_dict.dtos:
            dtos.append(ClusterManagerUtil.docker_stats_dto_to_dict(dto))
        d["dtos"] = dtos
        return d

    @staticmethod
    def convert_snort_ids_ip_alert_counters_dict(
            snort_ids_ip_alert_counters_d: Union[Dict[str, List[SnortIdsIPAlertCounters]], None]) \
            -> List[cluster_manager_pb2.SnortIdsIpAlertCountersDict]:
        """
        Converts a dict to list of SnortIdsIpAlertCountersDict

        :param snort_ids_ip_alert_counters_d: the dict to convert
        :return: the converted objected
        """
        if snort_ids_ip_alert_counters_d is None:
            return ClusterManagerUtil.get_empty_snort_ids_ip_alert_counters_dict()
        else:
            snort_ids_ip_alerts_dict_list = []
            for k, v in snort_ids_ip_alert_counters_d.items():
                snort_ids_ip_alerts_dict_list.append(cluster_manager_pb2.SnortIdsIpAlertCountersDict(
                    key=k, dtos=list(map(lambda x: ClusterManagerUtil.convert_snort_ids_ip_alert_counters_dto(x), v))))
            return snort_ids_ip_alerts_dict_list

    @staticmethod
    def convert_snort_ids_ip_alert_counters_dict_reverse(
            snort_ids_ip_alerts_counters_dict: Union[List[cluster_manager_pb2.SnortIdsIpAlertCountersDict], None]) \
            -> Dict[str, List[SnortIdsIPAlertCounters]]:
        """
        Converts a list of SnortIdsIpAlertCountersDict to a dict

        :param snort_ids_ip_alerts_counters_dict: the list to convert
        :return: the converted DTO
        """
        if snort_ids_ip_alerts_counters_dict is None:
            return ClusterManagerUtil.convert_snort_ids_ip_alert_counters_dict_reverse(
                ClusterManagerUtil.get_empty_snort_ids_ip_alert_counters_dict())
        else:
            d: Dict[str, Any] = {}
            for ds in snort_ids_ip_alerts_counters_dict:
                d[ds.key] = list(map(lambda x: ClusterManagerUtil.convert_snort_ids_ip_alert_counters_dto_reverse(x),
                                     ds.dtos))
            return d

    @staticmethod
    def get_empty_snort_ids_ip_alert_counters_dict() -> List[cluster_manager_pb2.SnortIdsIpAlertCountersDict]:
        """
        Gets an empty list of SnortIdsIpAlertCountersDict

        :return: an empty list of SnortIdsIpAlertCountersDict
        """
        return []

    @staticmethod
    def snort_ids_ip_alert_counters_dict_to_dict(
            snort_ids_ip_alert_counters_dict: cluster_manager_pb2.SnortIdsIpAlertCountersDict) -> Dict[str, Any]:
        """
        Converts a DTO to a dict

        :param snort_ids_ip_alert_counters_dict: the DTO to convert
        :return: the dict
        """
        d: Dict[str, Any] = {}
        d["key"] = snort_ids_ip_alert_counters_dict.key
        dtos = []
        for dto in snort_ids_ip_alert_counters_dict.dtos:
            dtos.append(ClusterManagerUtil.snort_ids_ip_alert_counters_dto_to_dict(dto))
        d["dtos"] = dtos
        return d

    @staticmethod
    def convert_snort_ids_alert_counters_dict(
            snort_ids_alert_counters_d: Union[Dict[str, List[SnortIdsAlertCounters]], None]) \
            -> List[cluster_manager_pb2.SnortIdsAlertCountersDict]:
        """
        Converts a dict to list of SnortIdsAlertCountersDict

        :param snort_ids_alert_counters_d: the dict to convert
        :return: the converted objected
        """
        if snort_ids_alert_counters_d is None:
            return ClusterManagerUtil.get_empty_snort_ids_alert_counters_dict()
        else:
            snort_ids_alerts_dict_list = []
            for k, v in snort_ids_alert_counters_d.items():
                snort_ids_alerts_dict_list.append(cluster_manager_pb2.SnortIdsAlertCountersDict(
                    key=k, dtos=list(map(lambda x: ClusterManagerUtil.convert_snort_ids_alert_counters_dto(x), v))))
            return snort_ids_alerts_dict_list

    @staticmethod
    def convert_snort_ids_alert_counters_dict_reverse(
            snort_ids_alerts_counters_dict: Union[List[cluster_manager_pb2.SnortIdsAlertCountersDict], None]) \
            -> Dict[str, List[SnortIdsAlertCounters]]:
        """
        Converts a list of SnortIdsIpAlertCountersDict to a dict

        :param snort_ids_alerts_counters_dict: the list to convert
        :return: the converted DTO
        """
        if snort_ids_alerts_counters_dict is None:
            return ClusterManagerUtil.convert_snort_ids_alert_counters_dict_reverse(
                ClusterManagerUtil.get_empty_snort_ids_alert_counters_dict())
        else:
            d: Dict[str, Any] = {}
            for ds in snort_ids_alerts_counters_dict:
                d[ds.key] = list(map(lambda x: ClusterManagerUtil.convert_snort_ids_alert_counters_dto_reverse(x),
                                     ds.dtos))
            return d

    @staticmethod
    def get_empty_snort_ids_alert_counters_dict() -> List[cluster_manager_pb2.SnortIdsAlertCountersDict]:
        """
        Gets an empty list of SnortIdsAlertCountersDict

        :return: an empty list of SnortIdsAlertCountersDict
        """
        return []

    @staticmethod
    def snort_ids_alert_counters_dict_to_dict(
            snort_ids_alert_counters_dict: cluster_manager_pb2.SnortIdsAlertCountersDict) -> Dict[str, Any]:
        """
        Converts a DTO to a dict

        :param snort_ids_alert_counters_dict: the DTO to convert
        :return: the dict
        """
        d: Dict[str, Any] = {}
        d["key"] = snort_ids_alert_counters_dict.key
        dtos = []
        for dto in snort_ids_alert_counters_dict.dtos:
            dtos.append(ClusterManagerUtil.snort_ids_alert_counters_dto_to_dict(dto))
        d["dtos"] = dtos
        return d

    @staticmethod
    def convert_snort_ids_rule_counters_dict(
            snort_ids_rule_counters_d: Union[None, Dict[str, List[SnortIdsRuleCounters]]]) \
            -> List[cluster_manager_pb2.SnortIdsRuleCountersDict]:
        """
        Converts a dict to list of SnortIdsRuleCountersDict

        :param snort_ids_rule_counters_d: the dict to convert
        :return: the converted objected
        """
        if snort_ids_rule_counters_d is None:
            return ClusterManagerUtil.get_empty_snort_ids_rule_counters_dict()
        else:
            snort_ids_rule_dict_list = []
            for k, v in snort_ids_rule_counters_d.items():
                snort_ids_rule_dict_list.append(cluster_manager_pb2.SnortIdsRuleCountersDict(
                    key=k, dtos=list(map(lambda x: ClusterManagerUtil.convert_snort_ids_rule_counters_dto(x), v))))
            return snort_ids_rule_dict_list

    @staticmethod
    def convert_snort_ids_rule_counters_dict_reverse(
            snort_ids_rule_counters_dict: Union[None, List[cluster_manager_pb2.SnortIdsRuleCountersDict]]) \
            -> Dict[str, List[SnortIdsRuleCounters]]:
        """
        Converts a list of SnortIdsRuleCountersDict to a dict

        :param snort_ids_rule_counters_dict: the list to convert
        :return: the converted DTO
        """
        if snort_ids_rule_counters_dict is None:
            return ClusterManagerUtil.convert_snort_ids_rule_counters_dict_reverse(
                ClusterManagerUtil.get_empty_snort_ids_rule_counters_dict())
        else:
            d: Dict[str, Any] = {}
            for ds in snort_ids_rule_counters_dict:
                d[ds.key] = list(map(lambda x: ClusterManagerUtil.convert_snort_ids_rule_counters_dto_reverse(x),
                                     ds.dtos))
            return d

    @staticmethod
    def get_empty_snort_ids_rule_counters_dict() -> List[cluster_manager_pb2.SnortIdsRuleCountersDict]:
        """
        Gets an empty list of SnortIdsRuleCountersDict

        :return: an empty list of SnortIdsRuleCountersDict
        """
        return []

    @staticmethod
    def snort_ids_rule_counters_dict_to_dict(
            snort_ids_rule_counters_dict: cluster_manager_pb2.SnortIdsRuleCountersDict) -> Dict[str, Any]:
        """
        Converts a DTO to a dict

        :param snort_ids_rule_counters_dict: the DTO to convert
        :return: the dict
        """
        d: Dict[str, Any] = {}
        d["key"] = snort_ids_rule_counters_dict.key
        dtos = []
        for dto in snort_ids_rule_counters_dict.dtos:
            dtos.append(ClusterManagerUtil.snort_ids_rule_counters_dto_to_dict(dto))
        d["dtos"] = dtos
        return d

    @staticmethod
    def convert_host_metrics_dict(host_metrics_dict: Union[Dict[str, List[HostMetrics]], None]) \
            -> List[cluster_manager_pb2.HostMetricsDict]:
        """
        Converts a dict to list of HostMetricsDict

        :param host_metrics_dict: the dict to convert
        :return: the converted objected
        """
        if host_metrics_dict is None:
            return ClusterManagerUtil.get_empty_host_metrics_dict()
        else:
            host_metrics_dict_list = []
            for k, v in host_metrics_dict.items():
                host_metrics_dict_list.append(cluster_manager_pb2.HostMetricsDict(
                    key=k, dtos=list(map(lambda x: ClusterManagerUtil.convert_host_metrics_dto(x), v))))
            return host_metrics_dict_list

    @staticmethod
    def convert_host_metrics_dict_reverse(host_metrics_dict: Union[List[cluster_manager_pb2.HostMetricsDict], None]) \
            -> Dict[str, List[HostMetrics]]:
        """
        Converts a list of HostMetricsDict to a dict

        :param host_metrics_dict: the list to convert
        :return: the converted DTO
        """
        if host_metrics_dict is None:
            return ClusterManagerUtil.convert_host_metrics_dict_reverse(
                ClusterManagerUtil.get_empty_host_metrics_dict())
        else:
            d: Dict[str, Any] = {}
            for ds in host_metrics_dict:
                d[ds.key] = list(map(lambda x: ClusterManagerUtil.convert_host_metrics_dto_reverse(x), ds.dtos))
            return d

    @staticmethod
    def get_empty_host_metrics_dict() -> List[cluster_manager_pb2.HostMetricsDict]:
        """
        Gets an empty list of HostMetricsDict

        :return: an empty HostMetricsDict
        """
        return []

    @staticmethod
    def host_metrics_dict_to_dict(host_metrics_dict: cluster_manager_pb2.HostMetricsDict) \
            -> Dict[str, Any]:
        """
        Converts a DTO to a dict

        :param host_metrics_dict: the DTO to convert
        :return: the dict
        """
        d: Dict[str, Any] = {}
        d["key"] = host_metrics_dict.key
        dtos = []
        for dto in host_metrics_dict.dtos:
            dtos.append(ClusterManagerUtil.host_metrics_dto_to_dict(dto))
        d["dtos"] = dtos
        return d

    @staticmethod
    def convert_ossec_ids_alert_counters_dict(
            ossec_ids_alert_counters_dict: Union[Dict[str, List[OSSECIdsAlertCounters]], None]) \
            -> List[cluster_manager_pb2.OSSECIdsAlertCountersDict]:
        """
        Converts a dict to list of OSSECIdsAlertCountersDict

        :param ossec_ids_alert_counters_dict: the dict to convert
        :return: the converted objected
        """
        if ossec_ids_alert_counters_dict is None:
            return ClusterManagerUtil.get_empty_ossec_ids_alert_counters_dict()
        else:
            ossec_ids_alert_counters_dict_list = []
            for k, v in ossec_ids_alert_counters_dict.items():
                ossec_ids_alert_counters_dict_list.append(cluster_manager_pb2.OSSECIdsAlertCountersDict(
                    key=k, dtos=list(map(lambda x: ClusterManagerUtil.convert_ossec_ids_alert_counters_dto(x), v))))
            return ossec_ids_alert_counters_dict_list

    @staticmethod
    def convert_ossec_ids_alert_counters_dict_reverse(
            ossec_ids_alert_counters_dict: Union[List[cluster_manager_pb2.OSSECIdsAlertCountersDict], None]) \
            -> Dict[str, List[OSSECIdsAlertCounters]]:
        """
        Converts a list of OSSECIdsAlertCountersDict to a dict

        :param ossec_ids_alert_counters_dict: the list to convert
        :return: the converted DTO
        """
        if ossec_ids_alert_counters_dict is None:
            return ClusterManagerUtil.convert_ossec_ids_alert_counters_dict_reverse(
                ClusterManagerUtil.get_empty_ossec_ids_alert_counters_dict())
        else:
            d: Dict[str, Any] = {}
            for ds in ossec_ids_alert_counters_dict:
                d[ds.key] = list(map(lambda x: ClusterManagerUtil.convert_ossec_ids_alert_counters_dto_reverse(x),
                                     ds.dtos))
            return d

    @staticmethod
    def get_empty_ossec_ids_alert_counters_dict() -> List[cluster_manager_pb2.OSSECIdsAlertCountersDict]:
        """
        Gets an empty list of OSSECIdsAlertCountersDict
        :return: an empty OSSECIdsAlertCountersDict
        """
        return []

    @staticmethod
    def ossec_ids_alert_counters_dict_to_dict(
            ossec_ids_alert_counters_dict: cluster_manager_pb2.OSSECIdsAlertCountersDict) -> Dict[str, Any]:
        """
        Converts a DTO to a dict

        :param ossec_ids_alert_counters_dict: the DTO to convert
        :return: the dict
        """
        d: Dict[str, Any] = {}
        d["key"] = ossec_ids_alert_counters_dict.key
        dtos = []
        for dto in ossec_ids_alert_counters_dict.dtos:
            dtos.append(ClusterManagerUtil.ossec_ids_alert_counters_dto_to_dict(dto))
        d["dtos"] = dtos
        return d

    @staticmethod
    def convert_flow_statistic_dict(flow_statistic_dict: Union[None, Dict[str, List[FlowStatistic]]]) \
            -> List[cluster_manager_pb2.FlowStatisticDict]:
        """
        Converts a dict to list of FlowStatisticDict

        :param flow_statistic_dict: the dict to convert
        :return: the converted objected
        """
        if flow_statistic_dict is None:
            return ClusterManagerUtil.get_empty_flow_statistic_dict()
        else:
            flow_statistic_dict_list = []
            for k, v in flow_statistic_dict.items():
                flow_statistic_dict_list.append(cluster_manager_pb2.FlowStatisticDict(
                    key=k, dtos=list(map(lambda x: ClusterManagerUtil.convert_flow_statistics_dto(x), v))))
            return flow_statistic_dict_list

    @staticmethod
    def convert_flow_statistic_dict_reverse(
            flow_statistics_dict: Union[List[cluster_manager_pb2.FlowStatisticDict], None]) \
            -> Dict[str, List[FlowStatistic]]:
        """
        Converts a list of FlowStatisticDict to a dict

        :param flow_statistics_dict: the list to convert
        :return: the converted DTO
        """
        if flow_statistics_dict is None:
            return ClusterManagerUtil.convert_flow_statistic_dict_reverse(
                ClusterManagerUtil.get_empty_flow_statistic_dict())
        else:
            d: Dict[str, Any] = {}
            for ds in flow_statistics_dict:
                d[ds.key] = list(map(lambda x: ClusterManagerUtil.convert_flow_statistic_dto_reverse(x), ds.dtos))
            return d

    @staticmethod
    def get_empty_flow_statistic_dict() -> List[cluster_manager_pb2.FlowStatisticDict]:
        """
        Gets an empty list of FlowStatisticDict

        :return: an empty list of FlowStatisticDict
        """
        return []

    @staticmethod
    def flow_statistics_dict_to_dict(flow_statistics_dict: cluster_manager_pb2.FlowStatisticDict) -> Dict[str, Any]:
        """
        Converts a DTO to a dict

        :param flow_statistics_dict: the DTO to convert
        :return: the dict
        """
        d: Dict[str, Any] = {}
        d["key"] = flow_statistics_dict.key
        dtos = []
        for dto in flow_statistics_dict.dtos:
            dtos.append(ClusterManagerUtil.flow_statistic_dto_to_dict(dto))
        d["dtos"] = dtos
        return d

    @staticmethod
    def convert_port_statistic_dict(port_statistic_dict: Union[None, Dict[str, List[PortStatistic]]]) \
            -> List[cluster_manager_pb2.PortStatisticDict]:
        """
        Converts a dict to list of PortStatisticDict

        :param port_statistic_dict: the dict to convert
        :return: the converted object
        """
        if port_statistic_dict is None:
            return ClusterManagerUtil.get_empty_port_statistic_dict()
        else:
            port_statistic_dict_list = []
            for k, v in port_statistic_dict.items():
                port_statistic_dict_list.append(cluster_manager_pb2.PortStatisticDict(
                    key=k, dtos=list(map(lambda x: ClusterManagerUtil.convert_port_statistics_dto(x), v))))
            return port_statistic_dict_list

    @staticmethod
    def convert_port_statistic_dict_reverse(
            port_statistics_dict: Union[None, List[cluster_manager_pb2.PortStatisticDict]]) \
            -> Dict[str, List[PortStatistic]]:
        """
        Converts a list of PortStatisticDict to a dict

        :param port_statistics_dict: the list to convert
        :return: the converted DTO
        """
        if port_statistics_dict is None:
            return ClusterManagerUtil.convert_port_statistic_dict_reverse(
                ClusterManagerUtil.get_empty_port_statistic_dict())
        else:
            d: Dict[str, Any] = {}
            for ds in port_statistics_dict:
                d[ds.key] = list(map(lambda x: ClusterManagerUtil.convert_port_statistic_dto_reverse(x), ds.dtos))
            return d

    @staticmethod
    def get_empty_port_statistic_dict() -> List[cluster_manager_pb2.PortStatisticDict]:
        """
        Gets an list of PortStatisticDict

        :return: an empty list of PortStatisticDict
        """
        return []

    @staticmethod
    def port_statistics_dict_to_dict(port_statistics_dict: cluster_manager_pb2.PortStatisticDict) -> Dict[str, Any]:
        """
        Converts a DTO to a dict

        :param port_statistics_dict: the DTO to convert
        :return: the dict
        """
        d: Dict[str, Any] = {}
        d["key"] = port_statistics_dict.key
        dtos = []
        for dto in port_statistics_dict.dtos:
            dtos.append(ClusterManagerUtil.port_statistic_dto_to_dict(dto))
        d["dtos"] = dtos
        return d

    @staticmethod
    def convert_avg_flow_statistic_dict(avg_flow_statistic_dict: Union[None, Dict[str, List[AvgFlowStatistic]]]) \
            -> List[cluster_manager_pb2.AvgFlowStatisticDict]:
        """
        Converts a dict to list of AvgFlowStatisticDict

        :param avg_flow_statistic_dict: the dict to convert
        :return: the converted objected
        """
        if avg_flow_statistic_dict is None:
            return ClusterManagerUtil.get_empty_avg_flow_statistic_dict()
        else:
            avg_flow_statistic_dict_list = []
            for k, v in avg_flow_statistic_dict.items():
                avg_flow_statistic_dict_list.append(cluster_manager_pb2.AvgFlowStatisticDict(
                    key=k, dtos=list(map(lambda x: ClusterManagerUtil.convert_avg_flow_statistic_dto(x), v))))
            return avg_flow_statistic_dict_list

    @staticmethod
    def convert_avg_flow_statistic_dict_reverse(
            avg_flow_statistics_dict: Union[None, List[cluster_manager_pb2.AvgFlowStatisticDict]]) \
            -> Dict[str, List[AvgFlowStatistic]]:
        """
        Converts a list of AvgFlowStatisticDict to a dict

        :param avg_flow_statistics_dict: the list to convert
        :return: the converted DTO
        """
        if avg_flow_statistics_dict is None:
            return ClusterManagerUtil.convert_avg_flow_statistic_dict_reverse(
                ClusterManagerUtil.get_empty_avg_flow_statistic_dict())
        else:
            d: Dict[str, Any] = {}
            for ds in avg_flow_statistics_dict:
                d[ds.key] = list(map(lambda x: ClusterManagerUtil.convert_avg_flow_statistic_dto_reverse(x), ds.dtos))
            return d

    @staticmethod
    def get_empty_avg_flow_statistic_dict() -> List[cluster_manager_pb2.AvgFlowStatisticDict]:
        """
        Gets an empty list of AvgFlowStatisticDict

        :return: an empty list of AvgFlowStatisticDict
        """
        return []

    @staticmethod
    def avg_flow_statistics_dict_to_dict(
            avg_flow_statistics_dict: cluster_manager_pb2.AvgFlowStatisticDict) -> Dict[str, Any]:
        """
        Converts a DTO to a dict

        :param avg_flow_statistics_dict: the DTO to convert
        :return: the dict
        """
        d: Dict[str, Any] = {}
        d["key"] = avg_flow_statistics_dict.key
        dtos = []
        for dto in avg_flow_statistics_dict.dtos:
            dtos.append(ClusterManagerUtil.avg_flow_statistic_dto_to_dict(dto))
        d["dtos"] = dtos
        return d

    @staticmethod
    def convert_agg_flow_statistic_dict(agg_flow_statistic_dict: Union[None, Dict[str, List[AggFlowStatistic]]]) \
            -> List[cluster_manager_pb2.AggFlowStatisticDict]:
        """
        Converts a dict to list of AggFlowStatisticDict

        :param agg_flow_statistic_dict: the dict to convert
        :return: the converted objected
        """
        if agg_flow_statistic_dict is None:
            return ClusterManagerUtil.get_empty_agg_flow_statistic_dict()
        else:
            agg_flow_statistic_dict_list = []
            for k, v in agg_flow_statistic_dict.items():
                agg_flow_statistic_dict_list.append(cluster_manager_pb2.AggFlowStatisticDict(
                    key=k, dtos=list(map(lambda x: ClusterManagerUtil.convert_agg_flow_statistic_dto(x), v))))
            return agg_flow_statistic_dict_list

    @staticmethod
    def convert_agg_flow_statistic_dict_reverse(
            agg_flow_statistics_dict: Union[None, List[cluster_manager_pb2.AggFlowStatisticDict]]) \
            -> Dict[str, List[AggFlowStatistic]]:
        """
        Converts a list of AggFlowStatisticDict to a dict

        :param agg_flow_statistics_dict: the list to convert
        :return: the converted DTO
        """
        if agg_flow_statistics_dict is None:
            return ClusterManagerUtil.convert_agg_flow_statistic_dict_reverse(
                ClusterManagerUtil.get_empty_agg_flow_statistic_dict())
        else:
            d: Dict[str, Any] = {}
            for ds in agg_flow_statistics_dict:
                d[ds.key] = list(map(lambda x: ClusterManagerUtil.convert_agg_flow_statistic_dto_reverse(x), ds.dtos))
            return d

    @staticmethod
    def get_empty_agg_flow_statistic_dict() -> List[cluster_manager_pb2.AggFlowStatisticDict]:
        """
        Gets an empty list of AggFlowStatisticDict
        :return: an empty list of AggFlowStatisticDict
        """
        return []

    @staticmethod
    def agg_flow_statistics_dict_to_dict(
            agg_flow_statistics_dict: cluster_manager_pb2.AggFlowStatisticDict) -> Dict[str, Any]:
        """
        Converts a DTO to a dict

        :param agg_flow_statistics_dict: the DTO to convert
        :return: the dict
        """
        d: Dict[str, Any] = {}
        d["key"] = agg_flow_statistics_dict.key
        dtos = []
        for dto in agg_flow_statistics_dict.dtos:
            dtos.append(ClusterManagerUtil.agg_flow_statistic_dto_to_dict(dto))
        d["dtos"] = dtos
        return d

    @staticmethod
    def convert_avg_port_statistic_dict(avg_port_statistic_dict: Union[None, Dict[str, List[AvgPortStatistic]]]) \
            -> List[cluster_manager_pb2.AvgPortStatisticDict]:
        """
        Converts a dict to list of AvgPortStatisticDict

        :param avg_port_statistic_dict: the dict to convert
        :return: the converted objected
        """
        if avg_port_statistic_dict is None:
            return ClusterManagerUtil.get_empty_avg_port_statistic_dict()
        else:
            avg_port_statistic_dict_list = []
            for k, v in avg_port_statistic_dict.items():
                avg_port_statistic_dict_list.append(cluster_manager_pb2.AvgPortStatisticDict(
                    key=k, dtos=list(map(lambda x: ClusterManagerUtil.convert_avg_port_statistic_dto(x), v))))
            return avg_port_statistic_dict_list

    @staticmethod
    def convert_avg_port_statistic_dict_reverse(
            avg_port_statistics_dict: Union[None, List[cluster_manager_pb2.AvgPortStatisticDict]]) \
            -> Dict[str, List[AvgPortStatistic]]:
        """
        Converts a list of AvgPortStatisticDict to a dict

        :param avg_port_statistics_dict: the list to convert
        :return: the converted DTO
        """
        if avg_port_statistics_dict is None:
            return ClusterManagerUtil.convert_avg_port_statistic_dict_reverse(
                ClusterManagerUtil.get_empty_avg_port_statistic_dict())
        else:
            d: Dict[str, Any] = {}
            for ds in avg_port_statistics_dict:
                d[ds.key] = list(map(lambda x: ClusterManagerUtil.convert_avg_port_statistic_dto_reverse(x), ds.dtos))
            return d

    @staticmethod
    def get_empty_avg_port_statistic_dict() -> List[cluster_manager_pb2.AvgPortStatisticDict]:
        """
        Gets an empty list of AvgPortStatisticDict

        :return: an empty list of AvgPortStatisticDict
        """
        return []

    @staticmethod
    def avg_port_statistics_dict_to_dict(
            avg_port_statistics_dict: cluster_manager_pb2.AvgPortStatisticDict) -> Dict[str, Any]:
        """
        Converts a DTO to a dict

        :param avg_port_statistics_dict: the DTO to convert
        :return: the dict
        """
        d: Dict[str, Any] = {}
        d["key"] = avg_port_statistics_dict.key
        dtos = []
        for dto in avg_port_statistics_dict.dtos:
            dtos.append(ClusterManagerUtil.avg_port_statistic_dto_to_dict(dto))
        d["dtos"] = dtos
        return d

    @staticmethod
    def get_empty_emulation_metrics_time_series_dto() -> cluster_manager_pb2.EmulationMetricsTimeSeriesDTO:
        """
        Gets an empty emulation metric series dto

        :return: an empty EmulationMetricsTimeSeriesDTO
        """
        return cluster_manager_pb2.EmulationMetricsTimeSeriesDTO(
            client_metrics=[ClusterManagerUtil.get_empty_client_population_metrics_dto()],
            aggregated_docker_stats=[ClusterManagerUtil.get_empty_docker_stats_dto()],
            docker_host_stats=ClusterManagerUtil.get_empty_docker_stats_dict(),
            host_metrics=ClusterManagerUtil.get_empty_host_metrics_dict(),
            aggregated_host_metrics=[ClusterManagerUtil.get_empty_host_metrics_dto()],
            defender_actions=[ClusterManagerUtil.get_empty_emulation_defender_action_dto()],
            attacker_actions=[ClusterManagerUtil.get_empty_emulation_attacker_action_dto()],
            agg_snort_ids_metrics=[ClusterManagerUtil.get_empty_snort_ids_alert_counters_dto()],
            emulation_id=-1,
            ossec_host_alert_counters=ClusterManagerUtil.get_empty_ossec_ids_alert_counters_dict(),
            aggregated_ossec_host_alert_counters=[ClusterManagerUtil.get_empty_ossec_ids_alert_counters_dto()],
            openflow_flow_stats=[ClusterManagerUtil.get_empty_flow_statistic_dto()],
            openflow_port_stats=[ClusterManagerUtil.get_empty_port_statistic_dto()],
            avg_openflow_flow_stats=[ClusterManagerUtil.get_empty_avg_flow_statistic_dto()],
            avg_openflow_port_stats=[ClusterManagerUtil.get_empty_avg_port_statistic_dto()],
            openflow_flow_metrics_per_switch=ClusterManagerUtil.get_empty_flow_statistic_dict(),
            openflow_port_metrics_per_switch=ClusterManagerUtil.get_empty_port_statistic_dict(),
            openflow_flow_avg_metrics_per_switch=ClusterManagerUtil.get_empty_avg_flow_statistic_dict(),
            openflow_port_avg_metrics_per_switch=ClusterManagerUtil.get_empty_avg_port_statistic_dict(),
            agg_openflow_flow_metrics_per_switch=ClusterManagerUtil.get_empty_agg_flow_statistic_dict(),
            agg_openflow_flow_stats=[ClusterManagerUtil.get_empty_agg_flow_statistic_dto()],
            agg_snort_ids_rule_metrics=[ClusterManagerUtil.get_empty_snort_ids_rule_counters_dto()],
            snort_ids_ip_metrics=ClusterManagerUtil.get_empty_snort_ids_ip_alert_counters_dict(),
            snort_alert_metrics_per_ids=ClusterManagerUtil.get_empty_snort_ids_alert_counters_dict(),
            snort_rule_metrics_per_ids=ClusterManagerUtil.get_empty_snort_ids_rule_counters_dict()
        )

    @staticmethod
    def convert_emulation_metrics_time_series_dto(time_series_dto: EmulationMetricsTimeSeries) \
            -> cluster_manager_pb2.EmulationMetricsTimeSeriesDTO:
        """
        Converts a EmulationMetricsTimeSeries to a EmulationMetricsTimeSeriesDTO

        :param time_series_dto: the dict to convert
        :return: the converted objected
        """
        if time_series_dto is None:
            return ClusterManagerUtil.get_empty_emulation_metrics_time_series_dto()
        else:
            return cluster_manager_pb2.EmulationMetricsTimeSeriesDTO(
                client_metrics=list(map(lambda x: ClusterManagerUtil.convert_client_population_metrics_dto(x),
                                        time_series_dto.client_metrics)),
                aggregated_docker_stats=list(map(lambda x: ClusterManagerUtil.convert_docker_stats_dto(x),
                                                 time_series_dto.aggregated_docker_stats)),
                docker_host_stats=ClusterManagerUtil.convert_docker_stats_dict(time_series_dto.docker_host_stats),
                host_metrics=ClusterManagerUtil.convert_host_metrics_dict(time_series_dto.host_metrics),
                aggregated_host_metrics=list(map(lambda x: ClusterManagerUtil.convert_host_metrics_dto(x),
                                                 time_series_dto.aggregated_host_metrics)),
                defender_actions=list(map(lambda x: ClusterManagerUtil.convert_emulation_defender_action_dto(x),
                                          time_series_dto.defender_actions)),
                attacker_actions=list(map(lambda x: ClusterManagerUtil.convert_emulation_attacker_action_dto(x),
                                          time_series_dto.attacker_actions)),
                agg_snort_ids_metrics=list(map(lambda x: ClusterManagerUtil.convert_snort_ids_alert_counters_dto(x),
                                               time_series_dto.agg_snort_ids_metrics)),
                emulation_id=time_series_dto.emulation_env_config.id,
                ossec_host_alert_counters=ClusterManagerUtil.convert_ossec_ids_alert_counters_dict(
                    time_series_dto.ossec_host_alert_counters),
                aggregated_ossec_host_alert_counters=list(
                    map(lambda x: ClusterManagerUtil.convert_ossec_ids_alert_counters_dto(x),
                        time_series_dto.aggregated_ossec_host_alert_counters)),
                openflow_flow_stats=list(map(lambda x: ClusterManagerUtil.convert_flow_statistics_dto(x),
                                             time_series_dto.openflow_flow_stats)),
                openflow_port_stats=list(map(lambda x: ClusterManagerUtil.convert_port_statistics_dto(x),
                                             time_series_dto.openflow_port_stats)),
                avg_openflow_flow_stats=list(map(lambda x: ClusterManagerUtil.convert_avg_flow_statistic_dto(x),
                                                 time_series_dto.avg_openflow_flow_stats)),
                avg_openflow_port_stats=list(map(lambda x: ClusterManagerUtil.convert_avg_port_statistic_dto(x),
                                                 time_series_dto.avg_openflow_port_stats)),
                openflow_flow_metrics_per_switch=ClusterManagerUtil.convert_flow_statistic_dict(
                    time_series_dto.openflow_flow_metrics_per_switch),
                openflow_port_metrics_per_switch=ClusterManagerUtil.convert_port_statistic_dict(
                    time_series_dto.openflow_port_metrics_per_switch),
                openflow_flow_avg_metrics_per_switch=ClusterManagerUtil.convert_avg_flow_statistic_dict(
                    time_series_dto.openflow_flow_avg_metrics_per_switch),
                openflow_port_avg_metrics_per_switch=ClusterManagerUtil.convert_avg_port_statistic_dict(
                    time_series_dto.openflow_port_avg_metrics_per_switch),
                agg_openflow_flow_metrics_per_switch=ClusterManagerUtil.convert_agg_flow_statistic_dict(
                    time_series_dto.agg_openflow_flow_metrics_per_switch),
                agg_openflow_flow_stats=list(map(lambda x: ClusterManagerUtil.convert_agg_flow_statistic_dto(x),
                                                 time_series_dto.agg_openflow_flow_stats)),
                agg_snort_ids_rule_metrics=list(map(lambda x: ClusterManagerUtil.convert_snort_ids_rule_counters_dto(x),
                                                    time_series_dto.agg_snort_ids_rule_metrics)),
                snort_ids_ip_metrics=ClusterManagerUtil.convert_snort_ids_ip_alert_counters_dict(
                    time_series_dto.snort_ids_ip_metrics),
                snort_rule_metrics_per_ids=ClusterManagerUtil.convert_snort_ids_rule_counters_dict(
                    time_series_dto.snort_rule_metrics_per_ids),
                snort_alert_metrics_per_ids=ClusterManagerUtil.convert_snort_ids_alert_counters_dict(
                    time_series_dto.snort_alert_metrics_per_ids)
            )

    @staticmethod
    def convert_emulation_metrics_time_series_dto_reverse(
            time_series_dto: Union[None, cluster_manager_pb2.EmulationMetricsTimeSeriesDTO]) \
            -> EmulationMetricsTimeSeries:
        """
        Converts a EmulationMetricsTimeSeriesDTO to a EmulationMetricsTimeSeries

        :param time_series_dto: the DTO to convert
        :return: the converted DTO
        """
        if time_series_dto is None:
            return ClusterManagerUtil.convert_emulation_metrics_time_series_dto_reverse(
                ClusterManagerUtil.get_empty_emulation_metrics_time_series_dto())
        else:
            emulation_config = MetastoreFacade.get_emulation(id=time_series_dto.emulation_id)
            return EmulationMetricsTimeSeries(
                client_metrics=list(map(lambda x: ClusterManagerUtil.convert_client_population_metrics_dto_reverse(x),
                                        time_series_dto.client_metrics)),
                aggregated_docker_stats=list(map(lambda x: ClusterManagerUtil.convert_docker_stats_dto_reverse(x),
                                                 time_series_dto.aggregated_docker_stats)),
                docker_host_stats=ClusterManagerUtil.convert_docker_stats_dict_reverse(
                    list(time_series_dto.docker_host_stats)),
                host_metrics=ClusterManagerUtil.convert_host_metrics_dict_reverse(list(time_series_dto.host_metrics)),
                aggregated_host_metrics=list(map(lambda x: ClusterManagerUtil.convert_host_metrics_dto_reverse(x),
                                                 list(time_series_dto.aggregated_host_metrics))),
                defender_actions=list(map(lambda x: ClusterManagerUtil.convert_emulation_defender_action_dto_reverse(x),
                                          list(time_series_dto.defender_actions))),
                attacker_actions=list(map(lambda x: ClusterManagerUtil.convert_emulation_attacker_action_dto_reverse(x),
                                          list(time_series_dto.attacker_actions))),
                agg_snort_ids_metrics=list(
                    map(lambda x: ClusterManagerUtil.convert_snort_ids_alert_counters_dto_reverse(x),
                        list(time_series_dto.agg_snort_ids_metrics))),
                emulation_env_config=emulation_config,
                ossec_host_alert_counters=ClusterManagerUtil.convert_ossec_ids_alert_counters_dict_reverse(
                    list(time_series_dto.ossec_host_alert_counters)),
                aggregated_ossec_host_alert_counters=list(
                    map(lambda x: ClusterManagerUtil.convert_ossec_ids_alert_counters_dto_reverse(x),
                        list(time_series_dto.aggregated_ossec_host_alert_counters))),
                openflow_flow_stats=list(map(lambda x: ClusterManagerUtil.convert_flow_statistic_dto_reverse(x),
                                             list(time_series_dto.openflow_flow_stats))),
                openflow_port_stats=list(map(lambda x: ClusterManagerUtil.convert_port_statistic_dto_reverse(x),
                                             list(time_series_dto.openflow_port_stats))),
                avg_openflow_flow_stats=list(map(lambda x: ClusterManagerUtil.convert_avg_flow_statistic_dto_reverse(x),
                                                 list(time_series_dto.avg_openflow_flow_stats))),
                avg_openflow_port_stats=list(map(lambda x: ClusterManagerUtil.convert_avg_port_statistic_dto_reverse(x),
                                                 list(time_series_dto.avg_openflow_port_stats))),
                openflow_flow_metrics_per_switch=ClusterManagerUtil.convert_flow_statistic_dict_reverse(
                    list(time_series_dto.openflow_flow_metrics_per_switch)),
                openflow_port_metrics_per_switch=ClusterManagerUtil.convert_port_statistic_dict_reverse(
                    list(time_series_dto.openflow_port_metrics_per_switch)),
                openflow_flow_avg_metrics_per_switch=ClusterManagerUtil.convert_avg_flow_statistic_dict_reverse(
                    list(time_series_dto.openflow_flow_avg_metrics_per_switch)),
                openflow_port_avg_metrics_per_switch=ClusterManagerUtil.convert_avg_port_statistic_dict_reverse(
                    list(time_series_dto.openflow_port_avg_metrics_per_switch)),
                agg_openflow_flow_metrics_per_switch=ClusterManagerUtil.convert_agg_flow_statistic_dict_reverse(
                    list(time_series_dto.agg_openflow_flow_metrics_per_switch)),
                agg_openflow_flow_stats=list(map(lambda x: ClusterManagerUtil.convert_agg_flow_statistic_dto_reverse(x),
                                                 list(time_series_dto.agg_openflow_flow_stats))),
                agg_snort_ids_rule_metrics=list(
                    map(lambda x: ClusterManagerUtil.convert_snort_ids_rule_counters_dto_reverse(x),
                        list(time_series_dto.agg_snort_ids_rule_metrics))),
                snort_ids_ip_metrics=ClusterManagerUtil.convert_snort_ids_ip_alert_counters_dict_reverse(
                    list(time_series_dto.snort_ids_ip_metrics)),
                snort_rule_metrics_per_ids=ClusterManagerUtil.convert_snort_ids_rule_counters_dict_reverse(
                    list(time_series_dto.snort_rule_metrics_per_ids)),
                snort_alert_metrics_per_ids=ClusterManagerUtil.convert_snort_ids_alert_counters_dict_reverse(
                    list(time_series_dto.snort_alert_metrics_per_ids))
            )

    @staticmethod
    def emulation_metrics_time_series_dto_to_dict(time_series_dto: cluster_manager_pb2.EmulationMetricsTimeSeriesDTO) \
            -> Dict[str, Any]:
        """
        Converts a EmulationMetricsTimeSeriesDTO to a dict

        :param time_series_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["client_metrics"] = list(map(lambda x: ClusterManagerUtil.client_population_metrics_dto_to_dict(x),
                                       time_series_dto.client_metrics))
        d["aggregated_docker_stats"] = list(map(lambda x: ClusterManagerUtil.docker_stats_dto_to_dict(x),
                                                time_series_dto.aggregated_docker_stats))
        d["docker_host_stats"] = list(map(lambda x: ClusterManagerUtil.docker_stats_dict_to_dict(x),
                                          time_series_dto.docker_host_stats))
        d["host_metrics"] = list(map(lambda x: ClusterManagerUtil.host_metrics_dict_to_dict(x),
                                     time_series_dto.host_metrics))
        d["aggregated_host_metrics"] = list(map(lambda x: ClusterManagerUtil.host_metrics_dto_to_dict(x),
                                                time_series_dto.aggregated_host_metrics))
        d["defender_actions"] = list(map(lambda x: ClusterManagerUtil.emulation_defender_action_dto_to_dict(x),
                                         time_series_dto.defender_actions))
        d["attacker_actions"] = list(map(lambda x: ClusterManagerUtil.emulation_attacker_action_dto_to_dict(x),
                                         time_series_dto.attacker_actions))
        d["agg_snort_ids_metrics"] = list(map(lambda x: ClusterManagerUtil.snort_ids_alert_counters_dto_to_dict(x),
                                              time_series_dto.agg_snort_ids_metrics))
        d["emulation_id"] = time_series_dto.emulation_id
        d["ossec_host_alert_counters"] = list(map(lambda x: ClusterManagerUtil.ossec_ids_alert_counters_dict_to_dict(x),
                                                  time_series_dto.ossec_host_alert_counters))
        d["aggregated_ossec_host_alert_counters"] = list(
            map(lambda x: ClusterManagerUtil.ossec_ids_alert_counters_dto_to_dict(x),
                time_series_dto.aggregated_ossec_host_alert_counters))
        d["openflow_flow_stats"] = list(map(lambda x: ClusterManagerUtil.flow_statistic_dto_to_dict(x),
                                            time_series_dto.openflow_flow_stats))
        d["openflow_port_stats"] = list(map(lambda x: ClusterManagerUtil.port_statistic_dto_to_dict(x),
                                            time_series_dto.openflow_port_stats))
        d["avg_openflow_flow_stats"] = list(map(lambda x: ClusterManagerUtil.avg_flow_statistic_dto_to_dict(x),
                                                time_series_dto.avg_openflow_flow_stats))
        d["avg_openflow_port_stats"] = list(map(lambda x: ClusterManagerUtil.avg_port_statistic_dto_to_dict(x),
                                                time_series_dto.avg_openflow_port_stats))
        d["openflow_flow_metrics_per_switch"] = list(map(lambda x: ClusterManagerUtil.flow_statistics_dict_to_dict(x),
                                                         time_series_dto.openflow_flow_metrics_per_switch))
        d["openflow_port_metrics_per_switch"] = list(map(lambda x: ClusterManagerUtil.port_statistics_dict_to_dict(x),
                                                         time_series_dto.openflow_port_metrics_per_switch))
        d["openflow_flow_avg_metrics_per_switch"] = list(
            map(lambda x: ClusterManagerUtil.avg_flow_statistics_dict_to_dict(x),
                time_series_dto.openflow_flow_avg_metrics_per_switch))
        d["openflow_port_avg_metrics_per_switch"] = list(
            map(lambda x: ClusterManagerUtil.avg_port_statistics_dict_to_dict(x),
                time_series_dto.openflow_port_avg_metrics_per_switch))
        d["agg_openflow_flow_metrics_per_switch"] = list(
            map(lambda x: ClusterManagerUtil.agg_flow_statistics_dict_to_dict(x),
                time_series_dto.agg_openflow_flow_metrics_per_switch))
        d["agg_openflow_flow_stats"] = list(map(lambda x: ClusterManagerUtil.agg_flow_statistic_dto_to_dict(x),
                                                time_series_dto.agg_openflow_flow_stats))
        d["agg_snort_ids_rule_metrics"] = list(map(lambda x: ClusterManagerUtil.snort_ids_rule_counters_dto_to_dict(x),
                                                   time_series_dto.agg_snort_ids_rule_metrics))
        d["snort_ids_ip_metrics"] = list(map(lambda x: ClusterManagerUtil.snort_ids_ip_alert_counters_dict_to_dict(x),
                                             time_series_dto.snort_ids_ip_metrics))
        d["snort_rule_metrics_per_ids"] = list(map(lambda x: ClusterManagerUtil.snort_ids_rule_counters_dict_to_dict(x),
                                                   time_series_dto.snort_rule_metrics_per_ids))
        d["snort_alert_metrics_per_ids"] = list(
            map(lambda x: ClusterManagerUtil.snort_ids_alert_counters_dict_to_dict(x),
                time_series_dto.snort_alert_metrics_per_ids))
        return d
