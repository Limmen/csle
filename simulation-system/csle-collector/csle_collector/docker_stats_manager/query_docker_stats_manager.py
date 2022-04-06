from typing import List
import csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc
import csle_collector.docker_stats_manager.docker_stats_manager_pb2


def get_docker_stats_manager_status(
        stub: csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.DockerStatsManagerStub) \
        -> csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO:
    """
    Queries the docker stats manager for the status

    :param stub: the stub to send the remote gRPC to the server
    :return: a DockerStatsManagerDTO describing the status of the server
    """
    get_docker_stats_server_msg = \
        csle_collector.docker_stats_manager.docker_stats_manager_pb2.GetDockerStatsMonitorStatusMsg()
    docker_stats_manager_dto = stub.getDockerStatsMonitorStatus(get_docker_stats_server_msg)
    return docker_stats_manager_dto


def start_docker_stats_monitor(
        stub: csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.DockerStatsManagerStub,
        emulation: str, sink_ip: str, stats_queue_maxsize : int, time_step_len_seconds: int, sink_port: int,
        containers: List[csle_collector.docker_stats_manager.docker_stats_manager_pb2.ContainerIp]) \
        -> csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO:
    """
    Sends a request to the docker stats manager to start a new monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :param emulation: the name of the emulation
    :param sink_ip: the ip of the Kafka server to push stats to
    :param stats_queue_maxsize: the maximum size of the queue
    :param the length of the period between pushing data to Kafka
    :param sink_port: the port of the Kafka server
    :param containers: list of names and ips of  containers to monitor
    :return: a DockerStatsManagerDTO describing the status of the server
    """
    start_docker_stats_monitor_msg = \
        csle_collector.docker_stats_manager.docker_stats_manager_pb2.StartDockerStatsMonitorMsg(
            emulation=emulation, sink_ip=sink_ip, stats_queue_maxsize=stats_queue_maxsize,
            time_step_len_seconds=time_step_len_seconds, sink_port=sink_port, containers=containers
        )
    docker_stats_manager_dto = stub.startDockerStatsMonitor(start_docker_stats_monitor_msg)
    return docker_stats_manager_dto


def stop_docker_stats_monitor(
        stub: csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.DockerStatsManagerStub,
        emulation: str) \
        -> csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO:
    """
    Sends a request to the docker stats manager to start a new monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :param emulation: the emulation for which the monitor should be stopped
    :return: a DockerStatsManagerDTO describing the status of the server
    """
    stop_docker_stats_monitor_msg = \
        csle_collector.docker_stats_manager.docker_stats_manager_pb2.StopDockerStatsMonitorMsg(
            emulation=emulation)
    docker_stats_manager_dto = stub.stopDockerStatsMonitor(stop_docker_stats_monitor_msg)
    return docker_stats_manager_dto
