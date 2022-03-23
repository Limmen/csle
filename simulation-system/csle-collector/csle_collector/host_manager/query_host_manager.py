import csle_collector.host_manager.host_manager_pb2_grpc
import csle_collector.host_manager.host_manager_pb2


def get_host_monitor_status(
        stub: csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub) \
        -> csle_collector.host_manager.host_manager_pb2.HostMonitorDTO:
    """
    Queries the Host manager for the status of the Host monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :return: an HostMonitorDTO describing the status of the Host monitor thread
    """
    get_host_monitor_status_msg = \
        csle_collector.host_manager.host_manager_pb2.GetHostMonitorStatusMsg()
    host_monitor_dto = stub.getHostMonitorStatus(get_host_monitor_status_msg)
    return host_monitor_dto


def start_host_monitor(stub: csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub,
        kafka_ip : str, kafka_port: int, time_step_len_seconds: int) \
        -> csle_collector.host_manager.host_manager_pb2.HostMonitorDTO:
    """
    Sends a request to the Host manager to start the Host monitor thread

    :param kafka_ip: the ip of the Kafka server
    :param kafka_port: the port of the Kafka server
    :param time_step_len_seconds: the length of one time-step
    :param stub: the stub to send the remote gRPC to the server
    :return: an HostMonitorDTO describing the status of the Host monitor thread
    """
    start_host_monitor_msg = csle_collector.host_manager.host_manager_pb2.StartHostMonitorMsg(
        kafka_ip=kafka_ip, kafka_port=kafka_port, time_step_len_seconds=time_step_len_seconds
    )
    host_monitor_dto = stub.startHostMonitor(start_host_monitor_msg)
    return host_monitor_dto


def stop_host_monitor(
        stub: csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub) \
        -> csle_collector.host_manager.host_manager_pb2.HostMonitorDTO:
    """
    Sends a request to the Host manager to stop the Host monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :return: an HostMonitorDTO describing the status of the Host monitor thread
    """
    stop_host_monitor_msg = \
        csle_collector.host_manager.host_manager_pb2.StopHostMonitorMsg()
    host_monitor_dto = stub.stopHostMonitor(stop_host_monitor_msg)
    return host_monitor_dto


def get_host_metrics(
        stub: csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub, failed_auth_last_ts: float,
        login_last_ts: float) -> csle_collector.host_manager.host_manager_pb2.HostMetricsDTO:
    """
    Queries the Host manager for the data of the Host metrics from given timestamps

    :param stub: the stub to send the remote gRPC to the server
    :param failed_auth_last_ts: the timtestamp to parse failed login from
    :param login_last_ts: the timtestamp to parse the last login from
    :return: an HostMetricsDTO with host metrics
    """
    get_host_metrics_msg = \
        csle_collector.host_manager.host_manager_pb2.GetHostMetricsMsg(
            failed_auth_last_ts=failed_auth_last_ts, login_last_ts=login_last_ts)
    host_metrics_dto = stub.getHostMetrics(get_host_metrics_msg)
    return host_metrics_dto