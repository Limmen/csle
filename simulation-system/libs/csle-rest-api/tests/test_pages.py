import csle_common.constants.constants as constants
import pytest

import csle_rest_api.constants.constants as api_constants
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

    def test_container_terminal_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /container-terminal-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CONTAINER_TERMINAL_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_control_plane_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /control-plane-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CONTROL_PLANE_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_downloads_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-downloads-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DOWNLOADS_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_emulation_statistics_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-emulation-statistics URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_emulations_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-emulations-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.EMULATIONS_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_images_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-images-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.IMAGES_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_jobs_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-jobs-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.JOBS_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_login_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-login-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.LOGIN_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_logs_admin_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-logs-admin-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.LOGS_ADMIN_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_monitoring_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-monitoring-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.MONITORING_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_policies_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-policies-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.POLICIES_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_policy_examination_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-policy-examination-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.POLICY_EXAMINATION_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_register_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-register-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.REGISTER_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_sdn_cnotrollers_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-sdn-controllers-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_server_cluster_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-server-cluster-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SERVER_CLUSTER_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_simulations_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-simulations-page-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SIMULATIONS_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_system_admin_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-system-admin-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SYSTEM_ADMIN_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_system_models_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-system-models-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SYSTEM_MODELS_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_traces_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-traces-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.TRACES_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_training_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-training-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.TRAINING_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"

    def test_user_admin_page(self, flask_app, mocker) -> None:
        """
        Tests the GET HTTP method for the /test-user-admin-page URL

        :return: None
        """
        mocker.patch("flask.Blueprint.send_static_file", return_value="html")
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.USER_ADMIN_PAGE_RESOURCE)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        data = response.data.decode("utf-8")
        assert data is not None
        assert data != ""
        assert data == "html"
