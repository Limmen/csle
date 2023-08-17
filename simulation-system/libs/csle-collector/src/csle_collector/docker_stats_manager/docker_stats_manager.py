from typing import List
import os
import logging
from concurrent import futures
import grpc
import socket
import csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc
import csle_collector.docker_stats_manager.docker_stats_manager_pb2
import csle_collector.constants.constants as constants
from csle_collector.docker_stats_manager.threads.docker_stats_thread import DockerStatsThread


class DockerStatsManagerServicer(csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.
                                 DockerStatsManagerServicer):
    """
    gRPC server for managing a docker stats monitor server.
    Allows to start/stop the docker stats monitor remotely and also to query the
    state of the server.
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        file_name = constants.LOG_FILES.DOCKER_STATS_MANAGER_LOG_FILE
        dir = constants.LOG_FILES.DOCKER_STATS_MANAGER_LOG_DIR
        logfile = os.path.join(dir, file_name)
        logging.basicConfig(filename=logfile, level=logging.INFO)
        self.docker_stats_monitor_threads: List[DockerStatsThread] = []
        self.hostname = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ip = s.getsockname()[0]
        logging.info(f"Setting up DockerStatsManager, hostname: {self.hostname}, ip: {self.ip}")

    def get_docker_stats_monitor_threads(self) -> List[DockerStatsThread]:
        """
        Gets the list of Docker stats monitor threads

        :return: the list of Docker stats monitor threads
        """
        return self.docker_stats_monitor_threads

    def getDockerStatsMonitorStatus(
            self, request: csle_collector.docker_stats_manager.docker_stats_manager_pb2.GetDockerStatsMonitorStatusMsg,
            context: grpc.ServicerContext) \
            -> csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO:
        """
        Gets the state of the docker stats monitors

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the docker stats manager
        """
        new_docker_stats_monitor_threads = []
        emulations = []
        emulation_executions = []
        docker_stats_monitor_threads = self.get_docker_stats_monitor_threads()
        for dsmt in docker_stats_monitor_threads:
            if dsmt.is_alive() and not dsmt.stopped:
                new_docker_stats_monitor_threads.append(dsmt)
                emulations.append(dsmt.emulation)
                emulation_executions.append(dsmt.execution_first_ip_octet)
            else:
                dsmt.stopped = True
        emulations = list(set(emulations))
        emulation_executions = list(set(emulation_executions))
        self.docker_stats_monitor_threads = new_docker_stats_monitor_threads
        docker_stats_monitor_dto = csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO(
            num_monitors=len(new_docker_stats_monitor_threads), emulations=emulations,
            emulation_executions=emulation_executions)
        return docker_stats_monitor_dto

    def stopDockerStatsMonitor(
            self, request: csle_collector.docker_stats_manager.docker_stats_manager_pb2.StopDockerStatsMonitorMsg,
            context: grpc.ServicerContext):
        """
        Stops the docker stats monitor server

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the docker stats monitor server
        """
        logging.info(f"Stopping the docker stats monitor for emulation:{request.emulation}")

        new_docker_stats_monitor_threads = []
        emulations = []
        emulation_executions = []
        docker_stats_monitor_threads = self.get_docker_stats_monitor_threads()
        for dsmt in docker_stats_monitor_threads:
            if dsmt.emulation == request.emulation \
                    and dsmt.execution_first_ip_octet == request.execution_first_ip_octet:
                dsmt.stopped = True
            else:
                if dsmt.is_alive() and not dsmt.stopped:
                    new_docker_stats_monitor_threads.append(dsmt)
                    emulations.append(dsmt.emulation)
                    emulation_executions.append(dsmt.execution_first_ip_octet)
        self.docker_stats_monitor_threads = new_docker_stats_monitor_threads
        emulations = list(set(emulations))
        emulation_executions = list(set(emulation_executions))
        return csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO(
            num_monitors=len(new_docker_stats_monitor_threads), emulations=emulations,
            emulation_executions=emulation_executions)

    def startDockerStatsMonitor(
            self, request: csle_collector.docker_stats_manager.docker_stats_manager_pb2.StartDockerStatsMonitorMsg,
            context: grpc.ServicerContext) \
            -> csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO:
        """
        Starts a new docker stats monitor

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the docker stats monitor
        """
        logging.info(f"Starting the docker stats monitor for emulation:{request.emulation}")

        # Stop any existing thread with the same name
        new_docker_stats_monitor_threads = []
        emulations = []
        emulation_executions = []
        docker_stats_monitor_threads = self.get_docker_stats_monitor_threads()
        for dsmt in docker_stats_monitor_threads:
            if dsmt.is_alive() and not dsmt.stopped:
                new_docker_stats_monitor_threads.append(dsmt)
                emulations.append(dsmt.emulation)
                emulation_executions.append(dsmt.execution_first_ip_octet)
        docker_stats_monitor_thread = DockerStatsThread(list(request.containers), request.emulation,
                                                        request.execution_first_ip_octet, request.kafka_ip,
                                                        request.stats_queue_maxsize, request.time_step_len_seconds,
                                                        request.kafka_port)
        docker_stats_monitor_thread.start()
        new_docker_stats_monitor_threads.append(docker_stats_monitor_thread)
        emulations.append(request.emulation)
        emulation_executions.append(request.execution_first_ip_octet)
        emulations = list(set(emulations))
        emulation_executions = list(set(emulation_executions))
        self.docker_stats_monitor_threads = new_docker_stats_monitor_threads
        return csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO(
            num_monitors=len(new_docker_stats_monitor_threads), emulations=emulations,
            emulation_executions=emulation_executions)


def serve(port: int = 50046, log_dir: str = "/var/log/csle/", max_workers: int = 10,
          log_file_name: str = "docker_stats_manager.log") -> None:
    """
    Starts the gRPC server for managing docker stats collection

    :param port: the port that the server will listen to
    :param log_dir: the directory to write the log file
    :param log_file_name: the file name of the log
    :param max_workers: the maximum number of parallel gRPC workers
    :return: None
    """
    constants.LOG_FILES.DOCKER_STATS_MANAGER_LOG_DIR = log_dir
    constants.LOG_FILES.DOCKER_STATS_MANAGER_LOG_FILE = log_file_name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.add_DockerStatsManagerServicer_to_server(
        DockerStatsManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"DockerStatsManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
