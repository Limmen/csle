import json
import csle_common.constants.constants as constants
import pytest
import pytest_mock
from csle_cluster.cluster_manager.cluster_manager_pb2 import NodeStatusDTO, ServiceStatusDTO
from csle_common.dao.emulation_config.config import Config
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesDockerStatusSuite:
    """
    Test suite for /docker url
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
        Pytest fixture for mocking the get_config function

        :param mocker: the pytest mocker object
        :param example config: example config from the
        conftest.py file
        :return: the pytest fixture for the get_config functione
        """
        def get_config(id: int) -> Config:
            conf = example_config
            return conf
        
        get_config_mocker = mocker.MagicMock(side_effect=get_config)
        return get_config_mocker

    @pytest.fixture
    def stop_docker(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_docker_engine function
        :param mocker: the pytest mocker object
        :return: the pytest fixture for the stop_docker_engine function
        """
        def stop_docker_engine(ip: str, port: int) -> ServiceStatusDTO:
            status = ServiceStatusDTO(running=False)
            return status
        stop_docker_engine_mocker = mocker.MagicMock(side_effect=stop_docker_engine)
        return stop_docker_engine_mocker

    @pytest.fixture
    def start_docker(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_docker_engine function
        :param mocker: the pytest mocker object
        :return: the pytest fixture for the stop_docker_engine function
        """
        def start_docker_engine(ip: str, port: int) -> ServiceStatusDTO:
            status = ServiceStatusDTO(running=True)
            return status
        start_docker_engine_mocker = mocker.MagicMock(side_effect=start_docker_engine)
        return start_docker_engine_mocker

    @pytest.fixture
    def node_status_docker_running(self, mocker: pytest_mock.MockFixture,
                                   example_node_status: NodeStatusDTO):
        """
        Pytest fixture for mocking the get_node_status function when
        the Docker engine is running

        :param mocker: the pytest mocker object
        :param example_node_status: example config from the
        conftest.py file
        :return: the pytest fixture for the get_node_status function
        """
        def get_node_status(ip: str, port: int) -> NodeStatusDTO:
            node_status = example_node_status
            node_status.dockerEngineRunning = True
            return node_status
        get_node_status_mock = mocker.MagicMock(side_effect=get_node_status)
        return get_node_status_mock

    @pytest.fixture
    def node_status_docker_not_running(self, mocker: pytest_mock.MockFixture,
                                       example_node_status: NodeStatusDTO):
        """
        Pytest fixture for mocking the get_node_status function when
        the Docker engine is down

        :param mocker: the pytest mocker object
        :param example_node_status: example config from the
        conftest.py file
        :return: the pytest fixture for the get_node_status function
        """
        def get_node_status(ip: str, port: int) -> NodeStatusDTO:
            node_status = example_node_status
            node_status.dockerEngineRunning = False
            return node_status
        get_node_status_mock = mocker.MagicMock(
            side_effect=get_node_status)
        return get_node_status_mock

    def test_docker_get(self, flask_app, mocker,
                        config, node_status_docker_running,
                        not_logged_in, logged_in,
                        logged_in_as_admin, example_config,
                        example_node_status,
                        cluster_node_status):
        """
        Tests the GET HTTPS method for the /docker url

        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param get_: the config fixture
        :param node_status: the node_status fixture
        :return: None
        """
        test_ns = cluster_node_status
        test_ns_dict = test_ns[0]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
                     side_effect=node_status_docker_running)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DOCKER_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DOCKER_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        response_data_dict = response_data_list[0]
        for k in response_data_dict:
            assert response_data_dict[k] == test_ns_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DOCKER_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        response_data_dict = response_data_list[0]
        for k in response_data_dict:
            assert response_data_dict[k] == test_ns_dict[k]

    def test_docker_post(self, flask_app, mocker, node_status_docker_running, node_status_docker_not_running,
                         config, not_logged_in, logged_in, logged_in_as_admin, example_config, stop_docker,
                         start_docker, cluster_node_status) -> None:
        """
        Tests the POST HTTPS method for the /docker url

        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param get_: the config fixture
        :param node_status: the node_status fixture
        :return: None
        """
        # pytest.logger.info(type(cluster_node_status))
        test_ns = cluster_node_status
        test_ns_dict = test_ns[0]

        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
                     side_effect=node_status_docker_running)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_docker_engine",
                     side_effect=stop_docker)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_docker_engine",
                     side_effect=start_docker)
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.DOCKER_RESOURCE,
                                                data=json.dumps({}))
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.DOCKER_RESOURCE,
                                                data=json.dumps({}))
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.DOCKER_RESOURCE, data=json.dumps({}))
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        config = example_config
        config_cluster_dict = config.cluster_config.to_dict()['cluster_nodes'][0]
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.DOCKER_RESOURCE,
                                                data=json.dumps(config_cluster_dict))
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        response_data_dict = response_data_dict[0]
        for k in response_data_dict:
            if k == api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY:
                continue
            else:
                assert response_data_dict[k] == test_ns_dict[k]
        assert response_data_dict[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is False
        assert test_ns_dict[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert response_data_dict[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] != \
            test_ns_dict[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY]
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
                     side_effect=node_status_docker_not_running)
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.DOCKER_RESOURCE,
                                                data=json.dumps(config_cluster_dict))
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        response_data_dict = response_data_dict[0]
        for k in response_data_dict:
            if k == api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY:
                continue
            else:
                assert response_data_dict[k] == test_ns_dict[k]
        assert response_data_dict[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert test_ns_dict[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] is True
        assert response_data_dict[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY] == \
            test_ns_dict[api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY]
        config_cluster_dict[api_constants.MGMT_WEBAPP.IP_PROPERTY] = "000.000.00.00"
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.DOCKER_RESOURCE,
                                                data=json.dumps(config_cluster_dict))
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
