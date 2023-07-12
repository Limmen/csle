import pytest
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesVersionSuite:
    """
    Test suite for /version resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Fixture, which is run before every test. It sets up the Flask app

        :return: the Flask app
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    def test_version_resource(self, flask_app) -> None:
        """
        Tests the GET HTTPS method for the /version resource

        :return: None
        """
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.VERSION_RESOURCE)
        assert response.status_code == 200
        assert api_constants.MGMT_WEBAPP.VERSION_RESOURCE in response.data.decode("utf-8")
        assert len(response.data.decode("utf-8").split(".")) == 3
