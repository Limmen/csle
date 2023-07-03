import json
import logging

import csle_common.constants.constants as constants
import pytest
from csle_cluster.cluster_manager.cluster_manager_pb2 import NodeStatusDTO
from csle_common.dao.emulation_config.cluster_config import ClusterConfig
from csle_common.dao.emulation_config.cluster_node import ClusterNode
from csle_common.dao.emulation_config.config import Config

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesNodeExporterSuite(object):
    """
        Test suite for /node-exporter resource
    """
    pytest.logger = logging.getLogger("resources_users_tests")

    @pytest.fixture
    def flask_app(self):
        """
        :return: the flask app fixture representing the webserver
        """
        return create_app(
            static_folder="../../../../../management-system/csle-mgmt-webapp/build"
        )

    @pytest.fixture
    def stop(self, mocker):
        """
        Fixture for mocking the stop side-effect
        """

        def stop_node_exporter(ip, port):
            return None
        stop_node_exporter_mocker = mocker.MagicMock(side_effect=stop_node_exporter)
        return stop_node_exporter_mocker

    @pytest.fixture
    def start(self, mocker):
        """
        Fixture for mocking the start side-effect
        """

        def start_node_exporter(ip, port):
            return None
        start_node_exporter_mocker = mocker.MagicMock(side_effect=start_node_exporter)
        return start_node_exporter_mocker

    @pytest.fixture
    def config(self, mocker):
        """
        Fixture for mocking the config side-effect
        """
        def get_config(id):
            config = TestResourcesNodeExporterSuite.example_config()
            return config

        get_config_mock = mocker.MagicMock(side_effect=get_config)
        return get_config_mock

    @staticmethod
    def example_node_status() -> NodeStatusDTO:
        """
        Help function that returns an example node status

        :return: the example node status
        """
        node_status = NodeStatusDTO(
            ip="123.456.78.99",
            leader=True,
            cAdvisorRunning=True,
            prometheusRunning=True,
            grafanaRunning=True,
            pgAdminRunning=True,
            nginxRunning=True,
            flaskRunning=True,
            dockerStatsManagerRunning=True,
            nodeExporterRunning=True,
            postgreSQLRunning=True,
            dockerEngineRunning=True
        )
        return node_status

    @staticmethod
    def example_config():
        """
        Help function that returns a congif class when making
        fixtures and testing
        :return: Config class
        """
        c_node = ClusterNode(ip="123.456.78.99", leader=True, cpus=1, gpus=2, RAM=3)
        config = Config(
            management_admin_username_default="admin",
            management_admin_password_default="admin",
            management_admin_first_name_default="Admin",
            management_admin_last_name_default="Adminson",
            management_admin_email_default="admin@CSLE.com",
            management_admin_organization_default="CSLE",
            management_guest_username_default="guest",
            management_guest_password_default="guest",
            management_guest_first_name_default="Guest",
            management_guest_last_name_default="Guestson",
            management_guest_email_default="guest@CSLE.com",
            management_guest_organization_default="CSLE",
            ssh_admin_username="null",
            ssh_admin_password="null",
            ssh_agent_username="null",
            ssh_agent_password="null",
            metastore_user="null",
            metastore_password="null",
            metastore_database_name="null",
            metastore_ip="null",
            node_exporter_port=1,
            grafana_port=1,
            management_system_port=1,
            cadvisor_port=1,
            prometheus_port=1,
            node_exporter_pid_file="null",
            pgadmin_port=1,
            csle_mgmt_webapp_pid_file="null",
            docker_stats_manager_log_file="null",
            docker_stats_manager_log_dir="null",
            docker_stats_manager_port=1,
            docker_stats_manager_max_workers=1,
            docker_stats_manager_outfile="null",
            docker_stats_manager_pidfile="null",
            prometheus_pid_file="null",
            prometheus_log_file="null",
            prometheus_config_file="null",
            default_log_dir="null",
            cluster_config=ClusterConfig([c_node]),
            node_exporter_log_file="null",
            allow_registration=True,
            grafana_username="null",
            grafana_password="null",
            pgadmin_username="null",
            pgadmin_password="null",
            postgresql_log_dir="null",
            nginx_log_dir="null",
            flask_log_file="null",
            cluster_manager_log_file="null",
        )
        return config

    @pytest.fixture
    def node_status_node_exporter_running(self, mocker):
        """
        Fixture for mocking the get_node_status function where flask is running

        :param mocker: the pytest mocker object
        :return the fixture for the get_node_status_function
        """
        def get_node_status(ip: str, port: int) -> NodeStatusDTO:
            node_status = TestResourcesNodeExporterSuite.example_node_status()
            node_status.nodeExporterRunning = True
            return node_status
        get_node_status_mock = mocker.MagicMock(side_effect=get_node_status)
        return get_node_status_mock

    @pytest.fixture
    def node_status_node_exporter_not_running(self, mocker):
        """
        Fixture for mocking the get_node_status function where flask is not running

        :param mocker: the pytest mocker object
        :return the fixture for the get_node_status_function
        """
        def get_node_status(ip: str, port: int) -> NodeStatusDTO:
            node_status = TestResourcesNodeExporterSuite.example_node_status()
            node_status.nodeExporterRunning = False
            return node_status
        get_node_status_mock = mocker.MagicMock(side_effect=get_node_status)
        return get_node_status_mock

    @pytest.mark.usefixtures("logged_in", "logged_in_as_admin", "not_logged_in")
    def test_node_exporter_get(self, flask_app, mocker, logged_in_as_admin, logged_in, not_logged_in, config,
                               node_status_node_exporter_running, node_status_node_exporter_not_running, start, stop):
        """
        Tests the GET HTTPS method for the /node-exporter url

        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param config: the config fixture
        :param node_status: the node_status fixture
        :param start: the start fixture
        :param stop: the stop fixture
        :return: None
        """

        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
            side_effect=config,
        )
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.start_node_exporter",
            side_effect=start,
        )
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_node_exporter",
            side_effect=stop,
        )

        config = TestResourcesNodeExporterSuite.example_config()
        ip_adress = config.cluster_config.cluster_nodes[0].ip
        RAM = config.cluster_config.cluster_nodes[0].RAM
        cpus = config.cluster_config.cluster_nodes[0].cpus
        leader = config.cluster_config.cluster_nodes[0].leader
        gpus = config.cluster_config.cluster_nodes[0].gpus

        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
            side_effect=node_status_node_exporter_running,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE

        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        config_node = response_data_list[0]
        assert config_node[api_constants.MGMT_WEBAPP.RAM_PROPERTY] == 3
        assert config_node[api_constants.MGMT_WEBAPP.RAM_PROPERTY] == RAM
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.CADVISOR_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY] == constants.COMMANDS.CADVISOR_PORT
        assert config_node[api_constants.MGMT_WEBAPP.CPUS_PROPERTY] == cpus
        assert config_node[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY] == constants.COMMANDS.FLASK_PORT
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.FLASK_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.GPUS_PROPERTY] == gpus
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY] == constants.COMMANDS.GRAFANA_PORT
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.GRAFANA_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.IP_PROPERTY] == '123.456.78.99'
        assert config_node[api_constants.MGMT_WEBAPP.LEADER_PROPERTY] == leader
        assert config_node[api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY] \
            == constants.COMMANDS.NODE_EXPORTER_PORT
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.NODE_EXPORTER_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY] == constants.COMMANDS.PGADMIN_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.PGADMIN_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY] == constants.COMMANDS.PROMETHEUS_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.PROMETHEUS_PORT}/"
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        config_node = response_data_list[0]
        assert config_node[api_constants.MGMT_WEBAPP.RAM_PROPERTY] == RAM
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.CADVISOR_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY] == constants.COMMANDS.CADVISOR_PORT
        assert config_node[api_constants.MGMT_WEBAPP.CPUS_PROPERTY] == cpus
        assert config_node[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY] == constants.COMMANDS.FLASK_PORT
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.FLASK_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.GPUS_PROPERTY] == gpus
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY] == constants.COMMANDS.GRAFANA_PORT
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.GRAFANA_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.IP_PROPERTY] == '123.456.78.99'
        assert config_node[api_constants.MGMT_WEBAPP.LEADER_PROPERTY] == leader
        assert config_node[api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY] \
            == constants.COMMANDS.NODE_EXPORTER_PORT
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.NODE_EXPORTER_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY] == constants.COMMANDS.PGADMIN_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.PGADMIN_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY] == constants.COMMANDS.PROMETHEUS_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.PROMETHEUS_PORT}/"
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
            side_effect=node_status_node_exporter_not_running,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        config_node = response_data_list[0]
        assert config_node[api_constants.MGMT_WEBAPP.RAM_PROPERTY] == RAM
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.CADVISOR_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY] \
            == constants.COMMANDS.CADVISOR_PORT
        assert config_node[api_constants.MGMT_WEBAPP.CPUS_PROPERTY] == cpus
        assert config_node[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY] \
            == constants.COMMANDS.FLASK_PORT
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.FLASK_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.GPUS_PROPERTY] == gpus
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY] == constants.COMMANDS.GRAFANA_PORT
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.GRAFANA_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.IP_PROPERTY] == '123.456.78.99'
        assert config_node[api_constants.MGMT_WEBAPP.LEADER_PROPERTY] == leader
        assert config_node[api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY] \
            == constants.COMMANDS.NODE_EXPORTER_PORT
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY] is False
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.NODE_EXPORTER_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY] == constants.COMMANDS.PGADMIN_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.PGADMIN_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY] == constants.COMMANDS.PROMETHEUS_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.PROMETHEUS_PORT}/"
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        config_node = response_data_list[0]
        assert config_node[api_constants.MGMT_WEBAPP.RAM_PROPERTY] == RAM
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.CADVISOR_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY] == constants.COMMANDS.CADVISOR_PORT
        assert config_node[api_constants.MGMT_WEBAPP.CPUS_PROPERTY] == cpus
        assert config_node[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY] == constants.COMMANDS.FLASK_PORT
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.FLASK_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.GPUS_PROPERTY] == gpus
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY] == constants.COMMANDS.GRAFANA_PORT
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.GRAFANA_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.IP_PROPERTY] == '123.456.78.99'
        assert config_node[api_constants.MGMT_WEBAPP.LEADER_PROPERTY] == leader
        assert config_node[api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY] \
            == constants.COMMANDS.NODE_EXPORTER_PORT
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY] is False
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.NODE_EXPORTER_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY] == constants.COMMANDS.PGADMIN_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.PGADMIN_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY] == constants.COMMANDS.PROMETHEUS_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.PROMETHEUS_PORT}/"

    def test_node_exporter_post(self, flask_app, mocker, logged_in_as_admin, logged_in, not_logged_in, config,
                                node_status_node_exporter_running, node_status_node_exporter_not_running, start, stop):
        """
        Tests the POST HTTPS method for the /node-exporter url

        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param config: the config fixture
        :param node_status: the node_status fixture
        :param start: the start fixture
        :param stop: the stop fixture
        :return: None
        """
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
            side_effect=config,
        )
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.start_node_exporter",
            side_effect=start,
        )
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_node_exporter",
            side_effect=stop,
        )
        config = TestResourcesNodeExporterSuite.example_config()
        ip_adress = config.cluster_config.cluster_nodes[0].ip
        RAM = config.cluster_config.cluster_nodes[0].RAM
        cpus = config.cluster_config.cluster_nodes[0].cpus
        leader = config.cluster_config.cluster_nodes[0].leader
        gpus = config.cluster_config.cluster_nodes[0].gpus

        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
            side_effect=node_status_node_exporter_running,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE,
                                                data=json.dumps({}))

        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE,
                                                data=json.dumps({}))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        config_cluster_dict = config.cluster_config.to_dict()['cluster_nodes'][0]
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE,
                                                data=json.dumps(config_cluster_dict))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)

        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        config_node = response_data_list[0]
        assert config_node[api_constants.MGMT_WEBAPP.RAM_PROPERTY] == RAM
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.CADVISOR_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY] == constants.COMMANDS.CADVISOR_PORT
        assert config_node[api_constants.MGMT_WEBAPP.CPUS_PROPERTY] == cpus
        assert config_node[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY] == constants.COMMANDS.FLASK_PORT
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.FLASK_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.GPUS_PROPERTY] == gpus
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY] == constants.COMMANDS.GRAFANA_PORT
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.GRAFANA_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.IP_PROPERTY] == '123.456.78.99'
        assert config_node[api_constants.MGMT_WEBAPP.LEADER_PROPERTY] == leader
        assert config_node[api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY] \
            == constants.COMMANDS.NODE_EXPORTER_PORT
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY] is False
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.NODE_EXPORTER_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY] == constants.COMMANDS.PGADMIN_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.PGADMIN_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY] == constants.COMMANDS.PROMETHEUS_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.PROMETHEUS_PORT}/"
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
            side_effect=node_status_node_exporter_not_running,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE,
                                                data=json.dumps({}))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        config = TestResourcesNodeExporterSuite.example_config()
        config_cluster_dict = config.cluster_config.to_dict()['cluster_nodes'][0]
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE,
                                                data=json.dumps(config_cluster_dict))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        config_node = response_data_list[0]
        assert config_node[api_constants.MGMT_WEBAPP.RAM_PROPERTY] == RAM
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.CADVISOR_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY] \
            == constants.COMMANDS.CADVISOR_PORT
        assert config_node[api_constants.MGMT_WEBAPP.CPUS_PROPERTY] == cpus
        assert config_node[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY] == constants.COMMANDS.FLASK_PORT
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.FLASK_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.GPUS_PROPERTY] == gpus
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY] == constants.COMMANDS.GRAFANA_PORT
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.GRAFANA_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.IP_PROPERTY] == ip_adress
        assert config_node[api_constants.MGMT_WEBAPP.LEADER_PROPERTY] == leader
        assert config_node[api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY] \
            == constants.COMMANDS.NODE_EXPORTER_PORT
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.NODE_EXPORTER_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY] == constants.COMMANDS.PGADMIN_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.PGADMIN_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY] == constants.COMMANDS.PROMETHEUS_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY] \
            == f"http://{ip_adress}:{constants.COMMANDS.PROMETHEUS_PORT}/"
