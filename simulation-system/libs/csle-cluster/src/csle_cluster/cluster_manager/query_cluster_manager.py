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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartPostgreSQLMsg()
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartCAdvisorMsg()
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartNodeExporterMsg()
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartGrafanaMsg()
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartPrometheusMsg()
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartPgAdminMsg()
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartNginxMsg()
    service_status_dto = stub.startNginx(start_msg, timeout=timeout)
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartDockerStatsManagerMsg()
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
    start_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartDockerEngineMsg()
    service_status_dto = stub.startDockerEngine(start_msg, timeout=timeout)
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopCAdvisorMsg()
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopNodeExporterMsg()
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopGrafanaMsg()
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopPrometheusMsg()
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopPgAdminMsg()
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopNginxMsg()
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopFlaskMsg()
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopDockerStatsManagerMsg()
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
    stop_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StopDockerEngineMsg()
    service_status_dto = stub.stopDockerEngine(stop_msg, timeout=timeout)
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
    logs_dto = stub.getLogFile(get_log_file_msg, timeout=timeout)
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
    logs_dto = stub.getFlaskLogs(get_msg, timeout=timeout)
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
    logs_dto = stub.getPostrgreSQLLogs(get_msg, timeout=timeout)
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
    logs_dto = stub.getDockerLogs(get_msg, timeout=timeout)
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
    logs_dto = stub.getNginxLogs(get_msg, timeout=timeout)
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
    logs_dto = stub.getGrafanaLogs(get_msg, timeout=timeout)
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
    logs_dto = stub.getPgAdminLogs(get_msg, timeout=timeout)
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
    logs_dto = stub.getCadvisorLogs(get_msg, timeout=timeout)
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
    logs_dto = stub.getNodeExporterLogs(get_msg, timeout=timeout)
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
    logs_dto = stub.getPrometheusLogs(get_msg, timeout=timeout)
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
    logs_dto = stub.getDockerStatsManagerLogs(get_msg, timeout=timeout)
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
    logs_dto = stub.getCsleLogFiles(get_msg, timeout=timeout)
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
    operation_outcome_dto = stub.startContainersInExecution(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.attachContainersInExecutionToNetworks(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.installLibraries(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.applyKafkaConfig(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_ryu(
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
    operation_msg = csle_cluster.cluster_manager.cluster_manager_pb2.StartRyuMsg(
        emulation=emulation, ipFirstOctet=ip_first_octet
    )
    operation_outcome_dto = stub.startRyu(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.applyResourceConstraints(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.createOvsSwitches(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.pingExecution(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.configureOvs(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.startSdnControllerMonitor(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.createUsers(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.createVulnerabilities(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.createFlags(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.createTopology(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.startTrafficManagers(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.startTrafficGenerators(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.startClientPopulation(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.startKafkaClientProducer(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.stopKafkaClientProducer(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.startSnortIdses(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.startSnortIdsesMonitorThreads(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.startOssecIdses(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.startOssecIdsesMonitorThreads(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.startElkStack(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.startHostManagers(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.applyFileBeatsConfig(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.applyPacketBeatsConfig(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.applyMetricBeatsConfig(operation_msg, timeout=timeout)
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
    operation_outcome_dto = stub.applyHeartBeatsConfig(operation_msg, timeout=timeout)
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
        emulation=emulation, ipFirstOctet=ip_first_octet, initial_start=initial_start
    )
    operation_outcome_dto = stub.startFilebeats(operation_msg, timeout=timeout)
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
        emulation=emulation, ipFirstOctet=ip_first_octet, initial_start=initial_start
    )
    operation_outcome_dto = stub.startMetricbeats(operation_msg, timeout=timeout)
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
        emulation=emulation, ipFirstOctet=ip_first_octet, initial_start=initial_start
    )
    operation_outcome_dto = stub.startHeartbeats(operation_msg, timeout=timeout)
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
        emulation=emulation, ipFirstOctet=ip_first_octet, initial_start=initial_start
    )
    operation_outcome_dto = stub.startPacketbeats(operation_msg, timeout=timeout)
    return operation_outcome_dto


def start_docker_statsmanager_thread(
        stub: csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub,
        emulation: str, ip_first_octet: int,
        timeout=constants.GRPC.OPERATION_TIMEOUT_SECONDS) \
        -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
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
    operation_outcome_dto = stub.startDockerStatsManagerThread(operation_msg, timeout=timeout)
    return operation_outcome_dto
