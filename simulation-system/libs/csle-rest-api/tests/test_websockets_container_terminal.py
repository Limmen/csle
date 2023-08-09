import pytest
import pytest_mock
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app
from csle_rest_api import socketio
from csle_common.dao.emulation_config.config import Config


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

    @pytest.fixture
    def config(self, mocker: pytest_mock.MockFixture, example_config: Config):
        """
        Fixture for mocking the config side-effect

        :param mocker: the pytest mocker object
        :param example_config: the example config to use for mocking
        :return: the mock
        """

        def get_config(id: int) -> Config:
            config = example_config
            return config

        get_config_mock = mocker.MagicMock(side_effect=get_config)
        return get_config_mock

    def test_connect(self, flask_app, mocker: pytest_mock.MockFixture, logged_in_as_admin, logged_in, not_logged_in,
                     config) -> None:
        """
        Tests the connection to the websocket

        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        client1 = socketio.test_client(
            flask_app, namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                 f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}",
            flask_test_client=flask_app.test_client())
        assert not client1.is_connected()
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        client2 = socketio.test_client(
            flask_app, namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                 f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}",
            flask_test_client=flask_app.test_client())
        assert not client2.is_connected()
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        client3 = socketio.test_client(
            flask_app, namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                 f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}",
            flask_test_client=flask_app.test_client())
        assert not client3.is_connected()
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        mock_ssh_conn = mocker.MagicMock()
        mock_ssh_channel = mocker.MagicMock()
        mocker.patch("csle_rest_api.util.rest_api_util.ssh_connect", return_value=mock_ssh_conn)
        mocker.patch("csle_rest_api.util.rest_api_util.set_container_terminal_winsize", return_value=None)
        mock_ssh_conn.configure_mock(**{"invoke_shell.return_value": mock_ssh_channel})
        mock_ssh_channel.configure_mock(**{"setblocking.return_value": None})
        mock_ssh_channel.configure_mock(**{"recv_ready.return_value": False})
        ip = "172.10.10.10"
        client4 = socketio.test_client(
            flask_app, namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                 f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}",
            flask_test_client=flask_app.test_client(), query_string=f"?{api_constants.MGMT_WEBAPP.IP_QUERY_PARAM}={ip}")
        mock_ssh_conn.invoke_shell.assert_called_once()
        mock_ssh_conn.invoke_shell.assert_called_once_with(term="xterm")
        mock_ssh_channel.setblocking.assert_called_once_with(0)
        assert client4.is_connected(namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                              f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
        client5 = socketio.test_client(
            flask_app, namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                 f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}",
            flask_test_client=flask_app.test_client(), query_string=f"?{api_constants.MGMT_WEBAPP.IP_QUERY_PARAM}={ip}")
        assert client5.is_connected(namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                              f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
        assert client4.eio_sid != client5.eio_sid
        received = client4.get_received(namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                                  f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
        assert len(received) == 0
        client4.disconnect(namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                     f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
        assert not client4.is_connected(namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                                  f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
        assert client5.is_connected(namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                              f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
        client5.disconnect(namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                     f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
        assert not client5.is_connected(namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                                  f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")

    def test_container_terminal_resize(self, flask_app, mocker: pytest_mock.MockFixture, logged_in_as_admin, config) \
            -> None:
        """
        Tests the terminal resize event of the websocket

        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        mock_ssh_conn = mocker.MagicMock()
        mock_ssh_channel = mocker.MagicMock()
        mocker.patch("csle_rest_api.util.rest_api_util.ssh_connect", return_value=mock_ssh_conn)
        mocker.patch("csle_rest_api.util.rest_api_util.set_container_terminal_winsize", return_value=None)
        mock_ssh_conn.configure_mock(**{"invoke_shell.return_value": mock_ssh_channel})
        mock_ssh_channel.configure_mock(**{"setblocking.return_value": None})
        mock_ssh_channel.configure_mock(**{"recv_ready.return_value": False})
        ip = "172.10.10.10"
        client = socketio.test_client(
            flask_app, namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                 f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}",
            flask_test_client=flask_app.test_client(), query_string=f"?{api_constants.MGMT_WEBAPP.IP_QUERY_PARAM}={ip}")
        data = {api_constants.MGMT_WEBAPP.COLS_PROPERTY: 5, api_constants.MGMT_WEBAPP.ROWS_PROPERTY: 5}
        client.emit(api_constants.MGMT_WEBAPP.WS_RESIZE_MSG, data,
                    namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                              f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
        assert client.is_connected(namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                             f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")

    def test_container_terminal_input(self, flask_app, mocker: pytest_mock.MockFixture, logged_in_as_admin, config) \
            -> None:
        """
        Tests the input event of the websocket

        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        mock_ssh_conn = mocker.MagicMock()
        mock_ssh_channel = mocker.MagicMock()
        mocker.patch("csle_rest_api.util.rest_api_util.ssh_connect", return_value=mock_ssh_conn)
        mocker.patch("csle_rest_api.util.rest_api_util.set_container_terminal_winsize", return_value=None)
        mock_ssh_conn.configure_mock(**{"invoke_shell.return_value": mock_ssh_channel})
        mock_ssh_channel.configure_mock(**{"setblocking.return_value": None})
        mock_ssh_channel.configure_mock(**{"recv_ready.return_value": False})
        ip = "172.10.10.10"
        client = socketio.test_client(
            flask_app, namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                 f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}",
            flask_test_client=flask_app.test_client(), query_string=f"?{api_constants.MGMT_WEBAPP.IP_QUERY_PARAM}={ip}")
        data = {api_constants.MGMT_WEBAPP.INPUT_PROPERTY: "mydata"}
        client.emit(api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_INPUT_MSG, data,
                    namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                              f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
        assert client.is_connected(namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                             f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
        mock_ssh_channel.send.assert_called_once_with("mydata".encode())
