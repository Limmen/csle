from typing import List
import csle_cluster.cluster_manager.cluster_manager_pb2_grpc
import csle_cluster.cluster_manager.cluster_manager_pb2
import csle_collector.constants.constants as constants


def get_node_status(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
    """
    Queries the cluster manager for the status of the node

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a NodeStatusDTO describing the status of the node
    """
    get_node_status_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.GetNodeStatusMsg()
    node_status_dto = stub.getNodeStatus(get_node_status_msg, timeout=timeout)
    return node_status_dto


def start_postgresql(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to start the PostgreSQL service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the PostgreSQL service
    """
    start_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StartPostgreSQLMsg()
    service_status_dto = stub.startPostgreSQL(start_msg, timeout=timeout)
    return service_status_dto


def start_cadvisor(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to start the cAdvisor service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the cAdvisor service
    """
    start_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StartCAdvisorMsg()
    service_status_dto = stub.startCAdvisor(start_msg, timeout=timeout)
    return service_status_dto


def start_node_exporter(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to start the node exporter service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the node exporter service
    """
    start_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StartNodeExporterMsg()
    service_status_dto = stub.startNodeExporter(start_msg, timeout=timeout)
    return service_status_dto


def start_grafana(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to start the Grafana service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the Grafana service
    """
    start_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StartGrafanaMsg()
    service_status_dto = stub.startGrafana(start_msg, timeout=timeout)
    return service_status_dto


def start_prometheus(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to start the Prometheus service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the Prometheus service
    """
    start_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StartPrometheusMsg()
    service_status_dto = stub.startPrometheus(start_msg, timeout=timeout)
    return service_status_dto


def start_pgadmin(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to start the pgAdmin service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the pgAdmin service
    """
    start_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StartPgAdminMsg()
    service_status_dto = stub.startPgAdmin(start_msg, timeout=timeout)
    return service_status_dto


def start_nginx(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to start the nginx service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the nginx service
    """
    start_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StartNginxMsg()
    service_status_dto = stub.startNginx(start_msg, timeout=timeout)
    return service_status_dto


def start_flask(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to start the flask service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the flask service
    """
    start_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StartFlaskMsg()
    service_status_dto = stub.startFlask(start_msg, timeout=timeout)
    return service_status_dto


def start_docker_statsmanager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to start the docker statsmanager service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the docker statsmanager service
    """
    start_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StartDockerStatsManagerMsg()
    service_status_dto = stub.startDockerStatsManager(start_msg, timeout=timeout)
    return service_status_dto


def start_docker_engine(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to start the docker engine service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the docker engine service
    """
    start_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StartDockerEngineMsg()
    service_status_dto = stub.startDockerEngine(start_msg, timeout=timeout)
    return service_status_dto

# Stop

def stop_postgresql(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to stop the PostgreSQL service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the PostgreSQL service
    """
    stop_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StopPostgreSQLMsg()
    service_status_dto = stub.stopPostgreSQL(stop_msg, timeout=timeout)
    return service_status_dto


def stop_cadvisor(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to stop the cAdvisor service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the cAdvisor service
    """
    stop_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StopCAdvisorMsg()
    service_status_dto = stub.stopCAdvisor(stop_msg, timeout=timeout)
    return service_status_dto


def stop_node_exporter(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to stop the node exporter service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the node exporter service
    """
    stop_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StopNodeExporterMsg()
    service_status_dto = stub.stopNodeExporter(stop_msg, timeout=timeout)
    return service_status_dto


def stop_grafana(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to stop the Grafana service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the Grafana service
    """
    stop_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StopGrafanaMsg()
    service_status_dto = stub.stopGrafana(stop_msg, timeout=timeout)
    return service_status_dto


def stop_prometheus(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to stop the Prometheus service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the Prometheus service
    """
    stop_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StopPrometheusMsg()
    service_status_dto = stub.stopPrometheus(stop_msg, timeout=timeout)
    return service_status_dto


def stop_pgadmin(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to stop the pgAdmin service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the pgAdmin service
    """
    stop_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StopPgAdminMsg()
    service_status_dto = stub.stopPgAdmin(stop_msg, timeout=timeout)
    return service_status_dto


def stop_nginx(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to stop the nginx service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the nginx service
    """
    stop_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StopNginxMsg()
    service_status_dto = stub.stopNginx(stop_msg, timeout=timeout)
    return service_status_dto


def stop_flask(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to stop the flask service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the flask service
    """
    stop_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StopFlaskMsg()
    service_status_dto = stub.stopFlask(stop_msg, timeout=timeout)
    return service_status_dto


def stop_docker_statsmanager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to stop the docker statsmanager service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the docker statsmanager service
    """
    stop_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StopDockerStatsManagerMsg()
    service_status_dto = stub.stopDockerStatsManager(stop_msg, timeout=timeout)
    return service_status_dto


def stop_docker_engine(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to stop the docker engine service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the docker engine service
    """
    stop_msg = \
        csle_cluster.cluster_manager.cluster_manager_pb2.StopDockerEngineMsg()
    service_status_dto = stub.stopDockerEngine(stop_msg, timeout=timeout)
    return service_status_dto