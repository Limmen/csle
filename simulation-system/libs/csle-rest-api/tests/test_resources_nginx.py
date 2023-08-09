import json
import pytest
import pytest_mock
from csle_cluster.cluster_manager.cluster_manager_pb2 import NodeStatusDTO, ServiceStatusDTO
from csle_common.dao.emulation_config.config import Config
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesNginxSuite:
    """
    Test suite for /nginx resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def config(self, mocker: pytest_mock.MockFixture, example_config: Config):
        """
        Pytest fixture for mocking the get_config method
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_config(id: int) -> Config:
            conf = example_config
            return conf
        get_config_mocker = mocker.MagicMock(side_effect=get_config)
        return get_config_mocker

    @pytest.fixture
    def stop(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_nginx method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def stop_nginx(ip: str, port: int) -> ServiceStatusDTO:
            serv_stat = ServiceStatusDTO(running=False)
            return serv_stat
        stop_nginx_mocker = mocker.MagicMock(side_effect=stop_nginx)
        return stop_nginx_mocker

    @pytest.fixture
    def start(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_nginx method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def start_nginx(ip: str, port: int) -> ServiceStatusDTO:
            serv_stat = ServiceStatusDTO(running=True)
            return serv_stat
        start_nginx_mocker = mocker.MagicMock(side_effect=start_nginx)
        return start_nginx_mocker

    @pytest.fixture
    def node_status(self, mocker: pytest_mock.MockFixture, example_node_status):
        """
        pytest fixture for mocking the get_node_status method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_node_status(ip: str, port: int) -> NodeStatusDTO:
            node_stat = example_node_status
            return node_stat
        get_node_status_mocker = mocker.MagicMock(side_effect=get_node_status)
        return get_node_status_mocker

    @pytest.fixture
    def node_status_not_running(self, mocker: pytest_mock.MockFixture, example_node_status):
        """
        pytest fixture for mocking the get_node_status method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_node_status(ip: str, port: int) -> NodeStatusDTO:
            node_stat = example_node_status
            node_stat.nginxRunning = False
            return node_stat
        get_node_status_mocker = mocker.MagicMock(side_effect=get_node_status)
        return get_node_status_mocker

    def test_nginx_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in, logged_in_as_admin,
                       config, node_status, example_node_status, example_config) -> None:
        """
        testing the GET HTTPS method for the /nginx resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param config: the config fixture
        :param stop: the stop fixture
        :param start: the start fixture
        :param node_status: the node_status fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
                     side_effect=node_status)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.NGINX_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.NGINX_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]

        config = example_config
        cluster_statuses = []
        for node in config.cluster_config.cluster_nodes:
            node_status = example_node_status
            cluster_status_dict = {
                api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY: node_status.cAdvisorRunning,
                api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY: node_status.grafanaRunning,
                api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY: node_status.postgreSQLRunning,
                api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY: node_status.nodeExporterRunning,
                api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY: node_status.dockerEngineRunning,
                api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY: node_status.nginxRunning,
                api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY: node_status.flaskRunning,
                api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY: node_status.prometheusRunning,
                api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY: node_status.pgAdminRunning,
                api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY: f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                f"{node.ip}:{constants.COMMANDS.CADVISOR_PORT}/",
                api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY: f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{node.ip}:"
                f"{constants.COMMANDS.GRAFANA_PORT}/",
                api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY: f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{node.ip}:"
                f"{constants.COMMANDS.NODE_EXPORTER_PORT}/",
                api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY: f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{node.ip}:"
                f"{constants.COMMANDS.FLASK_PORT}/",
                api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY: f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{node.ip}:"
                f"{constants.COMMANDS.PROMETHEUS_PORT}/",
                api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY: f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{node.ip}:"
                f"{constants.COMMANDS.PGADMIN_PORT}/",
                api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY: constants.COMMANDS.CADVISOR_PORT,
                api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY: constants.COMMANDS.GRAFANA_PORT,
                api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY: constants.COMMANDS.NODE_EXPORTER_PORT,
                api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY: constants.COMMANDS.FLASK_PORT,
                api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY: constants.COMMANDS.PROMETHEUS_PORT,
                api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY: constants.COMMANDS.PGADMIN_PORT,
                api_constants.MGMT_WEBAPP.IP_PROPERTY: node.ip,
                api_constants.MGMT_WEBAPP.CPUS_PROPERTY: node.cpus,
                api_constants.MGMT_WEBAPP.GPUS_PROPERTY: node.gpus,
                api_constants.MGMT_WEBAPP.RAM_PROPERTY: node.RAM,
                api_constants.MGMT_WEBAPP.LEADER_PROPERTY: node.leader
            }
            cluster_statuses.append(cluster_status_dict)
        example_data_dict = cluster_statuses[0]
        for k in response_data_dict:
            assert response_data_dict[k] == example_data_dict[k]

        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.NGINX_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]

        for k in response_data_dict:
            assert response_data_dict[k] == example_data_dict[k]

    def test_nginx_post(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                        logged_in_as_admin, config, stop, start, node_status, example_node_status, example_config,
                        node_status_not_running) -> None:
        """
        testing the GET HTTPS method for the /nginx resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param config: the config fixture
        :param stop: the stop fixture
        :param start: the start fixture
        :param node_status: the node_status fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
                     side_effect=node_status)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_nginx", side_effect=stop)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_nginx", side_effect=start)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        test_data = json.dumps({api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"})
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.NGINX_RESOURCE, data=test_data)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        test_data = json.dumps({api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"})
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.NGINX_RESOURCE, data=test_data)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        test_data = json.dumps({api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"})
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.NGINX_RESOURCE, data=test_data)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        config = example_config
        cluster_statuses = []
        for node in config.cluster_config.cluster_nodes:
            node_status = example_node_status
            cluster_status_dict = {
                api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY: node_status.cAdvisorRunning,
                api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY: node_status.grafanaRunning,
                api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY: node_status.postgreSQLRunning,
                api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY: node_status.nodeExporterRunning,
                api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY: node_status.dockerEngineRunning,
                api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY: node_status.nginxRunning,
                api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY: node_status.flaskRunning,
                api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY: node_status.prometheusRunning,
                api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY: node_status.pgAdminRunning,
                api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY: f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                f"{node.ip}:{constants.COMMANDS.CADVISOR_PORT}/",
                api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY: f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{node.ip}:"
                f"{constants.COMMANDS.GRAFANA_PORT}/",
                api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY: f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{node.ip}:"
                f"{constants.COMMANDS.NODE_EXPORTER_PORT}/",
                api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY: f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{node.ip}:"
                f"{constants.COMMANDS.FLASK_PORT}/",
                api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY: f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{node.ip}:"
                f"{constants.COMMANDS.PROMETHEUS_PORT}/",
                api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY: f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{node.ip}:"
                f"{constants.COMMANDS.PGADMIN_PORT}/",
                api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY: constants.COMMANDS.CADVISOR_PORT,
                api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY: constants.COMMANDS.GRAFANA_PORT,
                api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY: constants.COMMANDS.NODE_EXPORTER_PORT,
                api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY: constants.COMMANDS.FLASK_PORT,
                api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY: constants.COMMANDS.PROMETHEUS_PORT,
                api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY: constants.COMMANDS.PGADMIN_PORT,
                api_constants.MGMT_WEBAPP.IP_PROPERTY: node.ip,
                api_constants.MGMT_WEBAPP.CPUS_PROPERTY: node.cpus,
                api_constants.MGMT_WEBAPP.GPUS_PROPERTY: node.gpus,
                api_constants.MGMT_WEBAPP.RAM_PROPERTY: node.RAM,
                api_constants.MGMT_WEBAPP.LEADER_PROPERTY: node.leader
            }
            cluster_statuses.append(cluster_status_dict)
        example_data_dict = cluster_statuses[0]
        for k in response_data_dict:
            assert response_data_dict[k] == example_data_dict[k]
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
                     side_effect=node_status_not_running)
        test_data = json.dumps({api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"})
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.NGINX_RESOURCE, data=test_data)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        for k in response_data_dict:
            if k == api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY:
                assert response_data_dict[k] != example_data_dict[k]
            else:
                assert response_data_dict[k] == example_data_dict[k]
