import logging

import csle_common.constants.constants as constants
import paramiko
import pytest
import pytest_mock
from flask import Blueprint, Flask
from flask_socketio import ConnectionRefusedError, SocketIO

import csle_rest_api.constants.constants as api_constants
import csle_rest_api.web_sockets.container_terminal.container_terminal as container_terminal
from csle_rest_api.rest_api import create_app

# from csle_rest_api import socketio

logger = logging.getLogger()


class TestWebsocketSuite:
    # app = Flask(__name__)
    # app.config['SECRET_KEY'] = 'secret!'
    # socketio = SocketIO(app)
    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")
        
    def test_web_socket_ct(self, mocker: pytest_mock.MockFixture, flask_app) -> None:
        logger.info("Hej")
        # socketio = SocketIO(flask_app)
        response = flask_app.test_client().on(api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_INPUT_MSG,
                                              namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                              f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
        logger.info(response)