from typing import List
import csle_collector.host_manager.host_manager_pb2_grpc
import csle_collector.host_manager.host_manager_pb2
import csle_collector.constants.constants as constants


def get_host_status(
        stub: csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
    """
    Queries the Host manager for the status of the Host monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a HostDTO describing the host status
    """
    get_host_monitor_status_msg = \
        csle_collector.host_manager.host_manager_pb2.GetHostStatusMsg()
    host_dto = stub.getHostStatus(get_host_monitor_status_msg, timeout=timeout)
    return host_dto


def start_host_monitor(stub: csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub,
                       kafka_ip: str, kafka_port: int, time_step_len_seconds: int,
                       timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
    """
    Sends a request to the Host manager to start the Host monitor thread

    :param kafka_ip: the ip of the Kafka server
    :param kafka_port: the port of the Kafka server
    :param time_step_len_seconds: the length of one time-step
    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a HostDTO describing the host status
    """
    start_host_monitor_msg = csle_collector.host_manager.host_manager_pb2.StartHostMonitorMsg(
        kafka_ip=kafka_ip, kafka_port=kafka_port, time_step_len_seconds=time_step_len_seconds
    )
    host_dto = stub.startHostMonitor(start_host_monitor_msg, timeout=timeout)
    return host_dto


def stop_host_monitor(
        stub: csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
    """
    Sends a request to the Host manager to stop the Host monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a HostDTO describing the host status
    """
    stop_host_monitor_msg = \
        csle_collector.host_manager.host_manager_pb2.StopHostMonitorMsg()
    host_dto = stub.stopHostMonitor(stop_host_monitor_msg, timeout=timeout)
    return host_dto


def start_filebeat(
        stub: csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
    """
    Sends a request to the Host manager to start filebeat

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a HostDTO describing the host status
    """
    start_filebeat_msg = \
        csle_collector.host_manager.host_manager_pb2.StartFilebeatMsg()
    host_dto = stub.startFilebeat(start_filebeat_msg, timeout=timeout)
    return host_dto


def stop_filebeat(
        stub: csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
    """
    Sends a request to the Host manager to stop filebeat

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a HostDTO describing the host status
    """
    stop_filebeat_msg = \
        csle_collector.host_manager.host_manager_pb2.StopFilebeatMsg()
    host_dto = stub.stopFilebeat(stop_filebeat_msg, timeout=timeout)
    return host_dto


def config_filebeat(
        stub: csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub,
        log_files_paths: List[str], kibana_ip: str, kibana_port: int, elastic_ip: str,
        elastic_port: int, num_elastic_shards: int, kafka_topics : List [str], kafka_ip: str,
        kafka_port: int, filebeat_modules : List [str], reload_enabled: bool = False, kafka: bool = False,
        timeout=constants.GRPC.TIMEOUT_SECONDS) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
    """
    Sends a request to the Host manager to update the filebeat configuration

    :param log_files_paths: the list of log files that filebeat should monitor
    :param kibana_ip: the IP of Kibana where the data should be visualized
    :param kibana_port: the port of Kibana where the data should be visualized
    :param elastic_ip: the IP of elastic where the data should be shipped
    :param elastic_port: the port of elastic where the data should be shipped
    :param num_elastic_shards: the number of elastic shards
    :param reload_enabled: whether automatic reload of modules should be enabled
    :param kafka: whether kafka should be added as input
    :param kafka_topics: list of kafka topics to ingest
    :param kafka_port: the kafka server port
    :param kafka_ip: the kafka server ip
    :param filebeat_modules: a list of filebeat modules to enable
    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a HostDTO describing the host status
    """
    config_filebeat_msg = \
        csle_collector.host_manager.host_manager_pb2.ConfigFilebeatMsg(
            log_files_paths=log_files_paths, kibana_ip=kibana_ip, kibana_port=kibana_port, elastic_ip=elastic_ip,
            elastic_port=elastic_port, num_elastic_shards=num_elastic_shards, reload_enabled=reload_enabled,
            kafka=kafka, kafka_port=kafka_port, kafka_ip=kafka_ip, kafka_topics=kafka_topics,
            filebeat_modules=filebeat_modules)
    host_dto = stub.configFilebeat(config_filebeat_msg, timeout=timeout)
    return host_dto


def get_host_metrics(
        stub: csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub, failed_auth_last_ts: float,
        login_last_ts: float, timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.host_manager.host_manager_pb2.HostMetricsDTO:
    """
    Queries the Host manager for the data of the Host metrics from given timestamps

    :param stub: the stub to send the remote gRPC to the server
    :param failed_auth_last_ts: the timtestamp to parse failed login from
    :param login_last_ts: the timtestamp to parse the last login from
    :param timeout: the GRPC timeout (seconds)
    :return: an HostMetricsDTO with host metrics
    """
    get_host_metrics_msg = \
        csle_collector.host_manager.host_manager_pb2.GetHostMetricsMsg(
            failed_auth_last_ts=failed_auth_last_ts, login_last_ts=login_last_ts)
    host_metrics_dto = stub.getHostMetrics(get_host_metrics_msg, timeout=timeout)
    return host_metrics_dto
