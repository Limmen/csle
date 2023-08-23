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
    get_node_status_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetNodeStatusMsg()
    node_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO = \
        stub.getNodeStatus(get_node_status_msg, timeout=timeout)
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartPostgreSQLMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.startPostgreSQL(start_msg, timeout=timeout)
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartCAdvisorMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.startCAdvisor(start_msg, timeout=timeout)
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartNodeExporterMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.startNodeExporter(start_msg, timeout=timeout)
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartGrafanaMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.startGrafana(start_msg, timeout=timeout)
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartPrometheusMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.startPrometheus(start_msg, timeout=timeout)
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartPgAdminMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.startPgAdmin(start_msg, timeout=timeout)
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartNginxMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.startNginx(start_msg, timeout=timeout)
    return service_status_dto


def start_flask(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.CONFIG_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Requests the cluster manager to start the flask service

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ServiceStatusDTO describing the status of the flask service
    """
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartFlaskMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.startFlask(start_msg, timeout=timeout)
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartDockerStatsManagerMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.startDockerStatsManager(start_msg, timeout=timeout)
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartDockerEngineMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.startDockerEngine(start_msg, timeout=timeout)
    return service_status_dto


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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopPostgreSQLMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.stopPostgreSQL(stop_msg, timeout=timeout)
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopCAdvisorMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.stopCAdvisor(stop_msg, timeout=timeout)
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopNodeExporterMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.stopNodeExporter(stop_msg, timeout=timeout)
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopGrafanaMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.stopGrafana(stop_msg, timeout=timeout)
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopPrometheusMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.stopPrometheus(stop_msg, timeout=timeout)
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopPgAdminMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.stopPgAdmin(stop_msg, timeout=timeout)
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopNginxMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.stopNginx(stop_msg, timeout=timeout)
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopFlaskMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.stopFlask(stop_msg, timeout=timeout)
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopDockerStatsManagerMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.stopDockerStatsManager(stop_msg, timeout=timeout)
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopDockerEngineMsg()
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.stopDockerEngine(stop_msg, timeout=timeout)
    return service_status_dto


def get_log_file(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        log_file_name: str, timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Fetches a given log file from the cluster manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param log_file_name: the name of the log file
    :return: a LogsDTO with the logs
    """
    get_log_file_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetLogFileMsg(name=log_file_name)
    logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getLogFile(get_log_file_msg, timeout=timeout)
    return logs_dto


def get_flask_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Fetches flask logs from the cluster manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a LogsDTO with the logs
    """
    get_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetFlaskLogsMsg()
    logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getFlaskLogs(get_msg, timeout=timeout)
    return logs_dto


def get_postgresql_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Fetches PostgreSQL logs from the cluster manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a LogsDTO with the logs
    """
    get_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetPostgreSQLLogsMsg()
    logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getPostrgreSQLLogs(get_msg, timeout=timeout)
    return logs_dto


def get_docker_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Fetches Docker logs from the cluster manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a LogsDTO with the logs
    """
    get_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetDockerLogsMsg()
    logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getDockerLogs(get_msg, timeout=timeout)
    return logs_dto


def get_nginx_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Fetches Nginx logs from the cluster manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a LogsDTO with the logs
    """
    get_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetNginxLogsMsg()
    logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getNginxLogs(get_msg, timeout=timeout)
    return logs_dto


def get_grafana_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Fetches grafana logs from the cluster manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a LogsDTO with the logs
    """
    get_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetGrafanaLogsMsg()
    logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getGrafanaLogs(get_msg, timeout=timeout)
    return logs_dto


def get_pgadmin_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Fetches pgAdmin logs from the cluster manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a LogsDTO with the logs
    """
    get_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetPgAdminLogsMsg()
    logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getPgAdminLogs(get_msg, timeout=timeout)
    return logs_dto


def get_cadvisor_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Fetches cAdvisor logs from the cluster manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a LogsDTO with the logs
    """
    get_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetCAdvisorLogsMsg()
    logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getCadvisorLogs(get_msg, timeout=timeout)
    return logs_dto


def get_node_exporter_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Fetches node exporter logs from the cluster manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a LogsDTO with the logs
    """
    get_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetNodeExporterLogsMsg()
    logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getNodeExporterLogs(get_msg, timeout=timeout)
    return logs_dto


def get_prometheus_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Fetches node exporter logs from the cluster manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a LogsDTO with the logs
    """
    get_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetPrometheusLogsMsg()
    logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getPrometheusLogs(get_msg, timeout=timeout)
    return logs_dto


def get_docker_statsmanager_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Fetches docker statsmanager logs from the cluster manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a LogsDTO with the logs
    """
    get_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetDockerStatsManagerLogsMsg()
    logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getDockerStatsManagerLogs(get_msg, timeout=timeout)
    return logs_dto


def get_csle_log_files(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Fetches CSLE log file names from the CSLE log directory from the cluster manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a LogsDTO with the logs
    """
    get_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetCsleLogFilesMsg()
    logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getCsleLogFiles(get_msg, timeout=timeout)
    return logs_dto


def start_containers_in_execution(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts containers of a given emulation execution that are configured to be deployed on the host

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartContainersInExecutionMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startContainersInExecution(operation_msg, timeout=timeout)
    return operation_outcome_dto


def attach_containers_in_execution_to_networks(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Attaches containers of a given emulation execution that are configured to be deployed on the host to networks

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.AttachContainersToNetworksInExecutionMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.attachContainersInExecutionToNetworks(operation_msg, timeout=timeout)
    return operation_outcome_dto


def install_libraries(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Installs CSLE libraries on containers in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.InstallLibrariesMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.installLibraries(operation_msg, timeout=timeout)
    return operation_outcome_dto


def apply_kafka_config(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Applies the kafka config to a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ApplyKafkaConfigMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.applyKafkaConfig(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_sdn_controller(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the RYU SDN controller in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartSdnControllerMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startSdnController(operation_msg, timeout=timeout)
    return operation_outcome_dto


def apply_resource_constraints(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Applies resource constraints to a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ApplyResouceConstraintsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.applyResourceConstraints(operation_msg, timeout=timeout)
    return operation_outcome_dto


def create_ovs_switches(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Creates OVS switches of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.CreateOvsSwitchesMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.createOvsSwitches(operation_msg, timeout=timeout)
    return operation_outcome_dto


def ping_execution(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Pings all containers in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.PingExecutionMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.pingExecution(operation_msg, timeout=timeout)
    return operation_outcome_dto


def configure_ovs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Configure OVS switches in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ConfigureOvsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.configureOvs(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_sdn_controller_monitor(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the SDN controller monitor in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartSdnControllerMonitorMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startSdnControllerMonitor(operation_msg, timeout=timeout)
    return operation_outcome_dto


def create_users(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Creates users in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.CreateUsersMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.createUsers(operation_msg, timeout=timeout)
    return operation_outcome_dto


def create_vulnerabilities(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Creates vulnerabilities in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.CreateVulnsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.createVulnerabilities(operation_msg, timeout=timeout)
    return operation_outcome_dto


def create_flags(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Creates flags in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.CreateFlagsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.createFlags(operation_msg, timeout=timeout)
    return operation_outcome_dto


def create_topology(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Creates the topology of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.CreateTopologyMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.createTopology(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_traffic_managers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts traffic managers of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartTrafficManagersMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startTrafficManagers(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_traffic_generators(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts traffic generators of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartTrafficGeneratorsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startTrafficGenerators(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_client_population(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the client population of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartClientPopulationMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startClientPopulation(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_kafka_client_producer(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the Kafka client producer of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartKafkaClientProducerMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startKafkaClientProducer(operation_msg, timeout=timeout)
    return operation_outcome_dto


def stop_kafka_client_producer(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the Kafka client producer of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopKafkaClientProducerMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopKafkaClientProducer(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_snort_idses(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the Snort IDSes of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartSnortIdsesMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startSnortIdses(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_snort_idses_monitor_threads(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the Snort IDSes monitor threads of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartSnortIdsesMonitorThreadsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startSnortIdsesMonitorThreads(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_ossec_idses(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the OSSEC IDSes of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartOSSECIdsesMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startOssecIdses(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_ossec_idses_monitor_threads(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the OSSEC IDSes monitor threads of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartOSSECIdsesMonitorThreadsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startOssecIdsesMonitorThreads(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_elk_stack(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the ELK stack of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartElkStackMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startElkStack(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_host_managers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the Host managers of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartHostManagersMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startHostManagers(operation_msg, timeout=timeout)
    return operation_outcome_dto


def apply_filebeats_config(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Applies the filebeat configurations of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ApplyFileBeatConfigsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.applyFileBeatsConfig(operation_msg, timeout=timeout)
    return operation_outcome_dto


def apply_packetbeats_config(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Applies the packetbeat configurations of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ApplyPacketBeatConfigsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.applyPacketBeatsConfig(operation_msg, timeout=timeout)
    return operation_outcome_dto


def apply_metricbeats_config(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Applies the metricbeat configurations of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ApplyMetricBeatConfigsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.applyMetricBeatsConfig(operation_msg, timeout=timeout)
    return operation_outcome_dto


def apply_heartbeats_config(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Applies the heartbeat configurations of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ApplyHeartBeatConfigsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.applyHeartBeatsConfig(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_filebeats(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, initial_start: bool = False,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts filebeats of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param initial_start: boolean flag whether it is the initial start of the filebeats or not
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartFileBeatsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet, initialStart=initial_start
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startFilebeats(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_metricbeats(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, initial_start: bool = False,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts metricbeats of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param initial_start: boolean flag whether it is the initial start of the metricbeats or not
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartMetricBeatsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet, initialStart=initial_start
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startMetricbeats(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_heartbeats(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, initial_start: bool = False,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts heartbeats of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param initial_start: boolean flag whether it is the initial start of the heartbeats or not
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartHeartBeatsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet, initialStart=initial_start
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startHeartbeats(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_packetbeats(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, initial_start: bool = False,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts packetbeats of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param initial_start: boolean flag whether it is the initial start of the packetbeats or not
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartPacketBeatsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet, initialStart=initial_start
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startPacketbeats(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_docker_statsmanager_thread(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
    """
    Starts a docker stats manager thread for a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartDockerStatsManagerThreadMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    service_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO = \
        stub.startDockerStatsManagerThread(operation_msg, timeout=timeout)
    return service_status_dto


def stop_all_executions_of_emulation(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops all executions of a given emulation

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopAllExecutionsOfEmulationMsg(
        emulation=emulation)
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopAllExecutionsOfEmulation(operation_msg, timeout=timeout)
    return operation_outcome_dto


def stop_execution(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops an emulation execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopExecutionMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopExecution(operation_msg, timeout=timeout)
    return operation_outcome_dto


def stop_all_executions(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops all executions

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopAllExecutionsMsg()
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopAllExecutions(operation_msg, timeout=timeout)
    return operation_outcome_dto


def clean_all_executions(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Cleans all executions

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.CleanAllExecutionsMsg()
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.cleanAllExecutions(operation_msg, timeout=timeout)
    return operation_outcome_dto


def clean_all_executions_of_emulation(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Cleans all executions of a given emulation

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.CleanAllExecutionsOfEmulationMsg(
        emulation=emulation)
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.cleanAllExecutionsOfEmulation(operation_msg, timeout=timeout)
    return operation_outcome_dto


def clean_execution(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Cleans an emulation execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.CleanExecutionMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.cleanExecution(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_traffic_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts a specific traffic manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param container_ip: the ip of the container to start the traffic manager
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartTrafficManagerMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet, containerIp=container_ip
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startTrafficManager(operation_msg, timeout=timeout)
    return operation_outcome_dto


def stop_traffic_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops a specific traffic manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param container_ip: the ip of the container to stop the traffic manager
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopTrafficManagerMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet, containerIp=container_ip
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopTrafficManager(operation_msg, timeout=timeout)
    return operation_outcome_dto


def stop_traffic_managers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops traffic managers of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopTrafficManagersMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopTrafficManagers(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_client_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the client manager of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartClientManagerMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startClientManager(operation_msg, timeout=timeout)
    return operation_outcome_dto


def stop_client_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the client manager of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopClientManagerMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopClientManager(operation_msg, timeout=timeout)
    return operation_outcome_dto


def stop_client_population(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the client population of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopClientPopulationMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopClientPopulation(operation_msg, timeout=timeout)
    return operation_outcome_dto


def get_num_active_clients(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.GetNumClientsDTO:
    """
    Gets the number of active clients of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetNumActiveClientsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    clients_dto: csle_cluster.cluster_manager.cluster_manager_pb2.GetNumClientsDTO = \
        stub.getNumActiveClients(operation_msg, timeout=timeout)
    return clients_dto


def stop_traffic_generators(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops traffic generators of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopTrafficGeneratorsMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopTrafficGenerators(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_traffic_generator(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts a specific traffic generator

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param container_ip: the ip of the container to start the traffic generator
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartTrafficGeneratorMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet, containerIp=container_ip
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startTrafficGenerator(operation_msg, timeout=timeout)
    return operation_outcome_dto


def stop_traffic_generator(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops a specific traffic generator

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param container_ip: the ip of the container to stop the traffic generator
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopTrafficGeneratorMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet, containerIp=container_ip
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopTrafficGenerator(operation_msg, timeout=timeout)
    return operation_outcome_dto


def get_client_managers_info(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ClientManagersInfoDTO:
    """
    Gets the info of client managers of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: a ClientManagersInfoDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetClientManagersInfoMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    client_managers_info_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ClientManagersInfoDTO = \
        stub.getClientManagersInfo(operation_msg, timeout=timeout)
    return client_managers_info_dto


def get_traffic_managers_info(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.TrafficManagersInfoDTO:
    """
    Gets the info of traffic managers of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: a TrafficManagersInfoDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetTrafficManagersInfoMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    traffic_managers_info_dto: csle_cluster.cluster_manager.cluster_manager_pb2.TrafficManagersInfoDTO = \
        stub.getTrafficManagersInfo(operation_msg, timeout=timeout)
    return traffic_managers_info_dto


def stop_all_running_containers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops all running containers

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopAllRunningContainersMsg()
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopAllRunningContainers(operation_msg, timeout=timeout)
    return operation_outcome_dto


def stop_container(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        container_name: str, timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_name: the name of the container
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopContainerMsg(name=container_name)
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopContainer(operation_msg, timeout=timeout)
    return operation_outcome_dto


def remove_all_stopped_containers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Removes all stopped containers

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.RemoveAllStoppedContainersMsg()
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.removeAllStoppedContainers(operation_msg, timeout=timeout)
    return operation_outcome_dto


def remove_container(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        container_name: str, timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Removes a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_name: the name of the container
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.RemoveContainerMsg(name=container_name)
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.removeContainer(operation_msg, timeout=timeout)
    return operation_outcome_dto


def remove_all_container_images(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Removes all container images

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.RemoveAllContainerImagesMsg()
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.removeAllContainerImages(operation_msg, timeout=timeout)
    return operation_outcome_dto


def remove_container_image(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        image_name: str, timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Removes a specific container image

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param image_name: the name of the container imge
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.RemoveContainerImageMsg(name=image_name)
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.removeContainerImage(operation_msg, timeout=timeout)
    return operation_outcome_dto


def list_all_container_images(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ContainerImagesDTO:
    """
    Lists all container images

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a ContainerImagesDTO with the container images
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ListAllContainerImagesMsg()
    container_images_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ContainerImagesDTO = \
        stub.listAllContainerImages(operation_msg, timeout=timeout)
    return container_images_dto


def list_all_docker_networks(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.DockerNetworksDTO:
    """
    Lists all Docker networks

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a DockerNetworksDTO wth the docker networks
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ListAllDockerNetworksMsg()
    docker_networks_dto: csle_cluster.cluster_manager.cluster_manager_pb2.DockerNetworksDTO = \
        stub.listAllDockerNetworks(operation_msg, timeout=timeout)
    return docker_networks_dto


def start_all_stopped_containers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts all stopped containers

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartAllStoppedContainersMsg()
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startAllStoppedContainers(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_container(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        container_name: str, timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_name: the name of the container imge
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartContainerMsg(name=container_name)
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startContainer(operation_msg, timeout=timeout)
    return operation_outcome_dto


def list_all_running_containers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.RunningContainersDTO:
    """
    Lists all running containers

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a RunningContainersDTO wth the running containers
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ListAllRunningContainersMsg()
    running_containers_dto: csle_cluster.cluster_manager.cluster_manager_pb2.RunningContainersDTO = \
        stub.listAllRunningContainers(operation_msg, timeout=timeout)
    return running_containers_dto


def list_all_running_emulations(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.RunningEmulationsDTO:
    """
    Lists all running emulations

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a RunningEmulationsDTO with the running emulations
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ListAllRunningEmulationsMsg()
    running_emulations_dto: csle_cluster.cluster_manager.cluster_manager_pb2.RunningEmulationsDTO = \
        stub.listAllRunningEmulations(operation_msg, timeout=timeout)
    return running_emulations_dto


def list_all_stopped_containers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.StoppedContainersDTO:
    """
    Lists all stopped containers

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a StoppedContainersDTO wth the stopped containers
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ListAllStoppedContainersMsg()
    stopped_containers_dto: csle_cluster.cluster_manager.cluster_manager_pb2.StoppedContainersDTO = \
        stub.listAllStoppedContainers(operation_msg, timeout=timeout)
    return stopped_containers_dto


def create_emulation_networks(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Creates Docker networks for a given emulation

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.CreateEmulationNetworksMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.createEmulationNetworks(operation_msg, timeout=timeout)
    return operation_outcome_dto


def stop_docker_statsmanager_thread(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the docker stats manager thread for a specific emulation execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopDockerStatsManagerThreadMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopDockerStatsManagerThread(operation_msg, timeout=timeout)
    return operation_outcome_dto


def get_docker_stats_manager_status(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        port: int, timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.DockerStatsMonitorStatusDTO:
    """
    Stops the docker stats manager thread for a specific emulation execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param port: the port that the docker statsmanage is listening to
    :return: a DockerStatsMonitorStatusDTO with the docker stats managers statuses
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetDockerStatsManagerStatusMsg(port=port)
    stats_manager_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.DockerStatsMonitorStatusDTO = \
        stub.getDockerStatsManagerStatus(operation_msg, timeout=timeout)
    return stats_manager_status_dto


def remove_docker_networks(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        networks: List[str], timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Removes a list of docker networks

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param networks: the list of docker networks to remove
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.RemoveDockerNetworksMsg(networks=networks)
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.removeDockerNetworks(operation_msg, timeout=timeout)
    return operation_outcome_dto


def remove_all_docker_networks(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Remove all docker networks

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.RemoveAllDockerNetworksMsg()
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.removeAllDockerNetworks(operation_msg, timeout=timeout)
    return operation_outcome_dto


def get_docker_stats_manager_info(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.DockerStatsManagersInfoDTO:
    """
    Gets the docker stats manager info

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: a DockerStatsManagersInfoDTO with the infos
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetDockerStatsManagersInfoMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    stats_managers_info_dto: csle_cluster.cluster_manager.cluster_manager_pb2.DockerStatsManagersInfoDTO = \
        stub.getDockerStatsManagersInfo(operation_msg, timeout=timeout)
    return stats_managers_info_dto


def stop_elk_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stop elk manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopElkManagerMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopElkManager(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_elk_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the elk manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartElkManagerMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startElkManager(operation_msg, timeout=timeout)
    return operation_outcome_dto


def get_elk_status(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ElkStatusDTO:
    """
    Gets the status of the Elk stack

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an ElkStatusDTO with the status
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetElkStackStatusMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    elk_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ElkStatusDTO = \
        stub.getElkStatus(operation_msg, timeout=timeout)
    return elk_status_dto


def stop_elk_stack(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the ELK stack

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopElkStackMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopElkStack(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_elastic(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts elastic

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartElasticServiceMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startElastic(operation_msg, timeout=timeout)
    return operation_outcome_dto


def stop_elastic(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops elastic

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopElasticServiceMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopElastic(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_kibana(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts Kibana

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartKibanaServiceMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startKibana(operation_msg, timeout=timeout)
    return operation_outcome_dto


def stop_kibana(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops Kibana

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopKibanaServiceMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopKibana(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_logstash(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts Logstash

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartLogstashServiceMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startLogstash(operation_msg, timeout=timeout)
    return operation_outcome_dto


def stop_logstash(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops Logstash

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopLogstashServiceMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopLogstash(operation_msg, timeout=timeout)
    return operation_outcome_dto


def get_elk_managers_info(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ElkManagersInfoDTO:
    """
    Gets the Elk managers info

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: a ElkManagersInfoDTO with the infos
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetElkManagersInfoMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    elk_managers_info_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ElkManagersInfoDTO = \
        stub.getElkManagersInfo(operation_msg, timeout=timeout)
    return elk_managers_info_dto


def start_containers_of_execution(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the containers of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartContainersOfExecutionMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startContainersOfExecution(operation_msg, timeout=timeout)
    return operation_outcome


def run_container(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        image: str, name: str, memory: int, num_cpus: int, create_network: bool,
        version: str, timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Runs a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param name: the name of the container
    :param image: the image of the container
    :param memory: the memory (GB) of the container
    :param num_cpus: the number of CPUs of the container
    :param create_network: whether to create a network for the container or not
    :param version: the version of the container
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.RunContainerMsg(
        image=image, name=name, num_cpus=num_cpus, create_network=create_network, version=version,
        memory=memory
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.runContainer(operation_msg, timeout=timeout)
    return operation_outcome


def stop_containers_of_execution(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the containers of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopContainersOfExecutionMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopContainersOfExecution(operation_msg, timeout=timeout)
    return operation_outcome


def start_host_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the host manager of a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param container_ip: the ip of the container to start the host manager
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartHostManagerMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startHostManager(operation_msg, timeout=timeout)
    return operation_outcome


def stop_host_managers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops all host managers of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopHostManagersMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopHostManagers(operation_msg, timeout=timeout)
    return operation_outcome


def stop_host_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops a specific host manager

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param container_ip: the ip of the container
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopHostManagerMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopHostManager(operation_msg, timeout=timeout)
    return operation_outcome


def start_host_monitor_threads(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the host monitor threads of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartHostMonitorThreadsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startHostMonitorThreads(operation_msg, timeout=timeout)
    return operation_outcome


def stop_filebeats(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops all filebeats of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopFilebeatsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopFilebeats(operation_msg, timeout=timeout)
    return operation_outcome


def stop_packetbeats(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops all packetbeats of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopPacketbeatsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopPacketbeats(operation_msg, timeout=timeout)
    return operation_outcome


def stop_metricbeats(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops all metricbeats of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopMetricbeatsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopMetricbeats(operation_msg, timeout=timeout)
    return operation_outcome


def stop_heartbeats(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops all heartbeats of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopHeartbeatsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopHeartbeats(operation_msg, timeout=timeout)
    return operation_outcome


def start_host_monitor_thread(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts a specific host monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param container_ip: the ip of the container
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartHostMonitorThreadMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startHostMonitorThread(operation_msg, timeout=timeout)
    return operation_outcome


def start_filebeat(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str, initial_start: bool = False,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops filebeat on a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param container_ip: the ip of the container
    :param initial_start: boolean flag indicating whether it is an initial start or not
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartFileBeatMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip, initialStart=initial_start
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startFilebeat(operation_msg, timeout=timeout)
    return operation_outcome


def start_packetbeat(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str, initial_start: bool = False,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts packetbeat on a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param container_ip: the ip of the container
    :param initial_start: boolean flag indicating whether it is an initial start or not
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartPacketBeatMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip, initialStart=initial_start
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startPacketbeat(operation_msg, timeout=timeout)
    return operation_outcome


def start_metricbeat(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str, initial_start: bool = False,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts metricbeat on a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param initial_start: boolean flag indicating whether it is an initial start or not
    :param container_ip: the ip of the container
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartMetricBeatMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip, initialStart=initial_start
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startMetricbeat(operation_msg, timeout=timeout)
    return operation_outcome


def start_heartbeat(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str, initial_start: bool = False,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts heartbeat on a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the IP of the container
    :param initial_start: boolean flag indicating whether it is an initial start or not
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartHeartBeatMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip, initialStart=initial_start
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startHeartbeat(operation_msg, timeout=timeout)
    return operation_outcome


def stop_filebeat(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops filebeat on a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param container_ip: the ip of the container
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopFileBeatMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopFilebeat(operation_msg, timeout=timeout)
    return operation_outcome


def stop_packetbeat(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops packetbeat on a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param container_ip: the IP of the container
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopPacketBeatMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopPacketbeat(operation_msg, timeout=timeout)
    return operation_outcome


def stop_metricbeat(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops metricbeat on a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the IP of the container
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopMetricBeatMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopMetricbeat(operation_msg, timeout=timeout)
    return operation_outcome


def stop_heartbeat(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops heartbeat on a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param container_ip: the ip of the container
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopHeartBeatMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopHeartbeat(operation_msg, timeout=timeout)
    return operation_outcome


def apply_filebeat_config(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Applies the filebeat config to a specific node

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param container_ip: the ip of the container
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ApplyFileBeatConfigMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.applyFileBeatConfig(operation_msg, timeout=timeout)
    return operation_outcome


def apply_packetbeat_config(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Applies the packetbeat configuration to a specific node

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param container_ip: the ip of the container
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ApplyPacketBeatConfigMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.applyPacketBeatConfig(operation_msg, timeout=timeout)
    return operation_outcome


def apply_metricbeat_config(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Applies the metricbeat  configuration to a specific node

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the IP of the node to apply the config
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ApplyMetricBeatConfigMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.applyMetricBeatConfig(operation_msg, timeout=timeout)
    return operation_outcome


def apply_heartbeat_config(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Applies the heartbeat configuration to a specific node

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the IP of the node to apply the config
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ApplyHeartBeatConfigMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.applyHeartBeatConfig(operation_msg, timeout=timeout)
    return operation_outcome


def get_host_monitor_threads_statuses(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.HostManagerStatusesDTO:
    """
    Gets the host monitor thread statuses of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the monitor thread statuses
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetHostMonitorThreadsStatusesMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    statuses: csle_cluster.cluster_manager.cluster_manager_pb2.HostManagerStatusesDTO = \
        stub.getHostMonitorThreadsStatuses(operation_msg, timeout=timeout)
    return statuses


def get_host_managers_info(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.HostManagersInfoDTO:
    """
    Gets the host managers info of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the host managers info
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetHostManagersInfoMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    host_managers_info: csle_cluster.cluster_manager.cluster_manager_pb2.HostManagersInfoDTO = \
        stub.getHostManagersInfo(operation_msg, timeout=timeout)
    return host_managers_info


def stop_kafka_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the kafka manager in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopKafkaManagerMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopKafkaManager(operation_msg, timeout=timeout)
    return operation_outcome


def start_kafka_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the kafka manager in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartKafkaManagerMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startKafkaManager(operation_msg, timeout=timeout)
    return operation_outcome


def create_kafka_topics(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Creates the kafka topics in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.CreateKafkaTopicsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.createKafkaTopics(operation_msg, timeout=timeout)
    return operation_outcome


def get_kafka_status(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.KafkaStatusDTO:
    """
    Gets the Kafka status in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the kafka status
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetKafkaManagerStatusMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    kafka_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.KafkaStatusDTO = \
        stub.getKafkaStatus(operation_msg, timeout=timeout)
    return kafka_status_dto


def stop_kafka_server(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the kafka server in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopKafkaServerMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopKafkaServer(operation_msg, timeout=timeout)
    return operation_outcome


def start_kafka_server(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the kafka server in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartKafkaServerMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startKafkaServer(operation_msg, timeout=timeout)
    return operation_outcome


def get_kafka_managers_info(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.KafkaManagersInfoDTO:
    """
    Gets the info of kafka managers

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetKafkaManagersInfoMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    kafka_managers_info: csle_cluster.cluster_manager.cluster_manager_pb2.KafkaManagersInfoDTO = \
        stub.getKafkaManagersInfo(operation_msg, timeout=timeout)
    return kafka_managers_info


def stop_ossec_idses(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stop the OSSEC IDSes in a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopOSSECIDSesMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopOSSECIDSes(operation_msg, timeout=timeout)
    return operation_outcome


def stop_ossec_ids(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the OSSEC IDS on a specific host

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the IP of the node to apply the config
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopOSSECIDSMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopOSSECIDS(operation_msg, timeout=timeout)
    return operation_outcome


def start_ossec_ids(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the OSSEC IDS on a specific host

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the IP of the node to apply the config
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartOSSECIDSMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startOSSECIDS(operation_msg, timeout=timeout)
    return operation_outcome


def start_ossec_ids_managers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the OSSEC IDS managers for a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartOSSECIDSManagers(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startOSSECIDSManagers(operation_msg, timeout=timeout)
    return operation_outcome


def stop_ossec_ids_managers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the OSSEC IDS managers of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopOSSECIDSManagers(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopOSSECIDSManagers(operation_msg, timeout=timeout)
    return operation_outcome


def start_ossec_ids_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the OSSEC IDS manager on a specific node

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the IP of the node to apply the config
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartOSSECIDSManager(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startOSSECIDSManager(operation_msg, timeout=timeout)
    return operation_outcome


def stop_ossec_ids_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the OSSEC IDS manager on a specific node

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the IP of the node to apply the config
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopOSSECIDSManager(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopOSSECIDSManager(operation_msg, timeout=timeout)
    return operation_outcome


def start_ossec_ids_monitor_thread(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the OSSEC IDS monitor thread on a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the IP of the node to apply the config
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartOSSECIDSMonitorThreadMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startOSSECIDSMonitorThread(operation_msg, timeout=timeout)
    return operation_outcome


def stop_ossec_ids_monitor_thread(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the OSSEC IDS monitor thread on a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the IP of the node to apply the config
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopOSSECIDSMonitorThreadMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopOSSECIDSMonitorThread(operation_msg, timeout=timeout)
    return operation_outcome


def stop_ossec_ids_monitor_threads(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the OSSEC IDS monitor threads for a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopOSSECIDSMonitorThreadsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopOSSECIDSMonitorThreads(operation_msg, timeout=timeout)
    return operation_outcome


def get_ossec_ids_monitor_thread_statuses(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OSSECIdsMonitorThreadStatusesDTO:
    """
    Gets the OSSEC IDS monitor thread statuses for a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the statuses
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetOSSECIDSMonitorThreadStatusesMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    statuses: csle_cluster.cluster_manager.cluster_manager_pb2.OSSECIdsMonitorThreadStatusesDTO = \
        stub.getOSSECIDSMonitorThreadStatuses(operation_msg, timeout=timeout)
    return statuses


def get_ossec_ids_managers_info(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OSSECIdsManagersInfoDTO:
    """
    Gets the info of OSSEC IDS managers

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the info
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetOSSECIDSManagersInfoMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    info: csle_cluster.cluster_manager.cluster_manager_pb2.OSSECIdsManagersInfoDTO = \
        stub.getOSSECIdsManagersInfo(operation_msg, timeout=timeout)
    return info


def start_ryu_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the Ryu manager for a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartRyuManagerMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startRyuManager(operation_msg, timeout=timeout)
    return operation_outcome


def stop_ryu_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the Ryu manager for a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopRyuManagerMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopRyuManager(operation_msg, timeout=timeout)
    return operation_outcome


def get_ryu_status(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.RyuManagerStatusDTO:
    """
    Gets the Ryu status

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the status
    """
    get_status_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetRyuServiceStatusMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    status: csle_cluster.cluster_manager.cluster_manager_pb2.RyuManagerStatusDTO = \
        stub.getRyuStatus(get_status_msg, timeout=timeout)
    return status


def start_ryu(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts Ryu

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartRyuServiceMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startRyu(operation_msg, timeout=timeout)
    return operation_outcome


def stop_ryu(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops Ryu

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopRyuServiceMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopRyu(operation_msg, timeout=timeout)
    return operation_outcome


def get_ryu_managers_info(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.RyuManagersInfoDTO:
    """
    Gets the info of Ryu managers

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the infos
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetRyuManagersInfoMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    infos: csle_cluster.cluster_manager.cluster_manager_pb2.RyuManagersInfoDTO = \
        stub.getRyuManagersInfo(operation_msg, timeout=timeout)
    return infos


def stop_snort_idses(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the Snort IDSes for a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopSnortIdsesMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopSnortIdses(operation_msg, timeout=timeout)
    return operation_outcome


def stop_snort_idses_monitor_threads(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the Snort IDSes monitor threads for a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopSnortIdsesMonitorThreadsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopSnortIdsesMonitorThreads(operation_msg, timeout=timeout)
    return operation_outcome


def stop_snort_ids(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the Snort IDS on a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the ip of the container
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopSnortMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopSnortIds(operation_msg, timeout=timeout)
    return operation_outcome


def stop_snort_ids_monitor_thread(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the Snort IDS Monitor Thread on a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the ip of the container
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopSnortIdsMonitorThreadMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopSnortIdsMonitorThread(operation_msg, timeout=timeout)
    return operation_outcome


def start_snort_ids(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the Snort IDS on a specific container in a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the ip of the container
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartSnortMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startSnortIds(operation_msg, timeout=timeout)
    return operation_outcome


def start_snort_ids_monitor_thread(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the Snort IDS monitor thread on a specific container in a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param container_ip: the ip of the container
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartSnortIdsMonitorThreadMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startSnortIdsMonitorThread(operation_msg, timeout=timeout)
    return operation_outcome


def start_snort_ids_monitor_threads(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the Snort IDS monitor threads of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartSnortIdsMonitorThreadsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startSnortIdsMonitorThreads(operation_msg, timeout=timeout)
    return operation_outcome


def start_snort_ids_managers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the Snort IDS managers of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartSnortIdsManagersMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startSnortIdsManagers(operation_msg, timeout=timeout)
    return operation_outcome


def stop_snort_ids_managers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the Snort IDS managers of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopSnortIdsManagersMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopSnortIdsManagers(operation_msg, timeout=timeout)
    return operation_outcome


def start_snort_ids_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the Snort IDS manager at a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param container_ip: the ip of the container
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartSnortIdsManagerMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startSnortIdsManager(operation_msg, timeout=timeout)
    return operation_outcome


def stop_snort_ids_manager(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the Snort IDS manager at a specific container

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param container_ip: the ip of the container
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopSnortIdsManagerMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopSnortIdsManager(operation_msg, timeout=timeout)
    return operation_outcome


def stop_snort_ids_monitor_threads(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the Snort IDS managers of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopSnortIdsMonitorThreadsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopSnortIdsMonitorThreads(operation_msg, timeout=timeout)
    return operation_outcome


def get_snort_ids_managers_info(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.SnortIdsManagersInfoDTO:
    """
    Gets the info of Snort IDS managers

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the infos
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetSnortIdsManagersInfoMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    info: csle_cluster.cluster_manager.cluster_manager_pb2.SnortIdsManagersInfoDTO = \
        stub.getSnortIdsManagersInfo(operation_msg, timeout=timeout)
    return info


def get_execution_info(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.ExecutionInfoDTO:
    """
    Gets the info of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the execution info
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetExecutionInfoMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    exec_info: csle_cluster.cluster_manager.cluster_manager_pb2.ExecutionInfoDTO = \
        stub.getExecutionInfo(operation_msg, timeout=timeout)
    return exec_info


def get_snort_ids_monitor_thread_statuses(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.SnortIdsMonitorThreadStatusesDTO:
    """
    Gets the Snort IDS monitor thread statuses for a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the statuses
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetSnortIdsMonitorThreadStatusesMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    statuses: csle_cluster.cluster_manager.cluster_manager_pb2.SnortIdsMonitorThreadStatusesDTO = \
        stub.getSnortIdsMonitorThreadStatuses(operation_msg, timeout=timeout)
    return statuses


def create_kibana_tunnel(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Creates a Kibana tunnel for a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.CreateKibanaTunnelMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.createKibanaTunnel(operation_msg, timeout=timeout)
    return operation_outcome


def create_ryu_tunnel(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Creates a Ryu tunnel for a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.CreateRyuTunnelMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.createRyuTunnel(operation_msg, timeout=timeout)
    return operation_outcome


def list_kibana_tunnels(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.KibanaTunnelsDTO:
    """
    Lists the Kibana tunnels of a specific server

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ListKibanaTunnelsMsg()
    kibana_tunnels_dto: csle_cluster.cluster_manager.cluster_manager_pb2.KibanaTunnelsDTO = \
        stub.listKibanaTunnels(operation_msg, timeout=timeout)
    return kibana_tunnels_dto


def list_ryu_tunnels(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.RyuTunnelsDTO:
    """
    Lists the Ryu tunnels of a specific server

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.ListRyuTunnelsMsg()
    ryu_tunnels_dto: csle_cluster.cluster_manager.cluster_manager_pb2.RyuTunnelsDTO = \
        stub.listRyuTunnels(operation_msg, timeout=timeout)
    return ryu_tunnels_dto


def remove_ryu_tunnel(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Removes a Ryu tunnel for a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.RemoveRyuTunnelMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = stub.removeRyuTunnel(
        operation_msg, timeout=timeout)
    return operation_outcome


def remove_kibana_tunnel(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Removes a Kibana tunnel for a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.RemoveKibanaTunnelMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.removeKibanaTunnel(operation_msg, timeout=timeout)
    return operation_outcome


def stop_host_monitor_threads(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the host monitor threads of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopHostMonitorThreadsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopHostMonitorThreads(operation_msg, timeout=timeout)
    return operation_outcome


def stop_host_monitor_thread(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops a specific host monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param container_ip: the ip of the container
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopHostMonitorThreadMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopHostMonitorThread(operation_msg, timeout=timeout)
    return operation_outcome


def start_ryu_monitor(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the Ryu monitor for a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartRyuMonitorThreadMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startRyuMonitor(operation_msg, timeout=timeout)
    return operation_outcome


def stop_ryu_monitor(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the Ryu monitor for a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopRyuMonitorThreadMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopRyuMonitor(operation_msg, timeout=timeout)
    return operation_outcome


def get_ryu_manager_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Gets the logs of the Ryu manager of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the logs
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetRyuManagerLogsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    logs: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getRyuManagerLogs(operation_msg, timeout=timeout)
    return logs


def get_ryu_controller_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Gets the logs of the Ryu controller of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the logs
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetRyuControllerLogsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    logs: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getRyuControllerLogs(operation_msg, timeout=timeout)
    return logs


def get_elk_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Gets the logs of the ELK stack of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the logs
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetElkLogsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    logs: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getElkLogs(operation_msg, timeout=timeout)
    return logs


def get_elk_manager_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Gets the logs of the ELK manager of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the logs
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetElkManagerLogsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    logs: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getElkManagerLogs(operation_msg, timeout=timeout)
    return logs


def get_traffic_manager_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Gets the logs of a specific Traffic manager of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param container_ip: the ip of the container
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the logs
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetTrafficManagerLogsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    logs: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getTrafficManagerLogs(operation_msg, timeout=timeout)
    return logs


def get_host_manager_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Gets the logs of a specific host manager of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param container_ip: the ip of the container
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the logs
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetHostManagerLogsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    logs: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getHostManagerLogs(operation_msg, timeout=timeout)
    return logs


def get_ossec_ids_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Gets the logs of a specific OSSEC IDS of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param container_ip: the ip of the container
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the logs
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetOSSECIdsLogsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    logs: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getOSSECIdsLogs(operation_msg, timeout=timeout)
    return logs


def get_ossec_ids_manager_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Gets the logs of a specific OSSEC IDS Manager of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param container_ip: the ip of the container
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the logs
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetOSSECIdsManagerLogsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    logs: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getOSSECIdsManagerLogsMsg(operation_msg, timeout=timeout)
    return logs


def get_snort_ids_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Gets the logs of a specific Snort IDS of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param container_ip: the ip of the container
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the logs
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetSnortIdsLogsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    logs: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getSnortIdsLogs(operation_msg, timeout=timeout)
    return logs


def get_snort_ids_manager_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Gets the logs of a specific Snort IDS of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param container_ip: the ip of the container
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the logs
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetSnortIdsManagerLogsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    logs: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getSnortIdsManagerLogsMsg(operation_msg, timeout=timeout)
    return logs


def get_kafka_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Gets the logs of the Kafka server of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the logs
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetKafkaLogsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    logs: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getKafkaLogs(operation_msg, timeout=timeout)
    return logs


def get_kafka_manager_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Gets the logs of the Kafka manager of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the logs
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetKafkaManagerLogsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    logs: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getKafkaManagerLogs(operation_msg, timeout=timeout)
    return logs


def get_client_manager_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Gets the logs of the Client manager of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the logs
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetClientManagerLogsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation
    )
    logs: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getClientManagerLogsMsg(operation_msg, timeout=timeout)
    return logs


def get_container_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Gets the logs of a specific container of a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param container_ip: the ip of the container
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the logs
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetContainerLogsMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    logs: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getContainerLogs(operation_msg, timeout=timeout)
    return logs


def get_cluster_manager_logs(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
    """
    Fetches the logs of the cluster manager on a given physical node

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a LogsDTO with the logs
    """
    get_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetClusterManagerLogsMsg()
    logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO = \
        stub.getClusterManagerLogs(get_msg, timeout=timeout)
    return logs_dto


def get_execution_time_series_data(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, minutes: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.EmulationMetricsTimeSeriesDTO:
    """
    Fetches the logs of the cluster manager on a given physical node

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :param minutes: the number of minutes to get the data for
    :return: a DTO with the time series data
    """
    get_msg = csle_cluster.cluster_manager.cluster_manager_pb2.GetExecutionTimeSeriesDataMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet, minutes=minutes
    )
    time_series_dto: csle_cluster.cluster_manager.cluster_manager_pb2.EmulationMetricsTimeSeriesDTO = \
        stub.getExecutionTimeSeriesData(get_msg, timeout=timeout)
    return time_series_dto


def start_spark_servers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the Spark servers of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartSparkServersMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startSparkServers(operation_msg, timeout=timeout)
    return operation_outcome_dto


def stop_spark_servers(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the Spark servers of a given execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: an OperationOutcomeDTO with the outcome of the operation
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopSparkServersMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopSparkServers(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_spark_server(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Starts the Spark server on a specific container in a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the ip of the container
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartSparkServerMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.startSparkServer(operation_msg, timeout=timeout)
    return operation_outcome


def stop_spark_server(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int, container_ip: str,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops the Spark server on a specific container in a specific execution

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param container_ip: the ip of the container
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the subnet of the execution
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopSparkServerMsg(
        ipFirstOctet=ip_first_octet, emulation=emulation, containerIp=container_ip
    )
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopSparkServer(operation_msg, timeout=timeout)
    return operation_outcome


def check_pid(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        pid: int, timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Checks the status of a PID

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param pid: the pid to check
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.CheckPidMsg(pid=pid)
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.checkPid(operation_msg, timeout=timeout)
    return operation_outcome


def stop_pid(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        pid: int, timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
    """
    Stops a PID

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param pid: the pid to check
    :return: the operation outcome
    """
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopPidMsg(pid=pid)
    operation_outcome: csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO = \
        stub.stopPid(operation_msg, timeout=timeout)
    return operation_outcome
