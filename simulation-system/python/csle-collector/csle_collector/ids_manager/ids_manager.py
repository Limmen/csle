import logging
import socket
import time
import grpc
import threading
from concurrent import futures
from confluent_kafka import Producer
import csle_collector.ids_manager.ids_manager_pb2_grpc
import csle_collector.ids_manager.ids_manager_pb2
from csle_collector.ids_manager.ids_manager_util import IdsManagerUtil
import csle_collector.constants.constants as constants


class IDSMonitorThread(threading.Thread):
    """
    Thread that collects the IDS statistics and pushes it to Kafka periodically
    """

    def __init__(self, kafka_ip: str, kafka_port: int, ip: str, hostname: str, log_file_path: str,
                 time_step_len_seconds: int):
        """
        Intializes the thread

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
        self.conf = {'bootstrap.servers': f"{self.kafka_ip}:{self.kafka_port}", 'client.id': self.hostname}
        self.producer = Producer(**self.conf)
        self.running = True
        logging.info(f"IDSMonitor thread started successfully")

    def run(self) -> None:
        """
        Main loop of the thread. Parses the IDS log and pushes it to Kafka periodically

        :return: None
        """
        while self.running:
            time.sleep(self.time_step_len_seconds)
            alert_counters = IdsManagerUtil.read_ids_data(self.latest_ts)
            record = alert_counters.to_kafka_record(ip = self.ip)
            self.producer.produce(constants.LOG_SINK.IDS_LOG_TOPIC_NAME, record)
            self.latest_ts = time.time()


class IdsManagerServicer(csle_collector.ids_manager.ids_manager_pb2_grpc.IdsManagerServicer):
    """
    gRPC server for collecting IDS statistics.
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        logging.basicConfig(filename="/ids_manager.log", level=logging.INFO)
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        self.conf = {'bootstrap.servers': f"{self.ip}:9092",
                     'client.id': self.hostname}
        self.ids_monitor_thread = None
        logging.info(f"Starting the IDSManager hostname: {self.hostname} ip: {self.ip}")

    def getIdsAlerts(self, request: csle_collector.ids_manager.ids_manager_pb2.GetIdsAlertsMsg,
                     context: grpc.ServicerContext) -> csle_collector.ids_manager.ids_manager_pb2.IdsLogDTO:
        """
        Gets the statistics of the IDS log from a given timestamp

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with IDS statistics
        """
        alert_counters = IdsManagerUtil.read_ids_data(request.timestamp)
        ids_log_dto = alert_counters.to_dto(ip=self.ip)
        return ids_log_dto


    def startIdsMonitor(self, request: csle_collector.ids_manager.ids_manager_pb2.StartIdsMonitorMsg,
                     context: grpc.ServicerContext) -> csle_collector.ids_manager.ids_manager_pb2.IdsMonitorDTO:
        """
        Starts the IDS monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the IDS monitor thread
        """
        logging.info(f"Starting the IDSMonitor thread, timestep length: {request.time_step_len_seconds}, "
                     f"log file path: {request.log_file_path}, kafka ip: {request.kafka_ip}, "
                     f"kafka port: {request.kafka_port}")
        if self.ids_monitor_thread is not None:
            self.ids_monitor_thread.running = False
        self.ids_monitor_thread = IDSMonitorThread(kafka_ip=request.kafka_ip, kafka_port=request.kafka_port,
                                                   ip=self.ip, hostname=self.hostname,
                                                   log_file_path=request.log_file_path,
                                                   time_step_len_seconds=request.time_step_len_seconds)
        self.ids_monitor_thread.start()
        logging.info(f"Started the IDSMonitor thread")
        return csle_collector.ids_manager.ids_manager_pb2.IdsMonitorDTO(
            running = True
        )

    def stopIdsMonitor(self, request: csle_collector.ids_manager.ids_manager_pb2.StopIdsMonitorMsg,
                        context: grpc.ServicerContext) -> csle_collector.ids_manager.ids_manager_pb2.IdsMonitorDTO:
        """
        Stops the IDS monitor thread if it is running

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the IDS monitor thread
        """
        if self.ids_monitor_thread is not None:
            self.ids_monitor_thread.running = False
        return csle_collector.ids_manager.ids_manager_pb2.IdsMonitorDTO(
            running = False
        )

    def getIdsMonitorStatus(self, request: csle_collector.ids_manager.ids_manager_pb2.GetIdsMonitorStatusMsg,
                            context: grpc.ServicerContext) -> csle_collector.ids_manager.ids_manager_pb2.IdsMonitorDTO:
        """
        Gets the status of the IDS Monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the IDS monitor
        """
        running = False
        if self.ids_monitor_thread is not None:
            running = self.ids_monitor_thread.running
        return csle_collector.ids_manager.ids_manager_pb2.IdsMonitorDTO(
            running = running
        )


def serve(port : int = 50051) -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :return: None
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    csle_collector.ids_manager.ids_manager_pb2_grpc.add_IdsManagerServicer_to_server(
        IdsManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"IdsManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve(port=50051)