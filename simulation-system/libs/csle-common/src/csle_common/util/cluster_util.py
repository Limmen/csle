import os
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.config import Config
from csle_common.logging.log import Logger
from csle_common.util.general_util import GeneralUtil


class ClusterUtil:
    """
    Class with utility related to cluster management
    """

    @staticmethod
    def am_i_leader(ip: str, config: Config) -> bool:
        """
        Checks if a given IP is leader or not

        :param ip: the ip to check
        :param config: the cluster configuration
        :return: True if leader, False otherwise
        """
        leader = False
        for node in config.cluster_config.cluster_nodes:
            if node.ip == ip:
                leader = node.leader
        return leader

    @staticmethod
    def get_leader_ip(config: Config) -> str:
        """
        Returns the IP of the leader node

        :param config: the cluster configuration
        :return: The IP address of the leader node
        """
        for node in config.cluster_config.cluster_nodes:
            if node.leader:
                return node.ip
        raise ValueError("No leader node found")

    @staticmethod
    def get_config() -> Config:
        """
        Gets the current cluster config from the metastore or from disk depending on if it is the leader node or
        not
        :return: the cluster config
        """
        config = MetastoreFacade.get_config(id=1)
        if config is None:
            config = Config.read_config_file()
        if config.localhost:
            ip = constants.COMMON.LOCALHOST_127_0_0_1
        else:
            ip = GeneralUtil.get_host_ip()
        constants.METADATA_STORE.HOST = ip
        constants.CLUSTER_CONFIG.IP = ip
        leader = ClusterUtil.am_i_leader(ip=ip, config=config)
        constants.CLUSTER_CONFIG.LEADER = leader
        if leader:
            config = Config.read_config_file()
            current_config = MetastoreFacade.get_config(id=1)
            if current_config is None:
                Logger.__call__().get_logger().info("Saving config to metastore")
                MetastoreFacade.save_config(config)
            else:
                MetastoreFacade.update_config(config=config, id=1)
        return config

    @staticmethod
    def set_config_parameters_from_config_file() -> None:
        """
        Reads the config file from $CSLE_HOME/config.json and initializes certain config parameters

        :return: None
        """
        if constants.CONFIG_FILE.CSLE_HOME_ENV_PARAM in os.environ:
            csle_home = os.environ[constants.CONFIG_FILE.CSLE_HOME_ENV_PARAM]
        else:
            raise Exception(f"The environment parameter {constants.CONFIG_FILE.CSLE_HOME_ENV_PARAM} is not set")
        config_file_path = f"{csle_home}{constants.COMMANDS.SLASH_DELIM}" \
                           f"{constants.CONFIG_FILE.CONFIG_FILE_NAME}"
        try:
            config = ClusterUtil.get_config()
            constants.CONFIG_FILE.PARSED_CONFIG = config
            constants.CSLE_ADMIN.MANAGEMENT_USER = config.management_admin_username_default
            constants.CSLE_ADMIN.MANAGEMENT_PW = config.management_admin_password_default
            constants.CSLE_ADMIN.MANAGEMENT_EMAIL = config.management_admin_email_default
            constants.CSLE_ADMIN.MANAGEMENT_ORGANIZATION = config.management_admin_organization_default
            constants.CSLE_ADMIN.MANAGEMENT_FIRST_NAME = config.management_admin_first_name_default
            constants.CSLE_ADMIN.MANAGEMENT_LAST_NAME = config.management_admin_last_name_default
            constants.CSLE_ADMIN.SSH_USER = config.ssh_admin_username
            constants.CSLE_ADMIN.SSH_PW = config.ssh_admin_password
            constants.CSLE_GUEST.MANAGEMENT_USER = config.management_guest_username_default
            constants.CSLE_GUEST.MANAGEMENT_PW = config.management_guest_password_default
            constants.CSLE_GUEST.MANAGEMENT_EMAIL = config.management_guest_email_default
            constants.CSLE_GUEST.MANAGEMENT_ORGANIZATION = config.management_guest_organization_default
            constants.CSLE_GUEST.MANAGEMENT_FIRST_NAME = config.management_guest_first_name_default
            constants.CSLE_GUEST.MANAGEMENT_LAST_NAME = config.management_guest_last_name_default
            constants.AGENT.USER = config.ssh_agent_username
            constants.AGENT.PW = config.ssh_agent_password
            constants.METADATA_STORE.USER = config.metastore_user
            constants.METADATA_STORE.PASSWORD = config.metastore_password
            constants.METADATA_STORE.DBNAME = config.metastore_database_name
            constants.COMMANDS.PGADMIN_USERNAME = config.pgadmin_username
            constants.COMMANDS.PGADMIN_PW = config.pgadmin_password
            constants.COMMANDS.GRAFANA_USERNAME = config.grafana_username
            constants.COMMANDS.GRAFANA_PW = config.grafana_password
            constants.COMMANDS.PGADMIN_PW = config.pgadmin_password
            constants.COMMANDS.NODE_EXPORTER_PORT = config.node_exporter_port
            constants.COMMANDS.GRAFANA_PORT = config.grafana_port
            constants.COMMANDS.MANAGEMENT_SYSTEM_PORT = config.management_system_port
            constants.COMMANDS.CADVISOR_PORT = config.cadvisor_port
            constants.COMMANDS.PGADMIN_PORT = config.pgadmin_port
            constants.COMMANDS.PROMETHEUS_PORT = config.prometheus_port
            constants.COMMANDS.NODE_EXPORTER_PID_FILE = config.node_exporter_pid_file
            constants.COMMANDS.CSLE_MGMT_WEBAPP_PID_FILE = config.csle_mgmt_webapp_pid_file
            constants.COMMANDS.NODE_EXPORTER_LOG_FILE = config.node_exporter_log_file
            constants.COMMANDS.DOCKER_STATS_MANAGER_OUTFILE = config.docker_stats_manager_outfile
            constants.COMMANDS.DOCKER_STATS_MANAGER_PIDFILE = config.docker_stats_manager_pidfile
            constants.COMMANDS.PROMETHEUS_PID_FILE = config.prometheus_pid_file
            constants.COMMANDS.PROMETHEUS_LOG_FILE = config.prometheus_log_file
            constants.COMMANDS.POSTGRESQL_LOG_DIR = config.postgresql_log_dir
            constants.COMMANDS.NGINX_LOG_DIR = config.nginx_log_dir
            constants.COMMANDS.FLASK_LOG_FILE = config.flask_log_file
            constants.LOGGING.DEFAULT_LOG_DIR = config.default_log_dir
            Logger.__call__().get_logger().info(f"Successfully initialized configuration "
                                                f"from configuration file: {config_file_path}")
        except Exception as e:
            Logger.__call__().get_logger().info(f"Failed to read configuration file from: {config_file_path}. "
                                                f"Exception: {str(e)}, {repr(e)}")
