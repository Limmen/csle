import os
import logging
from concurrent import futures
import grpc
import subprocess
import csle_collector.constants.constants as collector_constants
from csle_common.dao.emulation_config.config import Config
import csle_common.constants.constants as constants
from csle_common.controllers.management_system_controller import ManagementSystemController
from csle_common.util.general_util import GeneralUtil
from csle_common.util.cluster_util import ClusterUtil
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.emulation_env_controller import EmulationEnvController
from csle_common.controllers.container_controller import ContainerController
from csle_common.controllers.sdn_controller_manager import SDNControllerManager
from csle_common.controllers.resource_constraints_controller import ResourceConstraintsController
from csle_common.controllers.users_controller import UsersController
from csle_common.controllers.vulnerabilities_controller import VulnerabilitiesController
from csle_common.controllers.flags_controller import FlagsController
from csle_common.controllers.traffic_controller import TrafficController
from csle_common.controllers.topology_controller import TopologyController
from csle_common.controllers.ovs_controller import OVSController
from csle_common.controllers.snort_ids_controller import SnortIDSController
from csle_common.controllers.ossec_ids_controller import OSSECIDSController
from csle_common.controllers.host_controller import HostController
from csle_common.controllers.elk_controller import ELKController
from csle_common.controllers.kafka_controller import KafkaController
from csle_common.util.read_emulation_statistics_util import ReadEmulationStatisticsUtil
import csle_ryu.constants.constants as ryu_constants
import csle_cluster.cluster_manager.cluster_manager_pb2_grpc
import csle_cluster.cluster_manager.cluster_manager_pb2
from csle_cluster.cluster_manager.cluster_manager_util import ClusterManagerUtil
import csle_cluster.constants.constants as cluster_constants


class ClusterManagerServicer(csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerServicer):
    """gRPC server for managing a node in the CSLE management system cluster"""

    def __init__(self) -> None:
        """Initializes the server"""

        file_name = collector_constants.LOG_FILES.CLUSTER_MANAGER_LOG_FILE
        dir = collector_constants.LOG_FILES.CLUSTER_MANAGER_LOG_DIR
        logfile = os.path.join(dir, file_name)
        logging.basicConfig(filename=logfile, level=logging.INFO)
        logging.info(f"Setting up ClusterManager, logfile: {logfile}")

    def getNodeStatus(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetNodeStatusMsg,
                      context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO:
        """
        Gets the status of a node in the CSLE cluster & management system

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the server
        """
        config = ClusterUtil.get_config()
        ip = GeneralUtil.get_host_ip()
        leader = ClusterUtil.am_i_leader(ip=ip, config=config)
        cadvisor_running = ManagementSystemController.is_cadvisor_running()
        prometheus_running = ManagementSystemController.is_prometheus_running()
        grafana_running = ManagementSystemController.is_grafana_running()
        pgadmin_running = ManagementSystemController.is_pgadmin_running()
        nginx_running = ManagementSystemController.is_nginx_running()
        flask_running = ManagementSystemController.is_flask_running()
        postgresql_running = ManagementSystemController.is_postgresql_running()
        docker_statsmanager_running = ManagementSystemController.is_statsmanager_running()
        node_exporter_running = ManagementSystemController.is_node_exporter_running()
        docker_engine_running = ManagementSystemController.is_docker_engine_running()
        return csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO(
            ip=ip, leader=leader, cAdvisorRunning=cadvisor_running, prometheusRunning=prometheus_running,
            grafanaRunning=grafana_running, pgAdminRunning=pgadmin_running, nginxRunning=nginx_running,
            flaskRunning=flask_running, dockerStatsManagerRunning=docker_statsmanager_running,
            nodeExporterRunning=node_exporter_running, postgreSQLRunning=postgresql_running,
            dockerEngineRunning=docker_engine_running
        )

    def startPostgreSQL(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartPostgreSQLMsg,
                        context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Postgresql

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of PostgreSQL
        """
        logging.info(f"Starting postgresql with command: {constants.COMMANDS.POSTGRESQL_START}")
        operation_status, stdout, stderr = ManagementSystemController.start_postgresql(logger=logging.getLogger())

        logging.info(f"Started postgresql, stdout:{stdout}, stderr: {stderr}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=True)

    def stopPostgreSQL(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopPostgreSQLMsg,
                       context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops Postgresql

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of PostgreSQL
        """
        logging.info(f"Stopping postgresql with command: {constants.COMMANDS.POSTGRESQL_STOP}")
        operation_status, stdout, stderr = ManagementSystemController.stop_postgresql(logger=logging.getLogger())
        logging.info(f"Stopped postgresql, stdout:{stdout}, stderr: {stderr}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=False)

    def startDockerEngine(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartDockerEngineMsg,
                          context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Docker Engine

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of  the Docker egine
        """
        logging.info(f"Starting the docker engine with command: {constants.COMMANDS.DOCKER_ENGINE_START}")
        operation_status, stdout, stderr = ManagementSystemController.start_docker_engine(logger=logging.getLogger())
        logging.info(f"Started the docker engine, stdout:{stdout}, stderr: {stderr}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=True)

    def stopDockerEngine(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopDockerEngineMsg,
                         context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops the Docker Engine

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Docker Engine
        """
        logging.info(f"Stopping the Docker engine with command: {constants.COMMANDS.DOCKER_ENGINE_STOP}")
        operation_status, stdout, stderr = ManagementSystemController.stop_docker_engine(logger=logging.getLogger())
        logging.info(f"Stopped the Docker engine, stdout:{stdout}, stderr: {stderr}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=False)

    def startNginx(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartNginxMsg,
                   context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Nginx

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of Nginx
        """
        logging.info(f"Starting nginx with command: {constants.COMMANDS.NGINX_START}")
        operation_status, stdout, stderr = ManagementSystemController.start_nginx(logger=logging.getLogger())
        logging.info(f"Started nginx, stdout:{stdout}, stderr: {stderr}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=True)

    def stopNginx(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopNginxMsg,
                  context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops Nginx

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of Nginx
        """
        logging.info(f"Stopping Nginx with command: {constants.COMMANDS.NGINX_STOP}")
        operation_status, stdout, stderr = ManagementSystemController.stop_nginx(logger=logging.getLogger())
        logging.info(f"Stopped Nginx, stdout:{stdout}, stderr: {stderr}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=False)

    def startCAdvisor(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartCAdvisorMsg,
                      context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts cAdvisor

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of cAdvisor
        """
        logging.info("Starting cAdvisor")
        ManagementSystemController.start_cadvisor(logger=logging.getLogger())
        logging.info("Started cAdvisor")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=True)

    def stopCAdvisor(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopCAdvisorMsg,
                     context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops cAdvisor

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of cAdvisor
        """
        logging.info("Stopping cAdvisor")
        ManagementSystemController.stop_cadvisor()
        logging.info("Stopped cAdvisor")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=False)

    def startNodeExporter(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartNodeExporterMsg,
                          context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts node exporter

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of node exporter
        """
        logging.info("Starting node exporter")
        ManagementSystemController.start_node_exporter(logger=logging.getLogger())
        logging.info("Started node exporter")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=True)

    def stopNodeExporter(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopNodeExporterMsg,
                         context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops node exporter

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of node exporter
        """
        logging.info("Stopping node exporter")
        ManagementSystemController.stop_node_exporter(logger=logging.getLogger())
        logging.info("Stopped node exporter")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=False)

    def startGrafana(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartGrafanaMsg,
                     context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts grafana

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of grafana
        """
        logging.info("Starting grafana")
        ManagementSystemController.start_grafana(logger=logging.getLogger())
        logging.info("Started grafana")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=True)

    def stopGrafana(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopGrafanaMsg,
                    context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops grafana

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of grafana
        """
        logging.info("Stopping grafana")
        ManagementSystemController.stop_grafana()
        logging.info("Stopped grafana")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=False)

    def startPrometheus(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartPrometheusMsg,
                        context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Prometheus

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of Prometheus
        """
        logging.info("Starting Prometheus")
        ManagementSystemController.start_prometheus(logger=logging.getLogger())
        logging.info("Started Prometheus")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=True)

    def stopPrometheus(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopPrometheusMsg,
                       context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops Prometheus

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of Prometheus
        """
        logging.info("Stopping Prometheus")
        ManagementSystemController.stop_prometheus(logger=logging.getLogger())
        logging.info("Stopped Prometheus")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=False)

    def startPgAdmin(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartPgAdminMsg,
                     context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts pgAdmin

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of pgAdmin
        """
        logging.info("Starting pgAdmin")
        ManagementSystemController.start_pgadmin(logger=logging.getLogger())
        logging.info("Started pgAdmin")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=True)

    def stopPgAdmin(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopPgAdminMsg,
                    context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops pgAdmin

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of pgAdmin
        """
        logging.info("Stopping pgAdmin")
        ManagementSystemController.stop_pgadmin()
        logging.info("Stopped pgAdmin")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=False)

    def startFlask(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartFlaskMsg,
                   context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Flask

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of flask
        """
        logging.info("Starting flask")
        ManagementSystemController.start_flask(logger=logging.getLogger())
        logging.info("Started flask")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=True)

    def stopFlask(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopFlaskMsg,
                  context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops Flask

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of flask
        """
        logging.info("Stopping flask")
        ManagementSystemController.stop_flask(logger=logging.getLogger())
        logging.info("Stopped flask")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=False)

    def startDockerStatsManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartDockerStatsManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts the docker statsmanager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the docker statsmanager
        """
        logging.info("Starting the docker statsmanager")
        ManagementSystemController.start_docker_statsmanager(logger=logging.getLogger())
        logging.info("Started the docker statsmanager")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=True)

    def stopDockerStatsManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopDockerStatsManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Stops the docker statsmanaager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the docker statsmanager
        """
        logging.info("Stopping the Docker statsmanager")
        ManagementSystemController.stop_docker_statsmanager(logger=logging.getLogger())
        logging.info("Stopped the Docker statsmanager")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=False)

    def getLogFile(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetLogFileMsg,
                   context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets a specific log file

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info(f"Getting log file: {request.name}")
        data = []
        try:
            if os.path.exists(request.name):
                try:
                    with open(request.name, 'r') as fp:
                        data = ClusterManagerUtil.tail(fp, window=100).split("\n")
                except Exception as e:
                    logging.info(f"Exception reading log file: {request.name}. Stacktrace: {str(e)}, {repr(e)}")
        except Exception as e:
            logging.info(f"Exception finding log file: {request.name}. Stacktrace: {str(e)}, {repr(e)}")
        logs = data
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=logs)

    def getFlaskLogs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetFlaskLogsMsg,
                     context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the Flask logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info("Getting the flask logs")
        config = Config.get_current_config()
        path = config.flask_log_file
        logs = []
        try:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as fp:
                        data = ClusterManagerUtil.tail(fp, window=100).split("\n")
                        logs = data
                except Exception as e:
                    logging.info(f"Exception reading log file: {path}. Stacktrace: {str(e)}, {repr(e)}")
        except Exception as e:
            logging.info(f"Exception reading flask logs. Stacktrace: {str(e)}, {repr(e)}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=logs)

    def getPostrgreSQLLogs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetPostgreSQLLogsMsg,
                           context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the PostgreSQL logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info("Getting the PostgreSQL logs")
        config = Config.get_current_config()
        path = config.postgresql_log_dir
        logs = []
        try:
            for f in os.listdir(path):
                item = os.path.join(path, f)
                if os.path.isfile(item) and constants.FILE_PATTERNS.LOG_SUFFIX in item and \
                        constants.FILE_PATTERNS.GZ_SUFFIX not in item:
                    try:
                        with open(item, 'r') as fp:
                            data = ClusterManagerUtil.tail(fp, window=100).split("\n")
                            logs = data
                    except Exception as e:
                        logging.info(f"Exception reading log file: {item}. Stacktrace: {str(e)}, {repr(e)}")
        except Exception as e:
            logging.info(f"Exception reading postgresql logs. Stacktrace: {str(e)}, {repr(e)}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=logs)

    def getDockerLogs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetDockerLogsMsg,
                      context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the Docker logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info("Getting the Docker logs")
        logs = []
        try:
            cmd = constants.COMMANDS.DOCKER_ENGINE_LOGS
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=subprocess.DEVNULL)
            (output_bytes, err) = p.communicate()
            output_str = output_bytes.decode("utf-8")
            output = output_str.split("\n")[-100:]
            logs = output
            if logs == ['']:
                alt_cmd = constants.COMMANDS.DOCKER_ENGINE_LOGS_ALTERNATIVE
                p = subprocess.Popen(alt_cmd, stdout=subprocess.PIPE, shell=True, stdin=subprocess.DEVNULL)
                (output_bytes, err) = p.communicate()
                output_str = output_bytes.decode("utf-8")
                output = output_str.split("\n")[-100:]
                logs = output
        except Exception as e:
            logging.info(f"Exception reading docker logs. Stacktrace: {str(e)}, {repr(e)}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=logs)

    def getNginxLogs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetNginxLogsMsg,
                     context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the nginx logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info("Getting the Nginx logs")
        config = Config.get_current_config()
        path = config.nginx_log_dir
        logs = []
        try:
            for f in os.listdir(path):
                item = os.path.join(path, f)
                if os.path.isfile(item) and constants.FILE_PATTERNS.LOG_SUFFIX in item \
                        and constants.FILE_PATTERNS.GZ_SUFFIX not in item:
                    try:
                        with open(item, 'r') as fp:
                            data = ClusterManagerUtil.tail(fp, window=100).split("\n")
                            logs = logs + data
                    except Exception as e:
                        logging.info(f"Exception reading log file: {item}. Stacktrace: {str(e)}, {repr(e)}")
        except Exception as e:
            logging.info(f"Exception reading nginx logs. Stacktrace: {str(e)}, {repr(e)}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=logs)

    def getGrafanaLogs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetGrafanaLogsMsg,
                       context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the Grafana logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info("Getting the Grafana logs")
        logs = []
        try:
            cmd = constants.COMMANDS.GRAFANA_LOGS
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output_bytes, err) = p.communicate()
            output_str = output_bytes.decode("utf-8")
            output = output_str.split("\n")[-100:]
            logs = output
        except Exception as e:
            logging.info(f"Exception reading grafana logs. Stacktrace: {str(e)}, {repr(e)}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=logs)

    def getPgAdminLogs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetPgAdminLogsMsg,
                       context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the pgAdmin logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info("Getting the pgAdmin logs")
        logs = []
        try:
            cmd = constants.COMMANDS.PGADMIN_LOGS
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output_bytes, err) = p.communicate()
            output_str = output_bytes.decode("utf-8")
            output = output_str.split("\n")[-100:]
            logs = output
        except Exception as e:
            logging.info(f"Exception reading nginx logs. Stacktrace: {str(e)}, {repr(e)}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=logs)

    def getCadvisorLogs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetCAdvisorLogsMsg,
                        context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the cAdvisor logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info("Getting the cAdvisor logs")
        logs = []
        try:
            cmd = constants.COMMANDS.CADVISOR_LOGS
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output_bytes, err) = p.communicate()
            output_str = output_bytes.decode("utf-8")
            output = output_str.split("\n")[-100:]
            logs = output
        except Exception as e:
            logging.info(f"Exception reading cadvisor logs. Stacktrace: {str(e)}, {repr(e)}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=logs)

    def getNodeExporterLogs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetNodeExporterLogsMsg,
                            context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the node exporter logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info("Getting the Node exporter logs")
        config = Config.get_current_config()
        path = config.node_exporter_log_file
        logs = []
        try:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as fp:
                        data = ClusterManagerUtil.tail(fp, window=100).split("\n")
                        logs = data
                except Exception as e:
                    logging.info(f"Exception reading log file: {path}. Stacktrace: {str(e)}, {repr(e)}")
        except Exception as e:
            logging.info(f"Exception reading node exporter logs. Stacktrace: {str(e)}, {repr(e)}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=logs)

    def getPrometheusLogs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetPrometheusLogsMsg,
                          context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the Prometheus logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info("Getting the Prometheus logs")
        config = Config.get_current_config()
        path = config.prometheus_log_file
        logs = []
        try:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as fp:
                        data = ClusterManagerUtil.tail(fp, window=100).split("\n")
                        logs = data
                except Exception as e:
                    logging.info(f"Exception reading log file: {path}. Stacktrace: {str(e)}, {repr(e)}")
        except Exception as e:
            logging.info(f"Exception reading prometheus logs. Stacktrace: {str(e)}, {repr(e)}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=logs)

    def getDockerStatsManagerLogs(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetDockerStatsManagerLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the Docker statsmanager logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info("Getting the Docker statsmanager logs")
        config = Config.get_current_config()
        path = config.docker_stats_manager_log_dir + config.docker_stats_manager_log_file
        logs = []
        try:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as fp:
                        data = ClusterManagerUtil.tail(fp, window=100).split("\n")
                        logs = data
                except Exception as e:
                    logging.info(f"Exception reading log file: {path}. Stacktrace: {str(e)}, {repr(e)}")
        except Exception as e:
            logging.info(f"Exception reading docker statsmanager logs. Stacktrace: {str(e)}, {repr(e)}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=logs)

    def getCsleLogFiles(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetCsleLogFilesMsg,
                        context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the list of file names in the CSLE log directory

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info("Getting the CSLE log file names")
        config = Config.get_current_config()
        path = config.default_log_dir
        log_files = []
        try:
            for f in os.listdir(path):
                item = os.path.join(path, f)
                if os.path.isfile(item):
                    log_files.append(item)
            if len(log_files) > 20:
                log_files = log_files[0:20]
        except Exception as e:
            logging.info(f"Exception reading csle log files. Stacktrace: {str(e)}, {repr(e)}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=log_files)

    def startContainersInExecution(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartContainersInExecutionMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the containers of a given emulation execution that are configured to be deployed on this host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting containers in execution with ID: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        EmulationEnvController.run_containers(emulation_execution=execution,
                                              physical_host_ip=GeneralUtil.get_host_ip(), logger=logging.getLogger())
        MetastoreFacade.update_emulation_execution(emulation_execution=execution,
                                                   ip_first_octet=execution.ip_first_octet,
                                                   emulation=execution.emulation_name)
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def attachContainersInExecutionToNetworks(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartContainersInExecutionMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Attaches the containers of a given emulation execution that are configured to be deployed on this host to
        their corresponding virtual overlay networks

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Attaching containers in execution with ID: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation} to networks")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        ContainerController.connect_containers_to_networks(emulation_env_config=execution.emulation_env_config,
                                                           physical_server_ip=GeneralUtil.get_host_ip(),
                                                           logger=logging.getLogger())
        MetastoreFacade.update_emulation_execution(emulation_execution=execution,
                                                   ip_first_octet=execution.ip_first_octet,
                                                   emulation=execution.emulation_name)
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def installLibraries(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.InstallLibrariesMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Installs CSLE libraries on containers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Install CSLE libraries on containers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        EmulationEnvController.install_csle_collector_and_ryu_libraries(
            emulation_env_config=execution.emulation_env_config, physical_server_ip=GeneralUtil.get_host_ip(),
            logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def applyKafkaConfig(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ApplyKafkaConfigMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Applies the Kafka configuration to an execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Applies the Kafka configuration on containers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        EmulationEnvController.apply_kafka_config(emulation_env_config=execution.emulation_env_config,
                                                  physical_server_ip=GeneralUtil.get_host_ip(),
                                                  logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startSdnController(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartSdnControllerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Ryu SDN controller of an execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the Ryu SDN controller in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        SDNControllerManager.start_ryu(emulation_env_config=execution.emulation_env_config,
                                       physical_server_ip=GeneralUtil.get_host_ip(),
                                       logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def applyResourceConstraints(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ApplyResouceConstraintsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Applies resource constraints to containers in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Applies resource constraints to containers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        ResourceConstraintsController.apply_resource_constraints(emulation_env_config=execution.emulation_env_config,
                                                                 physical_server_ip=GeneralUtil.get_host_ip(),
                                                                 logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def createOvsSwitches(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.CreateOvsSwitchesMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Creates OVS switches in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Creating OVS switches in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        OVSController.create_virtual_switches_on_container(
            containers_config=execution.emulation_env_config.containers_config,
            physical_server_ip=GeneralUtil.get_host_ip(), logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def pingExecution(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.PingExecutionMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Pings all containers in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Pinging containers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        EmulationEnvController.ping_all(emulation_env_config=execution.emulation_env_config,
                                        physical_server_ip=GeneralUtil.get_host_ip(),
                                        logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def configureOvs(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ConfigureOvsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Configures OVS switches in an execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Configuring OVS switches in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        logging.info(f"Found execution with id: {request.ipFirstOctet}, applying the configuration")
        OVSController.apply_ovs_config(emulation_env_config=execution.emulation_env_config,
                                       physical_server_ip=GeneralUtil.get_host_ip(), logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startSdnControllerMonitor(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartSdnControllerMonitorMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the SDN controller monitor in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starts the SDN controller monitor in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        SDNControllerManager.start_ryu_monitor(emulation_env_config=execution.emulation_env_config,
                                               physical_server_ip=GeneralUtil.get_host_ip(),
                                               logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def createUsers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.CreateUsersMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Creates users in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Creates users in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        UsersController.create_users(emulation_env_config=execution.emulation_env_config,
                                     physical_server_ip=GeneralUtil.get_host_ip(),
                                     logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def createVulnerabilities(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.CreateVulnsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Creates vulnerabilities in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Creates vulnerabilities in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        VulnerabilitiesController.create_vulns(emulation_env_config=execution.emulation_env_config,
                                               physical_server_ip=GeneralUtil.get_host_ip(),
                                               logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def createFlags(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.CreateFlagsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Creates flags in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Creates flags in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        FlagsController.create_flags(emulation_env_config=execution.emulation_env_config,
                                     physical_server_ip=GeneralUtil.get_host_ip(),
                                     logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def createTopology(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.CreateTopologyMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Configures the topology of a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Configures the topology in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        TopologyController.create_topology(emulation_env_config=execution.emulation_env_config,
                                           physical_server_ip=GeneralUtil.get_host_ip(),
                                           logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startTrafficManagers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartTrafficManagersMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts traffic managers in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starts traffic managers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        TrafficController.start_traffic_managers(emulation_env_config=execution.emulation_env_config,
                                                 physical_server_ip=GeneralUtil.get_host_ip(),
                                                 logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startTrafficGenerators(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartTrafficGeneratorsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts traffic generators in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starts traffic generators in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        TrafficController.start_internal_traffic_generators(emulation_env_config=execution.emulation_env_config,
                                                            physical_server_ip=GeneralUtil.get_host_ip(),
                                                            logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startClientPopulation(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartClientPopulationMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the client population of a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the client population in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        TrafficController.start_client_population(emulation_env_config=execution.emulation_env_config,
                                                  physical_server_ip=GeneralUtil.get_host_ip(),
                                                  logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startKafkaClientProducer(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartKafkaClientProducerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Kafka client producer of a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starts the Kafka client producer in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        TrafficController.start_client_producer(emulation_env_config=execution.emulation_env_config,
                                                physical_server_ip=GeneralUtil.get_host_ip(),
                                                logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopKafkaClientProducer(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopKafkaClientProducerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Kafka client producer of a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the Kafka client producer in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        TrafficController.stop_client_producer(emulation_env_config=execution.emulation_env_config,
                                               physical_server_ip=GeneralUtil.get_host_ip(),
                                               logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startSnortIdses(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartSnortIdsesMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Snort IDSes in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starts the Snort IDSes in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        SnortIDSController.start_snort_idses(emulation_env_config=execution.emulation_env_config,
                                             physical_server_ip=GeneralUtil.get_host_ip(),
                                             logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startSnortIdsesMonitorThreads(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartSnortIdsesMonitorThreadsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Snort IDSes monitor threads in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starts the Snort IDSes monitor threads in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        SnortIDSController.start_snort_idses_monitor_threads(emulation_env_config=execution.emulation_env_config,
                                                             physical_server_ip=GeneralUtil.get_host_ip(),
                                                             logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startOssecIdses(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartOSSECIdsesMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the OSSEC IDSes in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starts the OSSEC IDSes in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        OSSECIDSController.start_ossec_idses(emulation_env_config=execution.emulation_env_config,
                                             physical_server_ip=GeneralUtil.get_host_ip(),
                                             logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startOssecIdsesMonitorThreads(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartOSSECIdsesMonitorThreadsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the OSSEC IDSes monitor threads in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starts the OSSEC IDSes monitor threads in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        OSSECIDSController.start_ossec_idses_monitor_threads(emulation_env_config=execution.emulation_env_config,
                                                             physical_server_ip=GeneralUtil.get_host_ip(),
                                                             logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startElkStack(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartElkStackMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the ELK stack in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starts the ELK stack in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        ELKController.start_elk_stack(emulation_env_config=execution.emulation_env_config,
                                      physical_server_ip=GeneralUtil.get_host_ip(),
                                      logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startHostManagers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartHostManagersMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the host managers of a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starts the host managers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.start_host_monitor_threads(emulation_env_config=execution.emulation_env_config,
                                                  physical_server_ip=GeneralUtil.get_host_ip(),
                                                  logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def applyFileBeatsConfig(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ApplyFileBeatConfigsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Applies the filebeat configurations to a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Applies filebeat configurations to containers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.config_filebeats(emulation_env_config=execution.emulation_env_config,
                                        physical_server_ip=GeneralUtil.get_host_ip(),
                                        logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def applyPacketBeatsConfig(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ApplyPacketBeatConfigsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Applies the packetbeat configurations to a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Applies the packetbeat configurations in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.config_packetbeats(emulation_env_config=execution.emulation_env_config,
                                          physical_server_ip=GeneralUtil.get_host_ip(),
                                          logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def applyMetricBeatsConfig(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ApplyMetricBeatConfigsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Applies the metricbeat configurations to a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Applies the metricbeat configurations in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.config_metricbeats(emulation_env_config=execution.emulation_env_config,
                                          physical_server_ip=GeneralUtil.get_host_ip(),
                                          logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def applyHeartBeatsConfig(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ApplyHeartBeatConfigsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Applies the heartbeat configurations to a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Applies the heartbeat configurations in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.config_heartbeats(emulation_env_config=execution.emulation_env_config,
                                         physical_server_ip=GeneralUtil.get_host_ip(),
                                         logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startFilebeats(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartFileBeatsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts filebeats in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting filebeats in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.start_filebeats(emulation_env_config=execution.emulation_env_config,
                                       initial_start=request.initialStart,
                                       physical_server_ip=GeneralUtil.get_host_ip(),
                                       logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startPacketbeats(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartPacketBeatsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts packetbetas in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting packetbeats in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.start_packetbeats(emulation_env_config=execution.emulation_env_config,
                                         initial_start=request.initialStart,
                                         physical_server_ip=GeneralUtil.get_host_ip(),
                                         logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startMetricbeats(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartMetricBeatsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts metricbeats in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting metricbeats in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.start_metricbeats(emulation_env_config=execution.emulation_env_config,
                                         initial_start=request.initialStart,
                                         physical_server_ip=GeneralUtil.get_host_ip(),
                                         logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startHeartbeats(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartHeartBeatsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts heartbeats in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting heartbeats in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.start_heartbeats(emulation_env_config=execution.emulation_env_config,
                                        initial_start=request.initialStart,
                                        physical_server_ip=GeneralUtil.get_host_ip(),
                                        logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startDockerStatsManagerThread(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartDockerStatsManagerThreadMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts the docker stats manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting docker stats manager thread for execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=False)
        ContainerController.start_docker_stats_thread(execution=execution,
                                                      physical_server_ip=GeneralUtil.get_host_ip(),
                                                      logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=True)

    def stopAllExecutionsOfEmulation(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopAllExecutionsOfEmulationMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops all executions of a given emulation

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping executions of emulation: {request.emulation}")
        emulation = MetastoreFacade.get_emulation_by_name(name=request.emulation)
        if emulation is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        EmulationEnvController.stop_all_executions_of_emulation(emulation_env_config=emulation,
                                                                physical_server_ip=GeneralUtil.get_host_ip(),
                                                                logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopExecution(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopExecutionMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        EmulationEnvController.stop_execution_of_emulation(emulation_env_config=execution.emulation_env_config,
                                                           physical_server_ip=GeneralUtil.get_host_ip(),
                                                           execution_id=execution.ip_first_octet,
                                                           logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopAllExecutions(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopAllExecutionsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops all executions

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info("Stopping all executions")
        EmulationEnvController.stop_all_executions(physical_server_ip=GeneralUtil.get_host_ip(),
                                                   logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def cleanAllExecutions(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.CleanAllExecutionsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Cleans all executions

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info("Cleaning all executions")
        config = MetastoreFacade.get_config(id=1)
        leader = ClusterUtil.am_i_leader(ip=GeneralUtil.get_host_ip(), config=config)
        EmulationEnvController.clean_all_executions(physical_server_ip=GeneralUtil.get_host_ip(),
                                                    logger=logging.getLogger(), leader=leader)
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def cleanAllExecutionsOfEmulation(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.CleanAllExecutionsOfEmulationMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Cleans all executions of a given emulation

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Cleaning executions of emulation: {request.emulation}")
        emulation = MetastoreFacade.get_emulation_by_name(name=request.emulation)
        if emulation is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        config = MetastoreFacade.get_config(id=1)
        leader = ClusterUtil.am_i_leader(ip=GeneralUtil.get_host_ip(), config=config)
        EmulationEnvController.clean_all_emulation_executions(emulation_env_config=emulation,
                                                              physical_server_ip=GeneralUtil.get_host_ip(),
                                                              logger=logging.getLogger(), leader=leader)
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def cleanExecution(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.CleanExecutionMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Cleans a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Cleaning execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        config = MetastoreFacade.get_config(id=1)
        leader = ClusterUtil.am_i_leader(ip=GeneralUtil.get_host_ip(), config=config)
        EmulationEnvController.clean_emulation_execution(emulation_env_config=execution.emulation_env_config,
                                                         physical_server_ip=GeneralUtil.get_host_ip(),
                                                         execution_id=execution.ip_first_octet,
                                                         logger=logging.getLogger(), leader=leader)
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startTrafficManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartTrafficManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts a specific traffic manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting traffic manager with ip: {request.containerIp} "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        node_traffic_config = execution.emulation_env_config.traffic_config.get_node_traffic_config_by_ip(
            ip=request.containerIp)
        if node_traffic_config is not None and node_traffic_config.physical_host_ip == GeneralUtil.get_host_ip():
            TrafficController.start_traffic_manager(emulation_env_config=execution.emulation_env_config,
                                                    node_traffic_config=node_traffic_config,
                                                    logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopTrafficManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopTrafficManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops a specific traffic manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping traffic manager with ip: {request.containerIp} "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        node_traffic_config = execution.emulation_env_config.traffic_config.get_node_traffic_config_by_ip(
            ip=request.containerIp)
        if node_traffic_config is not None and node_traffic_config.physical_host_ip == GeneralUtil.get_host_ip():
            TrafficController.stop_traffic_manager(emulation_env_config=execution.emulation_env_config,
                                                   node_traffic_config=node_traffic_config,
                                                   logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopTrafficManagers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopTrafficManagersMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops traffic managers in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stops traffic managers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        TrafficController.stop_traffic_managers(emulation_env_config=execution.emulation_env_config,
                                                physical_server_ip=GeneralUtil.get_host_ip(),
                                                logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startClientManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartClientManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the client manager of a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starts the client manager in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        if execution.emulation_env_config.traffic_config.client_population_config.physical_host_ip \
                == GeneralUtil.get_host_ip():
            TrafficController.start_client_manager(emulation_env_config=execution.emulation_env_config,
                                                   logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopClientManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopClientManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the client manager of a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stops the client manager in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        if execution.emulation_env_config.traffic_config.client_population_config.physical_host_ip \
                == GeneralUtil.get_host_ip():
            TrafficController.stop_client_manager(emulation_env_config=execution.emulation_env_config,
                                                  logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopClientPopulation(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopClientPopulationMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the client population of a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stops the client population in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        if execution.emulation_env_config.traffic_config.client_population_config.physical_host_ip \
                == GeneralUtil.get_host_ip():
            TrafficController.stop_client_population(emulation_env_config=execution.emulation_env_config,
                                                     logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def getNumActiveClients(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetNumActiveClientsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.GetNumClientsDTO:
        """
        Gets the number of active clients of a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a GetNumActiveClientsMsg
        """
        logging.info(f"Getting the number of active clients in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None \
                and execution.emulation_env_config.traffic_config.client_population_config.physical_host_ip == \
                GeneralUtil.get_host_ip():
            clients_dto = TrafficController.get_num_active_clients(emulation_env_config=execution.emulation_env_config,
                                                                   logger=logging.getLogger())
            return ClusterManagerUtil.convert_client_dto_to_get_num_clients_dto(clients_dto=clients_dto)
        else:

            return ClusterManagerUtil.get_empty_get_num_clients_dto()

    def stopTrafficGenerators(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopTrafficGeneratorsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops traffic generators in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stops traffic generators in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        TrafficController.stop_internal_traffic_generators(emulation_env_config=execution.emulation_env_config,
                                                           physical_server_ip=GeneralUtil.get_host_ip(),
                                                           logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startTrafficGenerator(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartTrafficGeneratorMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts a specific traffic generator

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting traffic generator with ip: {request.containerIp} "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        node_traffic_config = execution.emulation_env_config.traffic_config.get_node_traffic_config_by_ip(
            ip=request.containerIp)
        node_container_config = execution.emulation_env_config.containers_config.get_container_from_ip(
            ip=request.containerIp)
        if node_traffic_config is not None and node_traffic_config.physical_host_ip == GeneralUtil.get_host_ip():
            TrafficController.start_internal_traffic_generator(emulation_env_config=execution.emulation_env_config,
                                                               node_traffic_config=node_traffic_config,
                                                               logger=logging.getLogger(),
                                                               container=node_container_config)
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopTrafficGenerator(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopTrafficGeneratorMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops a specific traffic generator

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping traffic generator with ip: {request.containerIp} "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        node_traffic_config = execution.emulation_env_config.traffic_config.get_node_traffic_config_by_ip(
            ip=request.containerIp)
        if node_traffic_config is not None and node_traffic_config.physical_host_ip == GeneralUtil.get_host_ip():
            TrafficController.stop_internal_traffic_generator(emulation_env_config=execution.emulation_env_config,
                                                              node_traffic_config=node_traffic_config,
                                                              logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def getClientManagersInfo(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetClientManagersInfoMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.ClientManagersInfoDTO:
        """
        Gets the info of client managers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a ClientManagersInfoDTO
        """
        logging.info(f"Getting the info of client managers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.traffic_config.client_population_config.physical_host_ip \
                == GeneralUtil.get_host_ip():

            client_managers_dto = TrafficController.get_client_managers_info(
                emulation_env_config=execution.emulation_env_config, logger=logging.getLogger(),
                active_ips=ClusterManagerUtil.get_active_ips(emulation_env_config=execution.emulation_env_config))

            return ClusterManagerUtil.convert_client_info_dto(client_managers_dto=client_managers_dto)
        else:
            return ClusterManagerUtil.get_empty_client_managers_info_dto()

    def getTrafficManagersInfo(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetTrafficManagersInfoMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.TrafficManagersInfoDTO:
        """
        Gets the info of traffic managers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a TrafficManagersInfoDTO
        """
        logging.info(f"Getting the info of traffic managers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None:
            traffic_managers_dto = TrafficController.get_traffic_managers_info(
                emulation_env_config=execution.emulation_env_config, logger=logging.getLogger(),
                active_ips=ClusterManagerUtil.get_active_ips(emulation_env_config=execution.emulation_env_config),
                physical_host_ip=GeneralUtil.get_host_ip()
            )
            return ClusterManagerUtil.convert_traffic_info_dto(traffic_managers_dto=traffic_managers_dto)
        else:
            return ClusterManagerUtil.get_empty_traffic_managers_info_dto()

    def stopAllRunningContainers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopAllRunningContainersMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops all running CSLE containers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info("Stopping all running CSLE containers")
        ContainerController.stop_all_running_containers()
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopContainer(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopContainerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops a specific container

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        outcome = ContainerController.stop_container(name=request.name)
        if outcome:
            logging.info(f"Stopping container: {request.name}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=outcome)

    def removeAllStoppedContainers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.RemoveAllStoppedContainersMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Removes all stopped containers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info("Removing all stopped containers")
        ContainerController.rm_all_stopped_containers()
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def removeContainer(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.RemoveContainerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Removes all specific container

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        outcome = ContainerController.rm_container(container_name=request.name)
        if outcome:
            logging.info(f"Removing container: {request.name}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=outcome)

    def removeAllContainerImages(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.RemoveAllContainerImagesMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Removes all CSLE container images

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info("Removing all container images")
        ContainerController.rm_all_images()
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def removeContainerImage(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.RemoveContainerImageMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Removes a specific container image

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        outcome = ContainerController.rm_image(name=request.name)
        if outcome:
            logging.info(f"Removing container image: {request.name}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=outcome)

    def listAllContainerImages(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ListAllContainerImagesMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.ContainerImagesDTO:
        """
        Removes a specific container image

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a ContainerImagesDTO
        """
        logging.info("Listing all container images")
        imgs_infos = ContainerController.list_all_images()
        images = []
        for img_info in imgs_infos:
            images.append(
                csle_cluster.cluster_manager.cluster_manager_pb2.ContainerImageDTO(
                    repoTags=img_info[0], created=img_info[1], os=img_info[2],
                    architecture=img_info[3], size=img_info[4]
                )
            )
        return csle_cluster.cluster_manager.cluster_manager_pb2.ContainerImagesDTO(images=images)

    def listAllDockerNetworks(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ListAllDockerNetworksMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.DockerNetworksDTO:
        """
        Lists all docker networks

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DockerNetworksDTO
        """
        logging.info("Listing all docker networks")
        networks, network_ids = ContainerController.list_docker_networks()
        return csle_cluster.cluster_manager.cluster_manager_pb2.DockerNetworksDTO(
            networks=networks, network_ids=network_ids)

    def startAllStoppedContainers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartAllStoppedContainersMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts all stopped containers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info("Starting all stopped CSLE containers")
        ContainerController.start_all_stopped_containers()
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startContainer(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartContainerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts a specific container

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        outcome = ContainerController.start_container(name=request.name)
        if outcome:
            logging.info(f"Starting the container: {request.name}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=outcome)

    def listAllRunningContainers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ListAllRunningContainersMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.RunningContainersDTO:
        """
        Lists all running containers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a RunningContainersDTO
        """
        logging.info("Listing all running containers")
        running_container_infos = ContainerController.list_all_running_containers()
        running_containers = []
        for rci in running_container_infos:
            running_containers.append(csle_cluster.cluster_manager.cluster_manager_pb2.DockerContainerDTO(
                name=rci[0], image=rci[1], ip=rci[2]))
        return csle_cluster.cluster_manager.cluster_manager_pb2.RunningContainersDTO(
            runningContainers=running_containers)

    def listAllRunningEmulations(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ListAllRunningEmulationsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.RunningEmulationsDTO:
        """
        Lists all running emulations

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a RunningEmulationsDTO
        """
        logging.info("Listing all running emulations")
        running_emulations = ContainerController.list_running_emulations()
        return csle_cluster.cluster_manager.cluster_manager_pb2.RunningEmulationsDTO(
            runningEmulations=running_emulations)

    def listAllStoppedContainers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ListAllStoppedContainersMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.StoppedContainersDTO:
        """
        Lists all stopped containers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a StoppedContainersDTOb
        """
        logging.info("Listing all stopped containers")
        stopped_container_infos = ContainerController.list_all_stopped_containers()
        stopped_containers = []
        for rci in stopped_container_infos:
            stopped_containers.append(csle_cluster.cluster_manager.cluster_manager_pb2.DockerContainerDTO(
                name=rci[0], image=rci[1], ip=rci[2]))
        return csle_cluster.cluster_manager.cluster_manager_pb2.StoppedContainersDTO(
            stoppedContainers=stopped_containers)

    def createEmulationNetworks(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.CreateEmulationNetworksMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Creates networks for a given emulation execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Creating networks for emulation: {request.emulation} and execution id:{request.ipFirstOctet}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        config = MetastoreFacade.get_config(id=1)
        leader = ClusterUtil.am_i_leader(ip=GeneralUtil.get_host_ip(), config=config)
        if execution is None or not leader:
            logging.info("Not leader, skipping creating networks")
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        ContainerController.create_networks(containers_config=execution.emulation_env_config.containers_config,
                                            logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopDockerStatsManagerThread(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopDockerStatsManagerThreadMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the docker stats manager thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the docker stats manager thread for execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        ContainerController.stop_docker_stats_thread(execution=execution,
                                                     physical_server_ip=GeneralUtil.get_host_ip(),
                                                     logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def getDockerStatsManagerStatus(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetDockerStatsManagerStatusMsg,
            context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.DockerStatsMonitorStatusDTO:
        """
        Gets the docker stats manager status

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DockerStatsMonitorStatusDTO
        """
        logging.info(f"Getting the docker stats manager status by sending a request on port: {request.port}")
        docker_stats_monitor_dto = ContainerController.get_docker_stats_manager_status_by_ip_and_port(
            ip=GeneralUtil.get_host_ip(), port=request.port)
        dto = ClusterManagerUtil.convert_docker_stats_monitor_dto(monitor_dto=docker_stats_monitor_dto)
        return dto

    def removeDockerNetworks(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.RemoveDockerNetworksMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Removes a list of docker networks

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        outcome = ContainerController.remove_networks(names=request.networks, logger=logging.getLogger())
        if outcome:
            logging.info(f"Removing docker networks: {list(request.networks)}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=outcome)

    def removeAllDockerNetworks(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.RemoveAllDockerNetworksMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Removes all docker networks related to CSLE

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info("Removing all docker networks")
        ContainerController.rm_all_networks(logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def getDockerStatsManagersInfo(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetDockerStatsManagersInfoMsg,
            context: grpc.ServicerContext) -> \
            csle_cluster.cluster_manager.cluster_manager_pb2.DockerStatsManagersInfoDTO:
        """
        Gets the info of docker stats maangers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DockerStatsManagersInfoDTO
        """
        logging.info(f"Getting the info of docker stats managers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None:
            docker_stats_managers_dto = ContainerController.get_docker_stats_managers_info(
                emulation_env_config=execution.emulation_env_config, logger=logging.getLogger(),
                active_ips=ClusterManagerUtil.get_active_ips(emulation_env_config=execution.emulation_env_config),
                physical_host_ip=GeneralUtil.get_host_ip()
            )
            return ClusterManagerUtil.convert_docker_info_dto(docker_stats_managers_dto=docker_stats_managers_dto)
        else:
            return ClusterManagerUtil.get_empty_docker_managers_info_dto()

    def stopElkManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopElkManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops a specific elk manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping elk manager "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.elk_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            ELKController.stop_elk_manager(emulation_env_config=execution.emulation_env_config,
                                           logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startElkManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartElkManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts a specific elk manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting elk manager "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.elk_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            ELKController.start_elk_manager(emulation_env_config=execution.emulation_env_config,
                                            logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def getElkStatus(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetElkStackStatusMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.ElkStatusDTO:
        """
        Gets the status of the Elk stack  for a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkStatusDTO
        """
        logging.info(f"Getting the status of the elk stack "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.elk_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            elk_dto = ELKController.get_elk_status(emulation_env_config=execution.emulation_env_config,
                                                   logger=logging.getLogger())
            return ClusterManagerUtil.convert_elk_dto(elk_dto=elk_dto)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.ElkStatusDTO(
                kibanaRunning=False, elasticRunning=False, logstashRunning=False)

    def stopElkStack(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopElkStackMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the elk stack of a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the ELK stack "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.elk_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            ELKController.stop_elk_stack(emulation_env_config=execution.emulation_env_config,
                                         logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startElastic(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartElasticServiceMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts elastic in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting elastic "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.elk_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            ELKController.start_elastic(emulation_env_config=execution.emulation_env_config,
                                        logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopElastic(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopElasticServiceMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops elastic in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping elastic "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.elk_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            ELKController.stop_elastic(emulation_env_config=execution.emulation_env_config,
                                       logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startKibana(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartKibanaServiceMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts Kibana in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting KIbana "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.elk_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            ELKController.start_kibana(emulation_env_config=execution.emulation_env_config,
                                       logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopKibana(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopKibanaServiceMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops Kibana in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping Kibana "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.elk_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            ELKController.stop_kibana(emulation_env_config=execution.emulation_env_config,
                                      logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startLogstash(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartLogstashServiceMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts Logstash in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting logstash "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.elk_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            ELKController.start_logstash(emulation_env_config=execution.emulation_env_config,
                                         logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopLogstash(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopLogstashServiceMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops Logstash in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stops logstash "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.elk_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            ELKController.stop_logstash(emulation_env_config=execution.emulation_env_config,
                                        logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def getElkManagersInfo(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetElkManagersInfoMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.ElkManagersInfoDTO:
        """
        Gets the info of elk managers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a ElkManagersInfoDTO
        """
        logging.info(f"Getting the info of elk managers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None:
            elk_managers_dto = ELKController.get_elk_managers_info(
                emulation_env_config=execution.emulation_env_config, logger=logging.getLogger(),
                active_ips=ClusterManagerUtil.get_active_ips(emulation_env_config=execution.emulation_env_config),
                physical_host_ip=GeneralUtil.get_host_ip())
            return ClusterManagerUtil.convert_elk_info_dto(elk_managers_dto=elk_managers_dto)
        else:
            return ClusterManagerUtil.get_empty_elk_managers_info_dto()

    def startContainersOfExecution(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartContainersOfExecutionMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the containers of a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starts containers "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        EmulationEnvController.start_containers_of_execution(emulation_execution=execution,
                                                             physical_host_ip=GeneralUtil.get_host_ip())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def runContainer(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.RunContainerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Runs a specific container

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Running container with image: {request.image}, name: {request.name}, memory: {request.memory},"
                     f"num_cpus: {request.num_cpus}, create_network: {request.create_network}, version"
                     f": {request.version} ")
        EmulationEnvController.run_container(image=request.image, name=request.name, memory=request.memory,
                                             num_cpus=request.num_cpus, create_network=request.create_network,
                                             version=request.version, logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopContainersOfExecution(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopContainersOfExecutionMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the containers of a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stops containers "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        EmulationEnvController.start_containers_of_execution(emulation_execution=execution,
                                                             physical_host_ip=GeneralUtil.get_host_ip())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startHostManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartHostManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts a specific host manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting host manager with ip: {request.containerIp} in  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            HostController.start_host_manager(emulation_env_config=execution.emulation_env_config,
                                              ip=container_config.docker_gw_bridge_ip, logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            logging.info(f"Container with ip: {request.containerIp} not found in execution "
                         f"with id: {request.ipFirstOctet} of emulation {request.emulation}")
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopHostManagers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopHostManagersMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the host managers of a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping host managers in  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.stop_host_managers(emulation_env_config=execution.emulation_env_config,
                                          physical_host_ip=GeneralUtil.get_host_ip())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopHostManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopHostManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops a specific host manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping host manager with ip: {request.containerIp} in  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            HostController.stop_host_manager(emulation_env_config=execution.emulation_env_config,
                                             ip=container_config.docker_gw_bridge_ip)
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startHostMonitorThreads(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartHostMonitorThreadsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the host monitor threads of a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting host monitor threads  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.start_host_monitor_threads(emulation_env_config=execution.emulation_env_config,
                                                  physical_server_ip=GeneralUtil.get_host_ip(),
                                                  logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopFilebeats(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopFilebeatsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops filebeats in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping filebeats  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.stop_filebeats(emulation_env_config=execution.emulation_env_config,
                                      physical_server_ip=GeneralUtil.get_host_ip(),
                                      logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopPacketbeats(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopPacketbeatsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops packetbeats in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping packetbeats  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.stop_packetbeats(emulation_env_config=execution.emulation_env_config,
                                        physical_server_ip=GeneralUtil.get_host_ip(),
                                        logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopMetricbeats(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopMetricbeatsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops Metricbeats in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping metricbeats  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.stop_metricbeats(emulation_env_config=execution.emulation_env_config,
                                        physical_server_ip=GeneralUtil.get_host_ip(),
                                        logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopHeartbeats(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopHeartbeatsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops Heartbeats in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping heartbeats  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.stop_heartbeats(emulation_env_config=execution.emulation_env_config,
                                       physical_server_ip=GeneralUtil.get_host_ip(),
                                       logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startHostMonitorThread(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartHostMonitorThreadMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts a specific host monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting host monitor thread on container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            HostController.start_host_monitor_thread(emulation_env_config=execution.emulation_env_config,
                                                     ip=container_config.docker_gw_bridge_ip,
                                                     logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startFilebeat(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartFileBeatMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts filebeat on a specific host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting filebeat on container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}, "
                     f"initial start: {request.initialStart}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            HostController.start_filebeat(emulation_env_config=execution.emulation_env_config,
                                          ips=[container_config.docker_gw_bridge_ip],
                                          logger=logging.getLogger(), initial_start=request.initialStart)
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startPacketbeat(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartPacketBeatMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts packetbeat on a specific host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting packetbeat on container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}, "
                     f"initialStart: {request.initialStart}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            HostController.start_packetbeat(emulation_env_config=execution.emulation_env_config,
                                            ips=[container_config.docker_gw_bridge_ip], logger=logging.getLogger(),
                                            initial_start=request.initialStart)
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startMetricbeat(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartMetricBeatMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts metricbeat on a specific host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting metricbeat on container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}, "
                     f"initialStart: {request.initialStart}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            HostController.start_metricbeat(emulation_env_config=execution.emulation_env_config,
                                            ips=[container_config.docker_gw_bridge_ip],
                                            logger=logging.getLogger(), initial_start=request.initialStart)
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startHeartbeat(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartHeartBeatMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts heartbeat on a specific host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting heartbeat on container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}, "
                     f"initialStart: {request.initialStart}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            HostController.start_heartbeat(emulation_env_config=execution.emulation_env_config,
                                           ips=[container_config.docker_gw_bridge_ip], logger=logging.getLogger(),
                                           initial_start=request.initialStart)
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopFilebeat(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopFileBeatMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops filebeat on a specific host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping filebeat on container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            HostController.stop_filebeat(emulation_env_config=execution.emulation_env_config,
                                         ip=container_config.docker_gw_bridge_ip, logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopPacketbeat(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopPacketBeatMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops packetbeat on a specific host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping packetbeat on container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            HostController.stop_packetbeat(emulation_env_config=execution.emulation_env_config,
                                           ip=container_config.docker_gw_bridge_ip, logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopMetricbeat(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopMetricBeatMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops metricbeat on a specific host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping metricbeat on container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            HostController.stop_metricbeat(emulation_env_config=execution.emulation_env_config,
                                           ip=container_config.docker_gw_bridge_ip, logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopHeartbeat(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopHeartBeatMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops heartbeat on a specific host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping heartbeat on container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            HostController.stop_heartbeat(emulation_env_config=execution.emulation_env_config,
                                          ip=container_config.docker_gw_bridge_ip, logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def applyFileBeatConfig(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ApplyFileBeatConfigMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Applies the filebeat config on a specific host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Applying the filebeat config to container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            HostController.config_filebeat(emulation_env_config=execution.emulation_env_config,
                                           container=container_config,
                                           logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def applyPacketBeatConfig(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ApplyPacketBeatConfigMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Applies the packetbeat config on a specific host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Applying the packetbeat config to container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            HostController.config_packetbeat(emulation_env_config=execution.emulation_env_config,
                                             container=container_config, logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def applyMetricBeatConfig(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ApplyMetricBeatConfigMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Applies the metricbeat config on a specific host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Applying the metricbeat config to container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None and container_config.physical_host_ip == GeneralUtil.get_host_ip():
            HostController.config_metricbeat(emulation_env_config=execution.emulation_env_config,
                                             container=container_config, logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def applyHeartBeatConfig(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ApplyHeartBeatConfigMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Applies the heartbeat config on a specific host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Applying the heartbeat config to container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None and container_config.physical_host_ip == GeneralUtil.get_host_ip():
            HostController.config_heartbeat(emulation_env_config=execution.emulation_env_config,
                                            container=container_config, logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def getHostMonitorThreadsStatuses(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetHostMonitorThreadsStatusesMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.HostManagerStatusesDTO:
        """
        Gets the host monitor thread statuses of a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a HostManagerStatusesDTO
        """
        logging.info(f"Getting the host monitor thread statuses "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None:
            host_statuses = \
                HostController.get_host_monitor_threads_statuses(emulation_env_config=execution.emulation_env_config,
                                                                 physical_server_ip=GeneralUtil.get_host_ip(),
                                                                 logger=logging.getLogger())
            host_manager_statuses = list(
                map(lambda x: ClusterManagerUtil.convert_host_status_to_host_manager_status_dto(x), host_statuses))
            return csle_cluster.cluster_manager.cluster_manager_pb2.HostManagerStatusesDTO(
                hostManagerStatuses=host_manager_statuses)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.HostManagerStatusesDTO(
                hostManagerStatuses=[]
            )

    def getHostManagersInfo(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetHostManagersInfoMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.HostManagersInfoDTO:
        """
        Gets the info of host managers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a HostManagersInfoDTO
        """
        logging.info(f"Getting the info of host managers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None:
            host_managers_dto = HostController.get_host_managers_info(
                emulation_env_config=execution.emulation_env_config, logger=logging.getLogger(),
                active_ips=ClusterManagerUtil.get_active_ips(emulation_env_config=execution.emulation_env_config),
                physical_host_ip=GeneralUtil.get_host_ip()
            )
            return ClusterManagerUtil.convert_host_info_dto(host_managers_dto=host_managers_dto)
        else:
            return ClusterManagerUtil.get_empty_host_managers_info_dto()

    def stopKafkaManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopKafkaManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the kafka manager in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the kafka manager  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.kafka_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            KafkaController.stop_kafka_manager(emulation_env_config=execution.emulation_env_config)
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startKafkaManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartKafkaManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the kafka manager in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the kafka manager  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.kafka_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            KafkaController.start_kafka_manager(emulation_env_config=execution.emulation_env_config)
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def createKafkaTopics(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.CreateKafkaTopicsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Creates the kafka topics in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Creating Kafka topics  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.kafka_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            KafkaController.create_topics(emulation_env_config=execution.emulation_env_config,
                                          logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def getKafkaStatus(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetKafkaManagerStatusMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.KafkaStatusDTO:
        """
        Gets the Kafka status in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Getting the Kafka status  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.kafka_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            kafka_dto = KafkaController.get_kafka_status(emulation_env_config=execution.emulation_env_config)
            return ClusterManagerUtil.convert_kafka_dto_to_kafka_status_dto(kafka_dto=kafka_dto)
        else:
            return ClusterManagerUtil.get_empty_kafka_dto()

    def stopKafkaServer(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopKafkaServerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the kafka server in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping kafka server  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.kafka_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            KafkaController.stop_kafka_server(emulation_env_config=execution.emulation_env_config,
                                              logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startKafkaServer(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartKafkaServerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the kafka server in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting kafka server  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.kafka_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            KafkaController.start_kafka_server(emulation_env_config=execution.emulation_env_config,
                                               logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def getKafkaManagersInfo(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetKafkaManagersInfoMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.KafkaManagersInfoDTO:
        """
        Gets the info of kafka managers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a KafkaManagersInfoDTO
        """
        logging.info(f"Getting the info of kafka managers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None:
            kafka_managers_info_dto = KafkaController.get_kafka_managers_info(
                emulation_env_config=execution.emulation_env_config, logger=logging.getLogger(),
                active_ips=ClusterManagerUtil.get_active_ips(emulation_env_config=execution.emulation_env_config),
                physical_host_ip=GeneralUtil.get_host_ip())
            return ClusterManagerUtil.convert_kafka_info_dto(kafka_managers_info_dto=kafka_managers_info_dto)
        else:
            return ClusterManagerUtil.get_empty_kafka_managers_info_dto()

    def stopOSSECIDSes(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopOSSECIDSesMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stop the OSSEC IDSes in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the OSSEC IDSes  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None:
            OSSECIDSController.stop_ossec_idses(emulation_env_config=execution.emulation_env_config,
                                                physical_host_ip=GeneralUtil.get_host_ip())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startOSSECIDSes(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartOSSECIDSesMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starting the OSSEC IDSes in a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the OSSEC IDSes  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        OSSECIDSController.start_ossec_idses(emulation_env_config=execution.emulation_env_config,
                                             physical_server_ip=GeneralUtil.get_host_ip(),
                                             logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopOSSECIDS(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopOSSECIDSMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the OSSEC IDS on a specific host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stops the OSSEC IDS on the container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            OSSECIDSController.stop_ossec_ids(emulation_env_config=execution.emulation_env_config,
                                              ip=container_config.docker_gw_bridge_ip)
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startOSSECIDS(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartOSSECIDSMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the OSSEC IDS on a specific host

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starts the OSSEC IDS on the container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            OSSECIDSController.start_ossec_ids(emulation_env_config=execution.emulation_env_config,
                                               ip=container_config.docker_gw_bridge_ip)
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startOSSECIDSManagers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartOSSECIDSManagers,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the OSSEC IDS managers for a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the OSSEC IDS maangers "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        OSSECIDSController.start_ossec_idses_managers(emulation_env_config=execution.emulation_env_config,
                                                      physical_server_ip=GeneralUtil.get_host_ip())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopOSSECIDSManagers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopOSSECIDSManagers,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the OSSEC IDS managers for a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the OSSEC IDS managers "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        OSSECIDSController.stop_ossec_idses_managers(emulation_env_config=execution.emulation_env_config,
                                                     physical_server_ip=GeneralUtil.get_host_ip())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startOSSECIDSManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartOSSECIDSManager,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the OSSEC IDS manager on a specific node

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starts the OSSEC IDS manager on the container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            OSSECIDSController.start_ossec_ids_manager(emulation_env_config=execution.emulation_env_config,
                                                       ip=container_config.docker_gw_bridge_ip)
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopOSSECIDSManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopOSSECIDSManager,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the OSSEC IDS manager on a specific node

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the OSSEC IDS manager on the container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            OSSECIDSController.stop_ossec_ids_manager(emulation_env_config=execution.emulation_env_config,
                                                      ip=container_config.docker_gw_bridge_ip)
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startOSSECIDSMonitorThread(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartOSSECIDSMonitorThreadMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the OSSEC IDS monitor thread on a specific container

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the OSSEC IDS monitor thread on the container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            OSSECIDSController.start_ossec_ids_monitor_thread(emulation_env_config=execution.emulation_env_config,
                                                              ip=container_config.docker_gw_bridge_ip)
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopOSSECIDSMonitorThread(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopOSSECIDSMonitorThreadMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the OSSEC IDS monitor thread on a specific container

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the OSSEC IDS monitor thread on the container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            OSSECIDSController.stop_ossec_ids_monitor_thread(emulation_env_config=execution.emulation_env_config,
                                                             ip=container_config.docker_gw_bridge_ip)
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopOSSECIDSMonitorThreads(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopOSSECIDSMonitorThreadsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the OSSEC IDS monitor threads for a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the OSSEC IDS monitor threads "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        OSSECIDSController.stop_ossec_idses_monitor_threads(
            emulation_env_config=execution.emulation_env_config, physical_server_ip=GeneralUtil.get_host_ip())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def getOSSECIDSMonitorThreadStatuses(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetOSSECIDSMonitorThreadStatusesMsg,
            context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.OSSECIdsMonitorThreadStatusesDTO:
        """
        Gets the OSSEC IDS monitor thread statuses for a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OSSECIdsMonitorThreadStatusesDTO
        """
        logging.info(f"Getting the OSSEC IDS monitor thread statuses "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None:
            status_dtos = OSSECIDSController.get_ossec_idses_monitor_threads_statuses(
                emulation_env_config=execution.emulation_env_config, physical_server_ip=GeneralUtil.get_host_ip())
            status_dtos = list(
                map(lambda x: ClusterManagerUtil.convert_ossec_ids_monitor_dto_to_ossec_ids_status_dto(x),
                    status_dtos))
            return csle_cluster.cluster_manager.cluster_manager_pb2.OSSECIdsMonitorThreadStatusesDTO(
                ossecIDSStatuses=status_dtos
            )
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OSSECIdsMonitorThreadStatusesDTO(
                ossecIDSStatuses=[]
            )

    def getOSSECIdsManagersInfo(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetOSSECIDSManagersInfoMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OSSECIdsManagersInfoDTO:
        """
        Gets the info of OSSEC IDS managers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a OSSECIdsManagersInfoDTO
        """
        logging.info(f"Getting the info of OSSEC IDS managers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None:
            ossec_ids_managers_info_dto = OSSECIDSController.get_ossec_managers_info(
                emulation_env_config=execution.emulation_env_config, logger=logging.getLogger(),
                active_ips=ClusterManagerUtil.get_active_ips(emulation_env_config=execution.emulation_env_config),
                physical_host_ip=GeneralUtil.get_host_ip())
            return ClusterManagerUtil.convert_ossec_info_dto(ossec_ids_managers_info_dto=ossec_ids_managers_info_dto)
        else:
            return ClusterManagerUtil.get_empty_ossec_managers_info_dto()

    def startRyuManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartRyuManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Ryu manager for a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the Ryu manager "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        if execution.emulation_env_config.sdn_controller_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            SDNControllerManager.start_ryu_manager(emulation_env_config=execution.emulation_env_config,
                                                   logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopRyuManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopRyuManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Ryu manager for a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the Ryu manager "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        if execution.emulation_env_config.sdn_controller_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            SDNControllerManager.stop_ryu_manager(emulation_env_config=execution.emulation_env_config,
                                                  logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def getRyuStatus(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetRyuServiceStatusMsg,
            context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.RyuManagerStatusDTO:
        """
        Gets the Ryu status

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a RyuManagerStatusDTO
        """
        logging.info(f"Getting the Ryu status "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.sdn_controller_config.container.physical_host_ip == \
                GeneralUtil.get_host_ip():
            status_dto = SDNControllerManager.get_ryu_status(emulation_env_config=execution.emulation_env_config,
                                                             logger=logging.getLogger())
            return ClusterManagerUtil.convert_ryu_dto_to_ryu_status_dto(status_dto)
        else:
            return ClusterManagerUtil.get_empty_ryu_manager_status_dto()

    def startRyu(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartRyuServiceMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts Ryu

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting Ryu "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None and \
                execution.emulation_env_config.sdn_controller_config.container.physical_host_ip == \
                GeneralUtil.get_host_ip():
            SDNControllerManager.start_ryu(emulation_env_config=execution.emulation_env_config,
                                           physical_server_ip=GeneralUtil.get_host_ip(), logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopRyu(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopRyuServiceMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops Ryu

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping Ryu "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        if execution.emulation_env_config.sdn_controller_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            SDNControllerManager.stop_ryu(emulation_env_config=execution.emulation_env_config,
                                          logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def getRyuManagersInfo(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetRyuManagersInfoMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.RyuManagersInfoDTO:
        """
        Gets the info of Ryu managers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a RyuManagersInfoDTO
        """
        logging.info(f"Getting the info of Ryu managers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None:
            ryu_managers_info_dto = SDNControllerManager.get_ryu_managers_info(
                emulation_env_config=execution.emulation_env_config, logger=logging.getLogger(),
                active_ips=ClusterManagerUtil.get_active_ips(emulation_env_config=execution.emulation_env_config),
                physical_server_ip=GeneralUtil.get_host_ip())
            return ClusterManagerUtil.convert_ryu_info_dto(ryu_managers_info_dto=ryu_managers_info_dto)
        else:
            return ClusterManagerUtil.get_empty_ryu_managers_info_dto()

    def stopSnortIdses(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopSnortIdsesMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Snort IDSes for a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the Snort IDSes "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        SnortIDSController.stop_snort_idses(
            emulation_env_config=execution.emulation_env_config, physical_server_ip=GeneralUtil.get_host_ip(),
            logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def getSnortIdsMonitorThreadStatuses(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetSnortIdsMonitorThreadStatusesMsg,
            context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.SnortIdsMonitorThreadStatusesDTO:
        """
        Gets the Snort IDS monitor thread statuses for a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an SnortIdsMonitorThreadStatusesDTO
        """
        logging.info(f"Getting the Snort IDS monitor thread statuses "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None:
            status_dtos = SnortIDSController.get_snort_idses_monitor_threads_statuses(
                emulation_env_config=execution.emulation_env_config, physical_server_ip=GeneralUtil.get_host_ip(),
                logger=logging.getLogger())
            status_dtos = list(
                map(lambda x: ClusterManagerUtil.convert_snort_ids_monitor_dto_to_snort_ids_status_dto(x),
                    status_dtos))
            return csle_cluster.cluster_manager.cluster_manager_pb2.SnortIdsMonitorThreadStatusesDTO(
                snortIDSStatuses=status_dtos)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.SnortIdsMonitorThreadStatusesDTO(
                snortIDSStatuses=[])

    def stopSnortIdsesMonitorThreads(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopSnortIdsesMonitorThreadsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Snort IDSes monitor threads for a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the Snort IDSes monitor threads  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        SnortIDSController.stop_snort_idses_monitor_threads(
            emulation_env_config=execution.emulation_env_config, physical_server_ip=GeneralUtil.get_host_ip(),
            logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopSnortIds(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopSnortMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Snort IDS on a specific container

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the Snort IDS on the container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            SnortIDSController.stop_snort_ids(emulation_env_config=execution.emulation_env_config,
                                              ip=container_config.docker_gw_bridge_ip,
                                              logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopSnortIdsMonitorThread(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopSnortIdsMonitorThreadMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Snort IDS Monitor Thread on a specific container

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the Snort IDS monitor thread on the container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            SnortIDSController.stop_snort_idses_monitor_thread(emulation_env_config=execution.emulation_env_config,
                                                               ip=container_config.docker_gw_bridge_ip,
                                                               logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startSnortIds(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartSnortMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Snort IDS on a specific container in a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the Snort IDS on the container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            SnortIDSController.start_snort_ids(emulation_env_config=execution.emulation_env_config,
                                               ip=container_config.docker_gw_bridge_ip,
                                               logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startSnortIdsMonitorThread(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartSnortIdsMonitorThreadMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Snort IDS monitor thread on a specific container in a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the Snort IDS monitor thread on the container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            SnortIDSController.start_snort_idses_monitor_thread(emulation_env_config=execution.emulation_env_config,
                                                                ip=container_config.docker_gw_bridge_ip,
                                                                logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startSnortIdsMonitorThreads(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartSnortIdsMonitorThreadsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Snort IDS monitor threads of a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the Snort IDS monitor threads "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        SnortIDSController.start_snort_idses_monitor_threads(emulation_env_config=execution.emulation_env_config,
                                                             physical_server_ip=GeneralUtil.get_host_ip(),
                                                             logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startSnortIdsManagers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartSnortIdsManagersMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Snort IDS managers of a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the Snort IDS managers "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        SnortIDSController.start_snort_managers(emulation_env_config=execution.emulation_env_config,
                                                physical_server_ip=GeneralUtil.get_host_ip(),
                                                logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopSnortIdsManagers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopSnortIdsManagersMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Snort IDS managers of a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the Snort IDS managers "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        SnortIDSController.stop_snort_managers(emulation_env_config=execution.emulation_env_config,
                                               physical_server_ip=GeneralUtil.get_host_ip(),
                                               logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def startSnortIdsManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartSnortIdsManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Snort IDS manager at a specific container

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the Snort IDS manager on the container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            logging.info(container_config)
            SnortIDSController.start_snort_manager(emulation_env_config=execution.emulation_env_config,
                                                   ip=container_config.docker_gw_bridge_ip,
                                                   logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopSnortIdsManager(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopSnortIdsManagerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Snort IDS manager at a specific container

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the Snort IDS manager on the container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            SnortIDSController.stop_snort_manager(emulation_env_config=execution.emulation_env_config,
                                                  ip=container_config.docker_gw_bridge_ip,
                                                  logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopSnortIdsMonitorThreads(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopSnortIdsMonitorThreadsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Snort IDS managers of a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the Snort IDS monitor threads "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        SnortIDSController.stop_snort_idses_monitor_threads(emulation_env_config=execution.emulation_env_config,
                                                            physical_server_ip=GeneralUtil.get_host_ip(),
                                                            logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def getSnortIdsManagersInfo(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetSnortIdsManagersInfoMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.SnortIdsManagersInfoDTO:
        """
        Gets the info of Snort IDS managers

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a SnortIdsManagersInfoDTO
        """
        logging.info(f"Getting the info of Snort IDS managers in execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None:
            snort_ids_managers_info_dto = SnortIDSController.get_snort_managers_info(
                emulation_env_config=execution.emulation_env_config, logger=logging.getLogger(),
                active_ips=ClusterManagerUtil.get_active_ips(emulation_env_config=execution.emulation_env_config),
                physical_server_ip=GeneralUtil.get_host_ip())
            return ClusterManagerUtil.convert_snort_info_dto(snort_ids_managers_info_dto=snort_ids_managers_info_dto)
        else:
            return ClusterManagerUtil.get_empty_snort_managers_info_dto()

    def getExecutionInfo(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetExecutionInfoMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.ExecutionInfoDTO:
        """
        Gets the info of a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ExecutionInfoDTO
        """
        logging.info(f"Getting the info of the execution with id: {request.ipFirstOctet} "
                     f"and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is not None:
            execution_info_dto = EmulationEnvController.get_execution_info(
                execution=execution, logger=logging.getLogger(), physical_server_ip=GeneralUtil.get_host_ip())
            return ClusterManagerUtil.convert_execution_info_dto(execution_info_dto=execution_info_dto)
        else:
            return ClusterManagerUtil.get_empty_execution_info_dto()

    def listKibanaTunnels(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ListKibanaTunnelsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.KibanaTunnelsDTO:
        """
        Lists the Kibana tunnels

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an KibanaTunnelsDTO
        """
        logging.info("Getting the Kibana tunnels")
        return ClusterManagerUtil.create_kibana_tunnels_dto_from_dict(
            dict=cluster_constants.KIBANA_TUNNELS.KIBANA_TUNNELS_DICT)

    def listRyuTunnels(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.ListRyuTunnelsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.RyuTunnelsDTO:
        """
        Lists the Ryu tunnels

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a RyuTunnelsDTO
        """
        logging.info("Getting the Ryu tunnels")
        return ClusterManagerUtil.create_ryu_tunnels_dto_from_dict(dict=cluster_constants.RYU_TUNNELS.RYU_TUNNELS_DICT)

    def createKibanaTunnel(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.CreateKibanaTunnelMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Creates a new Kibana tunnel

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Creating a Kibana tunnel for emulation: {request.emulation}, "
                     f"execution id: {request.ipFirstOctet}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        ClusterManagerUtil.create_kibana_tunnel(execution=execution, logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def createRyuTunnel(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.CreateRyuTunnelMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Creates a new Ryu tunnel

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Creating a Ryu tunnel for emulation: {request.emulation}, "
                     f"execution id: {request.ipFirstOctet}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        ClusterManagerUtil.create_ryu_tunnel(execution=execution, logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def removeRyuTunnel(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.RemoveRyuTunnelMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Removes a Ryu tunnel

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Remove the Ryu tunnel for emulation: {request.emulation}, "
                     f"execution id: {request.ipFirstOctet}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        ClusterManagerUtil.remove_ryu_tunnel(execution=execution)
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def removeKibanaTunnel(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.RemoveKibanaTunnelMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Removes a Kibana tunnel

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Remove the Kibana tunnel for emulation: {request.emulation}, "
                     f"execution id: {request.ipFirstOctet}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        ClusterManagerUtil.remove_kibana_tunnel(execution=execution)
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopHostMonitorThreads(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopHostMonitorThreadsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the host monitor threads of a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping host monitor threads  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.stop_host_monitor_threads(emulation_env_config=execution.emulation_env_config,
                                                 physical_host_ip=GeneralUtil.get_host_ip(),
                                                 logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopHostMonitorThread(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopHostMonitorThreadMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops a specific host monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping host monitor thread on container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None:
            HostController.stop_host_monitor_thread(emulation_env_config=execution.emulation_env_config,
                                                    ip=container_config.docker_gw_bridge_ip,
                                                    logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startRyuMonitor(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartRyuMonitorThreadMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Ryu monitor thread for a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the Ryu monitor thread "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        if execution.emulation_env_config.sdn_controller_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            SDNControllerManager.start_ryu_monitor(emulation_env_config=execution.emulation_env_config,
                                                   physical_server_ip=GeneralUtil.get_host_ip(),
                                                   logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopRyuMonitor(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopRyuMonitorThreadMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Ryu monitor thread for a given execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the Ryu monitor thread "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        if execution.emulation_env_config.sdn_controller_config.container.physical_host_ip == GeneralUtil.get_host_ip():
            SDNControllerManager.stop_ryu_monitor(emulation_env_config=execution.emulation_env_config,
                                                  logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def getRyuManagerLogs(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetRyuManagerLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of a specific Ryu manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a LogsDTO with the logs
        """
        logging.info(f"Getting the logs of the Ryu manager "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None or \
                execution.emulation_env_config.sdn_controller_config is None \
                or execution.emulation_env_config.sdn_controller_config.container.physical_host_ip \
                != GeneralUtil.get_host_ip():
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        else:
            path = f"/{ryu_constants.RYU.LOG_FILE}"
            return ClusterManagerUtil.get_logs(
                execution=execution,
                ip=execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip,
                path=path)

    def getRyuControllerLogs(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetRyuControllerLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of a specific Ryu controller

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a LogsDTO with the logs
        """
        logging.info(f"Getting the logs of the Ryu controller "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None or execution.emulation_env_config.sdn_controller_config is None \
                or execution.emulation_env_config.sdn_controller_config.container.physical_host_ip \
                != GeneralUtil.get_host_ip():
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        else:
            path = (execution.emulation_env_config.sdn_controller_config.manager_log_dir +
                    execution.emulation_env_config.sdn_controller_config.manager_log_file)
            return ClusterManagerUtil.get_logs(
                execution=execution,
                ip=execution.emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip,
                path=path)

    def getElkLogs(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetElkLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of a specific ELK stack

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a LogsDTO with the logs
        """
        logging.info(f"Getting the logs of the ELK stack "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None or \
                execution.emulation_env_config.elk_config.container.physical_host_ip != GeneralUtil.get_host_ip():
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        else:
            path = collector_constants.ELK.ELK_LOG
            return ClusterManagerUtil.get_logs(
                execution=execution,
                ip=execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip,
                path=path)

    def getElkManagerLogs(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetElkManagerLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of a specific  ELK manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a LogsDTO with the logs
        """
        logging.info(f"Getting the logs of the ELK manager "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None or \
                execution.emulation_env_config.elk_config.container.physical_host_ip != GeneralUtil.get_host_ip():
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        else:
            path = (execution.emulation_env_config.elk_config.elk_manager_log_dir +
                    execution.emulation_env_config.elk_config.elk_manager_log_file)
            return ClusterManagerUtil.get_logs(
                execution=execution,
                ip=execution.emulation_env_config.elk_config.container.docker_gw_bridge_ip,
                path=path)

    def getTrafficManagerLogs(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetTrafficManagerLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of a specific traffic manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a LogsDTO with the logs
        """
        logging.info(f"Getting the logs of the traffic manager with ip: {request.containerIp} "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        else:
            path = execution.emulation_env_config.traffic_config.get_node_traffic_config_by_ip(
                ip=request.containerIp).traffic_manager_log_dir
            path = path + execution.emulation_env_config.traffic_config.get_node_traffic_config_by_ip(
                ip=request.containerIp).traffic_manager_log_file
            return ClusterManagerUtil.get_logs(
                execution=execution,
                ip=container_config.docker_gw_bridge_ip,
                path=path)

    def getHostManagerLogs(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetHostManagerLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of a specific host manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a LogsDTO with the logs
        """
        logging.info(f"Getting the logs of the host manager with ip: {request.containerIp} "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        else:
            path = (execution.emulation_env_config.host_manager_config.host_manager_log_dir +
                    execution.emulation_env_config.host_manager_config.host_manager_log_file)
            return ClusterManagerUtil.get_logs(
                execution=execution,
                ip=container_config.docker_gw_bridge_ip,
                path=path)

    def getOSSECIdsLogs(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetOSSECIdsLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of a specific OSSEC IDS

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a LogsDTO with the logs
        """
        logging.info(f"Getting the logs of the OSSEC IDS with ip: {request.containerIp} "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        else:
            path = collector_constants.OSSEC.OSSEC_LOG_FILE
            return ClusterManagerUtil.get_logs(execution=execution,
                                               ip=container_config.docker_gw_bridge_ip, path=path)

    def getOSSECIdsManagerLogsMsg(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetOSSECIdsManagerLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of a specific OSSEC IDS manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a LogsDTO with the logs
        """
        logging.info(f"Getting the logs of the OSSEC IDS manager with ip: {request.containerIp} "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        else:
            path = (execution.emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_log_dir +
                    execution.emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_log_file)
            return ClusterManagerUtil.get_logs(execution=execution,
                                               ip=container_config.docker_gw_bridge_ip, path=path)

    def getSnortIdsLogs(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetSnortIdsLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of a specific Snort IDS

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a LogsDTO with the logs
        """
        logging.info(f"Getting the logs of the Snort IDS with ip: {request.containerIp} "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        else:
            path = collector_constants.SNORT_IDS_ROUTER.SNORT_FAST_LOG_FILE
            return ClusterManagerUtil.get_logs(execution=execution, ip=container_config.docker_gw_bridge_ip, path=path)

    def getSnortIdsManagerLogsMsg(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetSnortIdsManagerLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of a specific Snort IDS manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a LogsDTO with the logs
        """
        logging.info(f"Getting the logs of the Snort IDS manager with ip: {request.containerIp} "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        else:
            path = (execution.emulation_env_config.snort_ids_manager_config.snort_ids_manager_log_dir +
                    execution.emulation_env_config.snort_ids_manager_config.snort_ids_manager_log_file)
            return ClusterManagerUtil.get_logs(execution=execution, ip=container_config.docker_gw_bridge_ip, path=path)

    def getKafkaLogs(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetKafkaLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of a specific Kafka server

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a LogsDTO with the logs
        """
        logging.info(f"Getting the logs of the Kafka server "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        if execution.emulation_env_config.kafka_config.container.physical_host_ip != GeneralUtil.get_host_ip():
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        else:
            path = collector_constants.LOG_FILES.KAFKA_LOG_FILE
            return ClusterManagerUtil.get_logs(
                execution=execution,
                ip=execution.emulation_env_config.kafka_config.container.docker_gw_bridge_ip, path=path)

    def getKafkaManagerLogs(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetKafkaManagerLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of a specific Kafka manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a LogsDTO with the logs
        """
        logging.info(f"Getting the logs of the Kafka manager "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        if execution.emulation_env_config.kafka_config.container.physical_host_ip != GeneralUtil.get_host_ip():
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        else:
            path = (execution.emulation_env_config.kafka_config.kafka_manager_log_dir +
                    execution.emulation_env_config.kafka_config.kafka_manager_log_file)
            return ClusterManagerUtil.get_logs(
                execution=execution,
                ip=execution.emulation_env_config.kafka_config.container.docker_gw_bridge_ip, path=path)

    def getClientManagerLogsMsg(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetClientManagerLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of a specific Client manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a LogsDTO with the logs
        """
        logging.info(f"Getting the logs of the Client manager "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        if execution.emulation_env_config.traffic_config.client_population_config.physical_host_ip != \
                GeneralUtil.get_host_ip():
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        else:
            path = (execution.emulation_env_config.traffic_config.client_population_config.client_manager_log_dir +
                    execution.emulation_env_config.traffic_config.client_population_config.client_manager_log_file)
            return ClusterManagerUtil.get_logs(
                execution=execution,
                ip=execution.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip,
                path=path)

    def getContainerLogs(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetContainerLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of a specific container

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a LogsDTO with the logs
        """
        logging.info(f"Getting the logs of the container with ip: {request.containerIp} "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=[])
        else:
            cmd = constants.COMMANDS.CONTAINER_LOGS.format(container_config.full_name_str)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output_bytes, err) = p.communicate()
            output_str = output_bytes.decode("utf-8")
            output = output_str.split("\n")[-100:]
            data = output
            return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=data)

    def getClusterManagerLogs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetClusterManagerLogsMsg,
                              context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the logs of the cluster manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info("Getting the cluster manager logs")
        config = Config.get_current_config()
        path = config.cluster_manager_log_file
        logs = []
        if os.path.exists(path):
            try:
                with open(path, 'r') as fp:
                    data = ClusterManagerUtil.tail(fp, window=100).split("\n")
                    logs = data
            except Exception as e:
                logging.info(f"Exception reading log file: {path}. Stacktrace: {str(e)}, {repr(e)}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs=logs)

    def getExecutionTimeSeriesData(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetExecutionTimeSeriesDataMsg,
            context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.EmulationMetricsTimeSeriesDTO:
        """
        Gets time-series data of an emulation execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info(f"Getting the time-series data of "
                     f"execution with id: {request.ipFirstOctet} and emulation: {request.emulation}, "
                     f"minutes: {request.minutes}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None or \
                execution.emulation_env_config.kafka_config.container.physical_host_ip != GeneralUtil.get_host_ip():
            return ClusterManagerUtil.get_empty_emulation_metrics_time_series_dto()
        else:

            time_series = ReadEmulationStatisticsUtil.read_all(emulation_env_config=execution.emulation_env_config,
                                                               time_window_minutes=request.minutes,
                                                               logger=logging.getLogger())
            return ClusterManagerUtil.convert_emulation_metrics_time_series_dto(time_series_dto=time_series)

    def startSparkServer(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartSparkServerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Spark server on a specific container in a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the Spark server on the container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None and container_config.physical_host_ip == GeneralUtil.get_host_ip():
            HostController.start_spark(emulation_env_config=execution.emulation_env_config,
                                       ips=[container_config.docker_gw_bridge_ip], logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def stopSparkServer(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopSparkServerMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Spark server on a specific container in a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the Spark server on the container with ip: {request.containerIp}  "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        container_config = ClusterManagerUtil.get_container_config(execution=execution, ip=request.containerIp)
        if container_config is not None and container_config.physical_host_ip == GeneralUtil.get_host_ip():
            HostController.stop_spark(emulation_env_config=execution.emulation_env_config,
                                      ips=[container_config.docker_gw_bridge_ip], logger=logging.getLogger())
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)
        else:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)

    def startSparkServers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartSparkServersMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Starts the Spark servers in a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Starting the Spark servers "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.start_sparks(emulation_env_config=execution.emulation_env_config,
                                    physical_server_ip=GeneralUtil.get_host_ip(),
                                    logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def stopSparkServers(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopSparkServersMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops the Spark servers in a specific execution

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping the Spark servers "
                     f"in execution with id: {request.ipFirstOctet} and emulation: {request.emulation}")
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=request.ipFirstOctet,
                                                            emulation_name=request.emulation)
        if execution is None:
            return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=False)
        HostController.stop_sparks(emulation_env_config=execution.emulation_env_config,
                                   physical_server_ip=GeneralUtil.get_host_ip(), logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)

    def checkPid(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.CheckPidMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Checks the status of a PID

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Checking the status of PID: {request.pid}")
        running = ManagementSystemController.is_pid_running(pid=request.pid, logger=logging.getLogger())
        logging.info(f"Is PID {request.pid} running? {running}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=running)

    def stopPid(
            self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StopPidMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO:
        """
        Stops a PID

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an OperationOutcomeDTO
        """
        logging.info(f"Stopping PID: {request.pid}")
        ManagementSystemController.stop_pid(pid=request.pid, logger=logging.getLogger())
        return csle_cluster.cluster_manager.cluster_manager_pb2.OperationOutcomeDTO(outcome=True)


def serve(port: int = 50041, log_dir: str = "/var/log/csle/", max_workers: int = 10,
          log_file_name: str = "cluster_manager.log") -> None:
    """
    Starts the gRPC server for managing the cluster node

    :param port: the port that the server will listen to
    :param log_dir: the directory to write the log file
    :param log_file_name: the file name of the log
    :param max_workers: the maximum number of parallel gRPC workers
    :return: None
    """
    collector_constants.LOG_FILES.CLUSTER_MANAGER_LOG_DIR = log_dir
    collector_constants.LOG_FILES.CLUSTER_MANAGER_LOG_FILE = log_file_name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    csle_cluster.cluster_manager.cluster_manager_pb2_grpc.add_ClusterManagerServicer_to_server(
        ClusterManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    logging.getLogger("paramiko").setLevel(logging.WARNING)
    server.start()
    logging.info(f"ClusterManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
