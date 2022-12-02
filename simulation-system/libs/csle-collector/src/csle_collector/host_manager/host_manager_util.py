from typing import Dict, Any, List, Union
import datetime
import subprocess
import yaml
import logging
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
            output = subprocess.run(cmd.split(" "), capture_output=True, text=True)
            login_attempts_str = output.stdout
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
        output = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        login_attempts_str = output.stdout
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
            output = subprocess.run(cmd.split(" "), capture_output=True, text=True)
            logins = output.stdout
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
        output = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        logins = output.stdout
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
        output = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        connections_str = output.stdout
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
        output = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        users_str = output.stdout
        users = users_str.split("\n")
        return len(users)

    @staticmethod
    def read_logged_in_users() -> int:
        """
        Measures the number of logged-in users on the server

        :return: the number of logged in users
        """
        cmd = constants.HOST_METRICS.LIST_LOGGED_IN_USERS_CMD
        output = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        users_str = output.stdout
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
            output = subprocess.run(cmd.split(" "), capture_output=True, text=True)
            processes_str = output.stdout
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
    def host_monitor_dto_to_dict(host_dto: csle_collector.host_manager.host_manager_pb2.HostStatusDTO) \
            -> Dict[str, Any]:
        """
        Converts a HostStatusDTO to a dict

        :param host_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["monitor_running"] = host_dto.monitor_running
        d["filebeat_running"] = host_dto.filebeat_running
        d["packetbeat_running"] = host_dto.packetbeat_running
        d["metricbeat_running"] = host_dto.metricbeat_running
        d["heartbeat_running"] = host_dto.heartbeat_running
        return d

    @staticmethod
    def host_monitor_dto_from_dict(d: Dict[str, Any]) -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        Converts a dict representation of a HostStatusDTO to a DTO

        :param d: the dict to convert
        :return: the converted DTO
        """
        host_dto = csle_collector.host_manager.host_manager_pb2.HostStatusDTO()
        host_dto.monitor_running = d["monitor_running"]
        host_dto.filebeat_running = d["filebeat_running"]
        host_dto.packetbeat_running = d["packetbeat_running"]
        host_dto.metricbeat_running = d["metricbeat_running"]
        host_dto.heartbeat_running = d["heartbeat_running"]
        return host_dto

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
    def host_monitor_dto_empty() -> csle_collector.host_manager.host_manager_pb2.HostStatusDTO:
        """
        :return: an empty HostStatusDTO
        """
        host_monitor_dto = csle_collector.host_manager.host_manager_pb2.HostStatusDTO()
        host_monitor_dto.monitor_running = False
        host_monitor_dto.filebeat_running = False
        host_monitor_dto.packetbeat_running = False
        host_monitor_dto.metricbeat_running = False
        host_monitor_dto.heartbeat_running = False
        return host_monitor_dto

    @staticmethod
    def filebeat_config(log_files_paths: List[str], kibana_ip: str, kibana_port: int, elastic_ip: str,
                        elastic_port: int, num_elastic_shards: int, kafka_topics: List[str], kafka_ip: str,
                        kafka_port: int, reload_enabled: bool = False, kafka: bool = False) \
            -> Dict[str, Any]:
        """
        Generates the filebeat.yml config

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
        :return: the filebeat configuration dict
        """
        filebeat_config = {}
        filebeat_config[constants.FILEBEAT.INPUTS_PROPERTY] = [
            {
                constants.BEATS.TYPE_PROPERTY: constants.BEATS.FILESTREAM_PROPERTY,
                constants.BEATS.ID_PROPERTY: 1,
                constants.BEATS.ENABLED_PROPERTY: True,
                constants.BEATS.PATHS_PROPERTY: log_files_paths
            }
        ]
        if kafka:
            filebeat_config[constants.FILEBEAT.INPUTS_PROPERTY].append(
                {
                    constants.BEATS.TYPE_PROPERTY: constants.BEATS.KAFKA_PROPERTY,
                    constants.BEATS.ENABLED_PROPERTY: True,
                    constants.BEATS.GROUP_ID_PROPERTY: constants.FILEBEAT.FILEBEAT_GROUP_ID,
                    constants.BEATS.TOPICS_PROPERTY: kafka_topics,
                    constants.BEATS.HOSTS_PROPERTY: [f"{kafka_ip}:{kafka_port}"],
                }
            )
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
    def write_yaml_config(config: Union[Dict[str, Any], List[Dict[str, Any]]], path: str) -> None:
        """
        Writes a given filebeat config to disk

        :param config: the filebeat config to write
        :param path: the path to write the file to
        :return: None
        """
        logging.info(f"Writing configuration file to path: {path}")
        with open(path, 'w') as file:
            yaml.dump(config, file)

    @staticmethod
    def filebeat_snort_module_config() -> List[Dict[str, Any]]:
        """
        :return: the snort filebeat module config
        """
        snort_config = [
            {
                constants.BEATS.MODULE_PROPERTY: constants.FILEBEAT.SNORT_MODULE,
                constants.BEATS.LOG_PROPERTY: {
                    constants.BEATS.ENABLED_PROPERTY: True,
                    constants.BEATS.VAR_INPUT_PROPERTY: constants.BEATS.FILE_PROPERTY,
                    constants.BEATS.VAR_PATHS_PROPERTY: [
                        constants.SNORT_IDS_ROUTER.SNORT_FAST_LOG_FILE
                    ]
                }
            }
        ]
        return snort_config

    @staticmethod
    def filebeat_elasticsearch_module_config() -> List[Dict[str, Any]]:
        """
        :return: the elasticsearch filebeat module config
        """
        elastic_config = [
            {
                constants.BEATS.MODULE_PROPERTY: constants.FILEBEAT.ELASTICSEARCH_MODULE,
                constants.BEATS.SERVER_PROPERTY: {
                    constants.BEATS.ENABLED_PROPERTY: True,
                    constants.BEATS.VAR_PATHS_PROPERTY: [
                        f"{constants.ELK.ELASTICSEARCH_LOG_DIR}*.log",
                        f"{constants.ELK.ELASTICSEARCH_LOG_DIR}*_server.json"
                    ]
                }
            }
        ]
        return elastic_config

    @staticmethod
    def filebeat_logstash_module_config() -> List[Dict[str, Any]]:
        """
        :return: the logstash filebeat module config
        """
        logstash_config = [
            {
                constants.BEATS.MODULE_PROPERTY: constants.FILEBEAT.LOGSTASH_MODULE,
                constants.BEATS.LOG_PROPERTY: {
                    constants.BEATS.ENABLED_PROPERTY: True,
                    constants.BEATS.VAR_PATHS_PROPERTY: [
                        f"{constants.ELK.LOGSTASH_LOG_DIR}logstash.log*"
                    ]
                },
                constants.BEATS.SLOWLOG_PROPERTY: {
                    constants.BEATS.ENABLED_PROPERTY: True,
                    constants.BEATS.VAR_PATHS_PROPERTY: [
                        f"{constants.ELK.LOGSTASH_LOG_DIR}logstash-slowlog.log*"
                    ]
                }
            }
        ]
        return logstash_config

    @staticmethod
    def filebeat_kibana_module_config() -> List[Dict[str, Any]]:
        """
        :return: the kibana filebeat module config
        """
        kibana_config = [
            {
                constants.BEATS.MODULE_PROPERTY: constants.FILEBEAT.KIBANA_MODULE,
                constants.BEATS.LOG_PROPERTY: {
                    constants.BEATS.ENABLED_PROPERTY: True,
                    constants.BEATS.VAR_PATHS_PROPERTY: [
                        f"{constants.ELK.KIBANA_LOG_DIR}*.log"
                    ]
                },
                constants.BEATS.AUDIT_PROPERTY: {
                    constants.BEATS.ENABLED_PROPERTY: True
                }
            }
        ]
        return kibana_config

    @staticmethod
    def filebeat_system_module_config() -> List[Dict[str, Any]]:
        """
        :return: the system filebeat module config
        """
        system_config = [
            {
                constants.BEATS.MODULE_PROPERTY: constants.FILEBEAT.SYSTEM_MODULE,
                constants.BEATS.SYSLOG_PROPERTY: {
                    constants.BEATS.ENABLED_PROPERTY: True,
                    constants.BEATS.VAR_PATHS_PROPERTY: [
                        f"{constants.SYSTEM.SYSLOG}*"
                    ]
                },
                constants.BEATS.AUTH_PROPERTY: {
                    constants.BEATS.ENABLED_PROPERTY: True,
                    constants.BEATS.VAR_PATHS_PROPERTY: [
                        f"{constants.SYSTEM.AUTH_LOG}"
                    ]
                }
            }
        ]
        return system_config

    @staticmethod
    def filebeat_kafka_module_config() -> List[Dict[str, Any]]:
        """
        :return: the kafka filebeat module config
        """
        system_config = [
            {
                constants.BEATS.MODULE_PROPERTY: constants.FILEBEAT.KAFKA_MODULE,
                constants.BEATS.LOG_PROPERTY: {
                    constants.BEATS.ENABLED_PROPERTY: True,
                    constants.BEATS.VAR_PATHS_PROPERTY: [
                        f"{constants.KAFKA.DIR}controller.log*",
                        f"{constants.KAFKA.DIR}server.log*",
                        f"{constants.KAFKA.DIR}state-change.log*",
                        f"{constants.KAFKA.DIR}kafka-*.log*"
                    ]
                }
            }
        ]
        return system_config

    @staticmethod
    def packetbeat_config(kibana_ip: str, kibana_port: int, elastic_ip: str, elastic_port: int,
                          num_elastic_shards: int) -> Dict[str, Any]:
        """
        Generates the packetbeat.yml config

        :param kibana_ip: the IP of Kibana where the data should be visualized
        :param kibana_port: the port of Kibana where the data should be visualized
        :param elastic_ip: the IP of elastic where the data should be shipped
        :param elastic_port: the port of elastic where the data should be shipped
        :param num_elastic_shards: the number of elastic shards
        :return: the filebeat configuration dict
        """
        packetbeat_config = {}
        packetbeat_config[constants.PACKETBEAT.INTERFACES_TYPE_PROPERTY] = constants.PACKETBEAT.AF_PACKET_PROPERTY
        packetbeat_config[constants.PACKETBEAT.INTERFACES_DEVICE_PROPERTY] = constants.PACKETBEAT.ANY_DEVICE_PROPERTY
        packetbeat_config[constants.PACKETBEAT.FLOWS] = {
            constants.PACKETBEAT.TIMEOUT_PROPERTY: "30s",
            constants.BEATS.PERIOD_PROPERTY: "10s"
        }
        packetbeat_config[constants.PACKETBEAT.PROTOCOLS] = [
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.ICMP_PROTOCOL,
                constants.BEATS.ENABLED_PROPERTY: True
            },
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.AMQP_PROTOCOL,
                constants.PACKETBEAT.PORTS_PROPERTY: constants.PACKETBEAT.AMQP_PORTS
            },
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.CASSANDRA_PROTOCOL,
                constants.PACKETBEAT.PORTS_PROPERTY: constants.PACKETBEAT.CASSANDRA_PORTS
            },
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.DHCPV4_PROTOCOL,
                constants.PACKETBEAT.PORTS_PROPERTY: constants.PACKETBEAT.DHCPV4_PORTS
            },
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.DNS_PROTOCOL,
                constants.PACKETBEAT.PORTS_PROPERTY: constants.PACKETBEAT.DNS_PORTS
            },
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.HTTP_PROTOCOL,
                constants.PACKETBEAT.PORTS_PROPERTY: constants.PACKETBEAT.HTTP_PORTS
            },
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.MEMCACHE_PROTOCOL,
                constants.PACKETBEAT.PORTS_PROPERTY: constants.PACKETBEAT.MEMCACHE_PORTS
            },
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.MYSQL_PROTOCOL,
                constants.PACKETBEAT.PORTS_PROPERTY: constants.PACKETBEAT.MYSQL_PORTS
            },
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.PGSQL_PROTOCOL,
                constants.PACKETBEAT.PORTS_PROPERTY: constants.PACKETBEAT.PGSQL_PORTS
            },
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.REDIS_PROTOCOL,
                constants.PACKETBEAT.PORTS_PROPERTY: constants.PACKETBEAT.REDIS_PORTS
            },
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.THRIFT_PROTOCOL,
                constants.PACKETBEAT.PORTS_PROPERTY: constants.PACKETBEAT.THRIFT_PORTS
            },
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.MONGODB_PROTOCOL,
                constants.PACKETBEAT.PORTS_PROPERTY: constants.PACKETBEAT.MONGODB_PORTS
            },
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.NFS_PROTOCOL,
                constants.PACKETBEAT.PORTS_PROPERTY: constants.PACKETBEAT.NFS_PORTS
            },
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.TLS_PROTOCOL,
                constants.PACKETBEAT.PORTS_PROPERTY: constants.PACKETBEAT.TLS_PORTS
            },
            {
                constants.BEATS.TYPE_PROPERTY: constants.PACKETBEAT.SIP_PROTOCOL,
                constants.PACKETBEAT.PORTS_PROPERTY: constants.PACKETBEAT.SIP_PORTS
            }
        ]
        packetbeat_config[constants.BEATS.SETUP_TEMPLATE_SETTINGS_PROPERTY] = {
            constants.BEATS.INDEX_NUM_SHARDS_PROPERTY: num_elastic_shards
        }
        packetbeat_config[constants.BEATS.SETUP_KIBANA_PROPERTY] = {
            constants.BEATS.HOST_PROPERTY: f"{kibana_ip}:{kibana_port}"
        }
        packetbeat_config[constants.BEATS.ELASTIC_OUTPUT_PROPERTY] = {
            constants.BEATS.HOSTS_PROPERTY: [f"{elastic_ip}:{elastic_port}"]
        }
        packetbeat_config[constants.BEATS.PROCESSORS_PROPERTY] = {
            constants.BEATS.ADD_HOST_METADATA_PROPERTY: {
                constants.BEATS.WHEN_NOT_CONTAIN_TAGS_PROPERTY: constants.BEATS.FORWARDED_PROPERTY
            }
        }
        return packetbeat_config

    @staticmethod
    def metricbeat_config(kibana_ip: str, kibana_port: int, elastic_ip: str,
                          elastic_port: int, num_elastic_shards: int, reload_enabled: bool = False) -> Dict[str, Any]:
        """
        Generates the metricbeat.yml config

        :param kibana_ip: the IP of Kibana where the data should be visualized
        :param kibana_port: the port of Kibana where the data should be visualized
        :param elastic_ip: the IP of elastic where the data should be shipped
        :param elastic_port: the port of elastic where the data should be shipped
        :param num_elastic_shards: the number of elastic shards
        :param reload_enabled: whether automatic reload of modules should be enabled
        :return: the metricbeat configuration dict
        """
        metricbeat_config = {}
        metricbeat_config[constants.METRICBEAT.MODULES_PROPERTY] = {
            constants.BEATS.PATH_PROPERTY: f"{constants.METRICBEAT.MODULES_CONFIG_DIR}*.yml",
            constants.BEATS.RELOAD_ENABLED_PROPERTY: reload_enabled
        }
        metricbeat_config[constants.BEATS.SETUP_TEMPLATE_SETTINGS_PROPERTY] = {
            constants.BEATS.INDEX_NUM_SHARDS_PROPERTY: num_elastic_shards
        }
        metricbeat_config[constants.BEATS.SETUP_KIBANA_PROPERTY] = {
            constants.BEATS.HOST_PROPERTY: f"{kibana_ip}:{kibana_port}"
        }
        metricbeat_config[constants.BEATS.ELASTIC_OUTPUT_PROPERTY] = {
            constants.BEATS.HOSTS_PROPERTY: [f"{elastic_ip}:{elastic_port}"]
        }
        metricbeat_config[constants.BEATS.PROCESSORS_PROPERTY] = {
            constants.BEATS.ADD_HOST_METADATA_PROPERTY: {
                constants.BEATS.WHEN_NOT_CONTAIN_TAGS_PROPERTY: constants.BEATS.FORWARDED_PROPERTY
            }
        }
        return metricbeat_config

    @staticmethod
    def metricbeat_elasticsearch_module_config(elastic_ip: str, elastic_port: int) -> List[Dict[str, Any]]:
        """
        :return: the elasticsearch metricbeat module config
        """
        elastic_config = [
            {
                constants.BEATS.MODULE_PROPERTY: constants.FILEBEAT.ELASTICSEARCH_MODULE,
                constants.BEATS.PERIOD_PROPERTY: "10s",
                constants.BEATS.HOSTS_PROPERTY: [f"{elastic_ip}:{elastic_port}"]
            }
        ]
        return elastic_config

    @staticmethod
    def metricbeat_kibana_module_config(kibana_ip: str, kibana_port: int) -> List[Dict[str, Any]]:
        """
        Creates the kibana metricbeat module configuration

        :param kibana_ip: the kibana host IP
        :param kibana_port: the kibana host port
        :return: the kibana metricbeat module config
        """
        kibana_config = [
            {
                constants.BEATS.MODULE_PROPERTY: constants.METRICBEAT.KIBANA_MODULE,
                constants.BEATS.PERIOD_PROPERTY: "10s",
                constants.BEATS.HOSTS_PROPERTY: [f"{kibana_ip}:{kibana_port}"]
            }
        ]
        return kibana_config

    @staticmethod
    def metricbeat_logstash_module_config(logstash_ip: str, logstash_port: int) -> List[Dict[str, Any]]:
        """
        Creates the logstash metricbeat module configuration

        :param logstash_ip: the kibana host IP
        :param logstash_port: the kibana host port
        :return: the kibana metricbeat module config
        """
        logstash_config = [
            {
                constants.BEATS.MODULE_PROPERTY: constants.METRICBEAT.LOGSTASH_MODULE,
                constants.BEATS.PERIOD_PROPERTY: "10s",
                constants.BEATS.HOSTS_PROPERTY: [f"{logstash_ip}:{logstash_port}"]
            }
        ]
        return logstash_config

    @staticmethod
    def metricbeat_kafka_module_config(kafka_ip: str, kafka_port: int) -> List[Dict[str, Any]]:
        """
        Creates the kafka metricbeat module configuration

        :param kafka_ip: the kibana host IP
        :param kafka_port: the kibana host port
        :return: the kafka metricbeat module config
        """
        kafka_config = [
            {
                constants.BEATS.MODULE_PROPERTY: constants.METRICBEAT.KAFKA_MODULE,
                constants.BEATS.PERIOD_PROPERTY: "10s",
                constants.BEATS.HOSTS_PROPERTY: [f"{kafka_ip}:{kafka_port}"]
            }
        ]
        return kafka_config

    @staticmethod
    def metricbeat_system_module_config() -> List[Dict[str, Any]]:
        """
        Creates the system metricbeat module configuration

        :return: the system metricbeat module config
        """
        system_config = [
            {
                constants.BEATS.MODULE_PROPERTY: constants.METRICBEAT.SYSTEM_MODULE,
                constants.BEATS.PERIOD_PROPERTY: "10s",
                constants.BEATS.METRICSETS_PROPERTY: [
                    constants.METRICBEAT.CPU_METRIC,
                    constants.METRICBEAT.LOAD_METRIC,
                    constants.METRICBEAT.MEMORY_METRIC,
                    constants.METRICBEAT.NETWORK_METRIC,
                    constants.METRICBEAT.PROCESS_METRIC,
                    constants.METRICBEAT.PROCESS_SUMMARY_METRIC,
                    constants.METRICBEAT.SOCKET_SUMMARY_METRIC
                ],
                constants.BEATS.ENABLED_PROPERTY: True,
                constants.METRICBEAT.PROCESSES_PROPERTY: [".*"],
                constants.METRICBEAT.CPU_METRICS_PROPERTY: [constants.METRICBEAT.PERCENTAGES_PROPERTY,
                                                            constants.METRICBEAT.NORMALIZED_PERCENTAGES_PROPERTY],
                constants.METRICBEAT.CORE_METRICS_PROPERTY: [constants.METRICBEAT.PERCENTAGES_PROPERTY]
            }
        ]
        return system_config

    @staticmethod
    def metricbeat_linux_module_config() -> List[Dict[str, Any]]:
        """
        Creates the linux metricbeat module configuration

        :return: the linux metricbeat module config
        """
        linux_config = [
            {
                constants.BEATS.MODULE_PROPERTY: constants.METRICBEAT.LINUX_MODULE,
                constants.BEATS.PERIOD_PROPERTY: "10s",
                constants.BEATS.METRICSETS_PROPERTY: {
                    constants.METRICBEAT.PAGEINFO_METRIC,
                    constants.METRICBEAT.SUMMARY_METRIC
                },
                constants.BEATS.ENABLED_PROPERTY: True
            }
        ]
        return linux_config

    @staticmethod
    def heartbeat_config(kibana_ip: str, kibana_port: int, elastic_ip: str, elastic_port: int,
                         num_elastic_shards: int, hosts_to_monitor: List[str]) -> Dict[str, Any]:
        """
        Generates the heartbeat.yml config

        :param kibana_ip: the IP of Kibana where the data should be visualized
        :param kibana_port: the port of Kibana where the data should be visualized
        :param elastic_ip: the IP of elastic where the data should be shipped
        :param elastic_port: the port of elastic where the data should be shipped
        :param num_elastic_shards: the number of elastic shards
        :param hosts_to_monitor: a list of host IP addresses to monitor
        :return: the heartbeat configuration dict
        """
        heartbeat_config = {}
        heartbeat_config[constants.HEARTBEAT.HEARTBEAT_MONITORS_PROPERTY] = [
            {
                constants.BEATS.TYPE_PROPERTY: constants.HEARTBEAT.ICMP_MONITOR_TYPE,
                constants.HEARTBEAT.SCHEDULE_PROPERTY: '*/5 * * * * * *',
                constants.BEATS.HOSTS_PROPERTY: hosts_to_monitor,
                constants.BEATS.ID_PROPERTY: constants.HEARTBEAT.CSLE_MONITOR_SERVICE_ID,
                constants.BEATS.NAME_PROPERTY: constants.HEARTBEAT.CSLE_MONITOR_SERVICE_NAME
            }
        ]
        heartbeat_config[constants.BEATS.SETUP_TEMPLATE_SETTINGS_PROPERTY] = {
            constants.BEATS.INDEX_NUM_SHARDS_PROPERTY: num_elastic_shards
        }
        heartbeat_config[constants.BEATS.SETUP_KIBANA_PROPERTY] = {
            constants.BEATS.HOST_PROPERTY: f"{kibana_ip}:{kibana_port}"
        }
        heartbeat_config[constants.BEATS.ELASTIC_OUTPUT_PROPERTY] = {
            constants.BEATS.HOSTS_PROPERTY: [f"{elastic_ip}:{elastic_port}"]
        }
        heartbeat_config[constants.BEATS.PROCESSORS_PROPERTY] = {
            constants.BEATS.ADD_HOST_METADATA_PROPERTY: {
                constants.BEATS.WHEN_NOT_CONTAIN_TAGS_PROPERTY: constants.BEATS.FORWARDED_PROPERTY
            }
        }
        return heartbeat_config
