import grpc
import csle_cluster.cluster_manager.cluster_manager_pb2_grpc
import csle_cluster.cluster_manager.cluster_manager_pb2
import csle_cluster.cluster_manager.query_cluster_manager


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
