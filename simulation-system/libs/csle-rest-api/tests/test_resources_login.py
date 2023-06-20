import logging
import pytest
import json
from csle_rest_api.rest_api import create_app
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants


class TestResourcesLoginSuite(object):
    """
    Test suite for /login resource
    """

    pytest.logger = logging.getLogger("resources_login_tests")

    @pytest.fixture
    def flask_app(self):
        """
        Fixture, which is run before every test. It sets up the Flask app

        :return: the Flask app
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    def test_successful_admin_login(self, flask_app) -> None:
        """
        Tests the /login resource when logging in with 'admin' and 'admin as
        username- and password credentials
        """

        a_response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.LOGIN_RESOURCE, 
        data=json.dumps({'username': 'admin', 'password': 'admin'}))
        a_response_data = a_response.data.decode("utf-8")
        a_response_data_dict = json.loads(a_response_data)
        # pytest.logger.info(a_response_data_dict)
        assert a_response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert a_response_data_dict[api_constants.MGMT_WEBAPP.ADMIN_PROPERTY] is True
        assert a_response_data_dict[api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY] == api_constants.MGMT_WEBAPP.ADMIN_PROPERTY
        assert a_response_data_dict[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY] == api_constants.MGMT_WEBAPP.ADMIN_PROPERTY
        assert len(a_response_data_dict.keys()) == len(a_response_data_dict.values())

    def test_successgful_guest_login(self, flask_app):
        '''Tests the /login resource when logging in with 'guest' username- and password credentials'''

        g_response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.LOGIN_RESOURCE,
                                            data=json.dumps({'username': 'guest', 'password': 'guest'}))
        g_response_data = g_response.data.decode("utf-8")

        g_response_data_dict = json.loads(g_response_data)

        pytest.logger.info(g_response_data)

        assert g_response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert g_response_data_dict[api_constants.MGMT_WEBAPP.ADMIN_PROPERTY] is False
        assert g_response_data_dict[api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY] == 'guest'
        assert g_response_data_dict[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY] == 'guest'
        assert len(g_response_data_dict.keys()) == len(g_response_data_dict.values())

    def test_unsuccessful_login(self, flask_app):
        '''Ensuring that unauthorized login credential fails to enter'''

        f_response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.LOGIN_RESOURCE,
                                            data=json.dumps({'username': 'asdf', 'password': 'asdf'}))
        # pytest.logger.info(f_response.status_code)

        assert f_response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE

    def test_malformed_login_request(slf, flask_app):

        '''Testing malformed login request. Please note that explicit return-statements
        had to be added at row 30 and 38 in the /login resource file, routes.py'''

        m_response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.LOGIN_RESOURCE, data=json.dumps({}))
        # pytest.logger.info(m_response.status_code)

        assert m_response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
