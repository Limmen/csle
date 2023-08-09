import json
import pytest
import pytest_mock
from csle_common.dao.emulation_config.config import Config
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app
import csle_common.constants.constants as constants


class TestResourcesServerClusterSuite:
    """
    Test suite for /server-cluster resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def read(self, mocker: pytest_mock.MockFixture, example_config: Config):
        """
        Pytest fixture for mocking the read_config_file method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def read_config_file() -> Config:
            conf = example_config
            return conf
        read_config_file_mocker = mocker.MagicMock(side_effect=read_config_file)
        return read_config_file_mocker

    @pytest.fixture
    def read_error(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the read_config_file method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def read_config_file() -> None:
            return None
        read_config_file_mocker = mocker.MagicMock(side_effect=read_config_file)
        return read_config_file_mocker

    def test_server_cluster_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                logged_in_as_admin, read, read_error, example_config) -> None:
        """
        Testing GET HTTPS method for the /server-cluster method

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param read: the read fixture
        """
        mocker.patch("csle_common.dao.emulation_config.config.Config.read_config_file", side_effect=read)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SERVER_CLUSTER_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SERVER_CLUSTER_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_conf = example_config
        ex_conf_dict = ex_conf.cluster_config.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_conf_dict[k]
        mocker.patch("csle_common.dao.emulation_config.config.Config.read_config_file", side_effect=read_error)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SERVER_CLUSTER_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.INTERNAL_SERVER_ERROR_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SERVER_CLUSTER_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_conf = example_config
        ex_conf_dict = ex_conf.cluster_config.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_conf_dict[k]
        mocker.patch("csle_common.dao.emulation_config.config.Config.read_config_file", side_effect=read_error)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SERVER_CLUSTER_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.INTERNAL_SERVER_ERROR_STATUS_CODE
