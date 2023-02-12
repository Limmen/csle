from typing import Dict, Any
import csle_cluster.cluster_manager.cluster_manager_pb2


class ClusterManagerUtil:
    """
    Class with utility functions related to the cluster manager
    """

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
