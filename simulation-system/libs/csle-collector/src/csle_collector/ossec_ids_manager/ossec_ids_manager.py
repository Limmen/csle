import logging
import socket
import time
import grpc
import threading
import subprocess
from concurrent import futures
from confluent_kafka import Producer
import csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc
import csle_collector.ossec_ids_manager.ossec_ids_manager_pb2
from csle_collector.ossec_ids_manager.ossec_ids_manager_util import OSSecManagerUtil
import csle_collector.constants.constants as constants


class OSSecIdsMonitorThread(threading.Thread):
    """
    Thread that collects the OSSEC IDS statistics and pushes it to Kafka periodically
    """

    def __init__(self, kafka_ip: str, kafka_port: int, ip: str, hostname: str, log_file_path: str,
                 time_step_len_seconds: int):
        """
        Initializes the thread

        :param kafka_ip: IP of the Kafka server to push to
        :param kafka_port: port of the Kafka server to push to
        :param ip: ip of the server we are pushing from
        :param hostname: hostname of the server we are pushing from
        :param log_file_path: path to the IDS log
        :param time_step_len_seconds: the length of a timestep
        """
        threading.Thread.__init__(self)
        self.kafka_ip = kafka_ip
        self.kafka_port = kafka_port
        self.ip = ip
        self.hostname = hostname
        self.log_file_path = log_file_path
        self.latest_ts = time.time()
        self.time_step_len_seconds = time_step_len_seconds
        self.conf = {constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_ip}:{self.kafka_port}",
                     constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.producer = Producer(**self.conf)
        self.running = True
        logging.info("OSSEC IDSMonitor thread started successfully")

    def run(self) -> None:
        """
        Main loop of the thread. Parses the IDS log and pushes it to Kafka periodically

        :return: None
        """
        while self.running:
            time.sleep(self.time_step_len_seconds)
            alert_counters = OSSecManagerUtil.read_ossec_ids_data(self.latest_ts)
            record = alert_counters.to_kafka_record(ip=self.ip)
            self.producer.produce(constants.KAFKA_CONFIG.OSSEC_IDS_LOG_TOPIC_NAME, record)
            self.producer.poll(0)
            self.latest_ts = time.time()


class OSSECIdsManagerServicer(csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.OSSECIdsManagerServicer):
    """
    gRPC server for collecting OSSEC IDS statistics.
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        logging.basicConfig(filename=f"{constants.LOG_FILES.OSSEC_IDS_MANAGER_LOG_DIR}"
                                     f"{constants.LOG_FILES.OSSEC_IDS_MANAGER_LOG_FILE}", level=logging.INFO)
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        self.conf = {
            constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.ip}:{constants.KAFKA.PORT}",
            constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.ids_monitor_thread = None
        logging.info(f"Starting the OSSEC IDSManager hostname: {self.hostname} ip: {self.ip}")

    def _is_ossec_running(self) -> bool:
        """
        Utility method to check if OSSEC is running

        :return: status and list of topics
        """
        status_output = subprocess.run(constants.OSSEC.CHECK_IF_OSSEC_IS_RUNNING_CMD.split(" "),
                                       capture_output=True, text=True).stdout
        running = constants.OSSEC.OSSEC_RUNNING_SEARCH in status_output
        return running

    def getOSSECIdsAlerts(self, request: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.GetOSSECIdsAlertsMsg,
                          context: grpc.ServicerContext) \
            -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsLogDTO:
        """
        Gets the statistics of the OSSEC IDS log from a given timestamp

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with IDS statistics
        """
        alert_counters = OSSecManagerUtil.read_ossec_ids_data(request.timestamp)
        ossec_ids_log_dto = alert_counters.to_dto(ip=self.ip)
        return ossec_ids_log_dto

    def startOSSECIdsMonitor(self,
                             request: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.StartOSSECIdsMonitorMsg,
                             context: grpc.ServicerContext) \
            -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO:
        """
        Starts the OSSEC IDS monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the IDS monitor thread
        """
        logging.info(f"Starting the OSSEC IDSMonitor thread, timestep length: {request.time_step_len_seconds}, "
                     f"log file path: {request.log_file_path}, kafka ip: {request.kafka_ip}, "
                     f"kafka port: {request.kafka_port}")
        if self.ids_monitor_thread is not None:
            self.ids_monitor_thread.running = False
        self.ids_monitor_thread = OSSecIdsMonitorThread(kafka_ip=request.kafka_ip, kafka_port=request.kafka_port,
                                                        ip=self.ip, hostname=self.hostname,
                                                        log_file_path=request.log_file_path,
                                                        time_step_len_seconds=request.time_step_len_seconds)
        self.ids_monitor_thread.start()
        logging.info("Started the OSSEC IDSMonitor thread")
        ossec_ids_running = self._is_ossec_running()
        return csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO(
            monitor_running=True, ossec_ids_running=ossec_ids_running)

    def stopOSSECIdsMonitor(self,
                            request: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.StartOSSECIdsMonitorMsg,
                            context: grpc.ServicerContext) \
            -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO:
        """
        Stops the OSSEC IDS monitor thread if it is running

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the IDS monitor thread
        """
        if self.ids_monitor_thread is not None:
            self.ids_monitor_thread.running = False
        ossec_ids_running = self._is_ossec_running()
        return csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO(
            monitor_running=False, ossec_ids_running=ossec_ids_running)

    def startOSSECIds(self, request: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.StartOSSECIdsMsg,
                      context: grpc.ServicerContext) \
            -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO:
        """
        Starts the OSSEC IDS

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the IDS and its monitor thread
        """
        logging.info("Starting the OSSEC IDS")
        monitor_running = False
        if self.ids_monitor_thread is not None:
            monitor_running = self.ids_monitor_thread.running
        ossec_running = self._is_ossec_running()
        if ossec_running:
            result = subprocess.run(constants.OSSEC.STOP_OSSEC_IDS.split(" "), capture_output=True, text=True)
            logging.info(f"Stopped the OSSEC IDS, stdout: {result.stdout}, stderr: {result.stderr}")
        if not ossec_running:
            result = subprocess.run(constants.OSSEC.START_OSSEC_IDS.split(" "), capture_output=True, text=True)
            logging.info(f"Started the OSSEC IDS, stdout: {result.stdout}, stderr: {result.stderr}")
        logging.info("Started the OSSEC IDS")
        return csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO(
            monitor_running=monitor_running, ossec_ids_running=True)

    def stopOSSECIds(self, request: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.StartOSSECIdsMsg,
                     context: grpc.ServicerContext) \
            -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO:
        """
        Stops the OSSEC IDS

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the IDS and its monitor thread
        """
        logging.info("Stopping the OSSECIDS")
        monitor_running = False
        if self.ids_monitor_thread is not None:
            monitor_running = self.ids_monitor_thread.running
        result = subprocess.run(constants.OSSEC.STOP_OSSEC_IDS.split(" "), capture_output=True, text=True)
        logging.info(f"Stopped the OSSECIDS, stdout: {result.stdout}, stderr: {result.stderr}")
        return csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO(
            monitor_running=monitor_running, ossec_ids_running=False)

    def getOSSECIdsMonitorStatus(
            self, request: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.GetOSSECIdsMonitorStatusMsg,
            context: grpc.ServicerContext) -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO:
        """
        Gets the status of the OSSEC IDS Monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the IDS monitor
        """
        monitor_running = False
        if self.ids_monitor_thread is not None:
            monitor_running = self.ids_monitor_thread.running
        ossec_ids_running = self._is_ossec_running()
        return csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO(
            monitor_running=monitor_running, ossec_ids_running=ossec_ids_running)


def serve(port: int = 50047, log_dir: str = "/", max_workers: int = 10,
          log_file_name: str = "ossec_ids_manager.log") -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :param log_dir: the directory to write the log file
    :param log_file_name: the file name of the log
    :param max_workers: the maximum number of GRPC workers
    :return: None
    """
    constants.LOG_FILES.OSSEC_IDS_MANAGER_LOG_DIR = log_dir
    constants.LOG_FILES.OSSEC_IDS_MANAGER_LOG_FILE = log_file_name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc.add_OSSECIdsManagerServicer_to_server(
        OSSECIdsManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"OSSECIdsManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
