from typing import List
import logging
import socket
import time
import grpc
import os
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
                         context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostMonitorDTO:
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
        return csle_collector.host_manager.host_manager_pb2.HostMonitorDTO(running=True)

    def stopHostMonitor(self, request: csle_collector.host_manager.host_manager_pb2.StopHostMonitorMsg,
                        context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostMonitorDTO:
        """
        Stops the Host monitor thread if it is running

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host monitor thread
        """
        if self.host_monitor_thread is not None:
            self.host_monitor_thread.running = False
        return csle_collector.host_manager.host_manager_pb2.HostMonitorDTO(running=False)

    def getHostMonitorStatus(self, request: csle_collector.host_manager.host_manager_pb2.GetHostMonitorStatusMsg,
                             context: grpc.ServicerContext) \
            -> csle_collector.host_manager.host_manager_pb2.HostMonitorDTO:
        """
        Gets the status of the Host Monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host monitor
        """
        running = False
        if self.host_monitor_thread is not None:
            running = self.host_monitor_thread.running
        return csle_collector.host_manager.host_manager_pb2.HostMonitorDTO(running=running)

    @staticmethod
    def _get_filebeat_status() -> bool:
        """
        Utility method to get the status of filebeat

        :return: status of filebeat
        """
        p = subprocess.Popen(constants.FILEBEAT.FILEBEAT_STATUS, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        status_output = output.decode()
        filebeat_running = not ("not" in status_output)
        return filebeat_running

    @staticmethod
    def _start_filebeat() -> None:
        """
        Utility method to start filebeat

        :return: None
        """
        logging.info("Starting filebeat")
        os.system(constants.FILEBEAT.FILEBEAT_START)

    @staticmethod
    def _stop_filebeat() -> None:
        """
        Utility method to stop filebeat

        :return: None
        """
        logging.info("Stopping filebeat")
        os.system(constants.FILEBEAT.FILEBEAT_STOP)

    @staticmethod
    def _set_filebeat_config(log_files_paths: List[str], kibana_ip: str, kibana_port: int, elastic_ip: str,
                             elastic_port: int, num_elastic_shards: int, reload_enabled: bool = False) -> None:
        """
        Updates the filebeat configuration file

        :param log_files_paths: the list of log files that filebeat should monitor
        :param kibana_ip: the IP of Kibana where the data should be visualized
        :param kibana_port: the port of Kibana where the data should be visualized
        :param elastic_ip: the IP of elastic where the data should be shipped
        :param elastic_port: the port of elastic where the data should be shipped
        :param num_elastic_shards: the number of elastic shards
        :param reload_enabled: whether automatic reload of modules should be enabled
        :return: None
        """
        filebeat_config = HostManagerUtil.filebeat_config(log_files_paths=log_files_paths, kibana_ip=kibana_ip,
                                                          kibana_port=kibana_port, elastic_ip=elastic_ip,
                                                          elastic_port=elastic_port,
                                                          num_elastic_shards=num_elastic_shards,
                                                          reload_enabled=reload_enabled)
        logging.info(f"Updating filebeat config: \n{filebeat_config}")
        HostManagerUtil.write_yaml_config(config=filebeat_config, path=constants.FILEBEAT.CONFIG_FILE)

    @staticmethod
    def set_filebeat_snort_module_config() -> None:
        """
        Updates the filebeat snort module configuration

        :return: None
        """
        p = subprocess.Popen(constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.SNORT_MODULE),
                             stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()
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
        p = subprocess.Popen(constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.ELASTICSEARCH_MODULE),
                             stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()
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
        p = subprocess.Popen(constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.LOGSTASH_MODULE),
                             stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()
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
        p = subprocess.Popen(constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.KIBANA_MODULE),
                             stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()
        kibana_module_config = HostManagerUtil.filebeat_kibana_module_config()
        logging.info(f"Updating filebeat kibana module config: \n{kibana_module_config}")
        HostManagerUtil.write_yaml_config(config=kibana_module_config,
                                          path=f"{constants.FILEBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.FILEBEAT.KIBANA_MODULE}")

    @staticmethod
    def set_filebeat_system_module_config() -> None:
        """
        Updates the filebeat system module configuration

        :return: None
        """
        p = subprocess.Popen(constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.SYSTEM_MODULE),
                             stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()
        system_module_config = HostManagerUtil.filebeat_system_module_config()
        logging.info(f"Updating filebeat system module config: \n{system_module_config}")
        HostManagerUtil.write_yaml_config(config=system_module_config,
                                          path=f"{constants.FILEBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.FILEBEAT.SYSTEM_MODULE}")

    @staticmethod
    def set_filebeat_kafka_module_config() -> None:
        """
        Updates the filebeat kafka module configuration

        :return: None
        """
        p = subprocess.Popen(constants.FILEBEAT.ENABLE_MODULE_CMD.format(constants.FILEBEAT.KAFKA_MODULE),
                             stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()
        kafka_module_config = HostManagerUtil.filebeat_kafka_module_config()
        logging.info(f"Updating filebeat kafka module config: \n{kafka_module_config}")
        HostManagerUtil.write_yaml_config(config=kafka_module_config,
                                          path=f"{constants.FILEBEAT.MODULES_CONFIG_DIR}"
                                               f"{constants.FILEBEAT.KAFKA_MODULE}")


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
