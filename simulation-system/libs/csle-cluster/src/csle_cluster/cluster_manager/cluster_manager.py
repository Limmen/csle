import os
import logging
from concurrent import futures
import grpc
import csle_cluster.cluster_manager.cluster_manager_pb2_grpc
import csle_cluster.cluster_manager.cluster_manager_pb2
import csle_collector.constants.constants as collector_constants
import csle_common.constants.constants as constants
from csle_common.controllers.management_system_controller import ManagementSystemController
from csle_common.util.general_util import GeneralUtil
from csle_common.util.cluster_util import ClusterUtil


class ClusterManagerServicer(csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerServicer):
    """
    gRPC server for managing a node in the CSLE management system cluster
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """

        file_name = collector_constants.LOG_FILES.CLUSTER_MANAGER_LOG_FILE
        dir = collector_constants.LOG_FILES.CLUSTER_MANAGER_LOG_DIR
        logfile = os.path.join(dir, file_name)
        logging.basicConfig(filename=logfile, level=logging.INFO)
        logging.info("Setting up ClusterManager")

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

    def startPosgtreSQL(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartPostgreSQLMsg,
                        context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Postgresql

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of PostgreSQL
        """
        logging.info(f"Starting postgresql with command: {constants.COMMANDS.POSTGRESQL_START}")
        operation_status, stdout, stderr = ManagementSystemController.start_postgresql()
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
        operation_status, stdout, stderr = ManagementSystemController.stop_postgresql()
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
        operation_status, stdout, stderr = ManagementSystemController.start_docker_engine()
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
        operation_status, stdout, stderr = ManagementSystemController.stop_docker_engine()
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
        operation_status, stdout, stderr = ManagementSystemController.start_nginx()
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
        operation_status, stdout, stderr = ManagementSystemController.stop_nginx()
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
        ManagementSystemController.start_cadvisor()
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
        ManagementSystemController.start_node_exporter()
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
        ManagementSystemController.stop_node_exporter()
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
        ManagementSystemController.start_grafana()
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
        ManagementSystemController.start_prometheus()
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
        ManagementSystemController.stop_prometheus()
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
        ManagementSystemController.start_pgadmin()
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
        ManagementSystemController.start_flask()
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
        ManagementSystemController.stop_flask()
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
        ManagementSystemController.start_docker_stats_manager()
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
        ManagementSystemController.stop_docker_stats_manager()
        logging.info("Stopped the Docker statsmanager")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=False)

    def get_log_file(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetLogFileMsg,
                        context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets a specific log file

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info(f"Getting log file: {request.name}")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs="")

    def get_flask_logs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetFlaskLogsMsg,
                     context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the Flask logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info(f"Getting the flask logs")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs="")

    def get_postgresql_logs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetPostgreSQLLogsMsg,
                       context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the PostgreSQL logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info(f"Getting the PostgreSQL logs")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs="")

    def get_docker_logs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetDockerLogsMsg,
                            context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the Docker logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info(f"Getting the Docker logs")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs="")

    def get_nginx_logs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetNginxLogsMsg,
                        context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the nginx logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info(f"Getting the Nginx logs")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs="")

    def get_grafana_logs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetGrafanaLogsMsg,
                       context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the Grafana logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info(f"Getting the Grafana logs")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs="")

    def get_pgadmin_logs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetPgAdminLogsMsg,
                         context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the pgAdmin logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info(f"Getting the pgAdmin logs")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs="")

    def get_cadvisor_logs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetCAdvisorLogsMsg,
                         context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the cAdvisor logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info(f"Getting the cAdvisor logs")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs="")

    def get_node_exporter_logs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetNodeExporterLogsMsg,
                          context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the node exporter logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info(f"Getting the Node exporter logs")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs="")

    def get_prometheus_logs(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetPrometheusLogsMsg,
                               context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the Prometheus logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info(f"Getting the Prometheus logs")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs="")

    def get_docker_statsmanager_logs(
            self,  request: csle_cluster.cluster_manager.cluster_manager_pb2.GetDockerStatsManagerLogsMsg,
            context: grpc.ServicerContext) -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the Docker statsmanager logs

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info(f"Getting the Docker statsmanager logs")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs="")

    def get_csle_log_files(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.GetCsleLogFilesMsg,
                            context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO:
        """
        Gets the list of file names in the CSLE log directory

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with logs
        """
        logging.info(f"Getting the CSLE log file names")
        return csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO(logs="")


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
    server.start()
    logging.info(f"ClusterManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
