import logging
import socket
import time
import grpc
import threading
import subprocess
from concurrent import futures
from confluent_kafka import Producer
import csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc
import csle_collector.snort_ids_manager.snort_ids_manager_pb2
from csle_collector.snort_ids_manager.snort_ids_manager_util import SnortIdsManagerUtil
import csle_collector.constants.constants as constants


class SnortIDSMonitorThread(threading.Thread):
    """
    Thread that collects the Snort IDS statistics and pushes it to Kafka periodically
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
        logging.info("SnortIDSMonitor thread started successfully")

    def run(self) -> None:
        """
        Main loop of the thread. Parses the IDS log and pushes it to Kafka periodically

        :return: None
        """
        while self.running:
            time.sleep(self.time_step_len_seconds)
            alert_counters = SnortIdsManagerUtil.read_snort_ids_data(self.latest_ts)
            record = alert_counters.to_kafka_record(ip=self.ip)
            self.producer.produce(constants.KAFKA_CONFIG.SNORT_IDS_LOG_TOPIC_NAME, record)
            self.producer.poll(0)
            self.latest_ts = time.time()


class SnortIdsManagerServicer(csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.SnortIdsManagerServicer):
    """
    gRPC server for collecting Snort IDS statistics.
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        logging.basicConfig(filename=f"{constants.LOG_FILES.SNORT_IDS_MANAGER_LOG_DIR}"
                                     f"{constants.LOG_FILES.SNORT_IDS_MANAGER_LOG_FILE}", level=logging.INFO)
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        self.conf = {
            constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.ip}:{constants.KAFKA.PORT}",
            constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.ids_monitor_thread = None
        logging.info(f"Starting the SnortIDSManager hostname: {self.hostname} ip: {self.ip}")

    def _is_snort_running(self) -> bool:
        """
        Utility method to check if Snort is running

        :return: status and list of topics
        """
        status_output = subprocess.run(constants.SNORT_IDS_ROUTER.CHECK_IF_SNORT_IS_RUNNING_CMD.split(" "),
                                       capture_output=True, text=True).stdout
        running = constants.SNORT_IDS_ROUTER.SEARCH_SNORT_RUNNING in status_output
        return running

    def getSnortIdsAlerts(
            self, request: csle_collector.snort_ids_manager.snort_ids_manager_pb2.GetSnortIdsAlertsMsg,
            context: grpc.ServicerContext) -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsLogDTO:
        """
        Gets the statistics of the IDS log from a given timestamp

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with IDS statistics
        """
        alert_counters = SnortIdsManagerUtil.read_snort_ids_data(request.timestamp)
        ids_log_dto = alert_counters.to_dto(ip=self.ip)
        return ids_log_dto

    def startSnortIdsMonitor(
            self, request: csle_collector.snort_ids_manager.snort_ids_manager_pb2.StartSnortIdsMonitorMsg,
            context: grpc.ServicerContext) -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO:
        """
        Starts the Snort IDS monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the IDS monitor thread
        """
        logging.info(f"Starting the SnortIDSMonitor thread, timestep length: {request.time_step_len_seconds}, "
                     f"log file path: {request.log_file_path}, kafka ip: {request.kafka_ip}, "
                     f"kafka port: {request.kafka_port}")
        if self.ids_monitor_thread is not None:
            self.ids_monitor_thread.running = False
        self.ids_monitor_thread = SnortIDSMonitorThread(kafka_ip=request.kafka_ip, kafka_port=request.kafka_port,
                                                        ip=self.ip, hostname=self.hostname,
                                                        log_file_path=request.log_file_path,
                                                        time_step_len_seconds=request.time_step_len_seconds)
        snort_running = self._is_snort_running()
        self.ids_monitor_thread.start()
        logging.info("Started the SnortIDSMonitor thread")
        return csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO(
            monitor_running=True, snort_ids_running=snort_running)

    def startSnortIds(self, request: csle_collector.snort_ids_manager.snort_ids_manager_pb2.StartSnortIdsMsg,
                      context: grpc.ServicerContext) \
            -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO:
        """
        Starts the Snort IDS

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the IDS and its monitor thread
        """
        logging.info("Starting the SnortIDS")
        monitor_running = False
        if self.ids_monitor_thread is not None:
            monitor_running = self.ids_monitor_thread.running
        snort_running = self._is_snort_running()
        if snort_running:
            result = subprocess.run(constants.SNORT_IDS_ROUTER.STOP_SNORT_IDS.split(" "),
                                    capture_output=True, text=True)
            logging.info(f"Stopped the Snort IDS, stdout:{result.stdout}, stderr: {result.stderr}")
        if not snort_running:
            result = subprocess.run(constants.SNORT_IDS_ROUTER.START_SNORT_IDS.split(" "),
                                    capture_output=True, text=True)
            logging.info(f"Started the Snort IDS, stdout:{result.stdout}, stderr: {result.stderr}")
        logging.info("Started the SnortIDS")
        return csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO(
            monitor_running=monitor_running, snort_ids_running=True)

    def stopSnortIds(self, request: csle_collector.snort_ids_manager.snort_ids_manager_pb2.StartSnortIdsMsg,
                     context: grpc.ServicerContext) \
            -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO:
        """
        Stops the Snort IDS

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the IDS and its monitor thread
        """
        logging.info("Stopping the SnortIDS")
        monitor_running = False
        if self.ids_monitor_thread is not None:
            monitor_running = self.ids_monitor_thread.running
        result = subprocess.run(constants.SNORT_IDS_ROUTER.STOP_SNORT_IDS.split(" "),
                                capture_output=True, text=True)
        logging.info(f"Stopped the SnortIDS, stdout: {result.stdout}, stderr: {result.stderr}")
        return csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO(
            monitor_running=monitor_running, snort_ids_running=False)

    def stopSnortIdsMonitor(self,
                            request: csle_collector.snort_ids_manager.snort_ids_manager_pb2.StopSnortIdsMonitorMsg,
                            context: grpc.ServicerContext) \
            -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO:
        """
        Stops the Snort IDS monitor thread if it is running

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the IDS monitor thread
        """
        if self.ids_monitor_thread is not None:
            self.ids_monitor_thread.running = False
        snort_running = self._is_snort_running()
        return csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO(
            monitor_running=False, snort_ids_running=snort_running)

    def getSnortIdsMonitorStatus(
            self, request: csle_collector.snort_ids_manager.snort_ids_manager_pb2.GetSnortIdsMonitorStatusMsg,
            context: grpc.ServicerContext) -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO:
        """
        Gets the status of the Snort IDS Monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the IDS monitor
        """
        running = False
        if self.ids_monitor_thread is not None:
            running = self.ids_monitor_thread.running
        snort_running = self._is_snort_running()
        return csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO(
            monitor_running=running, snort_ids_running=snort_running)


def serve(port: int = 50048, log_dir: str = "/", max_workers: int = 10,
          log_file_name: str = "snort_ids_manager.log") -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :param log_dir: the directory to write the log file
    :param log_file_name: the file name of the log
    :param max_workers: the maximum number of GRPC workers
    :return: None
    """
    constants.LOG_FILES.SNORT_IDS_MANAGER_LOG_DIR = log_dir
    constants.LOG_FILES.SNORT_IDS_MANAGER_LOG_FILE = log_file_name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.add_SnortIdsManagerServicer_to_server(
        SnortIdsManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"SnortIdsManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
