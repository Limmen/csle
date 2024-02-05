from typing import Dict, Any, List
import grpc
import time
import csle_common.constants.constants as constants
from csle_common.logging.log import Logger
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.emulation_env_controller import EmulationEnvController
from csle_common.dao.emulation_config.emulation_metrics_time_series import EmulationMetricsTimeSeries
import csle_cluster.cluster_manager.cluster_manager_pb2_grpc
import csle_cluster.cluster_manager.cluster_manager_pb2
import csle_cluster.cluster_manager.query_cluster_manager
from csle_cluster.cluster_manager.cluster_manager_util import ClusterManagerUtil
from csle_common.dao.emulation_config.emulation_execution_info import EmulationExecutionInfo


class ClusterController:
    """
    Controller managing API calls to cluster managers
    """

    @staticmethod
    def start_containers_in_execution(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the containers of a given execution

        :param ip: the ip of the node where to start the containers
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_containers_in_execution(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def attach_containers_in_execution_to_networks(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to attach the containers of a given execution to networks

        :param ip: the ip of the node where to attach the containers
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = \
                csle_cluster.cluster_manager.query_cluster_manager.attach_containers_in_execution_to_networks(
                    stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
                )
            return operation_outcome_dto

    @staticmethod
    def is_cluster_manager_running(ip: str, port: int, timeout_sec: int = 2) -> bool:
        """
        Utility function for checking if the cluster manager gRPC server is running on a given node

        :param ip: ip of the node
        :param port: port of the gRPC server
        :param timeout_sec: timeout in seconds
        :return: True if it is running, otherwise False.
        """
        channel = grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        try:
            grpc.channel_ready_future(channel).result(timeout=timeout_sec)
            return True
        except grpc.FutureTimeoutError:
            return False

    @staticmethod
    def get_node_status(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Gets the status of a cluster node

        :param ip: the ip of the node to get the status
        :param port: the port of the cluster manager
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.get_node_status(stub)
            return node_status_dto

    @staticmethod
    def start_postgresql(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts PostgreSQL on a cluster node

        :param ip: the ip of the node to start PostgreSQL
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_postgresql(stub)
            return service_status_dto

    @staticmethod
    def start_cadvisor(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts cAdvisor on a cluster node

        :param ip: the ip of the node to start cAdvisor
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_cadvisor(stub)
            return service_status_dto

    @staticmethod
    def start_node_exporter(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Node exporter on a cluster node

        :param ip: the ip of the node to start node exporter
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_node_exporter(stub)
            return service_status_dto

    @staticmethod
    def start_grafana(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Grafana on a cluster node

        :param ip: the ip of the node to start Grafana
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_grafana(stub)
            return service_status_dto

    @staticmethod
    def start_prometheus(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Prometheus on a cluster node

        :param ip: the ip of the node to start Prometheus
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_prometheus(stub)
            return service_status_dto

    @staticmethod
    def start_pgadmin(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts pgAdmin on a cluster node

        :param ip: the ip of the node to start pgAdmin
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_pgadmin(stub)
            return service_status_dto

    @staticmethod
    def start_nginx(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts nginx on a cluster node

        :param ip: the ip of the node to start Nginx
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_nginx(stub)
            return service_status_dto

    @staticmethod
    def start_flask(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Flask on a cluster node

        :param ip: the ip of the node to start flask
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_flask(stub)
            return service_status_dto

    @staticmethod
    def start_docker_statsmanager(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Docker statsmanager on a cluster node

        :param ip: the ip of the node to start the docker statsmanager
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_docker_statsmanager(stub)
            return service_status_dto

    @staticmethod
    def start_docker_engine(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops Docker engine on a cluster node

        :param ip: the ip of the node to stop the docker engine
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_docker_engine(stub)
            return service_status_dto

    @staticmethod
    def stop_postgresql(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops PostgreSQL on a cluster node

        :param ip: the ip of the node to stop PostgreSQL
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_postgresql(stub)
            return service_status_dto

    @staticmethod
    def stop_cadvisor(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops cAdvisor on a cluster node

        :param ip: the ip of the node to stop cAdvisor
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_cadvisor(stub)
            return service_status_dto

    @staticmethod
    def stop_node_exporter(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops Node exporter on a cluster node

        :param ip: the ip of the node to stop node exporter
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_node_exporter(stub)
            return service_status_dto

    @staticmethod
    def stop_grafana(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops Grafana on a cluster node

        :param ip: the ip of the node to stop Grafana
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_grafana(stub)
            return service_status_dto

    @staticmethod
    def stop_prometheus(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops Prometheus on a cluster node

        :param ip: the ip of the node to stop Prometheus
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_prometheus(stub)
            return service_status_dto

    @staticmethod
    def stop_pgadmin(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops pgAdmin on a cluster node

        :param ip: the ip of the node to stop pgAdmin
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_pgadmin(stub)
            return service_status_dto

    @staticmethod
    def stop_nginx(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops nginx on a cluster node

        :param ip: the ip of the node to stop Nginx
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_nginx(stub)
            return service_status_dto

    @staticmethod
    def stop_flask(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops Flask on a cluster node

        :param ip: the ip of the node to stop flask
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_flask(stub)
            return service_status_dto

    @staticmethod
    def stop_docker_statsmanager(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops Docker statsmanager on a cluster node

        :param ip: the ip of the node to stop the statsmanager
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_docker_statsmanager(stub)
            return service_status_dto

    @staticmethod
    def stop_docker_engine(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops Docker engine on a cluster node

        :param ip: the ip of the node to stop the docker engine
        :param port: the port of the cluster manager
        :return: The status of the service
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            service_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_docker_engine(stub)
            return service_status_dto

    @staticmethod
    def get_csle_log_files(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets a list of log files in the CSLE log directory

        :param ip: the ip of the node to get the CSLE logs from
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_csle_log_files(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_docker_statsmanager_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the docker statsmanager logs

        :param ip: the ip of the node to get the Docker statsmanager logs from
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_docker_statsmanager_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_prometheus_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the Prometheus logs

        :param ip: the ip of the node to get the Prometheus logs from
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_prometheus_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_node_exporter_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the node exporter logs

        :param ip: the ip of the node to get the node exporter logs from
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_node_exporter_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_cadvisor_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the cadvisor logs

        :param ip: the ip of the node to get the cAdvisor logs from
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_cadvisor_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_pgadmin_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the pgAdming logs

        :param ip: the ip of the node to get the pgAdmin logs from
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_pgadmin_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_grafana_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the Grafana logs

        :param ip: the ip of the node to get the Grafana logs from
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_grafana_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_nginx_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the Nginx logs

        :param ip: the ip of the node to get the Nginx logs from
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_nginx_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_docker_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the Docker logs

        :param ip: the ip of the node to get the Docker logs from
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_docker_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_postgresql_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the PostgreSQL logs

        :param ip: the ip of the node to get the PostgreSQL logs from
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_postgresql_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_flask_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the Flask logs

        :param ip: the ip of the node where to get the flask logs
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_flask_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_log_file(ip: str, port: int, log_file_name: str) -> Dict[str, Any]:
        """
        Gets a specific log file from a node

        :param ip: the ip of the node where to get the log file
        :param port: the port of the cluster manager
        :param log_file_name: the name of the log file
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_log_file(stub,
                                                                                       log_file_name=log_file_name)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def install_libraries(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to install CSLE libraries on the containers of a given execution

        :param ip: the ip of the node where to install the libraries
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.install_libraries(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def apply_kafka_config(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to apply the Kafka config to a given execution

        :param ip: the ip of the node where to apply the Kafka config
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_kafka_config(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_sdn_controller(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the Ryu SDN controller on a given execution

        :param ip: the ip of the node where to start the SDN controller
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_sdn_controller(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def apply_resource_constraints(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to apply resource constraints to containers of a given execution

        :param ip: the ip of the node where to apply the resouce constraints
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_resource_constraints(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def create_ovs_switches(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the OVS switches of a given execution

        :param ip: the ip of the node where to create the OVS switches
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.create_ovs_switches(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def ping_execution(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to ping all containers of a given execution

        :param ip: the ip of the node where to ping the execution
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.ping_execution(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def configure_ovs(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to configure OVS switches of a given execution

        :param ip: the ip of the node where to configure OVS
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.configure_ovs(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_sdn_controller_monitor(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the SDN controller monitor on a given execution

        :param ip: the ip of the node where to start teh SDN controller monitor
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_sdn_controller_monitor(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def create_users(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to create users on a given execution

        :param ip: the ip of the node where to create the users
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.create_users(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def create_vulnerabilities(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to create vulnerabilities of a given execution

        :param ip: the ip of the node where to create the vulnerabilities
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.create_vulnerabilities(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def create_flags(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to create flags of a given execution

        :param ip: the ip of the node where to create the flags
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.create_flags(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def create_topology(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to create the topology of a given execution

        :param ip: the ip of the node where to create the topology
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.create_topology(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_traffic_managers(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the traffic managers of a given execution

        :param ip: the ip of the node where to start the traffic managers
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_traffic_managers(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_traffic_generators(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the traffic generators of a given execution

        :param ip: the ip of the node where to start the traffic generators
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_traffic_generators(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_client_population(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the client population of a given execution

        :param ip: the ip of the node where to start the client population
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_client_population(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_kafka_client_producer(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the kafka client producer of a given execution

        :param ip: the ip of the node where to start the kafka client producer
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_kafka_client_producer(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def stop_kafka_client_producer(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the kafka client producer of a given execution

        :param ip: the ip of the node where to stop the kafka client producer
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_kafka_client_producer(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_snort_idses(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the Snort IDSes of a given execution

        :param ip: the ip of the node where to start the Snort IDSes
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_snort_idses(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_snort_idses_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the Snort IDSes monitor threads of a given execution

        :param ip: the ip of the node where to start the Snort IDS monitor threads
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = \
                csle_cluster.cluster_manager.query_cluster_manager.start_snort_idses_monitor_threads(
                    stub=stub, emulation=emulation, ip_first_octet=ip_first_octet)
            return operation_outcome_dto

    @staticmethod
    def start_ossec_idses(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the OSSEC IDSes of a given execution

        :param ip: the ip of the node where to start the OSSEC IDS
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_ossec_idses(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_ossec_idses_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the OSSEC IDSes monitor threads of a given execution

        :param ip: the ip of the node where to start the OSSEC IDS monitor threads
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = \
                csle_cluster.cluster_manager.query_cluster_manager.start_ossec_idses_monitor_threads(
                    stub=stub, emulation=emulation, ip_first_octet=ip_first_octet)
            return operation_outcome_dto

    @staticmethod
    def start_elk_stack(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the ELK stack of a given execution

        :param ip: the ip of the node where to start the elk stack
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_elk_stack(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_host_managers(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the host managers of a given execution

        :param ip: the ip of the node where to start the host managers
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_host_managers(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def apply_filebeats_config(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to apply the filebeats configuration to a given execution

        :param ip: the ip of the node where to start the filebeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_filebeats_config(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def apply_packetbeats_config(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to apply the packetbeats configuration to a given execution

        :param ip: the ip of the node where to start the packetbeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_packetbeats_config(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def apply_metricbeats_config(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to apply the metricbeats configuration to a given execution

        :param ip: the ip of the node where to start the metricbeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_metricbeats_config(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def apply_heartbeats_config(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to apply the hearbeats config to a given execution

        :param ip: the ip of the node where to start the heartbeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_heartbeats_config(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_filebeats(ip: str, port: int, emulation: str, ip_first_octet: int, initial_start: bool = False) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the filebeats of a given execution

        :param ip: the ip of the node where to start the filebeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param initial_start: boolean flag whether it is the initial start of the filebeats or not
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_filebeats(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet, initial_start=initial_start
            )
            return operation_outcome_dto

    @staticmethod
    def start_metricbeats(ip: str, port: int, emulation: str, ip_first_octet: int, initial_start: bool = False) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the metricbeats of a given execution

        :param ip: the ip of the node where to start the metricbeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param initial_start: boolean flag whether it is the initial start of the metricbeats or not
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_metricbeats(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet, initial_start=initial_start
            )
            return operation_outcome_dto

    @staticmethod
    def start_heartbeats(ip: str, port: int, emulation: str, ip_first_octet: int, initial_start: bool = False) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the heartbeats of a given execution

        :param ip: the ip of the node where to start the heartbeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param initial_start: boolean flag whether it is the initial start of the heartbeats or not
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_heartbeats(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet, initial_start=initial_start
            )
            return operation_outcome_dto

    @staticmethod
    def start_packetbeats(ip: str, port: int, emulation: str, ip_first_octet: int, initial_start: bool = False) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the packetbeats of a given execution

        :param ip: the ip of the node where to start the packetbeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param initial_start: boolean flag whether it is the initial start of the packetbeats or not
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_packetbeats(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet, initial_start=initial_start
            )
            return operation_outcome_dto

    @staticmethod
    def start_docker_statsmanager_thread(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Sends a request to start a docker statsmanager thread for a given execution

        :param ip: the ip of the node where to start the statsmanager
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_docker_statsmanager_thread(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def stop_all_executions_of_emulation(ip: str, port: int, emulation: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to a node to stop all executions of a given emulation

        :param ip: the ip of the node where to stop the executions
        :param port: the port of the cluster manager
        :param emulation: the name of the emulation
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_all_executions_of_emulation(
                stub=stub, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_execution(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop a given execution

        :param ip: the ip of the node where to stop the execution
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_execution(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def stop_all_executions(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop all executions on a given node

        :param ip: the ip of the node where to stop the executions
        :param port: the port of the cluster manager
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_all_executions(stub=stub)
            return operation_outcome_dto

    @staticmethod
    def clean_all_executions(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to clean all executions on a given node

        :param ip: the ip of the node where to stop the executions
        :param port: the port of the cluster manager
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.clean_all_executions(stub=stub)
            return operation_outcome_dto

    @staticmethod
    def clean_all_executions_of_emulation(ip: str, port: int, emulation: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to a node to clean all executions of a given emulation

        :param ip: the ip of the node where to clean the executions
        :param port: the port of the cluster manager
        :param emulation: the name of the emulation
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = \
                csle_cluster.cluster_manager.query_cluster_manager.clean_all_executions_of_emulation(
                    stub=stub, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def clean_execution(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to clean a given execution

        :param ip: the ip of the node where to clean the execution
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.clean_execution(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_traffic_manager(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start a specific traffic manager

        :param ip: the ip of the node where to stop the traffic manager
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the ip of the container where the traffic manager should be started
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_traffic_manager(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet, container_ip=container_ip
            )
            return operation_outcome_dto

    @staticmethod
    def stop_traffic_manager(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop a specific traffic manager

        :param ip: the ip of the node where to stop the traffic manager
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the ip of the container where the traffic manager should be stopped
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_traffic_manager(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet, container_ip=container_ip
            )
            return operation_outcome_dto

    @staticmethod
    def stop_traffic_managers(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the traffic managers of a given execution

        :param ip: the ip of the node where to stop the traffic managers
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_traffic_managers(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_client_manager(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the client manager of a given execution

        :param ip: the ip of the node where to start the client manager
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_client_manager(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def stop_client_manager(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the client manager of a given execution

        :param ip: the ip of the node where to start the client manager
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_client_manager(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def stop_client_population(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the client population of a given execution

        :param ip: the ip of the node where to stop the client population
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_client_population(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def get_num_active_clients(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.GetNumClientsDTO:
        """
        Sends a request to get the number of active clients of a given execution

        :param ip: the ip of the node where query for the number of active clients
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            clients_dto = csle_cluster.cluster_manager.query_cluster_manager.get_num_active_clients(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return clients_dto

    @staticmethod
    def stop_traffic_generators(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the traffic generators of a given execution

        :param ip: the ip of the node where to stop the traffic generators
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_traffic_generators(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_traffic_generator(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start a specific traffic generator

        :param ip: the ip of the node where to start the traffic generator
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the ip of the container where the traffic generator should be started
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_traffic_generator(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet, container_ip=container_ip
            )
            return operation_outcome_dto

    @staticmethod
    def stop_traffic_generator(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop a specific traffic generator

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the ip of the container where the traffic generator should be stopped
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_traffic_generator(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet, container_ip=container_ip
            )
            return operation_outcome_dto

    @staticmethod
    def get_client_managers_info(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ClientManagersInfoDTO:
        """
        Sends a request to get the client managers infos of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: a ClientManagersInfoDTO
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            client_managers_info_dto = csle_cluster.cluster_manager.query_cluster_manager.get_client_managers_info(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return client_managers_info_dto

    @staticmethod
    def get_traffic_managers_info(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.TrafficManagersInfoDTO:
        """
        Sends a request to get the client managers infos of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: a TrafficManagersInfoDTO
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            traffic_managers_info_dto = csle_cluster.cluster_manager.query_cluster_manager.get_traffic_managers_info(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return traffic_managers_info_dto

    @staticmethod
    def stop_all_running_containers(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop all running containers on a given node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_all_running_containers(
                stub=stub)
            return operation_outcome_dto

    @staticmethod
    def stop_container(ip: str, port: int, container_name) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop a specific container on a given node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param container_name: the name of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_container(
                stub=stub, container_name=container_name)
            return operation_outcome_dto

    @staticmethod
    def remove_all_stopped_containers(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to remove all stopped containers on a given node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.remove_all_stopped_containers(
                stub=stub)
            return operation_outcome_dto

    @staticmethod
    def remove_container(ip: str, port: int, container_name: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to remove a specific container on a specific nodep

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param container_name: the name of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.remove_container(
                stub=stub, container_name=container_name)
            return operation_outcome_dto

    @staticmethod
    def remove_all_container_images(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to remove all container images on a specific node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.remove_all_container_images(
                stub=stub)
            return operation_outcome_dto

    @staticmethod
    def remove_container_image(ip: str, port: int, image_name: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to remove a specific container image on a specific node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param image_name: the name of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.remove_container_image(
                stub=stub, image_name=image_name)
            return operation_outcome_dto

    @staticmethod
    def list_all_container_images(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ContainerImagesDTO:
        """
        Sends a request to list all container images on a specific node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :return: The container images
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            images_dto = csle_cluster.cluster_manager.query_cluster_manager.list_all_container_images(
                stub=stub)
            return images_dto

    @staticmethod
    def list_all_docker_networks(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.DockerNetworksDTO:
        """
        Sends a request to list all Docker networks on a specific node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :return: The docker networks
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            docker_networks_dto = csle_cluster.cluster_manager.query_cluster_manager.list_all_docker_networks(
                stub=stub)
            return docker_networks_dto

    @staticmethod
    def start_all_stopped_containers(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start all stopped containers on a given node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_all_stopped_containers(
                stub=stub)
            return operation_outcome_dto

    @staticmethod
    def start_container(ip: str, port: int, container_name: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start a specific container on a specific node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param container_name: the name of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_container(
                stub=stub, container_name=container_name)
            return operation_outcome_dto

    @staticmethod
    def list_all_running_containers(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.RunningContainersDTO:
        """
        Sends a request to list all running containers on a specific node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :return: The docker networks
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            running_containers_dto = csle_cluster.cluster_manager.query_cluster_manager.list_all_running_containers(
                stub=stub)
            return running_containers_dto

    @staticmethod
    def list_all_running_emulations(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.RunningEmulationsDTO:
        """
        Sends a request to list all running emulations on a given node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :return: The docker networks
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            running_emulations_dto = csle_cluster.cluster_manager.query_cluster_manager.list_all_running_emulations(
                stub=stub)
            return running_emulations_dto

    @staticmethod
    def list_all_stopped_containers(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.StoppedContainersDTO:
        """
        Sends a request to list all running containers on a specific node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :return: The docker networks
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            stopped_containers_dto = csle_cluster.cluster_manager.query_cluster_manager.list_all_stopped_containers(
                stub=stub)
            return stopped_containers_dto

    @staticmethod
    def create_emulation_networks(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to create the networks of a specific emulation on a specific node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.create_emulation_networks(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet)
            return operation_outcome_dto

    @staticmethod
    def stop_docker_statsmanager_thread(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the docker stats manager thread

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_docker_statsmanager_thread(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet)
            return operation_outcome_dto

    @staticmethod
    def get_docker_stats_manager_status(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.DockerStatsMonitorStatusDTO:
        """
        Sends a request to get the docker stats manager status on a specific node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :return: The docker stats manager status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            docker_stats_manager_status_dwto = \
                csle_cluster.cluster_manager.query_cluster_manager.get_docker_stats_manager_status(
                    stub=stub, port=constants.GRPC_SERVERS.DOCKER_STATS_MANAGER_PORT)
            return docker_stats_manager_status_dwto

    @staticmethod
    def remove_docker_networks(ip: str, port: int, networks: List[str]) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to remove a list of docker networks on a given node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param networks: the list of networks to remove
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.remove_docker_networks(
                stub=stub, networks=networks)
            return operation_outcome_dto

    @staticmethod
    def remove_all_docker_networks(ip: str, port: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to remove all docker networks on a given node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.remove_all_docker_networks(
                stub=stub)
            return operation_outcome_dto

    @staticmethod
    def get_docker_stats_manager_info(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.DockerStatsManagersInfoDTO:
        """
        Sends a request to get the docker stats manager infos of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: a DockerStatsManagersInfoDTO
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            docker_stats_managers_info_dto = \
                csle_cluster.cluster_manager.query_cluster_manager.get_docker_stats_manager_info(
                    stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
                )
            return docker_stats_managers_info_dto

    @staticmethod
    def stop_elk_manager(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the elk manager of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_elk_manager(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def start_elk_manager(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the elk manager of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_elk_manager(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def get_elk_status(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ElkStatusDTO:
        """
        Sends a request to get the status of the ELK stack of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The status of the ELK stack
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            elk_status_dto = csle_cluster.cluster_manager.query_cluster_manager.get_elk_status(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return elk_status_dto

    @staticmethod
    def stop_elk_stack(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the ELK stack of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_elk_stack(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def start_elastic(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start elastic of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_elastic(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_elastic(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop elastic on a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_elastic(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def start_kibana(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start Kibana of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_kibana(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_kibana(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop Kibana of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_kibana(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def start_logstash(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start Logstash of a given execution

        :param ip: the ip of the node where to stop the traffic generator
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_logstash(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_logstash(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop Logstash of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_logstash(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def get_elk_managers_info(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ElkManagersInfoDTO:
        """
        Sends a request to get the elk managers infos of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: an ElkManagersInfoDTO
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            elk_managers_info_dto = \
                csle_cluster.cluster_manager.query_cluster_manager.get_elk_managers_info(
                    stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
                )
            return elk_managers_info_dto

    @staticmethod
    def start_containers_of_execution(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the containers of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_containers_of_execution(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def run_container(ip: str, port: int, image: str, name: str, memory: int, num_cpus: int, create_network: bool,
                      version: str) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to run a container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param image: the docker image
        :param name: the name of the container
        :param memory: the memory of the container (in GB)
        :param num_cpus: the number of CPUs of the container
        :param version: the version of the container
        :param create_network: boolean flag inidicating whether a network should be created for the container or not
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.run_container(
                stub=stub, image=image, name=name, memory=memory, num_cpus=num_cpus, create_network=create_network,
                version=version)
            return operation_outcome_dto

    @staticmethod
    def stop_containers_of_execution(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the containers of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_containers_of_execution(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def start_host_manager(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the host manager on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_host_manager(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def stop_host_managers(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the host managers of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_host_managers(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_host_manager(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the host manager on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the ip of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_host_manager(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def start_host_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the host monitor threads of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_host_monitor_threads(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_filebeats(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the filebeats of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_filebeats(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_packetbeats(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the packetbeats of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_packetbeats(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_metricbeats(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the metricbeats of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_metricbeats(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_heartbeats(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the heartbeats of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_heartbeats(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def start_host_monitor_thread(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the host monitor thread on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_host_monitor_thread(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def start_filebeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str,
                       initial_start: bool = False) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start filebeat on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :param initial_start: boolean flag indicating whether it is an initial start or not
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_filebeat(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip,
                initial_start=initial_start)
            return operation_outcome_dto

    @staticmethod
    def start_packetbeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str,
                         initial_start: bool = False) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start packetbeat on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the ip of the container
        :param initial_start: boolean flag indicating whether it is an initial start or not
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_packetbeat(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip,
                initial_start=initial_start)
            return operation_outcome_dto

    @staticmethod
    def start_metricbeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str,
                         initial_start: bool = False) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start metricbeat on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param initial_start: boolean flag indicating whether it is an initial start or not
        :param container_ip: the ip of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_metricbeat(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip,
                initial_start=initial_start)
            return operation_outcome_dto

    @staticmethod
    def start_heartbeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str,
                        initial_start: bool = False) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start heartbeat on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :param initial_start: boolean flag indicating whether it is an initial start or not
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_heartbeat(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip,
                initial_start=initial_start)
            return operation_outcome_dto

    @staticmethod
    def stop_filebeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop filebeat on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the ip of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_filebeat(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def stop_packetbeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops packetbeat on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_packetbeat(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def stop_metricbeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops metricbeat on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_metricbeat(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def stop_heartbeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops heartbeat on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the ip of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_heartbeat(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def apply_filebeat_config(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Applies the filebeat config to a specific node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param container_ip: the ip of the container
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_filebeat_config(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def apply_packetbeat_config(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Applies the packetbeat configuration to a specific node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the node to apply the config
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_packetbeat_config(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def apply_metricbeat_config(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Applies the metricbeat  configuration to a specific node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the node to apply the config
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_metricbeat_config(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def apply_heartbeat_config(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Applies the heartbeat configuration to a specific node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the node to apply the config
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_heartbeat_config(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def get_host_monitor_threads_statuses(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.HostManagerStatusesDTO:
        """
        Gets the host monitor thread statuses of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The statuses
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            statuses_dtos = \
                csle_cluster.cluster_manager.query_cluster_manager.get_host_monitor_threads_statuses(
                    stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return statuses_dtos

    @staticmethod
    def get_host_managers_info(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.HostManagersInfoDTO:
        """
        Gets the host managers info of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The host managers info
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            managers_info_dto = csle_cluster.cluster_manager.query_cluster_manager.get_host_managers_info(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return managers_info_dto

    @staticmethod
    def stop_kafka_manager(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the kafka manager of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_kafka_manager(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def start_kafka_manager(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the kafka manager in a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_kafka_manager(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def create_kafka_topics(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Creates the kafka topics in a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.create_kafka_topics(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def get_kafka_status(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.KafkaStatusDTO:
        """
        Sends a request to stop the containers of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The kafka status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            status_dto = csle_cluster.cluster_manager.query_cluster_manager.get_kafka_status(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return status_dto

    @staticmethod
    def stop_kafka_server(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the kafka server in a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_kafka_server(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def start_kafka_server(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the kafka server in a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_kafka_server(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def get_kafka_managers_info(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.KafkaManagersInfoDTO:
        """
        Gets the info of kafka managers

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The kafka managers infos
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            kafka_managers_info = csle_cluster.cluster_manager.query_cluster_manager.get_kafka_managers_info(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return kafka_managers_info

    @staticmethod
    def stop_ossec_idses(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stop the OSSEC IDSes in a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_ossec_idses(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_ossec_ids(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the OSSEC IDS on a specific host

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param container_ip: the IP of the node to apply the config
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_ossec_ids(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def start_ossec_ids(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the OSSEC IDS on a specific host

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_ossec_ids(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def start_ossec_ids_managers(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the OSSEC IDS managers for a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_ossec_ids_managers(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_ossec_ids_managers(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the OSSEC IDS managers of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_ossec_ids_managers(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def start_ossec_ids_manager(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the OSSEC IDS manager on a specific node

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the node to apply the config
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_ossec_ids_manager(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def stop_ossec_ids_manager(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the containers of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the node to apply the config
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_ossec_ids_manager(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def start_ossec_ids_monitor_thread(ip: str, port: int, emulation: str, ip_first_octet: int,
                                       container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the OSSEC IDS monitor thread on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the node to apply the config
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_ossec_ids_monitor_thread(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def stop_ossec_ids_monitor_thread(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the OSSEC IDS monitor thread on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param container_ip: the IP of the node to apply the config
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_ossec_ids_monitor_thread(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def stop_ossec_ids_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the OSSEC IDS monitor threads for a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_ossec_ids_monitor_threads(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def get_ossec_ids_monitor_thread_statuses(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OSSECIdsMonitorThreadStatusesDTO:
        """
        Gets the OSSEC IDS monitor thread statuses for a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The thread statuses
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            statuses_dtos = \
                csle_cluster.cluster_manager.query_cluster_manager.get_ossec_ids_monitor_thread_statuses(
                    stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return statuses_dtos

    @staticmethod
    def get_ossec_ids_managers_info(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OSSECIdsManagersInfoDTO:
        """
        Gets the info of OSSEC IDS managers

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The managers infos
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            managers_info = csle_cluster.cluster_manager.query_cluster_manager.get_ossec_ids_managers_info(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return managers_info

    @staticmethod
    def start_ryu_manager(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Ryu manager for a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_ryu_manager(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_ryu_manager(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Ryu manager for a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_ryu_manager(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def get_ryu_status(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.RyuManagerStatusDTO:
        """
        Gets the Ryu status

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The Ryu status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            ryu_status_dto = csle_cluster.cluster_manager.query_cluster_manager.get_ryu_status(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return ryu_status_dto

    @staticmethod
    def start_ryu(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts Ryu

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_ryu(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_ryu(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops Ryu

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_ryu(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def get_ryu_managers_info(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.RyuManagersInfoDTO:
        """
        Gets the info of Ryu managers

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The ryu manager infos
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            ryu_manager_infos = csle_cluster.cluster_manager.query_cluster_manager.get_ryu_managers_info(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return ryu_manager_infos

    @staticmethod
    def stop_snort_idses(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Snort IDSes for a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_snort_idses(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_snort_idses_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Snort IDSes monitor threads for a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_snort_idses_monitor_threads(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_snort_ids(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Snort IDS on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param container_ip: the ip of the container
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_snort_ids(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def stop_snort_ids_monitor_thread(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Snort IDS Monitor Thread on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_snort_ids_monitor_thread(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def start_snort_ids(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Snort IDS on a specific container in a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the ip of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_snort_ids(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def start_snort_ids_monitor_thread(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Snort IDS monitor thread on a specific container in a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the  container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_snort_ids_monitor_thread(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def start_snort_ids_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Snort IDS monitor threads of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_snort_ids_monitor_threads(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def start_snort_ids_managers(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Snort IDS managers of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_snort_ids_managers(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_snort_ids_managers(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Snort IDS managers of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_snort_ids_managers(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def start_snort_ids_manager(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Snort IDS manager at a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the ip of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_snort_ids_manager(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def stop_snort_ids_manager(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the OSSEC IDS monitor threads for a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the ip of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_snort_ids_manager(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def stop_snort_ids_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Snort IDS managers of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_snort_ids_monitor_threads(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def get_snort_ids_managers_info(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.SnortIdsManagersInfoDTO:
        """
        Gets the info of Snort IDS managers

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The Snort IDS managers infos
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            snort_managers_info = csle_cluster.cluster_manager.query_cluster_manager.get_snort_ids_managers_info(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return snort_managers_info

    @staticmethod
    def get_execution_info(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ExecutionInfoDTO:
        """
        Gets the info of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The execution info
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            exec_info_dto = csle_cluster.cluster_manager.query_cluster_manager.get_execution_info(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return exec_info_dto

    @staticmethod
    def get_snort_ids_monitor_thread_statuses(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.SnortIdsMonitorThreadStatusesDTO:
        """
        Gets the Snort IDS monitor thread statuses for a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The thread statuses
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            statuses_dtos = \
                csle_cluster.cluster_manager.query_cluster_manager.get_snort_ids_monitor_thread_statuses(
                    stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return statuses_dtos

    @staticmethod
    def create_ryu_tunnel(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Creates a Ryu tunnel for a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.create_ryu_tunnel(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def create_kibana_tunnel(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Creates a Kibana tunnel for a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.create_kibana_tunnel(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def list_kibana_tunnels(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.KibanaTunnelsDTO:
        """
        Lists the Kibana tunnels of a given server

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.list_kibana_tunnels(stub=stub)
            return operation_outcome_dto

    @staticmethod
    def list_ryu_tunnels(ip: str, port: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.RyuTunnelsDTO:
        """
        Lists the Ryu tunnels of a given server

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.list_ryu_tunnels(stub=stub)
            return operation_outcome_dto

    @staticmethod
    def get_merged_execution_info(execution: EmulationExecution) -> EmulationExecutionInfo:
        """
        Gets the runtime info of a specific execution

        :param execution: the execution to get the info for
        :return: the info
        """
        config = MetastoreFacade.get_config(id=1)
        infos = []
        for node in config.cluster_config.cluster_nodes:
            Logger.__call__().get_logger().info(f"getting execution info for node: {node.ip}")
            infos.append(
                ClusterController.get_execution_info(
                    ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=execution.emulation_name,
                    ip_first_octet=execution.ip_first_octet))
        execution_info = ClusterManagerUtil.merge_execution_infos(execution_infos=infos)
        return execution_info

    @staticmethod
    def remove_kibana_tunnel(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Removes a Kibana tunnel for a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.remove_kibana_tunnel(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def remove_ryu_tunnel(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Removes a Ryu tunnel for a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.remove_ryu_tunnel(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_host_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the host monitor threads of a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_host_monitor_threads(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_host_monitor_thread(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the host monitor thread on a specific container

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_host_monitor_thread(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def start_ryu_monitor(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Ryu monitor for a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_ryu_monitor(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def stop_ryu_monitor(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Ryu monitor for a given execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_ryu_monitor(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return operation_outcome_dto

    @staticmethod
    def run_emulation(execution: EmulationExecution, physical_servers: List[str], no_traffic: bool = False,
                      no_clients: bool = False, no_beats: bool = False) -> None:
        """
        Runs a given emulation execution

        :param execution: details about the execution to start
        :param physical_servers: the list of physical servers the emulation will be run on
        :param no_traffic: boolean flag indicating whether internal traffic generators should be started or not
        :param no_clients: boolean flag indicating whether clients should be started or not
        :param no_beats: boolean flag indicating whether configuration/starting of beats should be skipped or not
        :return: None
        """
        steps = 41
        if no_traffic:
            steps = steps - 1
        if no_beats:
            steps = steps - 8
        if no_clients:
            execution.emulation_env_config.traffic_config.client_population_config = \
                execution.emulation_env_config.traffic_config.client_population_config.no_clients()

        current_step = 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting containers --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"-- Starting containers of "
                                                f"emulation: {execution.emulation_env_config.name} "
                                                f"on server: {ip}--")
            ClusterController.start_containers_in_execution(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                                                            emulation=execution.emulation_name,
                                                            ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating networks for emulation: "
                                            f"{execution.emulation_env_config.name} --")
        config = MetastoreFacade.get_config(id=1)
        for node in config.cluster_config.cluster_nodes:
            if node.leader:
                ClusterController.create_emulation_networks(
                    ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=execution.emulation_name,
                    ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Connect containers to networks --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"-- Connecting containers of: "
                                                f"emulation {execution.emulation_env_config.name} to networks"
                                                f" on server: {ip}--")
            ClusterController.attach_containers_in_execution_to_networks(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=execution.emulation_name,
                ip_first_octet=execution.ip_first_octet)

        # Update execution config with the new IPs for the docker-gw
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution.ip_first_octet,
                                                            emulation_name=execution.emulation_name)
        execution = EmulationEnvController.update_execution_config_w_docker_gw_bridge_ip(
            execution=execution)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Installing python libraries --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Installing libraries on containers in "
                                                f"emulation {execution.emulation_env_config.name} "
                                                f"deployed on server: {ip}")
            ClusterController.install_libraries(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Start Spark instances --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"-- Starting spark instances of "
                                                f"emulation {execution.emulation_env_config.name}"
                                                f" on server: {ip}--")
            ClusterController.start_spark_servers(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=execution.emulation_name,
                ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Apply kafka config --")
        for ip in physical_servers:
            if execution.emulation_env_config.kafka_config.container.physical_host_ip == ip:
                Logger.__call__().get_logger().info(f"Applying Kafka config to containers in "
                                                    f"emulation: {execution.emulation_env_config.name} on server: {ip}")
                ClusterController.apply_kafka_config(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                                                     emulation=execution.emulation_name,
                                                     ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Start SDN controller --")
        if execution.emulation_env_config.sdn_controller_config is not None:
            for ip in physical_servers:
                if execution.emulation_env_config.sdn_controller_config.container.physical_host_ip == ip:
                    Logger.__call__().get_logger().info(f"Starting Ryu on the Ryu container "
                                                        f"in emulation: {execution.emulation_env_config.name} "
                                                        f"on server: {ip}")
                    ClusterController.start_sdn_controller(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                                                           emulation=execution.emulation_name,
                                                           ip_first_octet=execution.ip_first_octet)
            time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating resource constraints --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Applying resource constraints to containers "
                                                f"in emulation:{execution.emulation_env_config.name} on server: {ip}")
            ClusterController.apply_resource_constraints(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Create OVS switches --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Creating OVS switches on containers in "
                                                f"emulation: {execution.emulation_env_config.name} on server: {ip}")
            ClusterController.create_ovs_switches(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Update OVS switches --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Updating OVS switches on containers in "
                                                f"emulation: {execution.emulation_env_config.name} on server: {ip}")
            ClusterController.create_ovs_switches(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating topology --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Creating topology on containers in "
                                                f"emulation: {execution.emulation_env_config.name} on server: {ip}")
            ClusterController.create_topology(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Configure OVS switches --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Configuring OVS switches on containers in "
                                                f"emulation: {execution.emulation_env_config.name} on server: {ip}")
            ClusterController.configure_ovs(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Start SDN controller monitor --")
        if execution.emulation_env_config.sdn_controller_config is not None:
            for ip in physical_servers:
                if execution.emulation_env_config.sdn_controller_config.container.physical_host_ip == ip:
                    Logger.__call__().get_logger().info(
                        f"Starting SDN controller monitor on containers "
                        f"in emulation: {execution.emulation_env_config.name} on server: {ip}")
                    ClusterController.start_sdn_controller_monitor(
                        ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                        emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating users --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Creating users on containers "
                                                f"in emulation: {execution.emulation_env_config.name} on server: {ip}")
            ClusterController.create_users(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating vulnerabilities --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Creating vulnerabilities on containers in "
                                                f"emulation: {execution.emulation_env_config.name} on server: {ip}")
            ClusterController.create_vulnerabilities(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating flags --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Creating flags on containers in "
                                                f"emulation: {execution.emulation_env_config.name} on server: {ip}")
            ClusterController.create_flags(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting traffic managers --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Starting traffic managers on containers "
                                                f"in emulation: {execution.emulation_env_config.name} on server: {ip}")
            ClusterController.start_traffic_managers(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        if not no_traffic:
            current_step += 1
            Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting traffic generators "
                                                f"on internal nodes --")
            for ip in physical_servers:
                Logger.__call__().get_logger().info(f"Starting traffic generators on containers "
                                                    f"in emulation: {execution.emulation_env_config.name} "
                                                    f"on server: {ip}")
                ClusterController.start_traffic_generators(
                    ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                    emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting client population --")
        for ip in physical_servers:
            if execution.emulation_env_config.traffic_config.client_population_config.physical_host_ip == ip:
                Logger.__call__().get_logger().info(f"Stopping the kafka client producer on the containers "
                                                    f"in emulation: {execution.emulation_env_config.name} "
                                                    f"on server: {ip}")
                ClusterController.stop_kafka_client_producer(
                    ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                    emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)
                Logger.__call__().get_logger().info(f"Starting the client population containers "
                                                    f"in emulation: {execution.emulation_env_config.name} "
                                                    f"on server: {ip}")
                ClusterController.start_client_population(
                    ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                    emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting client Kafka producer --")
        for ip in physical_servers:
            if execution.emulation_env_config.traffic_config.client_population_config.physical_host_ip == ip:
                Logger.__call__().get_logger().info(f"Starting the kafka client producer "
                                                    f"in emulation: {execution.emulation_env_config.name} "
                                                    f"on server: {ip}")
                ClusterController.start_kafka_client_producer(
                    ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                    emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step "
                                            f"{current_step}/{steps}: Starting the Snort Intrusion Detection System --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Starting the Snort IDSes "
                                                f"in emulation: {execution.emulation_env_config.name} on server: {ip}")
            ClusterController.start_snort_idses(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)
            time.sleep(10)
            Logger.__call__().get_logger().info(f"Starting the Snort IDSes monitor threads "
                                                f"in emulation: {execution.emulation_env_config.name} on server: {ip}")
            ClusterController.start_snort_idses_monitor_threads(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)
        time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step "
                                            f"{current_step}/{steps}: Starting the OSSEC Intrusion Detection System --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Starting the OSSEC IDSes on containers "
                                                f"in emulation: {execution.emulation_env_config.name} on server: {ip}")
            ClusterController.start_ossec_idses(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)
            time.sleep(10)
            Logger.__call__().get_logger().info(
                f"Starting the OSSEC IDSes monitor threads in emulation: {execution.emulation_env_config.name} "
                f"on containers on server: {ip}")
            ClusterController.start_ossec_idses_monitor_threads(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)
        time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting the ELK stack --")
        for ip in physical_servers:
            if execution.emulation_env_config.elk_config.container.physical_host_ip == ip:
                Logger.__call__().get_logger().info(f"Starting the ELK stack on containers "
                                                    f"in emulation: {execution.emulation_env_config.name} "
                                                    f"on server: {ip}")
                ClusterController.start_elk_stack(
                    ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                    emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting the Host managers "
                                            f"and host monitors --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Starting the host managers on containers "
                                                f"in emulation: {execution.emulation_env_config.name} on server: {ip}")
            ClusterController.start_host_managers(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)
        time.sleep(10)

        if not no_beats:
            current_step += 1
            Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Applying filebeats configurations --")
            for ip in physical_servers:
                Logger.__call__().get_logger().info(f"Applying filebeat configurations on containers "
                                                    f"in emulation: {execution.emulation_env_config.name} "
                                                    f"on server: {ip}")
                ClusterController.apply_filebeats_config(
                    ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                    emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)
            time.sleep(10)

            current_step += 1
            Logger.__call__().get_logger().info(
                f"-- Step {current_step}/{steps}: Applying packetbeats configurations --")
            for ip in physical_servers:
                Logger.__call__().get_logger().info(f"Applying packetbeat configurations on containers "
                                                    f"in emulation: {execution.emulation_env_config.name} "
                                                    f"on server: {ip}")
                ClusterController.apply_packetbeats_config(
                    ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                    emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)
            time.sleep(10)

            current_step += 1
            Logger.__call__().get_logger().info(
                f"-- Step {current_step}/{steps}: Applying metricbeats configurations --")
            for ip in physical_servers:
                Logger.__call__().get_logger().info(f"Applying metricbeat configurations on containers "
                                                    f"in emulation: {execution.emulation_env_config.name} "
                                                    f"on server: {ip}")
                ClusterController.apply_metricbeats_config(
                    ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                    emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)
            time.sleep(10)

            current_step += 1
            Logger.__call__().get_logger().info(
                f"-- Step {current_step}/{steps}: Applying heartbeats configurations --")
            for ip in physical_servers:
                Logger.__call__().get_logger().info(f"Applying heartbeat configurations on containers"
                                                    f" in emulation: {execution.emulation_env_config.name} "
                                                    f"on server: {ip}")
                ClusterController.apply_heartbeats_config(
                    ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                    emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)
            time.sleep(10)

            current_step += 1
            Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting filebeats --")
            for ip in physical_servers:
                Logger.__call__().get_logger().info(f"Starting filebeats on containers "
                                                    f"in emulation: {execution.emulation_env_config.name} "
                                                    f"on server: {ip}")
                ClusterController.start_filebeats(
                    ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                    emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet, initial_start=True)
            time.sleep(10)

            current_step += 1
            Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting packetbeats --")
            for ip in physical_servers:
                Logger.__call__().get_logger().info(f"Starting packetbeats on containers "
                                                    f"in emulation: {execution.emulation_env_config.name} "
                                                    f"on server: {ip}")
                ClusterController.start_packetbeats(
                    ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                    emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet, initial_start=True)
            time.sleep(10)

            current_step += 1
            Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting metricbeats --")
            for ip in physical_servers:
                Logger.__call__().get_logger().info(f"Starting metricbeats on containers "
                                                    f"in emulation: {execution.emulation_env_config.name} "
                                                    f"on server: {ip}")
                ClusterController.start_metricbeats(
                    ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                    emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet, initial_start=True)
            time.sleep(10)

            current_step += 1
            Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting heartbeats --")
            for ip in physical_servers:
                Logger.__call__().get_logger().info(f"Starting heartbeats on containers "
                                                    f"in emulation: {execution.emulation_env_config.name} "
                                                    f"on server: {ip}")
                ClusterController.start_heartbeats(
                    ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                    emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet, initial_start=True)
            time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting the Docker stats monitor --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Starting the Docker statsmanager on server: {ip}")
            ClusterController.start_docker_statsmanager(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
            time.sleep(15)
            Logger.__call__().get_logger().info(f"Starting the Docker statsmanager thread "
                                                f"for emulation: {execution.emulation_env_config.name} on server: {ip}")
            ClusterController.start_docker_statsmanager_thread(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting Cadvisor --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Starting cAdvisor on server: {ip}")
            ClusterController.start_cadvisor(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        time.sleep(2)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting Grafana --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Starting Grafana on server: {ip}")
            ClusterController.start_grafana(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        time.sleep(2)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting Node_exporter --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Starting Node exporter on server: {ip}")
            ClusterController.start_node_exporter(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        time.sleep(2)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting Prometheus --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Starting Prometheus on server: {ip}")
            ClusterController.start_prometheus(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        time.sleep(2)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting pgAdmin --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Starting pgAdmin on server: {ip}")
            ClusterController.start_pgadmin(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        time.sleep(2)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting Nginx --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Starting Nginx on server: {ip}")
            ClusterController.start_nginx(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        time.sleep(2)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting Flask --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Starting Flask on server: {ip}")
            ClusterController.start_flask(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        time.sleep(2)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting the Host managers "
                                            f"and host monitors --")
        for ip in physical_servers:
            Logger.__call__().get_logger().info(f"Starting the host managers on containers "
                                                f"in emulation: {execution.emulation_env_config.name} on server: {ip}")
            ClusterController.start_host_managers(
                ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                emulation=execution.emulation_name, ip_first_octet=execution.ip_first_octet)
        time.sleep(10)

    @staticmethod
    def get_ryu_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> Dict[str, Any]:
        """
        Gets the logs of the Ryu manager of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_ryu_manager_logs(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_ryu_controller_logs(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> Dict[str, Any]:
        """
        Gets the logs of the Ryu controller of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_ryu_controller_logs(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_elk_logs(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> Dict[str, Any]:
        """
        Gets the logs of the ELK stack of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_elk_logs(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_elk_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> Dict[str, Any]:
        """
        Gets the logs of the ELK stack of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_elk_manager_logs(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_traffic_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> Dict[str, Any]:
        """
        Gets the logs of a specific Traffic manager of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_traffic_manager_logs(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_host_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> Dict[str, Any]:
        """
        Gets the logs of a specific host manager of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_host_manager_logs(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_ossec_ids_logs(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> Dict[str, Any]:
        """
        Gets the logs of a specific OSSEC IDS of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_ossec_ids_logs(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_ossec_ids_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> Dict[str, Any]:
        """
        Gets the logs of a specific OSSEC IDS Manager of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_ossec_ids_manager_logs(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_snort_ids_logs(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> Dict[str, Any]:
        """
        Gets the logs of a specific Snort IDS of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_snort_ids_logs(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_snort_ids_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> Dict[str, Any]:
        """
        Gets the logs of a specific Snort IDS of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_snort_ids_manager_logs(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_kafka_logs(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> Dict[str, Any]:
        """
        Gets the logs of the Kafka server of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_kafka_logs(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_kafka_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> Dict[str, Any]:
        """
        Gets the logs of the Kafka manager of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_kafka_manager_logs(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_client_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> Dict[str, Any]:
        """
        Gets the logs of the Client manager of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_client_manager_logs(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_container_logs(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> Dict[str, Any]:
        """
        Gets the logs of a specific container of a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the IP of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_container_logs(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_cluster_manager_logs(ip: str, port: int) -> Dict[str, Any]:
        """
        Gets the cluster manager logs

        :param ip: the ip of the node where to get the cluster manager logs
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_cluster_manager_logs(stub)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def get_execution_time_series_data(ip: str, port: int, emulation: str, ip_first_octet: int, minutes: int) \
            -> EmulationMetricsTimeSeries:
        """
        Sends a request to get time series data of a number of minutes of a given execution

        :param ip: the ip of the node where to start the containers
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param minutes: the number of minutes of data to get in the time series
        :return: The time series data dto
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            time_series_data_dto = csle_cluster.cluster_manager.query_cluster_manager.get_execution_time_series_data(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet, minutes=minutes
            )
            return ClusterManagerUtil.convert_emulation_metrics_time_series_dto_reverse(
                time_series_dto=time_series_data_dto)

    @staticmethod
    def start_spark_servers(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to start the Spark servers of a given execution

        :param ip: the ip of the node where to start the Snort IDSes
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_spark_servers(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def stop_spark_servers(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Sends a request to stop the Spark servers of a given execution

        :param ip: the ip of the node where to start the Snort IDSes
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_spark_servers(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return operation_outcome_dto

    @staticmethod
    def start_spark_server(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Spark server on a specific container in a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the ip of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.start_spark_server(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def stop_spark_server(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Spark server on a specific container in a specific execution

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param container_ip: the ip of the container
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_spark_server(
                stub=stub, ip_first_octet=ip_first_octet, emulation=emulation, container_ip=container_ip)
            return operation_outcome_dto

    @staticmethod
    def check_pid(ip: str, port: int, pid: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Checks the status of a PID of a specific server

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param pid: the PID to check
        :return: The operation outcome
        """
        config = MetastoreFacade.get_config(id=1)
        ips = [node.ip for node in config.cluster_config.cluster_nodes]
        if ip not in ips:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.check_pid(stub=stub, pid=pid)
            return operation_outcome_dto

    @staticmethod
    def stop_pid(ip: str, port: int, pid: int) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops a PID of a specific server

        :param ip: the ip of the physical node
        :param port: the port of the cluster manager
        :param pid: the PID to check
        :return: The operation outcome
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            operation_outcome_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_pid(stub=stub, pid=pid)
            return operation_outcome_dto
