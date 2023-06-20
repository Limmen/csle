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
                                                data=json.dumps({'username':'admin', 'password':'admin'}))
        
        a_response_data = a_response.data.decode("utf-8")
        a_response_data_dict = json.loads(a_response_data)
        #pytest.logger.info(a_response.status_code)

        #pytest.logger.info(response.data.decode('utf-8'))

        #pytest.logger.info(a_response_data_dict)

        assert a_response.status_code == 200
        assert a_response_data_dict[api_constants.MGMT_WEBAPP.ADMIN_PROPERTY] == True 
        assert a_response_data_dict[api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY] == api_constants.MGMT_WEBAPP.ADMIN_PROPERTY
        assert a_response_data_dict[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY] == api_constants.MGMT_WEBAPP.ADMIN_PROPERTY
        
        '''assert response.status_code == constants.HTTPS.OK_STATUS_CODE

        assert api_constants.MGMT_WEBAPP.ADMIN_PROPERTY in a_response_data
        assert api_constants.MGMT_WEBAPP.TOKEN_PROPERTY in a_response_data
        assert api_constants.MGMT_WEBAPP.USERNAME_PROPERTY in a_response_data
        assert api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY in a_response_data
        assert api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY in a_response_data
        assert api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY in a_response_data
        assert api_constants.MGMT_WEBAPP.EMAIL_PROPERTY in a_response_data
        assert api_constants.MGMT_WEBAPP.ID_PROPERTY in a_response_data'''        


    def test_successgful_guest_login(self, flask_app):
        '''Tests the /login resource when logging in with 'guest' username- and password credentials'''
    
        g_response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.LOGIN_RESOURCE,
                                            data=json.dumps({'username':'guest', 'password':'guest'}))          
        g_response_data = g_response.data.decode("utf-8")
        g_response_data_dict = json.loads (g_response_data)
        
        pytest.logger.info(g_response_data_dict)
        
        assert g_response.status_code == 200
        assert g_response_data_dict[api_constants.MGMT_WEBAPP.ADMIN_PROPERTY] == False
        assert g_response_data_dict[api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY] == 'guest'
        assert g_response_data_dict[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY] == 'guest'