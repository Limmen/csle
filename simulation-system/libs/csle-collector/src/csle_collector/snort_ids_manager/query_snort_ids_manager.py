import csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc
import csle_collector.snort_ids_manager.snort_ids_manager_pb2
import csle_collector.constants.constants as constants


def get_snort_ids_monitor_status(
        stub: csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.SnortIdsManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO:
    """
    Queries the IDS manager for the status of the IDS monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an IdsMonitorDTO describing the status of the IDS monitor thread
    """
    get_ids_monitor_status_msg = \
        csle_collector.snort_ids_manager.snort_ids_manager_pb2.GetSnortIdsMonitorStatusMsg()
    ids_monitor_dto: csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO = \
        stub.getSnortIdsMonitorStatus(get_ids_monitor_status_msg, timeout=timeout)
    return ids_monitor_dto


def start_snort_ids_monitor(stub: csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.SnortIdsManagerStub,
                            kafka_ip: str, kafka_port: int, log_file_path: str, time_step_len_seconds: int,
                            timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO:
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
    start_ids_monitor_msg = csle_collector.snort_ids_manager.snort_ids_manager_pb2.StartSnortIdsMonitorMsg(
        kafka_ip=kafka_ip, kafka_port=kafka_port, log_file_path=log_file_path,
        time_step_len_seconds=time_step_len_seconds
    )
    ids_monitor_dto: csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO = \
        stub.startSnortIdsMonitor(start_ids_monitor_msg, timeout=timeout)
    return ids_monitor_dto


def stop_snort_ids_monitor(
        stub: csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.SnortIdsManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO:
    """
    Sends a request to the IDS manager to stop the IDS monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an IdsMonitorDTO describing the status of the IDS monitor thread
    """
    stop_ids_monitor_msg = \
        csle_collector.snort_ids_manager.snort_ids_manager_pb2.StopSnortIdsMonitorMsg()
    ids_monitor_dto: csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO = \
        stub.stopSnortIdsMonitor(stop_ids_monitor_msg, timeout=timeout)
    return ids_monitor_dto


def stop_snort_ids(
        stub: csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.SnortIdsManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO:
    """
    Sends a request to the IDS manager to stop the Snort IDS

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an IdsMonitorDTO describing the status of the IDS and its monitor thread
    """
    stop_ids_msg = \
        csle_collector.snort_ids_manager.snort_ids_manager_pb2.StopSnortIdsMsg()
    ids_monitor_dto: csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO = \
        stub.stopSnortIds(stop_ids_msg, timeout=timeout)
    return ids_monitor_dto


def start_snort_ids(
        stub: csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.SnortIdsManagerStub,
        ingress_interface: str, egress_interface: str, subnetmask: str, timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO:
    """
    Sends a request to the IDS manager to start the Snort IDS

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param ingress_interface: the ingress interface that Snort will listen to
    :param egress_interface: the egress interface that Snort will listen to
    :param subnetmask: the subnetmask that Snort will listen to
    :return: an IdsMonitorDTO describing the status of the IDS and its monitor thread
    """
    start_ids_msg = \
        csle_collector.snort_ids_manager.snort_ids_manager_pb2.StartSnortIdsMsg(
            ingress_interface=ingress_interface, egress_interface=egress_interface, subnetmask=subnetmask
        )
    ids_monitor_dto: csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO = \
        stub.startSnortIds(start_ids_msg, timeout=timeout)
    return ids_monitor_dto


def get_snort_ids_alerts(
        stub: csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.SnortIdsManagerStub, timestamp: float,
        log_file_path: str, timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsLogDTO:
    """
    Queries the IDS manager for the data of the IDS log from a given time-step

    :param stub: the stub to send the remote gRPC to the server
    :param timestamp: the timtestamp to parse the log from
    :param log_file_path: path to the IDS log file to read
    :param timeout: the GRPC timeout (seconds)
    :return: an IdsLogDTO with data of the IDS log
    """
    get_ids_log_alerts_msg = \
        csle_collector.snort_ids_manager.snort_ids_manager_pb2.GetSnortIdsAlertsMsg(
            timestamp=timestamp, log_file_path=log_file_path)
    ids_log_dto: csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsLogDTO = \
        stub.getSnortIdsAlerts(get_ids_log_alerts_msg, timeout=timeout)
    return ids_log_dto
