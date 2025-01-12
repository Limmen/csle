import logging
from typing import Any, Tuple
import subprocess
import docker
import psutil
import os
import csle_common.constants.constants as constants
import sys
import shutil


class ManagementSystemController:
    """
    Controller managing monitoring tools
    """

    @staticmethod
    def read_pid_file(path: str) -> int:
        """
        Reads the PID from a pidfile

        :param path: the path to the file
        :return: the parsed pid, or -1 if the pidfile could not be read
        """
        if os.path.exists(path):
            pid = int(open(path, "r").read())
            return pid
        return -1

    @staticmethod
    def is_prometheus_running() -> bool:
        """
        Checks if prometheus is running on the host

        :return: True if it is running, false otherwise
        """
        pid = ManagementSystemController.read_pid_file(constants.COMMANDS.PROMETHEUS_PID_FILE)
        if pid == -1:
            return False
        cmd = (constants.COMMANDS.PS_AUX + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PIPE_DELIM +
               constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.GREP
               + constants.COMMANDS.SPACE_DELIM + "prometheus")
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        output_1 = str(output)
        return constants.COMMANDS.SEARCH_PROMETHEUS in output_1 and str(pid) in output_1

    @staticmethod
    def is_node_exporter_running() -> bool:
        """
        Checks if node_exporter is running on the host

        :return: True if it is running, false otherwise
        """
        pid = ManagementSystemController.read_pid_file(constants.COMMANDS.NODE_EXPORTER_PID_FILE)
        if pid == -1:
            return False
        cmd = (constants.COMMANDS.PS_AUX + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PIPE_DELIM +
               constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.GREP + constants.COMMANDS.SPACE_DELIM +
               constants.COMMANDS.SEARCH_NODE_EXPORTER)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        output_1 = str(output)
        return constants.COMMANDS.SEARCH_NODE_EXPORTER in output_1 and str(pid) in output_1

    @staticmethod
    def is_nginx_running() -> bool:
        """
        Checks if Nginx is running on the host

        :return: True if nginx is running, false otherwise
        """
        output = ""
        try:
            output = subprocess.run(constants.COMMANDS.NGINX_STATUS.split(" "), capture_output=True, text=True).stdout
        except Exception:
            pass
        nginx_running = "active (running)" in output or "active (exited)" in output
        return nginx_running

    @staticmethod
    def is_postgresql_running() -> bool:
        """
        Checks if PostgreSQL is running on the host

        :return: True if PostgreSQL is running, false otherwise
        """
        output = ""
        try:
            output = subprocess.run(constants.COMMANDS.POSTGRESQL_STATUS.split(" "), capture_output=True,
                                    text=True).stdout
        except Exception:
            pass
        postgresql_running = "active (running)" in output or "active (exited)" in output
        if postgresql_running:
            return postgresql_running
        output = ""
        try:
            output = subprocess.run(constants.COMMANDS.POSTGRESQL_STATUS_VERSION.split(" "), capture_output=True,
                                    text=True).stdout
        except Exception:
            pass
        postgresql_running = "active (running)" in output or "active (exited)" in output
        return postgresql_running

    @staticmethod
    def is_docker_engine_running() -> bool:
        """
        Checks if Docker engine is running on the host

        :return: True if Docker engine is running, false otherwise
        """
        output = ""
        try:
            output = subprocess.run(constants.COMMANDS.DOCKER_ENGINE_STATUS.split(" "), capture_output=True,
                                    text=True).stdout
        except Exception:
            pass
        docker_engine_running = "active (running)" in output or "active (exited)" in output
        return docker_engine_running

    @staticmethod
    def is_flask_running() -> bool:
        """
        Checks if the flask web server is running on the host

        :return: True if it is running, false otherwise
        """
        pid = ManagementSystemController.read_pid_file(constants.COMMANDS.CSLE_MGMT_WEBAPP_PID_FILE)
        if pid == -1:
            return False
        cmd = (constants.COMMANDS.PS_AUX + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PIPE_DELIM +
               constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.GREP + constants.COMMANDS.SPACE_DELIM +
               constants.COMMANDS.SEARCH_MONITOR)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        output_1 = str(output)
        return constants.COMMANDS.SEARCH_MONITOR in output_1 and str(pid) in output_1

    @staticmethod
    def start_node_exporter(logger: logging.Logger) -> bool:
        """
        Starts the node exporter

        :param logger: the logger to use for logging
        :return: True if it was started, False otherwise
        """
        if ManagementSystemController.is_node_exporter_running():
            logger.info("Node exporter is already running")
            return False
        cmd = constants.COMMANDS.START_NODE_EXPORTER
        logger.info(f"Starting node exporter by running the command: {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
        return True

    @staticmethod
    def start_flask(logger: logging.Logger) -> bool:
        """
        Starts the Flask REST API Server

        :param logger: the logger to use for logging
        :return: True if it was started, False otherwise
        """
        if ManagementSystemController.is_flask_running():
            logger.info("Flask is already running")
            return False

        cmd = constants.COMMANDS.BUILD_CSLE_MGMT_WEBAPP
        logger.info(f"Building the web app with the command: {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            if p.stdout is None:
                raise ValueError("Cannot read due to NoneType")
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if str(out) != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()
        cmd = constants.COMMANDS.START_CSLE_MGMT_WEBAPP
        cmd = cmd.replace("python", str(shutil.which("python")))
        cmd = cmd.replace(f"${constants.CONFIG_FILE.CSLE_HOME_ENV_PARAM}",
                          os.environ[constants.CONFIG_FILE.CSLE_HOME_ENV_PARAM])
        logger.info(f"Starting flask with the command: {cmd}")
        p = subprocess.Popen(cmd.split(" "), stdout=subprocess.DEVNULL, shell=False)
        pid = p.pid

        cmd = constants.COMMANDS.SAVE_PID.format(pid, constants.COMMANDS.CSLE_MGMT_WEBAPP_PID_FILE)
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
        return True

    @staticmethod
    def stop_node_exporter(logger: logging.Logger) -> bool:
        """
        Stops the node exporter

        :param logger: the logger to use for logging
        :return: True if it was stopped, False otherwise
        """
        if not ManagementSystemController.is_node_exporter_running():
            logger.info("Node exporter is not running")
            return False
        pid = ManagementSystemController.read_pid_file(constants.COMMANDS.NODE_EXPORTER_PID_FILE)
        cmd = constants.COMMANDS.KILL_PROCESS.format(pid)
        logger.info(f"Stopping node exporter by running the command: {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
        return True

    @staticmethod
    def stop_flask(logger: logging.Logger) -> bool:
        """
        Stops the flask REST API

        :param logger: the logger to use for logging
        :return: True if it was stopped, False otherwise
        """
        if not ManagementSystemController.is_flask_running():
            logger.info("Flask is not running")
            return False
        pid = ManagementSystemController.read_pid_file(constants.COMMANDS.CSLE_MGMT_WEBAPP_PID_FILE)
        cmd = constants.COMMANDS.KILL_PROCESS.format(pid)
        logger.info(f"Stopping flask by running the command: {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
        return True

    @staticmethod
    def start_prometheus(logger: logging.Logger) -> bool:
        """
        Starts Prometheus

        :param logger: the logger to use for logging
        :return: True if it was started, False otherwise
        """
        if ManagementSystemController.is_prometheus_running():
            logger.info("Prometheus is already running")
            return False
        cmd = constants.COMMANDS.START_PROMETHEUS
        logger.info(f"Starting Prometheus by running the command: {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
        return True

    @staticmethod
    def stop_prometheus(logger: logging.RootLogger) -> bool:
        """
        Stops Prometheus

        :param logger: the logger to use for logging
        :return: True if it was stopped, False otherwise
        """
        if not ManagementSystemController.is_prometheus_running():
            logger.info("Prometheus is not running")
            return False
        pid = ManagementSystemController.read_pid_file(constants.COMMANDS.PROMETHEUS_PID_FILE)
        cmd = constants.COMMANDS.KILL_PROCESS.format(pid)
        logger.info(f"Stopping Prometheus by running the command: {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
        return True

    @staticmethod
    def is_cadvisor_running() -> bool:
        """
        :return: True if cadvisor is running, otherwise False
        """
        client_1 = docker.from_env()
        containers = client_1.containers.list()
        for c in containers:
            if constants.CONTAINER_IMAGES.CADVISOR in c.name:
                return True
        return False

    @staticmethod
    def is_pgadmin_running() -> bool:
        """
        :return: True if pgadmin is running, otherwise False
        """
        client_1 = docker.from_env()
        containers = client_1.containers.list()
        for c in containers:
            if constants.CONTAINER_IMAGES.PGADMIN in c.name:
                return True
        return False

    @staticmethod
    def stop_cadvisor() -> bool:
        """
        :return: True if cadvisor was stopped, otherwise False
        """
        client_1 = docker.from_env()
        containers = client_1.containers.list()
        for c in containers:
            if constants.CONTAINER_IMAGES.CADVISOR in c.name:
                c.stop()
                return True
        return False

    @staticmethod
    def stop_pgadmin() -> bool:
        """
        :return: True if pgadmin was stopped, otherwise False
        """
        client_1 = docker.from_env()
        containers = client_1.containers.list()
        for c in containers:
            if constants.CONTAINER_IMAGES.PGADMIN in c.name:
                c.stop()
                return True
        return False

    @staticmethod
    def start_cadvisor(logger: logging.Logger) -> bool:
        """
        Starts cAdvisor

        :param logger: the logger to use for logging
        :return: True if cadvisor was started, otherwise False
        """
        if ManagementSystemController.is_cadvisor_running():
            logger.info("cAdvisor is already running")
            return False
        client_1 = docker.from_env()
        containers = client_1.containers.list(all=True)
        for c in containers:
            if constants.CONTAINER_IMAGES.CADVISOR in c.name:
                container_state = c.attrs['State']
                running = container_state['Status'] == "running"
                if not running:
                    c.start()
                    return True
        cmd = constants.COMMANDS.START_CADVISOR
        logger.info(f"Starting cAdvisor by running the command: {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        (output, err) = p.communicate()
        return True

    @staticmethod
    def start_postgresql(logger: logging.RootLogger) -> Tuple[bool, Any, Any]:
        """
        Starts PostgreSQL

        :param logger: the logger to use for logging
        :return: True if postgresql was started, otherwise False
        """
        if ManagementSystemController.is_postgresql_running():
            logger.info("PostgreSQL is already running")
            return False, None, None
        cmd = constants.COMMANDS.POSTGRESQL_START
        logger.info(f"Starting PostgreSQL by running the command: {cmd}")
        output = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        return True, output.stdout, output.stderr

    @staticmethod
    def stop_postgresql(logger: logging.RootLogger) -> Tuple[bool, Any, Any]:
        """
        Stops PostgreSQL

        :param logger: the logger to use for logging
        :return: True if postgresql was stopped, otherwise False
        """
        if not ManagementSystemController.is_postgresql_running():
            logger.info("PostgreSQL is not running")
            return False, None, None
        cmd = constants.COMMANDS.POSTGRESQL_STOP
        logger.info(f"Stopping PostgreSQL by running the command: {cmd}")
        output = subprocess.run(constants.COMMANDS.POSTGRESQL_STOP.split(" "), capture_output=True, text=True)
        return True, output.stdout, output.stderr

    @staticmethod
    def start_nginx(logger: logging.RootLogger) -> Tuple[bool, Any, Any]:
        """
        Starts Nginx

        :param logger: the logger to use for logging
        :return: True if nginx was started, otherwise False
        """
        if ManagementSystemController.is_nginx_running():
            logger.info("Nginx is already running")
            return False, None, None
        cmd = constants.COMMANDS.NGINX_START
        logger.info(f"Starting Nginx by running the command: {cmd}")
        output = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        return True, output.stdout, output.stderr

    @staticmethod
    def stop_nginx(logger: logging.RootLogger) -> Tuple[bool, Any, Any]:
        """
        Stops Nginx

        :param logger: the logger to use for logging
        :return: True if postgresql was stopped, otherwise False
        """
        if not ManagementSystemController.is_nginx_running():
            logger.info("Nginx is not running")
            return False, None, None
        cmd = constants.COMMANDS.NGINX_STOP
        logger.info(f"Stopping Nginx by running the command: {cmd}")
        output = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        return True, output.stdout, output.stderr

    @staticmethod
    def start_docker_engine(logger: logging.RootLogger) -> Tuple[bool, Any, Any]:
        """
        Starts the Docker engine

        :param logger: the logger to use for logging
        :return: True if nginx was started, otherwise False
        """
        if ManagementSystemController.is_docker_engine_running():
            logger.info("The Docker engine is already running")
            return False, None, None
        cmd = constants.COMMANDS.DOCKER_ENGINE_START
        logger.info(f"Starting the Docker engine by running the command: {cmd}")
        output = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        return True, output.stdout, output.stderr

    @staticmethod
    def stop_docker_engine(logger: logging.RootLogger) -> Tuple[bool, Any, Any]:
        """
        Stops the Docker engine

        :param logger: the logger to use for logging
        :return: True if postgresql was stopped, otherwise False
        """
        if not ManagementSystemController.is_docker_engine_running():
            logger.info("The Docker engine is not running")
            return False, None, None
        cmd = constants.COMMANDS.DOCKER_ENGINE_STOP
        logger.info(f"Stopping the Docker engine by running the command: {cmd}")
        output = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        return True, output.stdout, output.stderr

    @staticmethod
    def start_pgadmin(logger: logging.RootLogger) -> bool:
        """
        Starts pgAdmin

        :param logger: the logger to use for logging
        :return: True if pgadmin was started, otherwise False
        """
        if ManagementSystemController.is_pgadmin_running():
            logger.info("pgAdmin is already running")
            return False
        client_1 = docker.from_env()
        containers = client_1.containers.list(all=True)
        for c in containers:
            if constants.CONTAINER_IMAGES.PGADMIN in c.name:
                container_state = c.attrs['State']
                running = container_state['Status'] == "running"
                if not running:
                    c.start()
                    return True
        cmd = constants.COMMANDS.START_PGADMIN
        logger.info(f"Starting pgAdmin by running the command: {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        (output, err) = p.communicate()
        return True

    @staticmethod
    def stop_grafana() -> bool:
        """
        Stops Grafana

        :return: True if grafana was stopped, otherwise False
        """
        client_1 = docker.from_env()
        containers = client_1.containers.list()
        for c in containers:
            if constants.CONTAINER_IMAGES.GRAFANA in c.name:
                c.stop()
                return True
        return False

    @staticmethod
    def start_grafana(logger: logging.RootLogger) -> bool:
        """
        Starts Grafana

        :param logger: the logger to use for logging
        :return: True if grafana was started, otherwise False
        """
        if ManagementSystemController.is_grafana_running():
            logger.info("Grafana is already running")
            return False
        client_1 = docker.from_env()
        containers = client_1.containers.list(all=True)
        for c in containers:
            if constants.CONTAINER_IMAGES.GRAFANA in c.name:
                container_state = c.attrs['State']
                running = container_state['Status'] == "running"
                if not running:
                    c.start()
                    return True
        cmd = constants.COMMANDS.START_GRAFANA
        logger.info(f"Starting Grafana by running the command: {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        (output, err) = p.communicate()
        return True

    @staticmethod
    def is_grafana_running() -> bool:
        """
        :return: True if grafana is running otherwise False
        """
        client_1 = docker.from_env()
        containers = client_1.containers.list()
        for c in containers:
            if constants.CONTAINER_IMAGES.GRAFANA in c.name:
                return True
        return False

    @staticmethod
    def is_statsmanager_running() -> bool:
        """
        Checks if the statsmanager is running on the host

        :return: True if it is running, false otherwise
        """
        pid = ManagementSystemController.read_pid_file(constants.COMMANDS.DOCKER_STATS_MANAGER_PIDFILE)
        if pid == -1:
            return False
        logging.getLogger().info(pid)
        cmd = (constants.COMMANDS.PS_AUX + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PIPE_DELIM +
               constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.GREP + constants.COMMANDS.SPACE_DELIM +
               constants.COMMANDS.SEARCH_DOCKER_STATS_MANAGER)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        output_1 = str(output)
        return constants.COMMANDS.SEARCH_DOCKER_STATS_MANAGER in output_1 and str(pid) in output_1

    @staticmethod
    def start_docker_statsmanager(logger: logging.Logger, log_file: str = "docker_stats_manager.log",
                                  log_dir: str = "/var/log/csle", max_workers: int = 10,
                                  port: int = 50046) -> bool:
        """
        Starts the docker stats manager on the docker host if it is not already started

        :param logger: the logger to use for logging
        :param port: the port that the docker stats manager will listen to
        :param log_file: log file of the docker stats manager
        :param log_dir: log dir of the docker stats manager
        :param max_workers: max workers of the docker stats manager
        :return: True if it was started, False otherwise
        """
        if ManagementSystemController.is_statsmanager_running():
            logger.info("The docker statsmanager is already running")
            return False
        cmd = constants.COMMANDS.START_DOCKER_STATS_MANAGER.format(port, log_dir, log_file, max_workers)
        logger.info(f"Starting the Docker stats manager by running the command: {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        (output, err) = p.communicate()
        return True

    @staticmethod
    def stop_docker_statsmanager(logger: logging.Logger) -> bool:
        """
        Stops the statsmanager

        :param logger: the logger to use for logging
        :return: True if it was stopped, False otherwise
        """
        if not ManagementSystemController.is_statsmanager_running():
            logger.info("The statsmanager is not running")
            return False
        pid = ManagementSystemController.read_pid_file(constants.COMMANDS.DOCKER_STATS_MANAGER_PIDFILE)
        cmd = constants.COMMANDS.KILL_PROCESS.format(pid)
        logger.info(f"Stopping the statsmanager by running the command: {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        (output, err) = p.communicate()
        return True

    @staticmethod
    def stop_cluster_manager() -> bool:
        """
        Stops the local cluster manager

        :return: True if it was stopped, False otherwise
        """
        pid = ManagementSystemController.read_pid_file(constants.COMMANDS.CLUSTER_MANAGER_PIDFILE)
        cmd = constants.COMMANDS.KILL_PROCESS.format(pid)
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        (output, err) = p.communicate()
        return True

    @staticmethod
    def is_pid_running(pid: int, logger: logging.Logger) -> bool:
        """
        Checks if the given pid is running on the host

        :param pid: the pid to check
        :param logger: the logger to use for logging
        :return: True if it is running, false otherwise
        """
        logger.info(f"Checking if PID: {pid} is running")
        return bool(psutil.pid_exists(pid))

    @staticmethod
    def stop_pid(pid, logger: logging.Logger) -> bool:
        """
        Stops a process with a given pid

        :param pid: the pid to stop
        :return: True if the pid was stopped, false if it was not running
        """
        if not ManagementSystemController.is_pid_running(pid, logger=logger):
            return False
        cmd = constants.COMMANDS.KILL_PROCESS.format(pid)
        logger.info(f"Stopping PID:{pid} with command: {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
        return True
