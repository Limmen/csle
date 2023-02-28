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
    def start_containers_in_execution(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the containers of a given execution

        :param ip: the ip of the node where to start the containers
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_containers_in_execution(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def attach_containers_in_execution_to_networks(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to attach the containers of a given execution to networks

        :param ip: the ip of the node where to attach the containers
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = \
                csle_cluster.cluster_manager.query_cluster_manager.attach_containers_in_execution_to_networks(
                    stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
                )
            return node_status_dto

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

        :param ip: the ip of the node to get the status
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

        :param ip: the ip of the node to start PostgreSQL
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

        :param ip: the ip of the node to start cAdvisor
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

        :param ip: the ip of the node to start node exporter
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

        :param ip: the ip of the node to start Grafana
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

        :param ip: the ip of the node to start Prometheus
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

        :param ip: the ip of the node to start pgAdmin
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

        :param ip: the ip of the node to start Nginx
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

        :param ip: the ip of the node to start flask
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

        :param ip: the ip of the node to start the docker statsmanager
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
        Stops Docker engine on a cluster node

        :param ip: the ip of the node to stop the docker engine
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
        Stops PostgreSQL on a cluster node

        :param ip: the ip of the node to stop PostgreSQL
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
        Stops cAdvisor on a cluster node

        :param ip: the ip of the node to stop cAdvisor
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
        Stops Node exporter on a cluster node

        :param ip: the ip of the node to stop node exporter
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
        Stops Grafana on a cluster node

        :param ip: the ip of the node to stop Grafana
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
        Stops Prometheus on a cluster node

        :param ip: the ip of the node to stop Prometheus
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
        Stops pgAdmin on a cluster node

        :param ip: the ip of the node to stop pgAdmin
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
        Stops nginx on a cluster node

        :param ip: the ip of the node to stop Nginx
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
        Stops Flask on a cluster node

        :param ip: the ip of the node to stop flask
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
        Stops Docker statsmanager on a cluster node

        :param ip: the ip of the node to stop the statsmanager
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
        Stops Docker engine on a cluster node

        :param ip: the ip of the node to stop the docker engine
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

        :param ip: the ip of the node to get the CSLE logs from
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

        :param ip: the ip of the node to get the Docker statsmanager logs from
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

        :param ip: the ip of the node to get the Prometheus logs from
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

        :param ip: the ip of the node to get the node exporter logs from
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

        :param ip: the ip of the node to get the cAdvisor logs from
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

        :param ip: the ip of the node to get the pgAdmin logs from
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

        :param ip: the ip of the node to get the Grafana logs from
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

        :param ip: the ip of the node to get the Nginx logs from
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

        :param ip: the ip of the node to get the Docker logs from
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

        :param ip: the ip of the node to get the PostgreSQL logs from
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

        :param ip: the ip of the node where to get the flask logs
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

        :param ip: the ip of the node where to get the log file
        :param port: the port of the cluster manager
        :return: A DTO with the log files
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            logs_dto = csle_cluster.cluster_manager.query_cluster_manager.get_log_file(stub,
                                                                                       log_file_name=log_file_name)
            return ClusterManagerUtil.logs_dto_to_dict(logs_dto=logs_dto)

    @staticmethod
    def install_libraries(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to install CSLE libraries on the containers of a given execution

        :param ip: the ip of the node where to install the libraries
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.install_libraries(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def apply_kafka_config(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to apply the Kafka config to a given execution

        :param ip: the ip of the node where to apply the Kafka config
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_kafka_config(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def start_sdn_controller(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the Ryu SDN controller on a given execution

        :param ip: the ip of the node where to start the SDN controller
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_sdn_controller(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def apply_resource_constraints(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to apply resource constraints to containers of a given execution

        :param ip: the ip of the node where to apply the resouce constraints
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_resource_constraints(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def create_ovs_switches(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the OVS switches of a given execution

        :param ip: the ip of the node where to create the OVS switches
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.create_ovs_switches(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def ping_execution(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to ping all containers of a given execution

        :param ip: the ip of the node where to ping the execution
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.ping_execution(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def configure_ovs(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to configure OVS switches of a given execution

        :param ip: the ip of the node where to configure OVS
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.configure_ovs(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def start_sdn_controller_monitor(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the SDN controller monitor on a given execution

        :param ip: the ip of the node where to start teh SDN controller monitor
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_sdn_controller_monitor(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def create_users(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to create users on a given execution

        :param ip: the ip of the node where to create the users
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.create_users(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def create_vulnerabilities(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to create vulnerabilities of a given execution

        :param ip: the ip of the node where to create the vulnerabilities
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.create_vulnerabilities(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def create_flags(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to create flags of a given execution

        :param ip: the ip of the node where to create the flags
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.create_flags(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def create_topology(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to create the topology of a given execution

        :param ip: the ip of the node where to create the topology
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.create_topology(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def start_traffic_managers(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the traffic managers of a given execution

        :param ip: the ip of the node where to start the traffic managers
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_traffic_managers(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def start_traffic_generators(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the traffic generators of a given execution

        :param ip: the ip of the node where to start the traffic generators
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_traffic_generators(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def start_client_population(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the client population of a given execution

        :param ip: the ip of the node where to start the client population
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_client_population(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def start_kafka_client_producer(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the kafka client producer of a given execution

        :param ip: the ip of the node where to start the kafka client producer
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_kafka_client_producer(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def stop_kafka_client_producer(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to stop the kafka client producer of a given execution

        :param ip: the ip of the node where to stop the kafka client producer
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_kafka_client_producer(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def start_snort_idses(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the Snort IDSes of a given execution

        :param ip: the ip of the node where to start the Snort IDSes
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_snort_idses(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def start_snort_idses_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the Snort IDSes monitor threads of a given execution

        :param ip: the ip of the node where to start the Snort IDS monitor threads
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_snort_idses_monitor_threads(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def start_ossec_idses(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the OSSEC IDSes of a given execution

        :param ip: the ip of the node where to start the OSSEC IDS
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_ossec_idses(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def start_ossec_idses_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the OSSEC IDSes monitor threads of a given execution

        :param ip: the ip of the node where to start the OSSEC IDS monitor threads
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_ossec_idses_monitor_threads(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def start_elk_stack(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the ELK stack of a given execution

        :param ip: the ip of the node where to start the elk stack
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_elk_stack(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def start_host_managers(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the host managers of a given execution

        :param ip: the ip of the node where to start the host managers
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_host_managers(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def apply_filebeats_config(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to apply the filebeats configuration to a given execution

        :param ip: the ip of the node where to start the filebeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_filebeats_config(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def apply_packetbeats_config(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to apply the packetbeats configuration to a given execution

        :param ip: the ip of the node where to start the packetbeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_packetbeats_config(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def apply_metricbeats_config(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to apply the metricbeats configuration to a given execution

        :param ip: the ip of the node where to start the metricbeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_metricbeats_config(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def apply_heartbeats_config(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to apply the hearbeats config to a given execution

        :param ip: the ip of the node where to start the heartbeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.apply_heartbeats_config(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def start_filebeats(ip: str, port: int, emulation: str, ip_first_octet: int, initial_start: bool = False) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the filebeats of a given execution

        :param ip: the ip of the node where to start the filebeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param initial_start: boolean flag whether it is the initial start of the filebeats or not
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_filebeats(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet, initial_start=initial_start
            )
            return node_status_dto

    @staticmethod
    def start_metricbeats(ip: str, port: int, emulation: str, ip_first_octet: int, initial_start: bool = False) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the metricbeats of a given execution

        :param ip: the ip of the node where to start the metricbeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param initial_start: boolean flag whether it is the initial start of the metricbeats or not
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_metricbeats(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet, initial_start=initial_start
            )
            return node_status_dto

    @staticmethod
    def start_heartbeats(ip: str, port: int, emulation: str, ip_first_octet: int, initial_start: bool = False) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the heartbeats of a given execution

        :param ip: the ip of the node where to start the heartbeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param initial_start: boolean flag whether it is the initial start of the heartbeats or not
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_heartbeats(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet, initial_start=initial_start
            )
            return node_status_dto

    @staticmethod
    def start_packetbeats(ip: str, port: int, emulation: str, ip_first_octet: int, initial_start: bool = False) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start the packetbeats of a given execution

        :param ip: the ip of the node where to start the packetbeats
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :param initial_start: boolean flag whether it is the initial start of the packetbeats or not
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_packetbeats(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet, initial_start=initial_start
            )
            return node_status_dto

    @staticmethod
    def start_docker_statsmanager_thread(ip: str, port: int, emulation: str, ip_first_octet: int) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to start a docker statsmanager thread for a given execution

        :param ip: the ip of the node where to start the statsmanager
        :param port: the port of the cluster manager
        :param emulation: the emulation of the execution
        :param ip_first_octet: the ID of the execution
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.start_docker_statsmanager_thread(
                stub=stub, emulation=emulation, ip_first_octet=ip_first_octet
            )
            return node_status_dto

    @staticmethod
    def stop_all_executions_of_emulation(ip: str, port: int, emulation: str) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Sends a request to a node to stop all executions of a given emulation

        :param ip: the ip of the node where to stop the executions
        :param port: the port of the cluster manager
        :param emulation: the name of the emulation
        :return: The node status
        """
        # Open a gRPC session
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
            node_status_dto = csle_cluster.cluster_manager.query_cluster_manager.stop_all_executions_of_emulation(
                stub=stub, emulation=emulation)
            return node_status_dto
