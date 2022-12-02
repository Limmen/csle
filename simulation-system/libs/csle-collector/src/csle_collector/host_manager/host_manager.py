from typing import List
import logging
import socket
import time
import grpc
import threading
from concurrent import futures
import subprocess
from confluent_kafka import Producer
import csle_collector.host_manager.host_manager_pb2_grpc
import csle_collector.host_manager.host_manager_pb2
from csle_collector.host_manager.host_manager_util import HostManagerUtil
import csle_collector.constants.constants as constants


class HostMonitorThread(threading.Thread):
    """
    Thread that collects the Host statistics and pushes it to Kafka periodically
    """

    def __init__(self, kafka_ip: str, kafka_port: int, ip: str, hostname: str,
                 time_step_len_seconds: int):
        """
        Initializes the thread

        :param kafka_ip: IP of the Kafka server to push to
        :param kafka_port: port of the Kafka server to push to
        :param ip: ip of the server we are pushing from
        :param hostname: hostname of the server we are pushing from
        :param time_step_len_seconds: the length of a timestep
        """
        threading.Thread.__init__(self)
        self.kafka_ip = kafka_ip
        self.kafka_port = kafka_port
        self.ip = ip
        self.hostname = hostname
        self.latest_ts = time.time()
        self.failed_auth_last_ts = HostManagerUtil.read_latest_ts_auth()
        self.login_last_ts = HostManagerUtil.read_latest_ts_login()
        self.time_step_len_seconds = time_step_len_seconds
        self.conf = {
            constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_ip}:{self.kafka_port}",
            constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.producer = Producer(**self.conf)
        self.running = True
        logging.info("HostMonitor thread started successfully")

    def run(self) -> None:
        """
        Main loop of the thread. Parses log files and metrics on the host and pushes it to Kafka periodically

        :return: None
        """
        while self.running:
            time.sleep(self.time_step_len_seconds)
            host_metrics = HostManagerUtil.read_host_metrics(failed_auth_last_ts=self.failed_auth_last_ts,
                                                             login_last_ts=self.login_last_ts)
            record = host_metrics.to_kafka_record(ip=self.ip)
            self.producer.produce(constants.KAFKA_CONFIG.HOST_METRICS_TOPIC_NAME, record)
            self.producer.poll(0)
            self.failed_auth_last_ts = HostManagerUtil.read_latest_ts_auth()
            self.login_last_ts = HostManagerUtil.read_latest_ts_login()


class HostManagerServicer(csle_collector.host_manager.host_manager_pb2_grpc.HostManagerServicer):
    """
    gRPC server for collecting Host statistics.
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        logging.basicConfig(filename=f"{constants.LOG_FILES.HOST_MANAGER_LOG_DIR}"
                                     f"{constants.LOG_FILES.HOST_MANAGER_LOG_FILE}", level=logging.INFO)
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        self.conf = {constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.ip}:{constants.KAFKA.PORT}",
                     constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.host_monitor_thread = None
        logging.info(f"Starting the HostManager hostname: {self.hostname} ip: {self.ip}")

    def getIdsAlerts(self, request: csle_collector.host_manager.host_manager_pb2.GetHostMetricsMsg,
                     context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostMetricsDTO:
        """
        Gets the host metrics from given timestamps

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with IDS statistics
        """
        host_metrics = HostManagerUtil.read_host_metrics(failed_auth_last_ts=request.failed_auth_last_ts,
                                                         login_last_ts=request.login_last_ts)
        host_metrics_dto = host_metrics.to_dto(ip=self.ip)
        return host_metrics_dto

    def startHostMonitor(self, request: csle_collector.host_manager.host_manager_pb2.StartHostMonitorMsg,
                         context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Starts the Host monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host monitor thread
        """
        logging.info(f"Starting the HostMonitor thread, timestep length: {request.time_step_len_seconds}, "
                     f"kafka ip: {request.kafka_ip}, "
                     f"kafka port: {request.kafka_port}")
        if self.host_monitor_thread is not None:
            self.host_monitor_thread.running = False
        self.host_monitor_thread = HostMonitorThread(kafka_ip=request.kafka_ip, kafka_port=request.kafka_port,
                                                     ip=self.ip, hostname=self.hostname,
                                                     time_step_len_seconds=request.time_step_len_seconds)
        self.host_monitor_thread.start()
        logging.info("Started the HostMonitor thread")
        filebeat_status = HostManagerServicer._get_filebeat_status()
        packetbeat_status = HostManagerServicer._get_packetbeat_status()
        metricbeat_status = HostManagerServicer._get_metricbeat_status()
        heartbeat_status = HostManagerServicer._get_heartbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=True,
                                                                          filebeat_running=filebeat_status,
                                                                          packetbeat_running=packetbeat_status,
                                                                          metricbeat_running=metricbeat_status,
                                                                          heartbeat_running=heartbeat_status)

    def stopHostMonitor(self, request: csle_collector.host_manager.host_manager_pb2.StopHostMonitorMsg,
                        context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Stops the Host monitor thread if it is running

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host monitor thread
        """
        logging.info("Stopping the host monitor")
        if self.host_monitor_thread is not None:
            self.host_monitor_thread.running = False
        logging.info("Host monitor stopped")
        filebeat_running = HostManagerServicer._get_filebeat_status()
        packetbeat_status = HostManagerServicer._get_packetbeat_status()
        metricbeat_status = HostManagerServicer._get_metricbeat_status()
        heartbeat_status = HostManagerServicer._get_heartbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=False,
                                                                          filebeat_running=filebeat_running,
                                                                          packetbeat_running=packetbeat_status,
                                                                          metricbeat_running=metricbeat_status,
                                                                          heartbeat_running=heartbeat_status)

    def startFilebeat(self, request: csle_collector.host_manager.host_manager_pb2.StartFilebeatMsg,
                      context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Starts filebeat

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host
        """
        logging.info("Starting filebeat")
        HostManagerServicer._start_filebeat()
        logging.info("Started filebeat")
        monitor_running = False
        if self.host_monitor_thread is not None:
            monitor_running = self.host_monitor_thread.running
        packetbeat_status = HostManagerServicer._get_packetbeat_status()
        metricbeat_status = HostManagerServicer._get_metricbeat_status()
        heartbeat_status = HostManagerServicer._get_heartbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=monitor_running,
                                                                          filebeat_running=True,
                                                                          packetbeat_running=packetbeat_status,
                                                                          metricbeat_running=metricbeat_status,
                                                                          heartbeat_running=heartbeat_status)

    def stopFilebeat(self, request: csle_collector.host_manager.host_manager_pb2.StopFilebeatMsg,
                     context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Stops filebeat

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host
        """
        logging.info("Stopping filebeat")
        HostManagerServicer._stop_filebeat()
        logging.info("Filebeat stopped")
        monitor_running = False
        if self.host_monitor_thread is not None:
            monitor_running = self.host_monitor_thread.running
        packetbeat_status = HostManagerServicer._get_packetbeat_status()
        metricbeat_status = HostManagerServicer._get_metricbeat_status()
        heartbeat_status = HostManagerServicer._get_heartbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=monitor_running,
                                                                          filebeat_running=False,
                                                                          packetbeat_running=packetbeat_status,
                                                                          metricbeat_running=metricbeat_status,
                                                                          heartbeat_running=heartbeat_status)

    def configFilebeat(self, request: csle_collector.host_manager.host_manager_pb2.ConfigFilebeatMsg,
                       context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Updates the configuration of filebeat

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host
        """
        logging.info(f"Updating the filebeat configuration, "
                     f"log_files_paths: {request.log_files_paths}, "
                     f"kibana_ip : {request.kibana_ip}, kibana_port: {request.kibana_port}, "
                     f"elastic_ip: {request.elastic_ip}, elastic_port: {request.elastic_port}, "
                     f"num_elastic_shards: {request.num_elastic_shards}, reload_enabled: {request.reload_enabled}, "
                     f"kafka: {request.kafka}, kafka_ip: {request.kafka_ip}, kafka_port: {request.kafka_port}, "
                     f"kafka_topics: {request.kafka_topics}, filebeat_modules: {request.filebeat_modules}")
        HostManagerServicer._set_filebeat_config(
            log_files_paths=list(request.log_files_paths), kibana_ip=request.kibana_ip, kibana_port=request.kibana_port,
            elastic_ip=request.elastic_ip, elastic_port=request.elastic_port,
            num_elastic_shards=request.num_elastic_shards, reload_enabled=request.reload_enabled,
            kafka=request.kafka, kafka_ip=request.kafka_ip, kafka_port=request.kafka_port,
            kafka_topics=list(request.kafka_topics), filebeat_modules=list(request.filebeat_modules))
        logging.info("Filebeat configuration updated")
        monitor_running = False
        if self.host_monitor_thread is not None:
            monitor_running = self.host_monitor_thread.running
        filebeat_running = HostManagerServicer._get_filebeat_status()
        packetbeat_status = HostManagerServicer._get_packetbeat_status()
        metricbeat_status = HostManagerServicer._get_metricbeat_status()
        heartbeat_status = HostManagerServicer._get_heartbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=monitor_running,
                                                                          filebeat_running=filebeat_running,
                                                                          packetbeat_running=packetbeat_status,
                                                                          metricbeat_running=metricbeat_status,
                                                                          heartbeat_running=heartbeat_status)

    def startMetricbeat(self, request: csle_collector.host_manager.host_manager_pb2.StartMetricbeatMsg,
                        context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Starts metricbeat

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host
        """
        logging.info("Starting metricbeat")
        HostManagerServicer._start_metricbeat()
        logging.info("Started metricbeat")
        monitor_running = False
        if self.host_monitor_thread is not None:
            monitor_running = self.host_monitor_thread.running
        packetbeat_status = HostManagerServicer._get_packetbeat_status()
        filebeat_status = HostManagerServicer._get_filebeat_status()
        heartbeat_status = HostManagerServicer._get_heartbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=monitor_running,
                                                                          filebeat_running=filebeat_status,
                                                                          packetbeat_running=packetbeat_status,
                                                                          metricbeat_running=True,
                                                                          heartbeat_running=heartbeat_status)

    def stopMetricbeat(self, request: csle_collector.host_manager.host_manager_pb2.StopMetricbeatMsg,
                       context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Stops metricbeat

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host
        """
        logging.info("Stopping metricbeat")
        HostManagerServicer._stop_metricbeat()
        logging.info("Metricbeat stopped")
        monitor_running = False
        if self.host_monitor_thread is not None:
            monitor_running = self.host_monitor_thread.running
        packetbeat_status = HostManagerServicer._get_packetbeat_status()
        filebeat_status = HostManagerServicer._get_filebeat_status()
        heartbeat_status = HostManagerServicer._get_heartbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=monitor_running,
                                                                          filebeat_running=filebeat_status,
                                                                          packetbeat_running=packetbeat_status,
                                                                          metricbeat_running=False,
                                                                          heartbeat_running=heartbeat_status)

    def configMetricbeat(self, request: csle_collector.host_manager.host_manager_pb2.ConfigMetricbeatMsg,
                         context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Updates the configuration of metricbeat

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host
        """
        logging.info(f"Updating the metricbeat configuration, "
                     f"kibana_ip : {request.kibana_ip}, kibana_port: {request.kibana_port}, "
                     f"elastic_ip: {request.elastic_ip}, elastic_port: {request.elastic_port}, "
                     f"num_elastic_shards: {request.num_elastic_shards}, reload_enabled: {request.reload_enabled}, "
                     f"kafka_ip: {request.kafka_ip}, kafka_port: {request.kafka_port}, "
                     f"metricbeat_modules: {request.metricbeat_modules}")
        HostManagerServicer._set_metricbeat_config(
            kibana_ip=request.kibana_ip, kibana_port=request.kibana_port,
            elastic_ip=request.elastic_ip, elastic_port=request.elastic_port,
            num_elastic_shards=request.num_elastic_shards, reload_enabled=request.reload_enabled,
            kafka_ip=request.kafka_ip, kafka_port=request.kafka_port, metricbeat_modules=request.metricbeat_modules)
        logging.info("Metricbeat configuration updated")
        monitor_running = False
        if self.host_monitor_thread is not None:
            monitor_running = self.host_monitor_thread.running
        filebeat_running = HostManagerServicer._get_filebeat_status()
        packetbeat_status = HostManagerServicer._get_packetbeat_status()
        metricbeat_status = HostManagerServicer._get_metricbeat_status()
        heartbeat_status = HostManagerServicer._get_heartbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=monitor_running,
                                                                          filebeat_running=filebeat_running,
                                                                          packetbeat_running=packetbeat_status,
                                                                          metricbeat_running=metricbeat_status,
                                                                          heartbeat_running=heartbeat_status)

    def startPacketbeat(self, request: csle_collector.host_manager.host_manager_pb2.StartPacketbeatMsg,
                        context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Starts packetbeat

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host
        """
        logging.info("Starting packetbeat")
        HostManagerServicer._start_packetbeat()
        logging.info("Started packetbeat")
        monitor_running = False
        if self.host_monitor_thread is not None:
            monitor_running = self.host_monitor_thread.running
        filebeat_status = HostManagerServicer._get_filebeat_status()
        metricbeat_status = HostManagerServicer._get_metricbeat_status()
        heartbeat_status = HostManagerServicer._get_heartbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=monitor_running,
                                                                          filebeat_running=filebeat_status,
                                                                          packetbeat_running=True,
                                                                          metricbeat_running=metricbeat_status,
                                                                          heartbeat_running=heartbeat_status)

    def stopPacketbeat(self, request: csle_collector.host_manager.host_manager_pb2.StopPacketbeatMsg,
                       context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Stops packetbeat

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host
        """
        logging.info("Stopping packetbeat")
        HostManagerServicer._stop_packetbeat()
        logging.info("Packetbeat stopped")
        monitor_running = False
        if self.host_monitor_thread is not None:
            monitor_running = self.host_monitor_thread.running
        filebeat_status = HostManagerServicer._get_filebeat_status()
        metricbeat_status = HostManagerServicer._get_metricbeat_status()
        heartbeat_status = HostManagerServicer._get_heartbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=monitor_running,
                                                                          filebeat_running=filebeat_status,
                                                                          packetbeat_running=False,
                                                                          metricbeat_running=metricbeat_status,
                                                                          heartbeat_running=heartbeat_status)

    def configPacketbeat(self, request: csle_collector.host_manager.host_manager_pb2.ConfigPacketbeatMsg,
                         context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Updates the configuration of packetbeat

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host
        """
        logging.info(f"Updating the packetbeat configuration,"
                     f"kibana_ip : {request.kibana_ip}, kibana_port: {request.kibana_port}, "
                     f"elastic_ip: {request.elastic_ip}, elastic_port: {request.elastic_port}, "
                     f"num_elastic_shards: {request.num_elastic_shards}")
        HostManagerServicer._set_packetbeat_config(
            kibana_ip=request.kibana_ip, kibana_port=request.kibana_port,
            elastic_ip=request.elastic_ip, elastic_port=request.elastic_port,
            num_elastic_shards=request.num_elastic_shards)
        logging.info("Packetbeat configuration updated")
        monitor_running = False
        if self.host_monitor_thread is not None:
            monitor_running = self.host_monitor_thread.running
        filebeat_running = HostManagerServicer._get_filebeat_status()
        packetbeat_status = HostManagerServicer._get_packetbeat_status()
        metricbeat_status = HostManagerServicer._get_metricbeat_status()
        heartbeat_status = HostManagerServicer._get_heartbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=monitor_running,
                                                                          filebeat_running=filebeat_running,
                                                                          packetbeat_running=packetbeat_status,
                                                                          metricbeat_running=metricbeat_status,
                                                                          heartbeat_running=heartbeat_status)

    def getHostStatus(self, request: csle_collector.host_manager.host_manager_pb2.GetHostStatusMsg,
                      context: grpc.ServicerContext) \
            -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Gets the status of the host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the host
        """
        monitor_running = False
        if self.host_monitor_thread is not None:
            monitor_running = self.host_monitor_thread.running
        filebeat_running = HostManagerServicer._get_filebeat_status()
        packetbeat_status = HostManagerServicer._get_packetbeat_status()
        metricbeat_status = HostManagerServicer._get_metricbeat_status()
        heartbeat_status = HostManagerServicer._get_heartbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=monitor_running,
                                                                          filebeat_running=filebeat_running,
                                                                          packetbeat_running=packetbeat_status,
                                                                          metricbeat_running=metricbeat_status,
                                                                          heartbeat_running=heartbeat_status)

    def startHeartbeat(self, request: csle_collector.host_manager.host_manager_pb2.StartHeartbeatMsg,
                       context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Starts heartbeat

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host
        """
        logging.info("Starting heartbeat")
        HostManagerServicer._start_heartbeat()
        logging.info("Started heartbeat")
        monitor_running = False
        if self.host_monitor_thread is not None:
            monitor_running = self.host_monitor_thread.running
        packetbeat_status = HostManagerServicer._get_packetbeat_status()
        filebeat_status = HostManagerServicer._get_filebeat_status()
        metricbeat_status = HostManagerServicer._get_metricbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=monitor_running,
                                                                          filebeat_running=filebeat_status,
                                                                          packetbeat_running=packetbeat_status,
                                                                          metricbeat_running=metricbeat_status,
                                                                          heartbeat_running=True)

    def stopHeartbeat(self, request: csle_collector.host_manager.host_manager_pb2.StopHeartbeatMsg,
                      context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Stops heartbeat

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host
        """
        logging.info("Stopping heartbeat")
        HostManagerServicer._stop_heartbeat()
        logging.info("Heartbeat stopped")
        monitor_running = False
        if self.host_monitor_thread is not None:
            monitor_running = self.host_monitor_thread.running
        packetbeat_status = HostManagerServicer._get_packetbeat_status()
        filebeat_status = HostManagerServicer._get_filebeat_status()
        metricbeat_status = HostManagerServicer._get_metricbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=monitor_running,
                                                                          filebeat_running=filebeat_status,
                                                                          packetbeat_running=packetbeat_status,
                                                                          metricbeat_running=metricbeat_status,
                                                                          heartbeat_running=False)

    def configHeartbeat(self, request: csle_collector.host_manager.host_manager_pb2.ConfigHeartbeatMsg,
                        context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Updates the configuration of heartbeat

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host
        """
        logging.info(f"Updating the heartbeat configuration, "
                     f"kibana_ip : {request.kibana_ip}, kibana_port: {request.kibana_port}, "
                     f"elastic_ip: {request.elastic_ip}, elastic_port: {request.elastic_port}, "
                     f"num_elastic_shards: {request.num_elastic_shards}, hosts_to_monitor: {request.hosts_to_monitor}")
        HostManagerServicer._set_heartbeat_config(
            kibana_ip=request.kibana_ip, kibana_port=request.kibana_port,
            elastic_ip=request.elastic_ip, elastic_port=request.elastic_port,
            num_elastic_shards=request.num_elastic_shards, hosts_to_monitor=list(request.hosts_to_monitor))
        logging.info("Heartbeat configuration updated")
        monitor_running = False
        if self.host_monitor_thread is not None:
            monitor_running = self.host_monitor_thread.running
        filebeat_running = HostManagerServicer._get_filebeat_status()
        packetbeat_status = HostManagerServicer._get_packetbeat_status()
        metricbeat_status = HostManagerServicer._get_metricbeat_status()
        heartbeat_status = HostManagerServicer._get_heartbeat_status()
        return csle_collector.host_manager.host_manager_pb2.HostStatusDTO(monitor_running=monitor_running,
                                                                          filebeat_running=filebeat_running,
                                                                          packetbeat_running=packetbeat_status,
                                                                          metricbeat_running=metricbeat_status,
                                                                          heartbeat_running=heartbeat_status)

    @staticmethod
    def _get_filebeat_status() -> bool:
        """
        Utility method to get the status of filebeat

        :return: status of filebeat
        """
        logging.info(f"Getting filebeat status with command: {constants.FILEBEAT.FILEBEAT_STATUS}")
        output = subprocess.run(constants.FILEBEAT.FILEBEAT_STATUS.split(" "), capture_output=True, text=True)
        filebeat_running = not ("not" in output.stdout)
        logging.info(f"Got filebeat status, output:{output.stdout}, err output: {output.stderr} ")
        return filebeat_running

    @staticmethod
    def _start_filebeat() -> None:
        """
        Utility method to start filebeat

        :return: None
        """
        logging.info(f"Starting filebeat with command: {constants.FILEBEAT.FILEBEAT_START}")
        output = subprocess.run(constants.FILEBEAT.FILEBEAT_START.split(" "), capture_output=True, text=True)
        logging.info(f"Started filebeat, stdout:{output.stdout}, stderr: {output.stderr}")

    @staticmethod
    def _stop_filebeat() -> None:
        """
        Utility method to stop filebeat

        :return: None
        """
        logging.info(f"Stopping filebeat with command: {constants.FILEBEAT.FILEBEAT_STOP}")
        output = subprocess.run(constants.FILEBEAT.FILEBEAT_STOP.split(" "), capture_output=True, text=True)
        logging.info(f"Stopped filebeat, output:{output.stdout}, err output: {output.stderr} ")

    @staticmethod
    def _set_filebeat_config(log_files_paths: List[str], kibana_ip: str, kibana_port: int, elastic_ip: str,
                             elastic_port: int, num_elastic_shards: int, kafka_topics: List[str], kafka_ip: str,
                             filebeat_modules: List[str],
                             kafka_port: int, reload_enabled: bool = False, kafka: bool = False) -> None:
        """
        Updates the filebeat configuration file

        :param log_files_paths: the list of log files that filebeat should monitor
        :param kibana_ip: the IP of Kibana where the data should be visualized
        :param kibana_port: the port of Kibana where the data should be visualized
        :param elastic_ip: the IP of elastic where the data should be shipped
        :param elastic_port: the port of elastic where the data should be shipped
        :param num_elastic_shards: the number of elastic shards
        :param reload_enabled: whether automatic reload of modules should be enabled
        :param kafka: whether kafka should be added as input
        :param kafka_topics: list of kafka topics to ingest
        :param kafka_port: the kafka server port
        :param kafka_ip: the kafka server ip
        :param filebeat_modules: list of filebeat modules to enable
        :return: None
        """
        filebeat_config = HostManagerUtil.filebeat_config(log_files_paths=log_files_paths, kibana_ip=kibana_ip,
                                                          kibana_port=kibana_port, elastic_ip=elastic_ip,
                                                          elastic_port=elastic_port,
                                                          num_elastic_shards=num_elastic_shards,
                                                          reload_enabled=reload_enabled, kafka=kafka,
                                                          kafka_port=kafka_port, kafka_ip=kafka_ip,
                                                          kafka_topics=kafka_topics)
        for module in filebeat_modules:
            if module == constants.FILEBEAT.SYSTEM_MODULE:
                HostManagerServicer.set_filebeat_system_module_config()
            elif module == constants.FILEBEAT.SNORT_MODULE:
                HostManagerServicer.set_filebeat_snort_module_config()
            elif module == constants.FILEBEAT.KAFKA_MODULE:
                HostManagerServicer.set_filebeat_kafka_module_config()
            elif module == constants.FILEBEAT.KIBANA_MODULE:
                HostManagerServicer.set_filebeat_kibana_module_config()
            elif module == constants.FILEBEAT.ELASTICSEARCH_MODULE:
                HostManagerServicer.set_filebeat_elasticsearch_module_config()
            elif module == constants.FILEBEAT.LOGSTASH_MODULE:
                HostManagerServicer.set_filebeat_logstash_module_config()
            else:
                logging.warning(f"Filebeat module: {module} not recognized")

        logging.info(f"Updating filebeat config: \n{filebeat_config}")
        HostManagerUtil.write_yaml_config(config=filebeat_config, path=constants.FILEBEAT.CONFIG_FILE)
        logging.info(f"Running filebeat setup command: {constants.FILEBEAT.SETUP_CMD}")
        output = subprocess.run(constants.FILEBEAT.SETUP_CMD.split(" "), capture_output=True, text=True)
        logging.info(f"Stdout of the setup command: {output.stdout}, stderr of the setup command: {output.stderr}")

    @staticmethod
    def _get_metricbeat_status() -> bool:
        """
        Utility method to get the status of metricbeat

        :return: status of metricbeat
        """
        logging.info(f"Getting metricbeat status with command: {constants.METRICBEAT.METRICBEAT_STATUS}")
        output = subprocess.run(constants.METRICBEAT.METRICBEAT_STATUS.split(" "), capture_output=True, text=True)
        metricbeat_running = not ("not" in output.stdout)
        logging.info(f"Got metricbeat status, output:{output.stdout}, err output: {output.stderr} ")
        return metricbeat_running

    @staticmethod
    def _start_metricbeat() -> None:
        """
        Utility method to start metricbeat

        :return: None
        """
        logging.info(f"Starting metricbeat with command: {constants.METRICBEAT.METRICBEAT_START}")
        output = subprocess.run(constants.METRICBEAT.METRICBEAT_START.split(" "), capture_output=True, text=True)
        logging.info(f"Started metricbeat, stdout:{output.stdout}, stderr: {output.stderr}")

    @staticmethod
    def _stop_metricbeat() -> None:
        """
        Utility method to stop metricbeat

        :return: None
        """
        logging.info(f"Stopping metricbeat with command: {constants.METRICBEAT.METRICBEAT_STOP}")
        output = subprocess.run(constants.METRICBEAT.METRICBEAT_STOP.split(" "), capture_output=True, text=True)
        logging.info(f"Stopped metricbeat, output:{output.stdout}, err output: {output.stderr} ")

    @staticmethod
    def _set_metricbeat_config(
            kibana_ip: str, kibana_port: int, elastic_ip: str, elastic_port: int, num_elastic_shards: int,
            metricbeat_modules: List[str], kafka_ip: str, kafka_port: int, reload_enabled: bool = False) -> None:
        """
        Updates the metricbeat configuration file

        :param kibana_ip: the IP of Kibana where the data should be visualized
        :param kibana_port: the port of Kibana where the data should be visualized
        :param elastic_ip: the IP of elastic where the data should be shipped
        :param elastic_port: the port of elastic where the data should be shipped
        :param num_elastic_shards: the number of elastic shards
        :param reload_enabled: whether automatic reload of modules should be enabled
        :param metricbeat_modules: list of metricbeat modules to enable
        :param kafka_ip: the ip of the kafka server
        :param kafka_port: the port of the kafka server
        :return: None
        """
        metricbeat_config = HostManagerUtil.metricbeat_config(
            kibana_ip=kibana_ip, kibana_port=kibana_port, elastic_ip=elastic_ip, elastic_port=elastic_port,
            num_elastic_shards=num_elastic_shards, reload_enabled=reload_enabled)
        for module in metricbeat_modules:
            if module == constants.METRICBEAT.SYSTEM_MODULE:
                HostManagerServicer.set_metricbeat_system_module_config()
            elif module == constants.METRICBEAT.LINUX_MODULE:
                HostManagerServicer.set_metricbeat_linux_module_config()
            elif module == constants.METRICBEAT.KAFKA_MODULE:
                HostManagerServicer.set_metricbeat_kafka_module_config(kafka_ip=kafka_ip, kafka_port=kafka_port)
            elif module == constants.METRICBEAT.KIBANA_MODULE:
                HostManagerServicer.set_metricbeat_kibana_module_config(kibana_ip=kibana_ip, kibana_port=kibana_port)
            elif module == constants.METRICBEAT.ELASTICSEARCH_MODULE:
                HostManagerServicer.set_metricbeat_elasticsearch_module_config(elastic_ip=elastic_ip,
                                                                               elastic_port=elastic_port)
            elif module == constants.METRICBEAT.LOGSTASH_MODULE:
                HostManagerServicer.set_metricbeat_logstash_module_config(logstash_ip=elastic_ip,
                                                                          logstash_port=elastic_port)
            else:
                logging.warning(f"Metricbeat module: {module} not recognized")

        logging.info(f"Updating metricbeat config: \n{metricbeat_config}")
        HostManagerUtil.write_yaml_config(config=metricbeat_config, path=constants.METRICBEAT.CONFIG_FILE)
        logging.info(f"Running metricbeat setup command: {constants.METRICBEAT.SETUP_CMD}")
        output = subprocess.run(constants.METRICBEAT.SETUP_CMD.split(" "), capture_output=True, text=True)
        logging.info(f"Stdout of the setup command: {output.stdout}, stderr of the setup command: {output.stderr}")

    @staticmethod
    def set_filebeat_snort_module_config() -> None:
        """
        Updates the filebeat snort module configuration

        :return: None
        """
        logging.info(f"Enabling module with command: "
                     f"{constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.SNORT_MODULE)}")
        output = subprocess.run(constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.SNORT_MODULE).split(" "),
                                capture_output=True, text=True)
        logging.info(f"Module enabled, output: {output.stdout}, err output: {output.stderr}")
        snort_module_config = HostManagerUtil.filebeat_snort_module_config()
        logging.info(f"Updating filebeat snort module config: \n{snort_module_config}")
        HostManagerUtil.write_yaml_config(config=snort_module_config,
                                          path=f"{constants.FILEBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.FILEBEAT.SNORT_MODULE_CONFIG_FILE}")

    @staticmethod
    def set_filebeat_elasticsearch_module_config() -> None:
        """
        Updates the filebeat elasticsearch module configuration

        :return: None
        """
        logging.info(f"Enabling module with command: "
                     f"{constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.ELASTICSEARCH_MODULE)}")
        output = subprocess.run(constants.FILEBEAT.ENABLE_MODULE_CMD.format(
            constants.FILEBEAT.ELASTICSEARCH_MODULE).split(" "), capture_output=True, text=True)
        logging.info(f"Module enabled, output: {output.stdout}, err output: {output.stderr}")
        elasticsearch_module_config = HostManagerUtil.filebeat_elasticsearch_module_config()
        logging.info(f"Updating filebeat elasticsearch module config: \n{elasticsearch_module_config}")
        HostManagerUtil.write_yaml_config(config=elasticsearch_module_config,
                                          path=f"{constants.FILEBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.FILEBEAT.ELASTICSEARCH_MODULE_CONFIG_FILE}")

    @staticmethod
    def set_filebeat_logstash_module_config() -> None:
        """
        Updates the filebeat logstash module configuration

        :return: None
        """
        logging.info(f"Enabling module with command: "
                     f"{constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.LOGSTASH_MODULE)}")
        output = subprocess.run(constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.LOGSTASH_MODULE).split(
            " "), capture_output=True, text=True)
        logging.info(f"Module enabled, output: {output.stdout}, err output: {output.stderr}")
        logstash_module_config = HostManagerUtil.filebeat_logstash_module_config()
        logging.info(f"Updating filebeat logstash module config: \n{logstash_module_config}")
        HostManagerUtil.write_yaml_config(config=logstash_module_config,
                                          path=f"{constants.FILEBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.FILEBEAT.LOGSTASH_MODULE_CONFIG_FILE}")

    @staticmethod
    def set_filebeat_kibana_module_config() -> None:
        """
        Updates the filebeat kibana module configuration

        :return: None
        """
        logging.info(f"Enabling module with command: "
                     f"{constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.KIBANA_MODULE)}")
        output = subprocess.run(constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.KIBANA_MODULE).split(
            " "), capture_output=True, text=True)
        logging.info(f"Module enabled, output: {output.stdout}, err output: {output.stderr}")
        kibana_module_config = HostManagerUtil.filebeat_kibana_module_config()
        logging.info(f"Updating filebeat kibana module config: \n{kibana_module_config}")
        HostManagerUtil.write_yaml_config(config=kibana_module_config,
                                          path=f"{constants.FILEBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.FILEBEAT.KIBANA_MODULE_CONFIG_FILE}")

    @staticmethod
    def set_filebeat_system_module_config() -> None:
        """
        Updates the filebeat system module configuration

        :return: None
        """
        logging.info(f"Enabling module with command: "
                     f"{constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.SYSTEM_MODULE)}")
        output = subprocess.run(constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.SYSTEM_MODULE).split(
            " "), capture_output=True, text=True)
        logging.info(f"Module enabled, output: {output.stdout}, err output: {output.stderr}")
        system_module_config = HostManagerUtil.filebeat_system_module_config()
        logging.info(f"Updating filebeat system module config: \n{system_module_config}")
        HostManagerUtil.write_yaml_config(config=system_module_config,
                                          path=f"{constants.FILEBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.FILEBEAT.SYSTEM_MODULE_CONFIG_FILE}")

    @staticmethod
    def set_filebeat_kafka_module_config() -> None:
        """
        Updates the filebeat kafka module configuration

        :return: None
        """
        logging.info(f"Enabling module with command: "
                     f"{constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.KAFKA_MODULE)}")
        output = subprocess.run(constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.KAFKA_MODULE).split(" "),
                                capture_output=True, text=True)
        logging.info(f"Module enabled, output: {output.stdout}, err output: {output.stderr}")
        kafka_module_config = HostManagerUtil.filebeat_kafka_module_config()
        logging.info(f"Updating filebeat kafka module config: \n{kafka_module_config}")
        HostManagerUtil.write_yaml_config(config=kafka_module_config,
                                          path=f"{constants.FILEBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.FILEBEAT.KAFKA_MODULE_CONFIG_FILE}")

    @staticmethod
    def _get_packetbeat_status() -> bool:
        """
        Utility method to get the status of packetbeat

        :return: status of filebeat
        """
        logging.info(f"Getting packetbeat status with command: {constants.PACKETBEAT.PACKETBEAT_STATUS}")
        output = subprocess.run(constants.PACKETBEAT.PACKETBEAT_STATUS.split(" "), capture_output=True, text=True)
        packetbeat_running = not ("not" in output.stdout)
        logging.info(f"Got packetbeat status, output:{output.stdout}, err output: {output.stderr} ")
        return packetbeat_running

    @staticmethod
    def _start_packetbeat() -> None:
        """
        Utility method to start packetbeat

        :return: None
        """
        logging.info(f"Starting packetbeat with command: {constants.PACKETBEAT.PACKETBEAT_START}")
        output = subprocess.run(constants.PACKETBEAT.PACKETBEAT_START.split(" "), capture_output=True, text=True)
        logging.info(f"Started packetbeat, stdout:{output.stdout}, stderr: {output.stderr}")

    @staticmethod
    def _stop_packetbeat() -> None:
        """
        Utility method to stop packetbeat

        :return: None
        """
        logging.info(f"Stopping packetbeat with command: {constants.PACKETBEAT.PACKETBEAT_STOP}")
        output = subprocess.run(constants.PACKETBEAT.PACKETBEAT_STOP.split(" "), capture_output=True, text=True)
        logging.info(f"Stopped packetbeat, output:{output.stdout}, err output: {output.stderr} ")

    @staticmethod
    def _set_packetbeat_config(kibana_ip: str, kibana_port: int, elastic_ip: str, elastic_port: int,
                               num_elastic_shards: int) -> None:
        """
        Updates the packetbeat configuration file

        :param kibana_ip: the IP of Kibana where the data should be visualized
        :param kibana_port: the port of Kibana where the data should be visualized
        :param elastic_ip: the IP of elastic where the data should be shipped
        :param elastic_port: the port of elastic where the data should be shipped
        :param num_elastic_shards: the number of elastic shards
        :return: None
        """
        packetbeat_config = HostManagerUtil.packetbeat_config(
            kibana_ip=kibana_ip, kibana_port=kibana_port, elastic_ip=elastic_ip, elastic_port=elastic_port,
            num_elastic_shards=num_elastic_shards)

        logging.info(f"Updating packetbeat config: \n{packetbeat_config}")
        HostManagerUtil.write_yaml_config(config=packetbeat_config, path=constants.PACKETBEAT.CONFIG_FILE)
        logging.info(f"Running packetbeat setup command: {constants.PACKETBEAT.SETUP_CMD}")
        output = subprocess.run(constants.PACKETBEAT.SETUP_CMD.split(" "), capture_output=True, text=True)
        logging.info(f"Stdout of the setup command: {output.stdout}, stderr of the setup command: {output.stderr}")

    @staticmethod
    def set_metricbeat_system_module_config() -> None:
        """
        Updates the metricbeat system module configuration

        :return: None
        """
        logging.info(f"Enabling system module with command: "
                     f"{constants.METRICBEAT.ENABLE_MODULE_CMD.format(constants.METRICBEAT.SYSTEM_MODULE)}")
        output = subprocess.run(constants.METRICBEAT.ENABLE_MODULE_CMD.format(
            constants.METRICBEAT.SYSTEM_MODULE).split(" "), capture_output=True, text=True)
        logging.info(f"Module enabled, output: {output.stdout}, err output: {output.stderr}")
        system_module_config = HostManagerUtil.metricbeat_system_module_config()
        logging.info(f"Updating metricbeat system module config: \n{system_module_config}")
        HostManagerUtil.write_yaml_config(config=system_module_config,
                                          path=f"{constants.METRICBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.METRICBEAT.SYSTEM_MODULE_CONFIG_FILE}")

    @staticmethod
    def set_metricbeat_linux_module_config() -> None:
        """
        Updates the metricbeat system module configuration

        :return: None
        """
        logging.info(f"Enabling linux module with command: "
                     f"{constants.METRICBEAT.ENABLE_MODULE_CMD.format(constants.METRICBEAT.LINUX_MODULE)}")
        output = subprocess.run(constants.METRICBEAT.ENABLE_MODULE_CMD.format(
            constants.METRICBEAT.LINUX_MODULE).split(" "), capture_output=True, text=True)
        logging.info(f"Module enabled, output: {output.stdout}, err output: {output.stderr}")
        linux_module_config = HostManagerUtil.metricbeat_linux_module_config()
        logging.info(f"Updating metricbeat linux module config: \n{linux_module_config}")
        HostManagerUtil.write_yaml_config(config=linux_module_config,
                                          path=f"{constants.METRICBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.METRICBEAT.LINUX_MODULE_CONFIG_FILE}")

    @staticmethod
    def set_metricbeat_kafka_module_config(kafka_ip: str, kafka_port: int) -> None:
        """
        Updates the metricbeat kafka module configuration

        :param kafka_ip: ip of the kafka server
        :param kafka_port: port of the kafka server
        :return: None
        """
        logging.info(f"Enabling kafka module with command: "
                     f"{constants.METRICBEAT.ENABLE_MODULE_CMD.format(constants.METRICBEAT.KAFKA_MODULE)}")
        output = subprocess.run(constants.METRICBEAT.ENABLE_MODULE_CMD.format(
            constants.METRICBEAT.KAFKA_MODULE).split(" "), capture_output=True, text=True)
        logging.info(f"Module enabled, output: {output.stdout}, err output: {output.stderr}")
        kafka_module_config = HostManagerUtil.metricbeat_kafka_module_config(kafka_ip=kafka_ip, kafka_port=kafka_port)
        logging.info(f"Updating metricbeat kafka module config: \n{kafka_module_config}")
        HostManagerUtil.write_yaml_config(config=kafka_module_config,
                                          path=f"{constants.METRICBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.METRICBEAT.KAFKA_MODULE_CONFIG_FILE}")

    @staticmethod
    def set_metricbeat_elasticsearch_module_config(elastic_ip: str, elastic_port: int) -> None:
        """
        Updates the metricbeat elastic module configuration

        :param elastic_ip: ip of the elastic server
        :param elastic_port: port of the elastic server
        :return: None
        """
        logging.info(f"Enabling elasticsearch module with command: "
                     f"{constants.METRICBEAT.ENABLE_MODULE_CMD.format(constants.METRICBEAT.ELASTICSEARCH_MODULE)}")
        output = subprocess.run(constants.METRICBEAT.ENABLE_MODULE_CMD.format(
            constants.METRICBEAT.ELASTICSEARCH_MODULE).split(" "), capture_output=True, text=True)
        logging.info(f"Module enabled, output: {output.stdout}, err output: {output.stderr}")
        elasticsearch_module_config = HostManagerUtil.metricbeat_elasticsearch_module_config(elastic_ip=elastic_ip,
                                                                                             elastic_port=elastic_port)
        logging.info(f"Updating metricbeat elasticsearch module config: \n{elasticsearch_module_config}")
        HostManagerUtil.write_yaml_config(config=elasticsearch_module_config,
                                          path=f"{constants.METRICBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.METRICBEAT.ELASTICSEARCH_MODULE_CONFIG_FILE}")

    @staticmethod
    def set_metricbeat_kibana_module_config(kibana_ip: str, kibana_port: int) -> None:
        """
        Updates the metricbeat kibana module configuration

        :param kibana_ip: ip of the kibana server
        :param kibana_port: port of the kibana server
        :return: None
        """
        logging.info(f"Enabling Kibana module with command: "
                     f"{constants.METRICBEAT.ENABLE_MODULE_CMD.format(constants.METRICBEAT.KIBANA_MODULE)}")
        output = subprocess.run(constants.METRICBEAT.ENABLE_MODULE_CMD.format(
            constants.METRICBEAT.KIBANA_MODULE).split(" "), capture_output=True, text=True)
        logging.info(f"Module enabled, output: {output.stdout}, err output: {output.stderr}")
        kibana_module_config = HostManagerUtil.metricbeat_kibana_module_config(
            kibana_ip=kibana_ip, kibana_port=kibana_port)
        logging.info(f"Updating metricbeat kibana module config: \n{kibana_module_config}")
        HostManagerUtil.write_yaml_config(config=kibana_module_config,
                                          path=f"{constants.METRICBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.METRICBEAT.KIBANA_MODULE_CONFIG_FILE}")

    @staticmethod
    def set_metricbeat_logstash_module_config(logstash_ip: str, logstash_port: int) -> None:
        """
        Updates the metricbeat logstas module configuration

        :param logstash_ip: ip of the logstash server
        :param logstash_port: port of the logstash server
        :return: None
        """
        logging.info(f"Enabling Logstash module with command: "
                     f"{constants.METRICBEAT.ENABLE_MODULE_CMD.format(constants.METRICBEAT.LOGSTASH_MODULE)}")
        output = subprocess.run(constants.METRICBEAT.ENABLE_MODULE_CMD.format(
            constants.METRICBEAT.LOGSTASH_MODULE).split(" "), capture_output=True, text=True)
        logging.info(f"Module enabled, output: {output.stdout}, err output: {output.stderr}")
        logstash_module_config = HostManagerUtil.metricbeat_logstash_module_config(logstash_ip=logstash_ip,
                                                                                   logstash_port=logstash_port)
        logging.info(f"Updating metricbeat logstash module config: \n{logstash_module_config}")
        HostManagerUtil.write_yaml_config(config=logstash_module_config,
                                          path=f"{constants.METRICBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.METRICBEAT.LOGSTASH_MODULE_CONFIG_FILE}")

    @staticmethod
    def _get_heartbeat_status() -> bool:
        """
        Utility method to get the status of heartbeat

        :return: status of heartbeat
        """
        logging.info(f"Getting heartbeat status with command: {constants.HEARTBEAT.HEARTBEAT_STATUS}")
        output = subprocess.run(constants.HEARTBEAT.HEARTBEAT_STATUS.split(" "), capture_output=True, text=True)
        heartbeat_running = not ("not" in output.stdout)
        logging.info(f"Got heartbeat status, output:{output.stdout}, err output: {output.stderr} ")
        return heartbeat_running

    @staticmethod
    def _start_heartbeat() -> None:
        """
        Utility method to start heartbeat

        :return: None
        """
        logging.info(f"Starting heartbeat with command: {constants.HEARTBEAT.HEARTBEAT_START}")
        output = subprocess.run(constants.HEARTBEAT.HEARTBEAT_START.split(" "), capture_output=True, text=True)
        logging.info(f"Started heartbeat, stdout:{output.stdout}, stderr: {output.stderr}")

    @staticmethod
    def _stop_heartbeat() -> None:
        """
        Utility method to stop heartbeat

        :return: None
        """
        logging.info(f"Stopping heartbeat with command: {constants.HEARTBEAT.HEARTBEAT_STOP}")
        output = subprocess.run(constants.HEARTBEAT.HEARTBEAT_STOP.split(" "), capture_output=True, text=True)
        logging.info(f"Stopped heartbeat, output:{output.stdout}, err output: {output.stderr} ")

    @staticmethod
    def _set_heartbeat_config(kibana_ip: str, kibana_port: int, elastic_ip: str,
                              elastic_port: int, num_elastic_shards: int, hosts_to_monitor: List[str]) -> None:
        """
        Updates the heartbeat configuration file

        :param hosts_to_monitor: the list of hosts to monitor
        :param kibana_ip: the IP of Kibana where the data should be visualized
        :param kibana_port: the port of Kibana where the data should be visualized
        :param elastic_ip: the IP of elastic where the data should be shipped
        :param elastic_port: the port of elastic where the data should be shipped
        :param num_elastic_shards: the number of elastic shards
        :return: None
        """
        heartbeat_config = HostManagerUtil.heartbeat_config(
            kibana_ip=kibana_ip, kibana_port=kibana_port, elastic_ip=elastic_ip, elastic_port=elastic_port,
            num_elastic_shards=num_elastic_shards, hosts_to_monitor=list(hosts_to_monitor))
        logging.info(f"Updating heartbeat config: \n{heartbeat_config}")
        HostManagerUtil.write_yaml_config(config=heartbeat_config, path=constants.HEARTBEAT.CONFIG_FILE)
        logging.info(f"Running heartbeat setup command: {constants.HEARTBEAT.SETUP_CMD}")
        output = subprocess.run(constants.HEARTBEAT.SETUP_CMD.split(" "), capture_output=True, text=True)
        logging.info(f"Stdout of the setup command: {output.stdout}, stderr of the setup command: {output.stderr}")


def serve(port: int = 50049, log_dir: str = "/", max_workers: int = 10,
          log_file_name: str = "host_manager.log") -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :param log_dir: the directory to write the log file
    :param log_file_name: the file name of the log
    :param max_workers: the maximum number of GRPC workers
    :return: None
    """
    constants.LOG_FILES.HOST_MANAGER_LOG_DIR = log_dir
    constants.LOG_FILES.HOST_MANAGER_LOG_FILE = log_file_name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    csle_collector.host_manager.host_manager_pb2_grpc.add_HostManagerServicer_to_server(
        HostManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"HostManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
