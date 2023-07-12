import pytest
import csle_rest_api.constants.constants as api_constants
import csle_common.constants.constants as constants
from csle_rest_api.rest_api import create_app


class TestPagesSuite:
    """
    Suite testing the serving of HTML pages
    """

    @pytest.fixture
    def flask_app(self):
        """
        Fixture, which is run before every test. It sets up the Flask app

        :return: the Flask app
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    def test_about_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /about-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.ABOUT_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"
