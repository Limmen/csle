import json
import numpy as np
import pytest
import pytest_mock
from flask import Flask
import csle_common.constants.constants as constants
from csle_common.dao.management.management_user import ManagementUser
from csle_common.dao.management.session_token import SessionToken
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util
from csle_rest_api.rest_api import create_app


class TestRestAPIUtilSuite:
    """
    Test suite for /experiments url
    """

    class SyntReq:
        """
        Mock class for synt reg
        """

        def __init__(self, args) -> None:
            """
            Initializes the object

            :param args: the arguments for syntreg
            """
            self.args = args

    class Args:
        """
        Mock class for syntehtic arguments to a request
        """

        def __init__(self) -> None:
            """
            Initializes the object
            """
            pass

        def get(self, token: str) -> None:
            """
            Mocks the get method of the arguments

            :param token: the token for authentication
            :return: None
            """
            return None

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def session_token(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_session_token_metadata method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_session_token_metadata(token: str) -> SessionToken:
            return SessionToken(token="null", timestamp=1.5, username="JDoe")

        get_session_token_metadata_mocker = mocker.MagicMock(side_effect=get_session_token_metadata)
        return get_session_token_metadata_mocker

    @pytest.fixture
    def session_token_exp(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_session_token_metadata method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_session_token_metadata(token: str) -> SessionToken:
            ses_tok = SessionToken(token="null", timestamp=1.5, username="JDoe")
            api_constants.SESSION_TOKENS.EXPIRE_TIME_HOURS = np.iinfo(np.int32).max
            return ses_tok

        get_session_token_metadata_mocker = mocker.MagicMock(side_effect=get_session_token_metadata)
        return get_session_token_metadata_mocker

    @pytest.fixture
    def management_user(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_management_user_by_username method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_management_user_by_username(username: str) -> ManagementUser:
            mng_user = TestRestAPIUtilSuite.get_synthetic_mng_user()
            return mng_user

        get_management_user_by_username_mocker = mocker.MagicMock(side_effect=get_management_user_by_username)
        return get_management_user_by_username_mocker

    @pytest.fixture
    def management_user_none(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_management_user_by_username method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_management_user_by_username(username: str) -> None:
            return None

        get_management_user_by_username_mocker = mocker.MagicMock(side_effect=get_management_user_by_username)
        return get_management_user_by_username_mocker

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the reomve_session_token method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def remove_session_token(session_token: SessionToken) -> None:
            return None

        remove_session_token_mocker = mocker.MagicMock(side_effect=remove_session_token)
        return remove_session_token_mocker

    @staticmethod
    def get_args() -> Args:
        """
        Returns a mock request argument

        :return: the mocked request argument
        """
        return TestRestAPIUtilSuite.Args()

    @staticmethod
    def get_synthetic_request(args) -> SyntReq:
        """
        Static help method for returning a synthetic/mocked request, customized to work for testing without the use
        of blueprint or flask app

        :param args: the arguments for the mock request
        :return: the syntethic request
        """
        return TestRestAPIUtilSuite.SyntReq(args)

    @staticmethod
    def get_synthetic_mng_user() -> ManagementUser:
        """
        Static help method for returning a synthetic/mocked management user

        :return: the mocked management user
        """
        mng_user = ManagementUser(username="JDoe", password="JDoe", email="jdoe@csle.com",
                                  first_name="John", last_name="Doe", organization="CSLE",
                                  admin=False, salt="null")
        return mng_user

    def test_util(self, flask_app, mocker: pytest_mock.MockFixture,
                  session_token, session_token_exp,
                  management_user, management_user_none, remove):
        """
        Test method for the rest-api util
        
        :param flask_app: the flask_app fixture
        :param mocker: the pytest mocker object
        :param session_token: the session_token fixture
        :param management_user: the management_user fixture
        :param remove: the remove fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_session_token_metadata",
                     side_effect=session_token)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_by_username",
                     side_effect=management_user)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_session_token", side_effect=remove)
        app = Flask(__name__)
        mng_user = TestRestAPIUtilSuite.get_synthetic_mng_user()
        args = TestRestAPIUtilSuite.get_args()
        req = TestRestAPIUtilSuite.get_synthetic_request(args)
        with app.app_context():
            response = rest_api_util.check_if_user_is_authorized(request=req)
            response1 = rest_api_util.check_if_user_edit_is_authorized(request=req, user=mng_user)
        assert response is not None
        response_data = response[0].data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        response_status_code = response[1]
        assert response_data_dict == {}
        assert response_status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response1 is not None
        response_data1 = response1[0].data.decode("utf-8")
        response_data_dict1 = json.loads(response_data1)
        response_status_code1 = response1[1]
        assert response_data_dict1 == {}
        assert response_status_code1 == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_by_username",
                     side_effect=management_user_none)
        with app.app_context():
            response1 = rest_api_util.check_if_user_edit_is_authorized(request=req, user=mng_user)
        assert response1 is not None
        response_data1 = response1[0].data.decode("utf-8")
        response_data_dict1 = json.loads(response_data1)
        response_status_code1 = response1[1]
        assert response_data_dict1 == {}
        assert response_status_code1 == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_by_username",
                     side_effect=management_user)
        with app.app_context():
            response = rest_api_util.check_if_user_is_authorized(request=req)
        assert response is not None
        response_data = response[0].data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        response_status_code = response[1]
        assert response_data_dict == {}
        assert response_status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_session_token_metadata",
                     side_effect=session_token_exp)
        with app.app_context():
            response = rest_api_util.check_if_user_is_authorized(request=req)
            response1 = rest_api_util.check_if_user_edit_is_authorized(request=req, user=mng_user)
        assert response is None
        assert response1 is not None
        assert isinstance(response1, ManagementUser)
        ex_mng_user = TestRestAPIUtilSuite.get_synthetic_mng_user()
        assert response1.username == ex_mng_user.username
        assert response1.password == ex_mng_user.password
        assert response1.admin == ex_mng_user.admin
        assert response1.id == ex_mng_user.id
        assert response1.salt == ex_mng_user.salt
        assert response1.email == ex_mng_user.email
        assert response1.first_name == ex_mng_user.first_name
        assert response1.last_name == ex_mng_user.last_name
        assert response1.organization == ex_mng_user.organization
        assert response_status_code1 == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        with app.app_context():
            response = rest_api_util.check_if_user_is_authorized(request=req, requires_admin=True)
        assert response is not None
        response_data = response[0].data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        response_status_code = response[1]
        assert response_data_dict == {}
        assert response_status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE

    def test_set_container_terminal_winsize(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the set_container_terminal_winsize utility function

        :return: None
        """
        mock_channel = mocker.MagicMock()
        mock_channel.configure_mock(**{"resize_pty.return_value": None})
        row = 2
        col = 2
        xpix = 5
        ypix = 5
        rest_api_util.set_container_terminal_winsize(ssh_channel=mock_channel, row=row, col=col, xpix=xpix, ypix=ypix)
        mock_channel.resize_pty.assert_called_once()
        mock_channel.resize_pty.assert_called_once_with(width=col, height=row, width_pixels=xpix, height_pixels=ypix)

    def test_ssh_connect(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the ssh_connect utility function

        :return: None
        """
        mock_conn = mocker.MagicMock()
        mock_transport = mocker.MagicMock()
        mock_conn.configure_mock(**{"set_missing_host_key_policy.return_value": None})
        mock_conn.configure_mock(**{"connect.return_value": None})
        mock_conn.configure_mock(**{"get_transport.return_value": mock_transport})
        mock_conn.configure_mock(**{"set_keepalive.return_value": None})
        mocker.patch("paramiko.SSHClient", return_value=mock_conn)
        ip = "test_ip"
        rest_api_util.ssh_connect(ip=ip)
        mock_conn.set_missing_host_key_policy.assert_called_once()
        mock_conn.connect.assert_called_once()
        mock_conn.connect.assert_called_once_with(ip, username=constants.CSLE_ADMIN.SSH_USER,
                                                  password=constants.CSLE_ADMIN.SSH_PW)
        mock_conn.get_transport.assert_called_once()
        mock_transport.set_keepalive.assert_called_once()
