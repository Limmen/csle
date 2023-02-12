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
        dir = collector_constants.LOG_FILES.CLIENT_MANAGER_LOG_DIR
        logfile = os.path.join(dir, file_name)
        logging.basicConfig(filename=logfile, level=logging.INFO)
        logging.info("Setting up ClusterManager")


    def get_cadvisor_running_status(self) -> bool:
        """
        :return: True if cadvisor is running, otherwise False
        """
        return ManagementSystemController.is_cadvisor_running()

    def get_grafana_runn(self) -> bool:
        """
        :return: True if cadvisor is running, otherwise False
        """
        return ManagementSystemController.is_cadvisor_running()

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
        logging.info(f"Starting cAdvisor")
        ManagementSystemController.start_cadvisor()
        logging.info(f"Started cAdvisor")
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
        logging.info(f"Stopping cAdvisor")
        ManagementSystemController.stop_cadvisor()
        logging.info(f"Stopped cAdvisor")
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
        logging.info(f"Starting node exporter")
        ManagementSystemController.start_node_exporter()
        logging.info(f"Started node exporter")
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
        logging.info(f"Stopping node exporter")
        ManagementSystemController.stop_node_exporter()
        logging.info(f"Stopped node exporter")
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
        logging.info(f"Starting grafana")
        ManagementSystemController.start_grafana()
        logging.info(f"Started grafana")
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
        logging.info(f"Stopping grafana")
        ManagementSystemController.stop_grafana()
        logging.info(f"Stopped grafana")
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
        logging.info(f"Starting Prometheus")
        ManagementSystemController.start_prometheus()
        logging.info(f"Started Prometheus")
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
        logging.info(f"Stopping Prometheus")
        ManagementSystemController.stop_prometheus()
        logging.info(f"Stopped Prometheus")
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
        logging.info(f"Starting pgAdmin")
        ManagementSystemController.start_pgadmin()
        logging.info(f"Started pgAdmin")
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
        logging.info(f"Stopping pgAdmin")
        ManagementSystemController.stop_pgadmin()
        logging.info(f"Stopped pgAdmin")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=False)

    def startFlask(self, request: csle_cluster.cluster_manager.cluster_manager_pb2.StartFlask,
                     context: grpc.ServicerContext) \
            -> csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO:
        """
        Starts Flask

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of flask
        """
        logging.info(f"Starting flask")
        ManagementSystemController.start_flask()
        logging.info(f"Started flask")
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
        logging.info(f"Stopping flask")
        ManagementSystemController.stop_flask()
        logging.info(f"Stopped flask")
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
        logging.info(f"Starting the docker statsmanager")
        ManagementSystemController.start_docker_stats_manager()
        logging.info(f"Started the docker statsmanager")
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
        logging.info(f"Stopping the Docker statsmanager")
        ManagementSystemController.stop_docker_stats_manager()
        logging.info(f"Stopped the Docker statsmanager")
        return csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO(running=False)


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
