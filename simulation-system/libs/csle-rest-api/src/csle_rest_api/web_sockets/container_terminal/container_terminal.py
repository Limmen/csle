from flask import request
from flask_socketio import ConnectionRefusedError
from flask import Blueprint
import csle_rest_api.util.rest_api_util as rest_api_util
import csle_rest_api.constants.constants as api_constants
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_rest_api import socketio


def get_container_terminal_bp(app):
    """
    Gets the blue print of the Web socket API for the container terminal

    :param app: the Flask app
    :return: the blue print
    """

    def read_and_forward_container_terminal_output() -> None:
        """
        Reads output from a given file descriptor and sends the output to the web socket

        :return: None
        """
        max_read_bytes = 1024 * 20
        while True:
            socketio.sleep(0.01)
            ssh_channel = app.config[api_constants.MGMT_WEBAPP.CONTAINER_TERMINAL_SSH_SHELL]
            data_ready = ssh_channel.recv_ready()
            if data_ready:
                output = ssh_channel.recv(max_read_bytes).decode(errors="ignore")
                socketio.emit(api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_OUTPUT_MSG,
                              {api_constants.MGMT_WEBAPP.OUTPUT_PROPERTY: output},
                              namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                        f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")

    @socketio.on(api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_INPUT_MSG,
                 namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                           f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
    def container_terminal_input(data) -> None:
        """
        Receives input msg on a websocket and writes it to the PTY representing the bash shell
        of the Container terminal.
        The pty sees this as if you are typing in a real terminal.

        :param data: the input data to write
        :return: None
        """
        cmd = data[api_constants.MGMT_WEBAPP.INPUT_PROPERTY].encode()
        ssh_channel = app.config[api_constants.MGMT_WEBAPP.CONTAINER_TERMINAL_SSH_SHELL]
        ssh_channel.send(cmd)

    @socketio.on(api_constants.MGMT_WEBAPP.WS_RESIZE_MSG,
                 namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                           f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
    def container_terminal_resize(data) -> None:
        """
        Handler when receiving a message on a websocket to resize the PTY window of a container terminal.
        The handler parses the data and resizes the window accordingly.

        :param data: data with information about the new PTY size
        :return: None
        """
        rest_api_util.set_container_terminal_winsize(
            ssh_channel=app.config[api_constants.MGMT_WEBAPP.CONTAINER_TERMINAL_SSH_SHELL],
            row=data[api_constants.MGMT_WEBAPP.ROWS_PROPERTY], col=data[api_constants.MGMT_WEBAPP.COLS_PROPERTY])

    @socketio.on(api_constants.MGMT_WEBAPP.WS_CONNECT_MSG,
                 namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                           f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
    def container_terminal_connect() -> None:
        """
        Handler for new websocket connection requests for the /container-terminal namespace.

        First checks if the user is authorized and then sets up the connection

        :return: None
        """
        authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
        config = MetastoreFacade.get_config(id=1)
        if authorized is not None or config is None:
            raise ConnectionRefusedError()
        ip_str = request.args.get(api_constants.MGMT_WEBAPP.IP_QUERY_PARAM)
        if ip_str is not None:
            ip = ip_str.replace("-", ".")
            term = u'xterm'
            ssh_conn = rest_api_util.ssh_connect(ip=ip)
            ssh_channel = ssh_conn.invoke_shell(term=term)
            ssh_channel.setblocking(0)
            rest_api_util.set_container_terminal_winsize(ssh_channel=ssh_channel, row=50, col=50)
            app.config[api_constants.MGMT_WEBAPP.CONTAINER_TERMINAL_SSH_SHELL] = ssh_channel
            app.config[api_constants.MGMT_WEBAPP.CONTAINER_TERMINAL_SSH_CONNECTION] = ssh_conn
            socketio.start_background_task(target=read_and_forward_container_terminal_output)
        else:
            ConnectionRefusedError()

    container_terminal_bp = Blueprint(api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE, __name__)
    return container_terminal_bp
