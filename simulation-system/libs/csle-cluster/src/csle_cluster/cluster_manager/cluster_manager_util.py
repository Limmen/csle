from typing import Dict, Any, List
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.controllers.container_controller import ContainerController
import csle_cluster.cluster_manager.cluster_manager_pb2
import csle_collector.client_manager.client_manager_pb2


class ClusterManagerUtil:
    """
    Class with utility functions related to the cluster manager
    """

    @staticmethod
    def get_empty_client_managers_info_dto() -> csle_cluster.cluster_manager.cluster_manager_pb2.ClientManagersInfoDTO:
        """
        :return: an empty ClientManagersInfoDTO
        """
        return csle_cluster.cluster_manager.cluster_manager_pb2.ClientManagersInfoDTO(
            ips = [], ports = [], emulationName = "", executionId = -1, clientManagersRunning = [],
            clientManagersStatuses = [])

    @staticmethod
    def get_empty_get_num_clients_dto() -> csle_cluster.cluster_manager.cluster_manager_pb2.GetNumActiveClientsMsg:
        """
        :return: an empty GetNumClientsDTO
        """
        return csle_cluster.cluster_manager.cluster_manager_pb2.GetNumClientsDTO(
            num_clients=0,
            client_process_active =False,
            producer_active = False,
            clients_time_step_len_seconds = 0,
            producer_time_step_len_seconds = 0
        )

    @staticmethod
    def convert_client_dto_to_get_num_clients_dto(
            clients_dto: csle_collector.client_manager.client_manager_pb2.ClientsDTO) -> \
            csle_cluster.cluster_manager.cluster_manager_pb2.GetNumActiveClientsMsg:
        """
        Converts a clients DTO to a GetNumClientsDTO

        :param clients_dto: the clients DTO to convert
        :return: the converted DTO
        """
        return csle_cluster.cluster_manager.cluster_manager_pb2.GetNumClientsDTO(
            num_clients=clients_dto.num_clients,
            client_process_active = clients_dto.client_process_active,
            producer_active = clients_dto.producer_active,
            clients_time_step_len_seconds = clients_dto.clients_time_step_len_seconds,
            producer_time_step_len_seconds = clients_dto.producer_time_step_len_seconds
        )

    @staticmethod
    def node_status_dto_to_dict(node_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO) \
            -> Dict[str, Any]:
        """
        Converts a NodeStatusDTO to a dict

        :param node_status_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
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
    def service_status_dto_to_dict(node_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO) \
            -> Dict[str, Any]:
        """
        Converts a ServiceStatusDTO to a dict

        :param node_status_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["running"] = node_status_dto.running
        return d

    @staticmethod
    def logs_dto_to_dict(logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO) \
            -> Dict[str, Any]:
        """
        Converts a LogsDTO to a dict

        :param logs_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["logs"] = list(logs_dto.logs)
        return d

    @staticmethod
    def get_num_clients_dto_to_dict(
            get_num_clients_dto: csle_cluster.cluster_manager.cluster_manager_pb2.GetNumClientsDTO) -> Dict[str, Any]:
        """
        Converts a GetNumClientsDTO to a dict

        :param get_num_clients_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
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
        active_ips = []
        for container in running_containers:
            active_ips = active_ips + container.get_ips()
        active_ips.append(constants.COMMON.LOCALHOST)
        active_ips.append(constants.COMMON.LOCALHOST_127_0_0_1)
        active_ips.append(constants.COMMON.LOCALHOST_127_0_1_1)
        return active_ips