from typing import Dict, Any
import grpc
import csle_cluster.cluster_manager.cluster_manager_pb2_grpc
import csle_cluster.cluster_manager.cluster_manager_pb2
import csle_cluster.cluster_manager.query_cluster_manager
from csle_cluster.cluster_manager.cluster_manager_util import ClusterManagerUtil


class ClusterController:
    """
    Controller managing API calls to cluster managers
    """

    @staticmethod
    def is_cluster_manager_running(ip: str, port: int, timeout_sec: int = 2) -> bool:
        """
        Utility function for checking if the cluster manager gRPC server is running on a given node

        :param ip: ip of the node
        :param port: port of the gRPC server
        :param timeout_sec: timeout in seconds
        :return: True if it is running, otherwise False.
        """
        channel = grpc.insecure_channel(f'{ip}:{port}')
        try:
            grpc.channel_ready_future(channel).result(timeout=timeout_sec)
            return True
        except grpc.FutureTimeoutError:
            return False

    @staticmethod
    def get_node_status(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Gets the status of a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.get_node_status(stub)
            return node_status_dto

    @staticmethod
    def start_postgresql(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts PostgreSQL on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_postgresql(stub)
            return service_status_dto

    @staticmethod
    def start_cadvisor(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts cAdvisor on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_cadvisor(stub)
            return service_status_dto

    @staticmethod
    def start_node_exporter(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Node exporter on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_node_exporter(stub)
            return service_status_dto

    @staticmethod
    def start_grafana(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Grafana on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_grafana(stub)
            return service_status_dto

    @staticmethod
    def start_prometheus(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Prometheus on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_prometheus(stub)
            return service_status_dto

    @staticmethod
    def start_pgadmin(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts pgAdmin on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_pgadmin(stub)
            return service_status_dto

    @staticmethod
    def start_nginx(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts nginx on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_nginx(stub)
            return service_status_dto

    @staticmethod
    def start_flask(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Flask on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_flask(stub)
            return service_status_dto

    @staticmethod
    def start_docker_statsmanager(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Docker statsmanager on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_docker_statsmanager(stub)
            return service_status_dto

    @staticmethod
    def start_docker_engine(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Docker engine on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_docker_engine(stub)
            return service_status_dto

    @staticmethod
    def stop_postgresql(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts PostgreSQL on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_postgresql(stub)
            return service_status_dto

    @staticmethod
    def stop_cadvisor(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts cAdvisor on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_cadvisor(stub)
            return service_status_dto

    @staticmethod
    def stop_node_exporter(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Node exporter on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_node_exporter(stub)
            return service_status_dto

    @staticmethod
    def stop_grafana(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Grafana on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_grafana(stub)
            return service_status_dto

    @staticmethod
    def stop_prometheus(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Prometheus on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_prometheus(stub)
            return service_status_dto

    @staticmethod
    def stop_pgadmin(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts pgAdmin on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_pgadmin(stub)
            return service_status_dto

    @staticmethod
    def stop_nginx(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts nginx on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_nginx(stub)
            return service_status_dto

    @staticmethod
    def stop_flask(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Flask on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_flask(stub)
            return service_status_dto

    @staticmethod
    def stop_docker_statsmanager(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Docker statsmanager on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_docker_statsmanager(stub)
            return service_status_dto

    @staticmethod
    def stop_docker_engine(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Docker engine on a cluster node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_docker_engine(stub)
            return service_status_dto

    @staticmethod
    def get_csle_log_files(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets a list of log files in the CSLE log directory

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_csle_log_files(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_docker_statsmanager_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the docker statsmanager logs

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_docker_statsmanager_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_prometheus_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the Prometheus logs

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_prometheus_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_node_exporter_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the node exporter logs

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_node_exporter_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_cadvisor_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the cadvisor logs

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_cadvisor_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_pgadmin_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the pgAdming logs

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_pgadmin_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_grafana_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the Grafana logs

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_grafana_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_nginx_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the Nginx logs

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_nginx_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_docker_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the Docker logs

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_docker_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_postgresql_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the PostgreSQL logs

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_postgresql_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_flask_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the Flask logs

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_flask_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_log_file(ip: str, port: int, log_file_name: str) -> Dict[str, Any]:
        """
        Gets a specific log file from a node

        :param ip: the ip of the node
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_log_file(stub,
                                                                                       log_file_name=log_file_name)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)