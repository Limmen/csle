import csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc
import csle_collector.ossec_ids_manager.ossec_ids_manager_pb2
import csle_collector.constants.constants as constants


def get_ossec_ids_monitor_status(
        stub: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO:
    """
    Queries the IDS manager for the status of the IDS monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :return: an IdsMonitorDTO describing the status of the IDS monitor thread
    """
    get_ids_monitor_status_msg = \
        csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.GetOSSECIdsMonitorStatusMsg()
    ids_monitor_dto: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO = \
        stub.getOSSECIdsMonitorStatus(get_ids_monitor_status_msg, timeout=timeout)
    return ids_monitor_dto


def start_ossec_ids_monitor(stub: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub,
                            kafka_ip: str, kafka_port: int, log_file_path: str, time_step_len_seconds: int,
                            timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO:
    """
    Sends a request to the IDS manager to start the IDS monitor thread

    :param kafka_ip: the ip of the Kafka server
    :param kafka_port: the port of the Kafka server
    :param log_file_path: the path top the IDS log
    :param time_step_len_seconds: the length of one time-step
    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an IdsMonitorDTO describing the status of the IDS monitor thread
    """
    start_ids_monitor_msg = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.StartOSSECIdsMonitorMsg(
        kafka_ip=kafka_ip, kafka_port=kafka_port, log_file_path=log_file_path,
        time_step_len_seconds=time_step_len_seconds
    )
    ids_monitor_dto: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO = \
        stub.startOSSECIdsMonitor(start_ids_monitor_msg, timeout=timeout)
    return ids_monitor_dto


def stop_ossec_ids_monitor(
        stub: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO:
    """
    Sends a request to the IDS manager to stop the IDS monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an IdsMonitorDTO describing the status of the IDS monitor thread
    """
    stop_ids_monitor_msg = \
        csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.StopOSSECIdsMonitorMsg()
    ids_monitor_dto: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO = \
        stub.stopOSSECIdsMonitor(stop_ids_monitor_msg, timeout=timeout)
    return ids_monitor_dto


def stop_ossec_ids(
        stub: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO:
    """
    Sends a request to the OSSEC IDS manager to stop the IDS

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an OSSECIdsMonitorDTO describing the status of the IDS and its monitor thread
    """
    stop_ossec_ids_msg = \
        csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.StopOSSECIdsMsg()
    ids_monitor_dto: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO = \
        stub.stopOSSECIds(stop_ossec_ids_msg, timeout=timeout)
    return ids_monitor_dto


def start_ossec_ids(
        stub: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO:
    """
    Sends a request to the OSSEC IDS manager to start the IDS

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an OSSECIdsMonitorDTO describing the status of the IDS and its monitor thread
    """
    start_ossec_ids_msg = \
        csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.StartOSSECIdsMsg()
    ids_monitor_dto: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO = \
        stub.startOSSECIds(start_ossec_ids_msg, timeout=timeout)
    return ids_monitor_dto


def get_ossec_ids_alerts(
        stub: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerStub, timestamp: float,
        log_file_path: str, timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsLogDTO:
    """
    Queries the IDS manager for the data of the IDS log from a given time-step

    :param stub: the stub to send the remote gRPC to the server
    :param timestamp: the timtestamp to parse the log from
    :param log_file_path: path to the IDS log file to read
    :param timeout: the GRPC timeout (seconds)
    :return: an IdsLogDTO with data of the IDS log
    """
    get_ids_log_alerts_msg = \
        csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.GetOSSECIdsAlertsMsg(
            timestamp=timestamp, log_file_path=log_file_path)
    ids_log_dto: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsLogDTO = \
        stub.getOSSECIdsAlerts(get_ids_log_alerts_msg, timeout=timeout)
    return ids_log_dto
