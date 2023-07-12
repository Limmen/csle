import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_cluster.cluster_manager.cluster_manager_pb2 import NodeStatusDTO
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app
from csle_common.dao.emulation_config.config import Config


class TestResourcesCadvisorSuite:
    """
    Test suite for /cadvisor resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def stop(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking the stop side-effect

        :param mocker: the pytest mocker object
        :return: the mock
        """

        def stop_cadvisor(ip: str, port: int):
            return None

        stop_cadvisor_mocker = mocker.MagicMock(side_effect=stop_cadvisor)
        return stop_cadvisor_mocker

    @pytest.fixture
    def start(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking the start side-effect

        :param mocker: the pytest mocker object
        :return: the mock
        """

        def start_cadvisor(ip: str, port: int) -> None:
            return None

        start_cadvisor_mocker = mocker.MagicMock(side_effect=start_cadvisor)
        return start_cadvisor_mocker

    @pytest.fixture
    def config(self, mocker: pytest_mock.MockFixture, example_config: Config):
        """
        Fixture for mocking the config side-effect

        :param mocker: the pytest mocker object
        :param example_config: the example config to use for mocking
        :return: the mock
        """

        def get_config(id: int) -> Config:
            config = example_config
            return config

        get_config_mock = mocker.MagicMock(side_effect=get_config)
        return get_config_mock

    @pytest.fixture
    def node_status_cadvisor_running(self, mocker: pytest_mock.MockFixture, example_node_status: NodeStatusDTO):
        """
        Fixture for mocking the get_node_status function where flask is running

        :param mocker: the pytest mocker object
        :param example_node_status: the exampe node status to use for mocking
        :return the fixture for the get_node_status_function
        """

        def get_node_status(ip: str, port: int) -> NodeStatusDTO:
            node_status = example_node_status
            node_status.cAdvisorRunning = True
            return node_status

        get_node_status_mock = mocker.MagicMock(side_effect=get_node_status)
        return get_node_status_mock

    @pytest.fixture
    def node_status_cadvisor_not_running(self, mocker: pytest_mock.MockFixture, example_node_status: NodeStatusDTO):
        """
        Fixture for mocking the get_node_status function where flask is not running

        :param mocker: the pytest mocker object
        :param example_node_status: the example node status to use for mocking
        :return the fixture for the get_node_status_function
        """

        def get_node_status(ip: str, port: int) -> NodeStatusDTO:
            node_status = example_node_status
            node_status.cAdvisorRunning = False
            return node_status

        get_node_status_mock = mocker.MagicMock(side_effect=get_node_status)
        return get_node_status_mock

    def test_cadvisor_get(self, flask_app, mocker: pytest_mock.MockFixture, logged_in_as_admin, logged_in,
                          not_logged_in, config, node_status_cadvisor_running, node_status_cadvisor_not_running, start,
                          stop, example_config) -> None:
        """
        Tests the GET HTTPS method for the /cadvisor url

        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param config: the config fixture
        :param node_status: the node_status fixture
        :param start: the start fixture
        :param stop: the stop fixture
        :param example_config: the example config (to use for assertions)
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_cadvisor",
                     side_effect=start)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_cadvisor",
                     side_effect=stop)
        config = example_config
        ip_adress = config.cluster_config.cluster_nodes[0].ip
        RAM = config.cluster_config.cluster_nodes[0].RAM
        cpus = config.cluster_config.cluster_nodes[0].cpus
        leader = config.cluster_config.cluster_nodes[0].leader
        gpus = config.cluster_config.cluster_nodes[0].gpus
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
                     side_effect=node_status_cadvisor_running)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        config_node = response_data_list[0]
        assert config_node[api_constants.MGMT_WEBAPP.RAM_PROPERTY] == 3
        assert config_node[api_constants.MGMT_WEBAPP.RAM_PROPERTY] == RAM
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.CADVISOR_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY] == constants.COMMANDS.CADVISOR_PORT
        assert config_node[api_constants.MGMT_WEBAPP.CPUS_PROPERTY] == cpus
        assert config_node[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY] == constants.COMMANDS.FLASK_PORT
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.FLASK_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.GPUS_PROPERTY] == gpus
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY] == constants.COMMANDS.GRAFANA_PORT
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.GRAFANA_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.IP_PROPERTY] == '123.456.78.99'
        assert config_node[api_constants.MGMT_WEBAPP.LEADER_PROPERTY] == leader
        assert config_node[api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY] \
               == constants.COMMANDS.NODE_EXPORTER_PORT
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.NODE_EXPORTER_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY] == constants.COMMANDS.PGADMIN_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.PGADMIN_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY] == constants.COMMANDS.PROMETHEUS_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.PROMETHEUS_PORT}/"
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        config_node = response_data_list[0]
        assert config_node[api_constants.MGMT_WEBAPP.RAM_PROPERTY] == RAM
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.CADVISOR_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY] == constants.COMMANDS.CADVISOR_PORT
        assert config_node[api_constants.MGMT_WEBAPP.CPUS_PROPERTY] == cpus
        assert config_node[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY] == constants.COMMANDS.FLASK_PORT
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.FLASK_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.GPUS_PROPERTY] == gpus
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY] == constants.COMMANDS.GRAFANA_PORT
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.GRAFANA_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.IP_PROPERTY] == '123.456.78.99'
        assert config_node[api_constants.MGMT_WEBAPP.LEADER_PROPERTY] == leader
        assert config_node[api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY] \
               == constants.COMMANDS.NODE_EXPORTER_PORT
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.NODE_EXPORTER_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY] == constants.COMMANDS.PGADMIN_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.PGADMIN_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY] == constants.COMMANDS.PROMETHEUS_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.PROMETHEUS_PORT}/"
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
                     side_effect=node_status_cadvisor_not_running)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        config_node = response_data_list[0]
        assert config_node[api_constants.MGMT_WEBAPP.RAM_PROPERTY] == RAM
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY] is False
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.CADVISOR_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY] \
               == constants.COMMANDS.CADVISOR_PORT
        assert config_node[api_constants.MGMT_WEBAPP.CPUS_PROPERTY] == cpus
        assert config_node[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY] \
               == constants.COMMANDS.FLASK_PORT
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.FLASK_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.GPUS_PROPERTY] == gpus
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY] == constants.COMMANDS.GRAFANA_PORT
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.GRAFANA_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.IP_PROPERTY] == '123.456.78.99'
        assert config_node[api_constants.MGMT_WEBAPP.LEADER_PROPERTY] == leader
        assert config_node[api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY] \
               == constants.COMMANDS.NODE_EXPORTER_PORT
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.NODE_EXPORTER_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY] == constants.COMMANDS.PGADMIN_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.PGADMIN_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY] == constants.COMMANDS.PROMETHEUS_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.PROMETHEUS_PORT}/"
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
                     side_effect=node_status_cadvisor_not_running)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        config_node = response_data_list[0]
        assert config_node[api_constants.MGMT_WEBAPP.RAM_PROPERTY] == RAM
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY] is False
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.CADVISOR_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY] == constants.COMMANDS.CADVISOR_PORT
        assert config_node[api_constants.MGMT_WEBAPP.CPUS_PROPERTY] == cpus
        assert config_node[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY] == constants.COMMANDS.FLASK_PORT
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.FLASK_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.GPUS_PROPERTY] == gpus
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY] == constants.COMMANDS.GRAFANA_PORT
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.GRAFANA_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.IP_PROPERTY] == '123.456.78.99'
        assert config_node[api_constants.MGMT_WEBAPP.LEADER_PROPERTY] == leader
        assert config_node[api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY] \
               == constants.COMMANDS.NODE_EXPORTER_PORT
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.NODE_EXPORTER_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY] == constants.COMMANDS.PGADMIN_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.PGADMIN_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY] == constants.COMMANDS.PROMETHEUS_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.PROMETHEUS_PORT}/"

    def test_cadvisor_post(self, flask_app, mocker: pytest_mock.MockFixture, logged_in_as_admin, logged_in,
                           not_logged_in, config,
                           node_status_cadvisor_running, node_status_cadvisor_not_running, start, stop,
                           example_config) -> None:
        """
        Tests the POST HTTPS method for the /cadvisor url

        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param config: the config fixture
        :param node_status: the node_status fixture
        :param start: the start fixture
        :param stop: the stop fixture
        :param example_config: the example config (to use for assertions)
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_cadvisor",
                     side_effect=start)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_cadvisor",
                     side_effect=stop)
        config = example_config
        ip_adress = config.cluster_config.cluster_nodes[0].ip
        RAM = config.cluster_config.cluster_nodes[0].RAM
        cpus = config.cluster_config.cluster_nodes[0].cpus
        leader = config.cluster_config.cluster_nodes[0].leader
        gpus = config.cluster_config.cluster_nodes[0].gpus
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
                     side_effect=node_status_cadvisor_running)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE, data=json.dumps({}))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE, data=json.dumps({}))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        config_cluster_dict = config.cluster_config.to_dict()['cluster_nodes'][0]
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE,
                                                data=json.dumps(config_cluster_dict))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        config_node = response_data_list[0]
        assert config_node[api_constants.MGMT_WEBAPP.RAM_PROPERTY] == RAM
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY] is False
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.CADVISOR_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY] == constants.COMMANDS.CADVISOR_PORT
        assert config_node[api_constants.MGMT_WEBAPP.CPUS_PROPERTY] == cpus
        assert config_node[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY] == constants.COMMANDS.FLASK_PORT
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.FLASK_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.GPUS_PROPERTY] == gpus
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY] == constants.COMMANDS.GRAFANA_PORT
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.GRAFANA_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.IP_PROPERTY] == '123.456.78.99'
        assert config_node[api_constants.MGMT_WEBAPP.LEADER_PROPERTY] == leader
        assert config_node[api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY] \
               == constants.COMMANDS.NODE_EXPORTER_PORT
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.NODE_EXPORTER_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY] == constants.COMMANDS.PGADMIN_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.PGADMIN_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY] == constants.COMMANDS.PROMETHEUS_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.PROMETHEUS_PORT}/"
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
                     side_effect=node_status_cadvisor_not_running)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE, data=json.dumps({}))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE, data=json.dumps({}))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        config = example_config
        config_cluster_dict = config.cluster_config.to_dict()['cluster_nodes'][0]
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE,
                                                data=json.dumps(config_cluster_dict))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        config_node = response_data_list[0]
        assert config_node[api_constants.MGMT_WEBAPP.RAM_PROPERTY] == RAM
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.CADVISOR_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY] \
               == constants.COMMANDS.CADVISOR_PORT
        assert config_node[api_constants.MGMT_WEBAPP.CPUS_PROPERTY] == cpus
        assert config_node[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY] == constants.COMMANDS.FLASK_PORT
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.FLASK_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.GPUS_PROPERTY] == gpus
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY] == constants.COMMANDS.GRAFANA_PORT
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.GRAFANA_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.IP_PROPERTY] == ip_adress
        assert config_node[api_constants.MGMT_WEBAPP.LEADER_PROPERTY] == leader
        assert config_node[api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY] \
               == constants.COMMANDS.NODE_EXPORTER_PORT
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.NODE_EXPORTER_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY] == constants.COMMANDS.PGADMIN_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.PGADMIN_PORT}/"
        assert config_node[api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY] == constants.COMMANDS.PROMETHEUS_PORT
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY] is True
        assert config_node[api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY] \
               == f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{ip_adress}:{constants.COMMANDS.PROMETHEUS_PORT}/"
