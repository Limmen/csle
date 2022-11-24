import subprocess
import docker
import os
import csle_common.constants.constants as constants
import sys


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
        output = str(output)
        return constants.COMMANDS.SEARCH_PROMETHEUS in str(output) and str(pid) in output

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
        output = str(output)
        return constants.COMMANDS.SEARCH_NODE_EXPORTER in output and str(pid) in output

    @staticmethod
    def is_management_system_running() -> bool:
        """
        Checks if the management system is running on the host

        :return: True if it is running, false otherwise
        """
        pid = ManagementSystemController.read_pid_file(constants.COMMANDS.MANAGEMENT_SYSTEM_PID_FILE)
        if pid == -1:
            return False
        cmd = (constants.COMMANDS.PS_AUX + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PIPE_DELIM +
               constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.GREP + constants.COMMANDS.SPACE_DELIM +
               constants.COMMANDS.SEARCH_MONITOR)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        output = str(output)
        return constants.COMMANDS.SEARCH_MONITOR in output and str(pid) in output

    @staticmethod
    def start_node_exporter() -> bool:
        """
        Starts the node exporter

        :return: True if it was started, False otherwise
        """
        if ManagementSystemController.is_node_exporter_running():
            return False
        cmd = constants.COMMANDS.START_NODE_EXPORTER
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
        return True

    @staticmethod
    def start_management_system() -> bool:
        """
        Starts the REST API

        :return: True if it was started, False otherwise
        """
        if ManagementSystemController.is_management_system_running():
            return False

        cmd = constants.COMMANDS.BUILD_MONITOR
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            out = p.stdout.read(1)
            if p.poll() is not None:
                break
            if out != '':
                try:
                    sys.stdout.write(out.decode("utf-8"))
                except Exception:
                    pass
                sys.stdout.flush()

        cmd = constants.COMMANDS.START_MONITOR
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
        pid = p.pid + 1

        cmd = constants.COMMANDS.SAVE_PID.format(pid, constants.COMMANDS.MANAGEMENT_SYSTEM_PID_FILE)
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
        return True

    @staticmethod
    def stop_node_exporter() -> bool:
        """
        Stops the node exporter

        :return: True if it was stopped, False otherwise
        """
        if not ManagementSystemController.is_node_exporter_running():
            return False
        pid = ManagementSystemController.read_pid_file(constants.COMMANDS.NODE_EXPORTER_PID_FILE)
        cmd = constants.COMMANDS.KILL_PROCESS.format(pid)
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
        return True

    @staticmethod
    def stop_management_system() -> bool:
        """
        Stops the management system

        :return: True if it was stopped, False otherwise
        """
        if not ManagementSystemController.is_management_system_running():
            return False
        pid = ManagementSystemController.read_pid_file(constants.COMMANDS.MANAGEMENT_SYSTEM_PID_FILE)
        cmd = constants.COMMANDS.KILL_PROCESS.format(pid)
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
        return True

    @staticmethod
    def start_prometheus() -> bool:
        """
        Starts Prometheus

        :return: True if it was started, False otherwise
        """
        if ManagementSystemController.is_prometheus_running():
            return False
        cmd = constants.COMMANDS.START_PROMETHEUS
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
        return True

    @staticmethod
    def stop_prometheus() -> bool:
        """
        Stops Prometheus

        :return: True if it was stopped, False otherwise
        """
        if not ManagementSystemController.is_prometheus_running():
            return False
        pid = ManagementSystemController.read_pid_file(constants.COMMANDS.PROMETHEUS_PID_FILE)
        cmd = constants.COMMANDS.KILL_PROCESS.format(pid)
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
    def start_cadvisor() -> bool:
        """
        :return: True if cadvisor was started, otherwise False
        """
        if ManagementSystemController.is_cadvisor_running():
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
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        (output, err) = p.communicate()
        return True

    @staticmethod
    def stop_grafana() -> bool:
        """
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
    def start_grafana() -> bool:
        """
        :return: True if grafana was started, otherwise False
        """
        if ManagementSystemController.is_grafana_running():
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
        cmd = (constants.COMMANDS.PS_AUX + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PIPE_DELIM +
               constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.GREP + constants.COMMANDS.SPACE_DELIM +
               constants.COMMANDS.SEARCH_DOCKER_STATS_MANAGER)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        output = str(output)
        return constants.COMMANDS.SEARCH_DOCKER_STATS_MANAGER in output and str(pid) in output

    @staticmethod
    def start_docker_stats_manager(log_file: str = "docker_stats_manager.log",
                                   log_dir: str = "/var/log/csle", max_workers: int = 10,
                                   port: int = 50046) -> bool:
        """
        Starts the docker stats manager on the docker host if it is not already started

        :param port: the port that the docker stats manager will listen to
        :param log_file: log file of the docker stats manager
        :param log_dir: log dir of the docker stats manager
        :param max_workers: max workers of the docker stats manager
        :return: True if it was started, False otherwise
        """
        if ManagementSystemController.is_statsmanager_running():
            return False
        cmd = constants.COMMANDS.START_DOCKER_STATS_MANAGER.format(port, log_dir, log_file, max_workers)
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        (output, err) = p.communicate()
        return True

    @staticmethod
    def stop_docker_stats_manager() -> bool:
        """
        Stops the statsmanager

        :return: True if it was stopped, False otherwise
        """
        if not ManagementSystemController.is_statsmanager_running():
            return False
        pid = ManagementSystemController.read_pid_file(constants.COMMANDS.DOCKER_STATS_MANAGER_PIDFILE)
        cmd = constants.COMMANDS.KILL_PROCESS.format(pid)
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        (output, err) = p.communicate()
        return True

    @staticmethod
    def is_pid_running(pid: int) -> bool:
        """
        Checks if the given pid is running on the host

        :param pid: the pid to check
        :return: True if it is running, false otherwise
        """
        cmd = (constants.COMMANDS.PS_AUX + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PIPE_DELIM +
               constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.GREP + constants.COMMANDS.SPACE_DELIM + str(pid))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        output = str(output)
        return str(pid) in output

    @staticmethod
    def stop_pid(pid) -> bool:
        """
        Stops a process with a given pid

        :param pid: the pid to stop
        :return: True if the pid was stopped, false if it was not running
        """
        if not ManagementSystemController.is_pid_running(pid):
            return False
        cmd = constants.COMMANDS.KILL_PROCESS.format(pid)
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
        return True
