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

    pytest.logger = logging.getLogger("resources_version_tests")

    @pytest.fixture
    def flask_app(self):
        """
        Fixture, which is run before every test. It sets up the Flask app

        :return: the Flask app
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    def test_login_resource(self, flask_app) -> None:
        """
        Tests the /login resource

        :return: None
        """
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.LOGIN_RESOURCE,
                                                data=json.dumps({'username':'admin', 'password':'admin'}))
        response_data = response.data.decode("utf-8")
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert api_constants.MGMT_WEBAPP.ADMIN_PROPERTY in response_data
        assert api_constants.MGMT_WEBAPP.TOKEN_PROPERTY in response_data
        assert api_constants.MGMT_WEBAPP.USERNAME_PROPERTY in response_data
        assert api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY in response_data
        assert api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY in response_data
        assert api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY in response_data
        assert api_constants.MGMT_WEBAPP.EMAIL_PROPERTY in response_data
        assert api_constants.MGMT_WEBAPP.ID_PROPERTY in response_data        
