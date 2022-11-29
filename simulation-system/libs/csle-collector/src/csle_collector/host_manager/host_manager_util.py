from typing import Dict, Any, List
import datetime
import subprocess
import yaml
import csle_collector.constants.constants as constants
from csle_collector.host_manager.failed_login_attempt import FailedLoginAttempt
from csle_collector.host_manager.successful_login import SuccessfulLogin
from csle_collector.host_manager.host_metrics import HostMetrics
import csle_collector.host_manager.host_manager_pb2


class HostManagerUtil:

    @staticmethod
    def read_latest_ts_auth() -> float:
        """
        Measures the timestamp of the latest failed login attempt

        :return: the number of recently failed login attempts
        """
        try:
            cmd = constants.HOST_METRICS.LIST_FAILED_LOGIN_ATTEMPTS
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p.wait()
            login_attempts_str = output.decode()
            login_attempts = login_attempts_str.split("\n")
            login_attempts = list(filter(lambda x: x != "" and len(x) > 14, login_attempts))
            year = datetime.datetime.now().year
            parsed_ts = FailedLoginAttempt.parse_from_str(str(year) + " " +
                                                          " ".join(login_attempts[-1][0:15].split())).timestamp
            return parsed_ts
        except Exception:
            return datetime.datetime.now().timestamp()

    @staticmethod
    def read_failed_login_attempts(failed_auth_last_ts: float) -> int:
        """
        Measures the number of recent failed login attempts

        :param emulation_config: configuration to connect to the node in the emulation
        :return: the number of recently failed login attempts
        """
        cmd = constants.HOST_METRICS.LIST_FAILED_LOGIN_ATTEMPTS
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        login_attempts_str = output.decode()
        login_attempts = login_attempts_str.split("\n")
        login_attempts = list(filter(lambda x: x != "" and len(x) > 14, login_attempts))
        year = datetime.datetime.now().year
        login_attempts = list(map(lambda x: FailedLoginAttempt.parse_from_str(
            str(year) + " " + " ".join(x[0:15].split())), login_attempts))
        login_attempts = list(filter(lambda x: x.timestamp > failed_auth_last_ts, login_attempts))
        return len(login_attempts)

    @staticmethod
    def read_latest_ts_login() -> float:
        """
        Measures the timestamp of the latest successful login attempt

        :return: the number of recently failed login attempts
        """
        try:
            cmd = constants.HOST_METRICS.LIST_SUCCESSFUL_LOGIN_ATTEMPTS
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p.wait()
            logins = output.decode()
            logins = logins.split("\n")
            logins = list(filter(lambda x: x != "" and len(x) > 0 and "wtmp begins" not in x, logins))
            year = datetime.datetime.now().year
            return SuccessfulLogin.parse_from_str(" ".join(logins[0].split()), year=year).timestamp
        except Exception:
            return datetime.datetime.now().timestamp()

    @staticmethod
    def read_successful_login_events(login_last_ts: float) -> int:
        """
        Measures the number of recent successful login attempts

        :param login_last_ts: the timestamp to use when filtering logins
        :return: the number of recently failed login attempts
        """
        cmd = constants.HOST_METRICS.LIST_SUCCESSFUL_LOGIN_ATTEMPTS
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        logins = output.decode()
        logins = logins.split("\n")
        logins = list(filter(lambda x: x != "" and len(x) > 0 and "wtmp begins" not in x, logins))
        year = datetime.datetime.now().year
        successful_logins = list(map(lambda x: SuccessfulLogin.parse_from_str(" ".join(x.split()), year=year), logins))
        successful_logins = list(filter(lambda x: x.timestamp is not None, successful_logins))
        successful_logins = list(filter(lambda x: x.timestamp > login_last_ts, successful_logins))
        return len(successful_logins)

    @staticmethod
    def read_open_connections() -> int:
        """
        Measures the number of open connections to the server

        :return: the number of open connections
        """
        cmd = constants.HOST_METRICS.LIST_OPEN_CONNECTIONS_CMD
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        connections_str = output.decode()
        parts = connections_str.split("Active UNIX domain sockets", 1)
        if len(parts) > 0:
            parts2 = parts[0].split("State")
            if len(parts2) > 1:
                parts3 = parts2[1].split("\n")
                return len(parts3) - 1
        return -1

    @staticmethod
    def read_users() -> int:
        """
        Measures the number of user accounts on the server

        :return: the number of user accounts
        """
        cmd = constants.HOST_METRICS.LIST_USER_ACCOUNTS
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        users_str = output.decode()
        users = users_str.split("\n")
        return len(users)

    @staticmethod
    def read_logged_in_users() -> int:
        """
        Measures the number of logged-in users on the server

        :return: the number of logged in users
        """
        cmd = constants.HOST_METRICS.LIST_LOGGED_IN_USERS_CMD
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        users_str = output.decode()
        users_str = users_str.replace("\n", "")
        users = users_str.split(" ")
        return len(users)

    @staticmethod
    def read_processes() -> int:
        """
        Measures the number of processes on the server

        :param emulation_config: configuration to connect to the node in the emulation
        :return: the number of processes
        """
        try:
            cmd = constants.HOST_METRICS.LIST_NUMBER_OF_PROCESSES
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p.wait()
            processes_str = output.decode()
            num_processes = int(processes_str)
        except Exception:
            num_processes = -1
        return num_processes

    @staticmethod
    def read_host_metrics(failed_auth_last_ts: float, login_last_ts: float) -> HostMetrics:
        """
        Reads the latest metrics from the host

        :param failed_auth_last_ts: the last time-step of read failed authentication attempts
        :param login_last_ts: the last time-step of read successful logins
        :return: The parsed host metrics
        """
        num_logged_in_users = HostManagerUtil.read_logged_in_users()
        num_failed_login_attempts = HostManagerUtil.read_failed_login_attempts(
            failed_auth_last_ts=failed_auth_last_ts)
        num_open_connections = HostManagerUtil.read_open_connections()
        if num_open_connections == -1:
            num_open_connections = 0
        num_login_events = HostManagerUtil.read_successful_login_events(login_last_ts=login_last_ts)
        num_processes = HostManagerUtil.read_processes()
        if num_processes == -1:
            num_processes = 0
        num_users = HostManagerUtil.read_users()
        host_metrics = HostMetrics(
            num_logged_in_users=num_logged_in_users,
            num_failed_login_attempts=num_failed_login_attempts,
            num_open_connections=num_open_connections,
            num_login_events=num_login_events,
            num_processes=num_processes,
            num_users=num_users
        )
        return host_metrics

    @staticmethod
    def host_monitor_dto_to_dict(host_monitor_dto: csle_collector.host_manager.host_manager_pb2.HostMonitorDTO) \
            -> Dict[str, Any]:
        """
        Converts a HostMonitorDTO to a dict

        :param host_monitor_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["running"] = host_monitor_dto.running
        return d

    @staticmethod
    def host_monitor_dto_from_dict(d: Dict[str, Any]) -> csle_collector.host_manager.host_manager_pb2.HostMonitorDTO:
        """
        Converts a dict representation of a HostMonitorDTO to a DTO

        :param d: the dict to convert
        :return: the converted DTO
        """
        host_monitor_dto = csle_collector.host_manager.host_manager_pb2.HostMonitorDTO()
        host_monitor_dto.running = d["running"]
        return host_monitor_dto

    @staticmethod
    def host_metrics_dto_to_dict(host_metrics_dto: csle_collector.host_manager.host_manager_pb2.HostMetricsDTO) \
            -> Dict[str, Any]:
        """
        Converts a HostMetricsDTO to a dict

        :param host_metrics_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["num_logged_in_users"] = host_metrics_dto.num_logged_in_users
        d["num_failed_login_attempts"] = host_metrics_dto.num_failed_login_attempts
        d["num_open_connections"] = host_metrics_dto.num_open_connections
        d["num_login_events"] = host_metrics_dto.num_login_events
        d["num_processes"] = host_metrics_dto.num_processes
        d["num_users"] = host_metrics_dto.num_users
        d["ip"] = host_metrics_dto.ip
        d["timestamp"] = host_metrics_dto.timestamp
        return d

    @staticmethod
    def host_metrics_dto_from_dict(d: Dict[str, Any]) -> csle_collector.host_manager.host_manager_pb2.HostMetricsDTO:
        """
        Converts a dict representation of a HostMetricsDTO to a DTO

        :param d: the dict to convert
        :return: the converted DTO
        """
        host_metrics_dto = csle_collector.host_manager.host_manager_pb2.HostMetricsDTO()
        host_metrics_dto.num_logged_in_users = d["num_logged_in_users"]
        host_metrics_dto.num_failed_login_attempts = d["num_failed_login_attempts"]
        host_metrics_dto.num_open_connections = d["num_open_connections"]
        host_metrics_dto.num_login_events = d["num_login_events"]
        host_metrics_dto.num_processes = d["num_processes"]
        host_metrics_dto.num_users = d["num_users"]
        host_metrics_dto.ip = d["ip"]
        host_metrics_dto.timestamp = d["timestamp"]
        return host_metrics_dto

    @staticmethod
    def host_metrics_dto_empty() -> csle_collector.host_manager.host_manager_pb2.HostMetricsDTO:
        """
        :return: an empty HostMetricsDTO
        """
        host_metrics_dto = csle_collector.host_manager.host_manager_pb2.HostMetricsDTO()
        host_metrics_dto.num_logged_in_users = 0
        host_metrics_dto.num_failed_login_attempts = 0
        host_metrics_dto.num_open_connections = 0
        host_metrics_dto.num_login_events = 0
        host_metrics_dto.num_processes = 0
        host_metrics_dto.num_users = 0
        host_metrics_dto.ip = ""
        host_metrics_dto.timestamp = 0
        return host_metrics_dto

    @staticmethod
    def host_monitor_dto_empty() -> csle_collector.host_manager.host_manager_pb2.HostMonitorDTO:
        """
        :return: an empty HostMonitorDTO
        """
        host_monitor_dto = csle_collector.host_manager.host_manager_pb2.HostMonitorDTO()
        host_monitor_dto.running = False
        return host_monitor_dto

    @staticmethod
    def filebeat_config(log_files_paths: List[str], kibana_ip: str, kibana_port: int, elastic_ip: str,
                        elastic_port: int, num_elastic_shards: int, reload_enabled: bool = False) -> Dict[str, Any]:
        """
        Generates the filebeat.yml config

        :param log_files_paths: the list of log files that filebeat should monitor
        :param kibana_ip: the IP of Kibana where the data should be visualized
        :param kibana_port: the port of Kibana where the data should be visualized
        :param elastic_ip: the IP of elastic where the data should be shipped
        :param elastic_port: the port of elastic where the data should be shipped
        :param num_elastic_shards: the number of elastic shards
        :param reload_enabled: whether automatic reload of modules should be enabled
        :return: the filebeat configuration dict
        """
        filebeat_config = {}
        filebeat_config[constants.FILEBEAT.INPUTS_PROPERTY] = [
            {
                constants.BEATS.TYPE_PROPERTY: constants.BEATS.FILESTREAM_PROPERTY,
                constants.BEATS.ID_PROPERTY: 1,
                constants.BEATS.ENABLED_PROPERTY: True,
                constants.BEATS.PATHS_PROPERTY: [
                    log_files_paths
                ]
            }
        ]
        filebeat_config[constants.FILEBEAT.MODULES_PROPERTY] = {
            constants.BEATS.PATH_PROPERTY: f"{constants.FILEBEAT.MODULES_CONFIG_DIR}*.yml",
            constants.BEATS.RELOAD_ENABLED_PROPERTY: reload_enabled
        }
        filebeat_config[constants.BEATS.SETUP_TEMPLATE_SETTINGS_PROPERTY] = {
            constants.BEATS.INDEX_NUM_SHARDS_PROPERTY: num_elastic_shards
        }
        filebeat_config[constants.BEATS.SETUP_KIBANA_PROPERTY] = {
            constants.BEATS.HOST_PROPERTY: f"{kibana_ip}:{kibana_port}"
        }
        filebeat_config[constants.BEATS.ELASTIC_OUTPUT_PROPERTY] = {
            constants.BEATS.HOSTS_PROPERTY: [f"{elastic_ip}:{elastic_port}"]
        }
        filebeat_config[constants.BEATS.PROCESSORS_PROPERTY] = {
            constants.BEATS.ADD_HOST_METADATA_PROPERTY: {
                constants.BEATS.WHEN_NOT_CONTAIN_TAGS_PROPERTY: constants.BEATS.FORWARDED_PROPERTY
            }
        }
        return filebeat_config

    @staticmethod
    def write_filebeat_config(filebeat_config: Dict[str, Any]) -> None:
        """
        Writes a given filebeat config to disk

        :param filebeat_config: the filebeat config to write
        :return: None
        """
        with open(constants.FILEBEAT.CONFIG_FILE, 'w') as file:
            yaml.dump(filebeat_config, file)

    @staticmethod
    def filebeat_snort_module_config() -> List[Dict[str, Any]]:
        """
        :return: the snort filebeat module config
        """
        snort_config = [
            {
                constants.BEATS.MODULE_PROPERTY: constants.FILEBEAT.SNORT_MODULE,
                constants.BEATS.LOG_PROPERTY: {
                    constants.BEATS.ENABLED_PROPERTY : True,
                    constants.BEATS.VAR_INPUT_PROPERTY: constants.BEATS.FILE_PROPERTY,
                    constants.BEATS.VAR_PATHS_PROPERTY: [
                        constants.SNORT_IDS_ROUTER.SNORT_FAST_LOG_FILE
                    ]
                }
            }
        ]
        return snort_config

    @staticmethod
    def write_filebeat_snort_module_config(snort_config: Dict[str, Any]) -> None:
        """
        Writes a given snort module config to disk

        :param snort_config: the filebeat config to write
        :return: None
        """
        with open(f"{constants.FILEBEAT.MODULES_CONFIG_DIR}{constants.FILEBEAT.SNORT_MODULE_CONFIG_FILE}", 'w') as file:
            yaml.dump(snort_config, file)
