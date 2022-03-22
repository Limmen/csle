import csle_collector.ids_manager.ids_manager_pb2_grpc
import csle_collector.ids_manager.ids_manager_pb2


def get_ids_monitor_status(
        stub: csle_collector.ids_manager.ids_manager_pb2_grpc.IdsManagerStub) \
        -> csle_collector.ids_manager.ids_manager_pb2.IdsMonitorDTO:
    """
    Queries the IDS manager for the status of the IDS monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :return: an IdsMonitorDTO describing the status of the IDS monitor thread
    """
    get_ids_monitor_status_msg = \
        csle_collector.ids_manager.ids_manager_pb2.GetIdsMonitorStatusMsg()
    ids_monitor_dto = stub.getIdsMonitorStatus(get_ids_monitor_status_msg)
    return ids_monitor_dto


def start_ids_monitor(stub: csle_collector.ids_manager.ids_manager_pb2_grpc.IdsManagerStub,
        kafka_ip : str, kafka_port: int, log_file_path: str, time_step_len_seconds: int) \
        -> csle_collector.ids_manager.ids_manager_pb2.IdsMonitorDTO:
    """
    Sends a request to the IDS manager to start the IDS monitor thread

    :param kafka_ip: the ip of the Kafka server
    :param kafka_port: the port of the Kafka server
    :param log_file_path: the path top the IDS log
    :param time_step_len_seconds: the length of one time-step
    :param stub: the stub to send the remote gRPC to the server
    :return: an IdsMonitorDTO describing the status of the IDS monitor thread
    """
    start_ids_monitor_msg = csle_collector.ids_manager.ids_manager_pb2.StartIdsMonitorMsg(
        kafka_ip=kafka_ip, kafka_port=kafka_port, log_file_path=log_file_path,
        time_step_len_seconds=time_step_len_seconds
    )
    ids_monitor_dto = stub.startIdsMonitor(start_ids_monitor_msg)
    return ids_monitor_dto


def stop_ids_monitor(
        stub: csle_collector.ids_manager.ids_manager_pb2_grpc.IdsManagerStub) \
        -> csle_collector.ids_manager.ids_manager_pb2.IdsMonitorDTO:
    """
    Sends a request to the IDS manager to stop the IDS monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :return: an IdsMonitorDTO describing the status of the IDS monitor thread
    """
    stop_ids_monitor_msg = \
        csle_collector.ids_manager.ids_manager_pb2.StopIdsMonitorMsg()
    ids_monitor_dto = stub.stopIdsMonitor(stop_ids_monitor_msg)
    return ids_monitor_dto


def get_ids_alerts(
        stub: csle_collector.ids_manager.ids_manager_pb2_grpc.IdsManagerStub, timestamp: float,
        log_file_path: str) -> csle_collector.ids_manager.ids_manager_pb2.IdsLogDTO:
    """
    Queries the IDS manager for the data of the IDS log from a given time-step

    :param stub: the stub to send the remote gRPC to the server
    :param timestamp: the timtestamp to parse the log from
    :param log_file_path: path to the IDS log file to read
    :return: an IdsLogDTO with data of the IDS log
    """
    get_ids_log_alerts_msg = \
        csle_collector.ids_manager.ids_manager_pb2.GetIdsAlertsMsg(
            timestamp=timestamp, log_file_path=log_file_path)
    ids_monitor_dto = stub.getIdsMonitorStatus(get_ids_log_alerts_msg)
    return ids_monitor_dto