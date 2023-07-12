from typing import Union
import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app
from csle_common.dao.management.session_token import SessionToken


class TestResourcesLoginSuite:
    """
    Test suite for /login resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def token(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking login tokens
        :param mocker: the pytest mocker object
        :return: the token fixture for mocking the token calls to the database
        """
        from csle_common.dao.management.session_token import SessionToken

        def get_session_token_by_username(username: str) -> Union[SessionToken, None]:
            if username == "admin":
                return SessionToken(token="123", timestamp=0.0, username="admin")
            elif username == "guest":
                return SessionToken(token="123", timestamp=0.0, username="guest")
            else:
                return None

        get_session_token_by_username_mock = mocker.MagicMock(side_effect=get_session_token_by_username)
        return get_session_token_by_username_mock

    @pytest.fixture
    def database(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking the database

        :param mocker: the pytest mocker object
        :return: fixture for mocking the users in the database
        """
        import bcrypt
        from csle_common.dao.management.management_user import ManagementUser

        def get_management_user_by_username(username: str) -> Union[ManagementUser, None]:
            if username == "admin":
                byte_pwd = "admin".encode("utf-8")
                salt = bcrypt.gensalt()
                pw_hash = bcrypt.hashpw(byte_pwd, salt)
                password = pw_hash.decode("utf-8")
                user = ManagementUser(
                    username="admin", password=password, email="admin@CSLE.com", admin=True, first_name="Admin",
                    last_name="Adminson", organization="CSLE", salt=salt.decode("utf-8"))
                user.id = 1
                return user
            elif username == "guest":
                byte_pwd = "guest".encode("utf-8")
                salt = bcrypt.gensalt()
                pw_hash = bcrypt.hashpw(byte_pwd, salt)
                password = pw_hash.decode("utf-8")
                user = ManagementUser(username="guest", password=password, email="guest@CSLE.com", admin=False,
                                      first_name="Guest", last_name="Guestson", organization="CSLE",
                                      salt=salt.decode("utf-8"))
                user.id = 2
                return user
            else:
                return None

        get_management_user_by_username_mock = mocker.MagicMock(side_effect=get_management_user_by_username)
        return get_management_user_by_username_mock

    @pytest.fixture
    def save(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking the save_session_token call

        :param mocker: the pytest mocker object
        :return: fixture for mocking the save_session_token_call
        """
        def save_session_token(session_token: SessionToken) -> str:
            return "mytesttoken"

        save_session_token_mock = mocker.MagicMock(side_effect=save_session_token)
        return save_session_token_mock

    @pytest.fixture
    def update(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking the session-update function call

        :param mocker: the pytest mocker object
        :return: fixture for mocking the update_session_token call
        """
        def update_session_token(session_token: SessionToken, token: str) -> None:
            return None
        update_session_token_mock = mocker.MagicMock(side_effect=update_session_token)
        return update_session_token_mock

    def test_successful_admin_login(self, flask_app, mocker: pytest_mock.MockFixture, database, token, save,
                                    update) -> None:
        """
        Tests the /login resource when logging in with 'admin' and 'admin as
        username- and password credentials

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param database: the database fixture
        :param token: the token fixture
        :param save: the save fixture
        :param update: the update fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_by_username",
                     side_effect=database)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_session_token_by_username",
                     side_effect=token)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.save_session_token", side_effect=save)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.update_session_token", side_effect=update)
        a_response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.LOGIN_RESOURCE,
                                                  data=json.dumps({"username": "admin", "password": "admin"}))
        a_response_data = a_response.data.decode("utf-8")
        a_response_data_dict = json.loads(a_response_data)
        assert a_response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert len(a_response_data_dict.keys()) == 8
        assert api_constants.MGMT_WEBAPP.TOKEN_PROPERTY in a_response_data_dict
        assert api_constants.MGMT_WEBAPP.ADMIN_PROPERTY in a_response_data_dict
        assert api_constants.MGMT_WEBAPP.USERNAME_PROPERTY in a_response_data_dict
        assert api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY in a_response_data_dict
        assert api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY in a_response_data_dict
        assert api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY in a_response_data_dict
        assert api_constants.MGMT_WEBAPP.EMAIL_PROPERTY in a_response_data_dict
        assert api_constants.MGMT_WEBAPP.ID_PROPERTY in a_response_data_dict
        assert a_response_data_dict[api_constants.MGMT_WEBAPP.ADMIN_PROPERTY] is True
        assert a_response_data_dict[api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY] == "Admin"
        assert a_response_data_dict[api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY] == "Adminson"
        assert a_response_data_dict[api_constants.MGMT_WEBAPP.EMAIL_PROPERTY] == "admin@CSLE.com"
        assert a_response_data_dict[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY] == "admin"
        assert a_response_data_dict[api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY] == "CSLE"

    def test_successful_guest_login(self, flask_app, mocker: pytest_mock.MockFixture, database, token, save,
                                    update) -> None:
        """
        Tests the /login resource when logging in with 'guest' username- and password credentials

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param database: the database fixture
        :param token: the token fixture
        :param save: the save fixture
        :param update: the update fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_by_username",
                     side_effect=database)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_session_token_by_username",
                     side_effect=token)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.save_session_token", side_effect=save)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.update_session_token", side_effect=update)
        g_response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.LOGIN_RESOURCE,
                                                  data=json.dumps({"username": "guest", "password": "guest"}))
        response_data = g_response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert g_response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert len(response_data_dict.keys()) == 8
        assert api_constants.MGMT_WEBAPP.TOKEN_PROPERTY in response_data_dict
        assert api_constants.MGMT_WEBAPP.ADMIN_PROPERTY in response_data_dict
        assert api_constants.MGMT_WEBAPP.USERNAME_PROPERTY in response_data_dict
        assert api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY in response_data_dict
        assert api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY in response_data_dict
        assert api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY in response_data_dict
        assert api_constants.MGMT_WEBAPP.EMAIL_PROPERTY in response_data_dict
        assert api_constants.MGMT_WEBAPP.ID_PROPERTY in response_data_dict
        assert response_data_dict[api_constants.MGMT_WEBAPP.ADMIN_PROPERTY] is False
        assert response_data_dict[api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY] == "Guest"
        assert response_data_dict[api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY] == "Guestson"
        assert response_data_dict[api_constants.MGMT_WEBAPP.EMAIL_PROPERTY] == "guest@CSLE.com"
        assert response_data_dict[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY] == "guest"
        assert response_data_dict[api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY] == "CSLE"
        assert response_data_dict[api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY] == "Guest"
        assert response_data_dict[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY] == "guest"

    def test_unsuccessful_login(self, flask_app, mocker: pytest_mock.MockFixture, database, token, save, update) \
            -> None:
        """
        Ensuring that unauthorized login credential fails to enter

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param database: the database fixture
        :param token: the token fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_by_username",
                     side_effect=database)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_session_token_by_username",
                     side_effect=token)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.save_session_token", side_effect=save)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.update_session_token", side_effect=update)
        f_response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.LOGIN_RESOURCE,
                                                  data=json.dumps({"username": "asdf", "password": "asdf"}))
        assert f_response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE

    def test_malformed_login_request(self, flask_app, mocker: pytest_mock.MockFixture, database, token, save,
                                     update) -> None:
        """
        Testing malformed login request. Please note that explicit return-statements
        had to be added at row 30 and 38 in the /login resource file, routes.py

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param database: the database fixture
        :param token: the token fixture
        :param save: the save fixture
        :param update: the update fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_by_username",
                     side_effect=database)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_session_token_by_username",
                     side_effect=token)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.save_session_token", side_effect=save)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.update_session_token", side_effect=update)
        m_response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.LOGIN_RESOURCE, data=json.dumps({}))
        response_data = m_response.data.decode("utf-8")
        response_dict = json.loads(response_data)
        assert m_response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_dict
