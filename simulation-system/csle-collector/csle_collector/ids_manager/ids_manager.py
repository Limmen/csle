import logging
import socket
import time
import grpc
import threading
from concurrent import futures
from confluent_kafka import Producer
import csle_collector.ids_manager.ids_manager_pb2_grpc.IdsManagerServicer
import csle_collector.ids_manager.ids_manager_pb2.IdsLogDTO
import csle_collector.ids_manager.ids_manager_pb2.IdsMonitorDTO


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

    def run(self) -> None:
        """
        Main loop of the thread. Parses the IDS log and pushes it to Kafka periodically

        :return: None
        """
        while self.running:
            time.sleep(self.time_step_len_seconds)
            ids_log_dto = parse_ids_log(timestamp=self.latest_ts, log_file_path=self.log_file_path)
            ids_log_dto.ip = self.ip
            record = f"{self.latest_ts},{self.ip},{ids_log_dto.attempted_admin_alerts}," \
                     f"{ids_log_dto.inappropriate_content_alerts}," \
                     f"{ids_log_dto.policy_violation_alerts}," \
                     f"{ids_log_dto.shellcode_detect_alerts}," \
                     f"{ids_log_dto.successful_admin_alerts}," \
                     f"{ids_log_dto.successful_user_alerts}," \
                     f"{ids_log_dto.trojan_activity_alerts}," \
                     f"{ids_log_dto.unsuccessful_user_alerts}," \
                     f"{ids_log_dto.web_application_attack_alerts}," \
                     f"{ids_log_dto.attempted_dos_alerts}," \
                     f"{ids_log_dto.attempted_recon_alerts}," \
                     f"{ids_log_dto.bad_unknown_alerts}," \
                     f"{ids_log_dto.default_login_attempt_alerts}," \
                     f"{ids_log_dto.denial_of_service_alerts}," \
                     f"{ids_log_dto.misc_attack_alerts}," \
                     f"{ids_log_dto.non_standard_protocol_alerts}," \
                     f"{ids_log_dto.rpc_portman_decode_alerts}," \
                     f"{ids_log_dto.successful_dos_alerts}," \
                     f"{ids_log_dto.successful_recon_largescale_alerts}," \
                     f"{ids_log_dto.successful_recon_limited_alerts}," \
                     f"{ids_log_dto.suspicious_filename_detect_alerts}," \
                     f"{ids_log_dto.suspicious_login_alerts}," \
                     f"{ids_log_dto.system_call_detect_alerts}," \
                     f"{ids_log_dto.unusual_client_port_connection_alerts}," \
                     f"{ids_log_dto.web_application_activity_alerts}," \
                     f"{ids_log_dto.icmp_event_alerts}," \
                     f"{ids_log_dto.misc_activity_alerts}," \
                     f"{ids_log_dto.network_scan_alerts}," \
                     f"{ids_log_dto.not_suspicious_alerts}," \
                     f"{ids_log_dto.protocol_command_decode_alerts}," \
                     f"{ids_log_dto.string_detect_alerts}," \
                     f"{ids_log_dto.unknown_alerts}," \
                     f"{ids_log_dto.tcp_connection_alerts}," \
                     f"{ids_log_dto.warning_alerts}," \
                     f"{ids_log_dto.severe_alerts}"
            self.producer.produce("ids_log", record)
            self.latest_ts = time.time()


def parse_ids_log(log_file_path: str, timestamp: float = -1) -> csle_collector.ids_manager.ids_manager_pb2.IdsLogDTO:
    """
    Parses the IDS log from a given timestamp
    :param timestamp: the timestamp to parse from
    :param log_file_path: path to the log file
    :return: a DTO with statistics of the log
    """
    if timestamp == -1:
        timestamp = time.time()

    return csle_collector.ids_manager.ids_manager_pb2.IdsLogDTO(
        timestamp = timestamp,
        ip = "temp",
        attempted_admin_alerts = 0,
        inappropriate_content_alerts = 0,
        policy_violation_alerts = 0,
        shellcode_detect_alerts = 0,
        successful_admin_alerts = 0,
        successful_user_alerts = 0,
        trojan_activity_alerts = 0,
        unsuccessful_user_alerts = 0,
        web_application_attack_alerts = 0,
        attempted_dos_alerts = 0,
        attempted_recon_alerts = 0,
        bad_unknown_alerts = 0,
        default_login_attempt_alerts = 0,
        denial_of_service_alerts = 0,
        misc_attack_alerts = 0,
        non_standard_protocol_alerts = 0,
        rpc_portman_decode_alerts = 0,
        successful_dos_alerts = 0,
        successful_recon_largescale_alerts = 0,
        successful_recon_limited_alerts = 0,
        suspicious_filename_detect_alerts = 0,
        suspicious_login_alerts = 0,
        system_call_detect_alerts = 0,
        unusual_client_port_connection_alerts = 0,
        web_application_activity_alerts = 0,
        icmp_event_alerts = 0,
        misc_activity_alerts = 0,
        network_scan_alerts = 0,
        not_suspicious_alerts = 0,
        protocol_command_decode_alerts = 0,
        string_detect_alerts = 0,
        unknown_alerts = 0,
        tcp_connection_alerts = 0,
        warning_alerts = 0,
        severe_alerts = 0
    )


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
        idslogDTO = parse_ids_log(timestamp=request.timestamp, log_file_path=request.log_file_path)
        idslogDTO.ip = self.ip


    def startIdsMonitor(self, request: csle_collector.ids_manager.ids_manager_pb2.StartIdsMonitorMsg,
                     context: grpc.ServicerContext) -> csle_collector.ids_manager.ids_manager_pb2.IdsMonitorDTO:
        """
        Starts the IDS monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the IDS monitor thread
        """
        if self.ids_monitor_thread is not None:
            self.ids_monitor_thread.running = False
        self.ids_monitor_thread = IDSMonitorThread(kafka_ip=request.kafka_ip, kafka_port=request.kafka_port,
                                                   ip=self.ip, hostname=self.hostname,
                                                   log_file_path=request.log_file_path)
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