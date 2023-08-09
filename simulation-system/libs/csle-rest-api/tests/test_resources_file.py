import json
import pytest
import pytest_mock
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app
import csle_common.constants.constants as constants


class TestResourcesFileSuite:
    """
    Test suite for /file resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def true_path(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the os.path.exists method

        :param mocker: the pytest mocker object
        :return: mocked function
        """

        def exists(path: str) -> bool:
            return True

        exists_mocker = mocker.MagicMock(side_effect=exists)
        return exists_mocker

    @pytest.fixture
    def read_data(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the open().read() method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def read() -> str:
            return "data"

        read_mocker = mocker.MagicMock(side_effect=read)
        return read_mocker

    @pytest.fixture
    def op(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the open method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def open(file: str, mode: str):
            class Open():
                def __init__(self) -> None:
                    pass

                def __enter__(self) -> "Open":
                    return self

                def __exit__(self, exc_type: str, exc_val: str, exc_tb: str) -> None:
                    pass

                def read(self) -> str:
                    return "DataSet"

            return Open()

        open_mocker = mocker.MagicMock(side_effect=open)
        return open_mocker

    @pytest.fixture
    def false_path(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the os.path.exists method

        :param mocker: the pytest mocker object
        :return: mocked function
        """

        def exists(path: str) -> bool:
            return False

        exists_mocker = mocker.MagicMock(side_effect=exists)
        return exists_mocker

    def test_file_post(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in, logged_in_as_admin,
                       true_path, false_path, op) -> None:
        """
        Testing the POST HTTPS method for the /file resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param true_path: the true_path fixture
        :param false_path: the false_path fixture
        :param op: the op fixture
        :return: None
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.FILE_RESOURCE,
                                                data=json.dumps({api_constants.MGMT_WEBAPP.PATH_PROPERTY: "null"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.FILE_RESOURCE,
                                                data=json.dumps({api_constants.MGMT_WEBAPP.PATH_PROPERTY: "null"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        mocker.patch("os.path.exists", side_effect=true_path)
        mocker.patch("builtins.open", side_effect=op)
        test_data = json.dumps({api_constants.MGMT_WEBAPP.PATH_PROPERTY: "/home/nils/csle/examples/examples.txt"})
        response = flask_app.test_client().post(
            api_constants.MGMT_WEBAPP.FILE_RESOURCE, data=test_data)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict[api_constants.MGMT_WEBAPP.LOGS_PROPERTY] == "DataSet"
        assert response_data_dict == {api_constants.MGMT_WEBAPP.LOGS_PROPERTY: "DataSet"}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        mocker.patch("os.path.exists", side_effect=false_path)
        test_data = json.dumps({api_constants.MGMT_WEBAPP.PATH_PROPERTY: "/home/nils/csle/examples/examples.txt"})
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.FILE_RESOURCE, data=test_data)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict[api_constants.MGMT_WEBAPP.LOGS_PROPERTY] == ""
        assert response_data_dict == {api_constants.MGMT_WEBAPP.LOGS_PROPERTY: ""}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
