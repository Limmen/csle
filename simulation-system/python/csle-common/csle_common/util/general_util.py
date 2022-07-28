import io
import json
import os
import csle_common.constants.constants as constants
from csle_common.logging.log import Logger


class GeneralUtil:
    """
    Class with general utility functions
    """

    @staticmethod
    def replace_first_octet_of_ip(ip: str, ip_first_octet: int) -> str:
        """
        Utility function for changing the first octet in an IP address

        :param ip: the IP to modify
        :param ip_first_octet: the first octet to insert
        :return: the new IP
        """
        index_of_first_octet_end = ip.find(".")
        return str(ip_first_octet) + ip[index_of_first_octet_end:]

    @staticmethod
    def set_config_parameters_from_config_file() -> None:
        """
        Reads the config file from $CSLE_HOME/config.json and initializes certain config parameters

        :return: None
        """
        csle_home = os.environ[constants.CONFIG_FILE.CSLE_HOME_ENV_PARAM]
        config_file_path = f"{csle_home}{constants.COMMANDS.SLASH_DELIM}" \
                           f"{constants.CONFIG_FILE.CONFIG_FILE_NAME}"
        try:
            with io.open(config_file_path, 'r', encoding='utf-8') as f:
                json_str = f.read()
                config_dict = json.loads(json_str)
                constants.CSLE_ADMIN.USER = config_dict["admin_username"]
                constants.CSLE_ADMIN.PW = config_dict["admin_password"]
                constants.AGENT.USER = config_dict["agent_username"]
                constants.AGENT.PW = config_dict["agent_password"]

                constants.METADATA_STORE.USER = config_dict["database_user"]
                constants.METADATA_STORE.PASSWORD = config_dict["database_password"]
                constants.METADATA_STORE.HOST = config_dict["database_host"]
                constants.METADATA_STORE.DBNAME = config_dict["database_name"]
                constants.COMMANDS.NODE_EXPORTER_PORT = config_dict["node_exporter_port"]
                constants.COMMANDS.GRAFANA_PORT = config_dict["grafana_port"]
                constants.COMMANDS.MONITOR_PORT = config_dict["monitor_port"]
                constants.COMMANDS.PROXY_PORT = config_dict["proxy_port"]
                constants.COMMANDS.CADVISOR_PORT = config_dict["cadvisor_port"]
                constants.COMMANDS.PROMETHEUS_PORT = config_dict["prometheus_port"]
                constants.COMMANDS.NODE_EXPORTER_PORT = config_dict["node_exporter_pid_file"]
                constants.COMMANDS.MONITOR_PID_FILE = config_dict["monitor_pid_file"]
                constants.COMMANDS.PROXY_PID_FILE = config_dict["proxy_pid_file"]
                constants.COMMANDS.NODE_EXPORTER_LOG_FILE = config_dict["node_exporter_log_file"]
                constants.COMMANDS.DOCKER_STATS_MANAGER_OUTFILE = config_dict["docker_stats_manager_outfile"]
                constants.COMMANDS.DOCKER_STATS_MANAGER_PIDFILE = config_dict["docker_stats_manager_pidfile"]
                constants.COMMANDS.PROMETHEUS_PID_FILE = config_dict["prometheus_pid_file"]
                constants.COMMANDS.PROMETHEUS_LOG_FILE = config_dict["prometheus_log_file"]
                constants.COMMANDS.PROMETHEUS_CONFIG_FILE = config_dict["prometheus_config_file"]
                constants.LOGGING.DEFAULT_LOG_DIR = config_dict["default_log_dir"]
                Logger.__call__().get_logger().info(f"Successfully initialized configuration "
                                                    f"from configuration file: {config_file_path}")
        except Exception as e:
            Logger.__call__().get_logger().info(f"Failed to read configuration file from: {config_file_path}. "
                                                f"Exception: {str(e)}, {repr(e)}")
