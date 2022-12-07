import logging
from concurrent import futures
import grpc
import socket
import os
import subprocess
import json
import requests
import csle_collector.ryu_manager.ryu_manager_pb2_grpc
import csle_collector.ryu_manager.ryu_manager_pb2
import csle_collector.constants.constants as constants


class RyuManagerServicer(csle_collector.ryu_manager.ryu_manager_pb2_grpc.RyuManagerServicer):
    """
    gRPC server for managing a Ryu controller. Allows to start/stop the ryu controller remotely and also to query the
    state of the controller
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        logging.basicConfig(filename=f"{constants.LOG_FILES.RYU_MANAGER_LOG_DIR}"
                                     f"{constants.LOG_FILES.RYU_MANAGER_LOG_FILE}", level=logging.INFO)
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        self.ryu_port = 6633
        self.ryu_web_port = 8080
        self.controller = ""
        self.kafka_ip = ""
        self.kafka_port = 9092
        self.time_step_len = 30
        logging.info(f"Setting up RyuManager hostname: {self.hostname} ip: {self.ip}")

    def _get_ryu_status(self) -> bool:
        """
        Utility method to get the status of Ryu

        :return: status
        """
        cmd = constants.RYU.CHECK_IF_RYU_CONTROLLER_IS_RUNNING
        output = subprocess.run(cmd.split(" "), capture_output=True, text=True).stdout
        running = constants.RYU.SEARCH_CONTROLLER in output
        return running

    def _get_monitor_status(self) -> bool:
        """
        Utility method to get the status of the monitor

        :return: status
        """
        running = False
        return running

    def getRyuStatus(self, request: csle_collector.ryu_manager.ryu_manager_pb2.GetRyuStatusMsg,
                     context: grpc.ServicerContext) \
            -> csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
        """
        Gets the state of the Ryu controller

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the Ryu server
        """
        ryu_running = self._get_ryu_status()
        monitor_running = False
        if ryu_running:
            monitor_running = self._get_monitor_status()
        ryu_dto = csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO(ryu_running=ryu_running,
                                                                    monitor_running=monitor_running,
                                                                    port=self.ryu_port,
                                                                    web_port=self.ryu_web_port,
                                                                    controller=self.controller,
                                                                    kafka_ip=self.kafka_ip,
                                                                    kafka_port=self.kafka_port,
                                                                    time_step_len=self.time_step_len)
        return ryu_dto

    def stopRyu(self, request: csle_collector.ryu_manager.ryu_manager_pb2.StopRyuMsg,
                context: grpc.ServicerContext):
        """
        Stops the Ryu controller

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the ryu server
        """
        logging.info("Stopping ryu")
        cmd = constants.RYU.STOP_RYU_CONTROLLER
        os.system(cmd)
        return csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO(ryu_running=False, monitor_running=False,
                                                                 port=self.ryu_port,
                                                                 web_port=self.ryu_web_port,
                                                                 controller=self.controller,
                                                                 kafka_ip=self.kafka_ip,
                                                                 kafka_port=self.kafka_port,
                                                                 time_step_len=self.time_step_len)

    def startRyu(self, request: csle_collector.ryu_manager.ryu_manager_pb2.StartRyuMsg,
                 context: grpc.ServicerContext) -> csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
        """
        Starts the ryu server

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the kafka server
        """
        logging.info("Starting Ryu")
        self.ryu_port = request.port
        self.ryu_web_port = request.web_port
        self.controller = request.controller

        # Check if controller is already running
        ryu_running = self._get_ryu_status()
        if not ryu_running:
            # Stop old background job if running
            cmd = constants.RYU.STOP_RYU_CONTROLLER
            os.system(cmd)
            cmd = constants.RYU.START_RYU_CONTROLLER.format(self.ryu_port, self.ryu_web_port, request.controller)
            result = subprocess.run(cmd.split(" "), capture_output=True, text=True)
            logging.info(f"Started RYU controller. Stdout: {result.stdout}, stderr: {result.stderr}")

        ryu_dto = csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO(ryu_running=True, monitor_running=False,
                                                                    port=self.ryu_port,
                                                                    web_port=self.ryu_web_port,
                                                                    controller=self.controller,
                                                                    kafka_ip=self.kafka_ip,
                                                                    kafka_port=self.kafka_port,
                                                                    time_step_len=self.time_step_len)
        return ryu_dto

    def stopRyuMonitor(self, request: csle_collector.ryu_manager.ryu_manager_pb2.StopRyuMsg,
                       context: grpc.ServicerContext):
        """
        Stops the Ryu monitor

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the ryu server
        """
        logging.info("Stopping ryu monitor")
        ryu_running = self._get_ryu_status()
        if ryu_running:
            requests.post(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{self.ip}:{self.ryu_web_port}"
                          f"{constants.RYU.STOP_PRODUCER_HTTP_RESOURCE}")
        return csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO(ryu_running=ryu_running, monitor_running=False,
                                                                 port=self.ryu_port,
                                                                 web_port=self.ryu_web_port,
                                                                 controller=self.controller,
                                                                 kafka_ip=self.kafka_ip,
                                                                 kafka_port=self.kafka_port,
                                                                 time_step_len=self.time_step_len)

    def startRyuMonitor(self, request: csle_collector.ryu_manager.ryu_manager_pb2.StartRyuMsg,
                        context: grpc.ServicerContext) -> csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
        """
        Starts the ryu monitor

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the kafka server
        """
        logging.info("Starting Ryu monitor")
        self.kafka_ip = request.kafka_ip
        self.kafka_port = request.kafka_port
        self.time_step_len = request.time_step_len
        ryu_running = self._get_ryu_status()
        monitor_running = False
        if ryu_running:
            response = requests.put(
                f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{self.ip}:{self.ryu_web_port}"
                f"{constants.RYU.START_PRODUCER_HTTP_RESOURCE}",
                data=json.dumps({constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: self.kafka_ip,
                                 constants.RYU.TIME_STEP_LEN_SECONDS: self.time_step_len}))
            monitor_running = response.status_code == 200
        ryu_dto = csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO(ryu_running=ryu_running,
                                                                    monitor_running=monitor_running,
                                                                    port=self.ryu_port,
                                                                    web_port=self.ryu_web_port,
                                                                    controller=self.controller,
                                                                    kafka_ip=self.kafka_ip,
                                                                    kafka_port=self.kafka_port,
                                                                    time_step_len=self.time_step_len)
        return ryu_dto


def serve(port: int = 50042, log_dir: str = "/", max_workers: int = 10,
          log_file_name: str = "ryu_manager.log") -> None:
    """
    Starts the gRPC server for managing the ryu controller

    :param port: the port that the server will listen to
    :param log_dir: the directory to write the log file
    :param log_file_name: the file name of the log
    :param max_workers: the maximum number of GRPC workers
    :return: None
    """
    constants.LOG_FILES.RYU_MANAGER_LOG_DIR = log_dir
    constants.LOG_FILES.RYU_MANAGER_LOG_FILE = log_file_name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    csle_collector.ryu_manager.ryu_manager_pb2_grpc.add_RyuManagerServicer_to_server(
        RyuManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"RyuManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
