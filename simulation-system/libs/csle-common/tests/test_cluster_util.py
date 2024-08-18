import os
from unittest.mock import patch, MagicMock
import csle_common.constants.constants as constants
from csle_common.util.cluster_util import ClusterUtil


class TestClusterUtilSuite:
    """
    Test suite for cluster util
    """

    def test_am_i_leader(self) -> None:
        """
        Test function that checks if a given IP is a leader or not
        """
        config = MagicMock()
        config.cluster_config.cluster_nodes.ip = "192.168.1.1"
        config.cluster_config.cluster_nodes.leader = False
        config.cluster_config.cluster_nodes.cpus = 1
        config.cluster_config.cluster_nodes.gpus = 2
        config.cluster_config.cluster_nodes.RAM = 8
        assert not ClusterUtil.am_i_leader("192.168.1.1", config)

    @patch("psycopg.connect")
    @patch("csle_common.util.cluster_util.ClusterUtil.get_config")
    @patch.dict(os.environ, {"CSLE_HOME": "/mock/csle/home"})
    def test_get_config(self, mock_get_config, mock_connect) -> None:
        """
        Test function that gets the current cluster config from the metastore or from disk
        depending on if it is the leader node or not

        :param mock_get_config: mock_get_config
        :param mock_connect: mock_connect
        :return: None
        """
        mock_config = MagicMock()
        mock_get_config.return_value = mock_config
        from csle_common.util.cluster_util import ClusterUtil

        result = ClusterUtil.get_config()
        assert result == mock_config

    @patch.dict(os.environ, {"CSLE_HOME": "/mock/csle/home"})
    @patch("csle_common.util.cluster_util.ClusterUtil.get_config")
    def test_set_config_parameters_from_config_file(self, mock_get_config) -> None:
        """
        Test function that reads the config file from $CSLE_HOME/config.json and initializes certain config parameters

        :param mock_get_config: mock_get_config
        :return: None
        """
        mock_config = MagicMock()
        mock_config.management_admin_username_default = "admin"
        mock_config.management_admin_password_default = "admin_pw"
        mock_config.management_admin_email_default = "admin@example.com"
        mock_config.management_admin_organization_default = "Example Org"
        mock_config.management_admin_first_name_default = "Admin"
        mock_config.management_admin_last_name_default = "User"
        mock_config.ssh_admin_username = "ssh_admin"
        mock_config.ssh_admin_password = "ssh_pw"
        mock_config.management_guest_username_default = "guest"
        mock_config.management_guest_password_default = "guest_pw"
        mock_config.management_guest_email_default = "guest@example.com"
        mock_config.management_guest_organization_default = "Example Org"
        mock_config.management_guest_first_name_default = "Guest"
        mock_config.management_guest_last_name_default = "User"
        mock_config.ssh_agent_username = "agent"
        mock_config.ssh_agent_password = "agent_pw"
        mock_config.metastore_user = "metastore_user"
        mock_config.metastore_password = "metastore_pw"
        mock_config.metastore_database_name = "metastore_db"
        mock_config.pgadmin_username = "pgadmin"
        mock_config.pgadmin_password = "pgadmin_pw"
        mock_config.grafana_username = "grafana"
        mock_config.grafana_password = "grafana_pw"
        mock_config.node_exporter_port = 9100
        mock_config.grafana_port = 3000
        mock_config.management_system_port = 8000
        mock_config.cadvisor_port = 8080
        mock_config.pgadmin_port = 5050
        mock_config.prometheus_port = 9090
        mock_config.node_exporter_pid_file = "/var/run/node_exporter.pid"
        mock_config.csle_mgmt_webapp_pid_file = "/var/run/csle_mgmt_webapp.pid"
        mock_config.node_exporter_log_file = "/var/log/node_exporter.log"
        mock_config.docker_stats_manager_outfile = "/var/log/docker_stats.out"
        mock_config.docker_stats_manager_pidfile = "/var/run/docker_stats.pid"
        mock_config.prometheus_pid_file = "/var/run/prometheus.pid"
        mock_config.prometheus_log_file = "/var/log/prometheus.log"
        mock_config.postgresql_log_dir = "/var/log/postgresql"
        mock_config.nginx_log_dir = "/var/log/nginx"
        mock_config.flask_log_file = "/var/log/flask.log"
        mock_config.default_log_dir = "/var/log"
        mock_get_config.return_value = mock_config
        ClusterUtil.set_config_parameters_from_config_file()
        assert constants.CONFIG_FILE.PARSED_CONFIG == mock_config
        assert constants.CSLE_ADMIN.MANAGEMENT_USER == "admin"
        assert constants.CSLE_ADMIN.MANAGEMENT_PW == "admin_pw"
        assert constants.CSLE_ADMIN.MANAGEMENT_EMAIL == "admin@example.com"
        assert constants.CSLE_ADMIN.MANAGEMENT_ORGANIZATION == "Example Org"
        assert constants.CSLE_ADMIN.MANAGEMENT_FIRST_NAME == "Admin"
        assert constants.CSLE_ADMIN.MANAGEMENT_LAST_NAME == "User"
        assert constants.CSLE_ADMIN.SSH_USER == "ssh_admin"
        assert constants.CSLE_ADMIN.SSH_PW == "ssh_pw"
        assert constants.CSLE_GUEST.MANAGEMENT_USER == "guest"
        assert constants.CSLE_GUEST.MANAGEMENT_PW == "guest_pw"
        assert constants.CSLE_GUEST.MANAGEMENT_EMAIL == "guest@example.com"
        assert constants.CSLE_GUEST.MANAGEMENT_ORGANIZATION == "Example Org"
        assert constants.CSLE_GUEST.MANAGEMENT_FIRST_NAME == "Guest"
        assert constants.CSLE_GUEST.MANAGEMENT_LAST_NAME == "User"
        assert constants.AGENT.USER == "agent"
        assert constants.AGENT.PW == "agent_pw"
        assert constants.METADATA_STORE.USER == "metastore_user"
        assert constants.METADATA_STORE.PASSWORD == "metastore_pw"
        assert constants.METADATA_STORE.DBNAME == "metastore_db"
        assert constants.COMMANDS.PGADMIN_USERNAME == "pgadmin"
        assert constants.COMMANDS.PGADMIN_PW == "pgadmin_pw"
        assert constants.COMMANDS.GRAFANA_USERNAME == "grafana"
        assert constants.COMMANDS.GRAFANA_PW == "grafana_pw"
        assert constants.COMMANDS.NODE_EXPORTER_PORT == 9100
        assert constants.COMMANDS.GRAFANA_PORT == 3000
        assert constants.COMMANDS.MANAGEMENT_SYSTEM_PORT == 8000
        assert constants.COMMANDS.CADVISOR_PORT == 8080
        assert constants.COMMANDS.PGADMIN_PORT == 5050
        assert constants.COMMANDS.PROMETHEUS_PORT == 9090
        assert constants.COMMANDS.NODE_EXPORTER_PID_FILE == "/var/run/node_exporter.pid"
        assert constants.COMMANDS.CSLE_MGMT_WEBAPP_PID_FILE == "/var/run/csle_mgmt_webapp.pid"
        assert constants.COMMANDS.NODE_EXPORTER_LOG_FILE == "/var/log/node_exporter.log"
        assert constants.COMMANDS.DOCKER_STATS_MANAGER_OUTFILE == "/var/log/docker_stats.out"
        assert constants.COMMANDS.DOCKER_STATS_MANAGER_PIDFILE == "/var/run/docker_stats.pid"
        assert constants.COMMANDS.PROMETHEUS_PID_FILE == "/var/run/prometheus.pid"
        assert constants.COMMANDS.PROMETHEUS_LOG_FILE == "/var/log/prometheus.log"
        assert constants.COMMANDS.POSTGRESQL_LOG_DIR == "/var/log/postgresql"
        assert constants.COMMANDS.NGINX_LOG_DIR == "/var/log/nginx"
        assert constants.COMMANDS.FLASK_LOG_FILE == "/var/log/flask.log"
        assert constants.LOGGING.DEFAULT_LOG_DIR == "/var/log"
