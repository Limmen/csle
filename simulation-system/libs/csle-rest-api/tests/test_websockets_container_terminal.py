import pytest
import pytest_mock
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app
from csle_rest_api import socketio
from csle_rest_api.web_sockets.container_terminal.container_terminal import get_container_terminal_bp


class TestWebsocketsContainerTerminalSuite:
    """
    Test suite for /container-terminal websocket
    """

    @pytest.fixture
    def flask_app(self):
        """
        Fixture, which is run before every test. It sets up the Flask app

        :return: the Flask app
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    # def test_connect(self, flask_app) -> None:
    #     """
    #     Tests the connection to the websocket
    #
    #     :return: None
    #     """
    #     client = socketio.test_client(flask_app, auth={'foo': 'bar'})
