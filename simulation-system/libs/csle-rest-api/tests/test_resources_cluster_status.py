import json
import csle_common.constants.constants as constants
import pytest
import pytest_mock
from csle_cluster.cluster_manager.cluster_manager_pb2 import NodeStatusDTO
from csle_common.dao.emulation_config.config import Config

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesClusterStatusSuite:
    """
    Test suite for /cluster_status url
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def config(self, mocker, example_config: Config):
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
        
        get_config_mocker = mocker.MagicMock(
            side_effect=get_config)
        return get_config_mocker

    @pytest.fixture
    def node_status(self, mocker: pytest_mock.MockFixture,
                    example_node_status: NodeStatusDTO):
        """
        Pytest fixture for mocking the get_node_status function

        :param mocker: the pytest mocker object
        :param example_node_status: example config from the
        conftest.py file
        :return: the pytest fixture for the get_node_status function
        """
        def get_node_status(ip: str, port: int) -> NodeStatusDTO:
            node_status = example_node_status
            return node_status
        get_node_status_mock = mocker.MagicMock(side_effect=get_node_status)
        return get_node_status_mock

    def test_cluster_status_get(self, flask_app, mocker,
                                node_status, config,
                                not_logged_in, logged_in,
                                logged_in_as_admin,
                                cluster_node_status):
        """
        Tests the GET HTTPS method for the /cluster_status url

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
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_node_status",
                     side_effect=node_status)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CLUSTER_STATUS_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CLUSTER_STATUS_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        response_data_dict = response_data_list[0]
        for k in response_data_dict:
            assert response_data_dict[k] == test_ns_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CLUSTER_STATUS_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        response_data_dict = response_data_list[0]
        for k in response_data_dict:
            assert response_data_dict[k] == test_ns_dict[k]
