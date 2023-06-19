import logging
import pytest
from csle_rest_api.rest_api import create_app
import csle_rest_api.constants.constants as api_constants


class TestResourcesVersionSuite(object):
    """
    Test suite for /version resource
    """

    pytest.logger = logging.getLogger("resources_version_tests")

    @pytest.fixture
    def flask_app(self):
        """
        Fixture, which is run before every test. It sets up the Flask app

        :return: the Flask app
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

        #OBS  pytest.logger.info för print-statements, inget annat

        #blablabla

    def test_version_resource(self, flask_app) -> None:
        """
        Tests the /version resource

        :return: None
        """
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.VERSION_RESOURCE)
        assert response.status_code == 200
        assert api_constants.MGMT_WEBAPP.VERSION_RESOURCE in response.data.decode("utf-8")
        assert len(response.data.decode("utf-8").split(".")) == 3
