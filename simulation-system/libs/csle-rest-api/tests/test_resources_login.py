import json
import logging

import csle_common.constants.constants as constants
import pytest

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesLoginSuite(object):
    """
    Test suite for /login resource
    """

    pytest.logger = logging.getLogger("resources_login_tests")

    @pytest.fixture
    def flask_app(self):
        """
        :return: the flask app fixture representing the webserver
        """
        return create_app(
            static_folder="../../../../../management-system/csle-mgmt-webapp/build"
        )

    @pytest.mark.usefixtures("database", "save", "token", "update")
    def test_successful_admin_login(self, flask_app, mocker, database, token, save, update) -> None:
        """
        Tests the /login resource when logging in with 'admin' and 'admin as
        username- and password credentials

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param database: the database fixture
        :param token: the token fixture
        :return: None
        """
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_by_username",
            side_effect=database,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_session_token_by_username",
            side_effect=token,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.save_session_token",
            side_effect=save,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.update_session_token",
            side_effect=update,
        )
        a_response = flask_app.test_client().post(
            api_constants.MGMT_WEBAPP.LOGIN_RESOURCE,
            data=json.dumps({"username": "admin", "password": "admin"}),
        )
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
        assert (
            a_response_data_dict[api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY]
            == "Admin"
        )
        assert (
            a_response_data_dict[api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY]
            == "Adminson"
        )
        assert (
            a_response_data_dict[api_constants.MGMT_WEBAPP.EMAIL_PROPERTY]
            == "admin@CSLE.com"
        )
        assert (
            a_response_data_dict[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY] == "admin"
        )
        assert (
            a_response_data_dict[api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY]
            == "CSLE"
        )

    def test_successful_guest_login(
        self, flask_app, mocker, database, token, save, update
    ) -> None:
        """
        Tests the /login resource when logging in with 'guest' username- and password credentials

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param database: the database fixture
        :param token: the token fixture
        :return: None
        """
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_by_username",
            side_effect=database,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_session_token_by_username",
            side_effect=token,
        )

        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.save_session_token",
            side_effect=save,
        )

        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.update_session_token",
            side_effect=update,
        )

        g_response = flask_app.test_client().post(
            api_constants.MGMT_WEBAPP.LOGIN_RESOURCE,
            data=json.dumps({"username": "guest", "password": "guest"}),
        )
        response_data = g_response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        pytest.logger.info(response_data_dict)
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
        assert (
            response_data_dict[api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY] == "Guest"
        )
        assert (
            response_data_dict[api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY]
            == "Guestson"
        )
        assert (
            response_data_dict[api_constants.MGMT_WEBAPP.EMAIL_PROPERTY]
            == "guest@CSLE.com"
        )
        assert (
            response_data_dict[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY] == "guest"
        )
        assert (
            response_data_dict[api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY]
            == "CSLE"
        )
        assert (
            response_data_dict[api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY] == "Guest"
        )
        assert (
            response_data_dict[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY] == "guest"
        )

    def test_unsuccessful_login(
        self, flask_app, mocker, database, token, save, update
    ) -> None:
        """
        Ensuring that unauthorized login credential fails to enter

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param database: the database fixture
        :param token: the token fixture
        :return: None
        """
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_by_username",
            side_effect=database,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_session_token_by_username",
            side_effect=token,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.save_session_token",
            side_effect=save,
        )

        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.update_session_token",
            side_effect=update,
        )
        f_response = flask_app.test_client().post(
            api_constants.MGMT_WEBAPP.LOGIN_RESOURCE,
            data=json.dumps({"username": "asdf", "password": "asdf"}),
        )
        response_data = f_response.data.decode("utf-8")
        response_dict = json.loads(response_data)
        assert f_response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_dict == {}

    def test_malformed_login_request(
        self, flask_app, mocker, database, token, save, update
    ) -> None:
        """
        Testing malformed login request. Please note that explicit return-statements
        had to be added at row 30 and 38 in the /login resource file, routes.py

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param database: the database fixture
        :param token: the token fixture
        :return: None
        """
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_by_username",
            side_effect=database,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_session_token_by_username",
            side_effect=token,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.save_session_token",
            side_effect=save,
        )

        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.update_session_token",
            side_effect=update,
        )
        m_response = flask_app.test_client().post(
            api_constants.MGMT_WEBAPP.LOGIN_RESOURCE, data=json.dumps({})
        )

        response_data = m_response.data.decode("utf-8")
        response_dict = json.loads(response_data)
        pytest.logger.info(m_response)
        assert m_response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_dict == {}
