from typing import Dict, Any
from csle_common.dao.emulation_config.cluster_config import ClusterConfig


class Config:
    """
    A DTO Class representing the CSLE configuration
    """

    def __init__(self, management_admin_username_default: str, management_admin_password_default: str,
                 management_admin_first_name_default: str, management_admin_last_name_default: str,
                 management_admin_email_default: str, management_admin_organization_default: str,
                 management_guest_username_default: str, management_guest_password_default: str,
                 management_guest_first_name_default: str, management_guest_last_name_default: str,
                 management_guest_email_default: str, management_guest_organization_default: str,
                 ssh_admin_username: str, ssh_admin_password: str, ssh_agent_username: str, ssh_agent_password: str,
                 metastore_user: str, metastore_password: str, metastore_database_name: str, metastore_ip: str,
                 node_exporter_port: int, grafana_port: int, proxy_port: int,
                 management_system_port: int, cadvisor_port: int, prometheus_port: int, node_exporter_pid_file: str,
                 management_system_pid_file: str, docker_stats_manager_log_file: str, docker_stats_manager_log_dir: str,
                 docker_stats_manager_port: int, docker_stats_manager_max_workers: int,
                 docker_stats_manager_outfile: str, docker_stats_manager_pidfile: str, prometheus_pid_file: str,
                 prometheus_log_file: str, prometheus_config_file: str, default_log_dir: str,
                 cluster_config: ClusterConfig):
        """
        Initializes the DTO

        :param management_admin_username_default: the default admin username to the management system
        :param management_admin_password_default: the default admin password to the management system
        :param management_admin_first_name_default: the default first name of the admin in the management system
        :param management_admin_last_name_default: the default last name of the admin in the management system
        :param management_admin_email_default: the default email of the admin in the management system
        :param management_admin_organization_default: the default organization of the admin in the management system
        :param management_guest_username_default: the default username of the guest user in the management system
        :param management_guest_password_default: teh default password of the guest user in the management system
        :param management_guest_first_name_default: teh default first name of the guest user in the management system
        :param management_guest_last_name_default: the default last name of the guest user in the management system
        :param management_guest_email_default: the default email of the guest user in the management system
        :param management_guest_organization_default: the default organization of the guest user in the management system
        :param ssh_admin_username: the default SSH admin username to containers in emulation environments
        :param ssh_admin_password: the default SSH admin password to containers in emulation environments
        :param ssh_agent_username: the default SSH agent username to containers in emulation environments
        :param ssh_agent_password: the default SSH agent password to containers in emulation environments
        :param metastore_user: the default user to the metastore
        :param metastore_password: the default password to the metastore
        :param metastore_database_name: the default metastore database name
        :param metastore_ip: the default ip to the metastore
        :param node_exporter_port: the default port to run node_exporter
        :param grafana_port: the default port to run grafana
        :param proxy_port: the default port to run the proxy
        :param management_system_port: the default port to run the management system
        :param cadvisor_port: the default port to run c_advisor
        :param prometheus_port: the default port to run prometheus
        :param node_exporter_pid_file: the default port to run node_exporter
        :param management_system_pid_file: the file to save the PID of the management system
        :param docker_stats_manager_log_file: the file to save the logs of docker statsmanager
        :param docker_stats_manager_log_dir: the directory to save the logs of the docker statsmanager
        :param docker_stats_manager_port: the port of the docker statsmanager
        :param docker_stats_manager_max_workers: the maximum number of GRPC workers of the docker statsmanager
        :param docker_stats_manager_outfile: the outputfile of the docker statsmanaer
        :param docker_stats_manager_pidfile: the file to save the PID of the docker statsmanager
        :param prometheus_pid_file: the file to save the PID of prometheus
        :param prometheus_log_file: the log file of prometheus
        :param prometheus_config_file: the the config file of prometheus
        :param default_log_dir: the default log directory for CSLE applications
        :param cluster_config: the cluster configuration of the CSLE deployment
        """
        self.management_admin_username_default = management_admin_username_default
        self.management_admin_password_default = management_admin_password_default
        self.management_admin_first_name_default = management_admin_first_name_default
        self.management_admin_last_name_default= management_admin_last_name_default
        self.management_admin_email_default = management_admin_email_default
        self.management_admin_organization_default = management_admin_organization_default
        self.management_guest_username_default = management_guest_username_default
        self.management_guest_password_default = management_guest_password_default
        self.management_guest_first_name_default = management_guest_first_name_default
        self.management_guest_last_name_default = management_guest_last_name_default
        self.management_guest_email_default = management_guest_email_default
        self.management_guest_organization_default = management_guest_organization_default
        self.ssh_admin_username = ssh_admin_username
        self.ssh_admin_password = ssh_admin_password
        self.ssh_agent_username= ssh_agent_username
        self.ssh_agent_password= ssh_agent_password
        self.metastore_user= metastore_user
        self.metastore_password= metastore_password
        self.metastore_database_name = metastore_database_name
        self.metastore_ip = metastore_ip
        self.node_exporter_port= node_exporter_port
        self.grafana_port = grafana_port
        self.proxy_port= proxy_port
        self.management_system_port= management_system_port
        self.cadvisor_port = cadvisor_port
        self.prometheus_port = prometheus_port
        self.node_exporter_pid_file = node_exporter_pid_file
        self.management_system_pid_file = management_system_pid_file
        self.docker_stats_manager_log_file = docker_stats_manager_log_file
        self.docker_stats_manager_log_dir = docker_stats_manager_log_dir
        self.docker_stats_manager_port = docker_stats_manager_port
        self.docker_stats_manager_max_workers = docker_stats_manager_max_workers
        self.docker_stats_manager_outfile = docker_stats_manager_outfile
        self.docker_stats_manager_pidfile = docker_stats_manager_pidfile
        self.prometheus_pid_file = prometheus_pid_file
        self.prometheus_log_file = prometheus_log_file
        self.prometheus_config_file = prometheus_config_file
        self.default_log_dir = default_log_dir
        self.cluster_config = cluster_config

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["management_admin_username_default"] = self.management_admin_username_default
        d["management_admin_password_default"] = self.management_admin_password_default
        d["management_admin_first_name_default"] = self.management_admin_first_name_default
        d["management_admin_last_name_default"] = self.management_admin_last_name_default
        d["management_admin_email_default"] = self.management_admin_email_default
        d["management_admin_organization_default"] = self.management_admin_organization_default
        d["management_guest_password_default"] = self.management_guest_password_default
        d["management_guest_first_name_default"] = self.management_guest_first_name_default
        d["management_guest_last_name_default"] = self.management_guest_last_name_default
        d["management_guest_email_default"] = self.management_guest_email_default
        d["management_guest_organization_default"] = self.management_guest_organization_default
        d["ssh_admin_username"] = self.ssh_admin_username
        d["ssh_admin_password"] = self.ssh_admin_password
        d["ssh_agent_username"] = self.ssh_agent_username
        d["ssh_agent_password"] = self.ssh_agent_password
        d["metastore_user"] = self.metastore_user
        d["metastore_password"] = self.metastore_password
        d["metastore_database_name"] = self.metastore_database_name
        d["metastore_ip"] = self.metastore_ip
        d["node_exporter_port"] = self.node_exporter_port
        d["grafana_port"] = self.grafana_port
        d["proxy_port"] = self.proxy_port
        d["management_system_port"] = self.management_system_port
        d["cadvisor_port"] = self.cadvisor_port
        d["prometheus_port"] = self.prometheus_port
        d["node_exporter_pid_file"] = self.node_exporter_pid_file
        d["management_system_pid_file"] = self.management_system_pid_file
        d["docker_stats_manager_log_file"] = self.docker_stats_manager_log_file
        d["docker_stats_manager_log_dir"] = self.docker_stats_manager_log_dir
        d["docker_stats_manager_port"] = self.docker_stats_manager_port
        d["docker_stats_manager_max_workers"] = self.docker_stats_manager_max_workers
        d["docker_stats_manager_outfile"] = self.docker_stats_manager_outfile
        d["docker_stats_manager_pidfile"] = self.docker_stats_manager_pidfile
        d["prometheus_pid_file"] = self.prometheus_pid_file
        d["prometheus_log_file"] = self.prometheus_log_file
        d["prometheus_config_file"] = self.prometheus_config_file
        d["default_log_dir"] = self.default_log_dir
        d["cluster_config"] = self.cluster_config.to_dict()
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Config":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = Config(management_admin_username_default = d["management_admin_username_default"],
                     management_admin_password_default = d["management_admin_password_default"],
                     management_admin_first_name_default = d["management_admin_first_name_default"],
                     management_admin_last_name_default = d["management_admin_last_name_default"],
                     management_admin_email_default = d["management_admin_email_default"],
                     management_admin_organization_default = d["management_admin_organization_default"],
                     management_guest_username_default = d["management_guest_username_default"],
                     management_guest_password_default = d["management_guest_password_default"],
                     management_guest_first_name_default = d["management_guest_first_name_default"],
                     management_guest_last_name_default = d["management_guest_last_name_default"],
                     management_guest_email_default = d["management_guest_email_default"],
                     management_guest_organization_default = d["management_guest_organization_default"],
                     ssh_admin_username = d["ssh_admin_username"],
                     ssh_admin_password = d["ssh_admin_password"],
                     ssh_agent_username = d["ssh_agent_username"],
                     ssh_agent_password = d["ssh_agent_password"],
                     metastore_user = d["metastore_user"],
                     metastore_password = d["metastore_password"],
                     metastore_database_name = d["metastore_database_name"],
                     metastore_ip = d["metastore_ip"],
                     node_exporter_port = d["node_exporter_port"],
                     grafana_port = d["grafana_port"],
                     proxy_port = d["proxy_port"],
                     management_system_port = d["management_system_port"],
                     cadvisor_port = d["cadvisor_port"],
                     prometheus_port = d["prometheus_port"],
                     node_exporter_pid_file = d["node_exporter_pid_file"],
                     management_system_pid_file = d["management_system_pid_file"],
                     docker_stats_manager_log_file = d["docker_stats_manager_log_file"],
                     docker_stats_manager_log_dir = d["docker_stats_manager_log_dir"],
                     docker_stats_manager_port = d["docker_stats_manager_port"],
                     docker_stats_manager_max_workers = d["docker_stats_manager_max_workers"],
                     docker_stats_manager_outfile = d["docker_stats_manager_outfile"],
                     docker_stats_manager_pidfile = d["docker_stats_manager_pidfile"],
                     prometheus_pid_file = d["prometheus_pid_file"],
                     prometheus_log_file = d["prometheus_log_file"],
                     prometheus_config_file = d["prometheus_config_file"],
                     default_log_dir = d["default_log_dir"],
                     cluster_config = ClusterConfig.from_dict(d["cluster_config"]))
        return dto

    def __str__(self) -> str:
        """
        :return: a string representation of the credential
        """
        return f"management_admin_username_default:{self.management_admin_username_default}, " \
               f"management_admin_password_default: {self.management_admin_password_default}," \
               f"management_admin_first_name_default: {self.management_admin_first_name_default}, " \
               f"management_admin_last_name_default: {self.management_admin_last_name_default}," \
               f"management_admin_email_default: {self.management_admin_email_default}, " \
               f"management_admin_organization_default: {self.management_admin_organization_default}, " \
               f"ssh_admin_username: {self.ssh_admin_username}, " \
               f"ssh_admin_password: {self.ssh_admin_password}, " \
               f"ssh_agent_username: {self.ssh_agent_username}, " \
               f"ssh_agent_password: {self.ssh_agent_password}, " \
               f"metastore_user: {self.metastore_user}, " \
               f"metastore_password: {self.metastore_password}, " \
               f"metastore_database_name: {self.metastore_database_name}, " \
               f"metastore_ip: {self.metastore_ip}, " \
               f"node_exporter_port: {self.node_exporter_port}, " \
               f"grafana_port: {self.grafana_port}, " \
               f"proxy_port: {self.proxy_port}, " \
               f"management_system_port: {self.management_system_port}, " \
               f"cadvisor_port: {self.cadvisor_port}, " \
               f"prometheus_port: {self.prometheus_port}, " \
               f"node_exporter_pid_file: {self.node_exporter_pid_file}, " \
               f"management_system_pid_file: {self.management_system_pid_file}, " \
               f"docker_stats_manager_log_file: {self.docker_stats_manager_log_file}, " \
               f"docker_stats_manager_log_dir: {self.docker_stats_manager_log_dir}, " \
               f"docker_stats_manager_port: {self.docker_stats_manager_port}, " \
               f"docker_stats_manager_max_workers: {self.docker_stats_manager_max_workers}, " \
               f"docker_stats_manager_outfile: {self.docker_stats_manager_outfile}, " \
               f"docker_stats_manager_pidfile: {self.docker_stats_manager_pidfile}, " \
               f"prometheus_pid_file: {self.prometheus_pid_file}, " \
               f"prometheus_log_file: {self.prometheus_log_file}, " \
               f"prometheus_config_file: {self.prometheus_config_file}, " \
               f"default_log_dir: {self.default_log_dir}, " \
               f"cluster_config: {self.cluster_config}"

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    def copy(self) -> "ClusterConfig":
        """
        :return: a copy of the DTO
        """
        return ClusterConfig.from_dict(self.to_dict())
