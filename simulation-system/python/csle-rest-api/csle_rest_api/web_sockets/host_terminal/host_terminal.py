from flask import request
import csle_rest_api.util.rest_api_util as rest_api_util
from flask_socketio import ConnectionRefusedError
from flask import Blueprint
import os
import pty
import struct
import fcntl
import subprocess
import termios
import select
import csle_rest_api.constants.constants as api_constants
import csle_common.constants.constants as constants
from csle_rest_api import socketio


def get_host_terminal_bp(app):
    """
    Gets the blue print of the Web socket API for the host terminal

    :param app: the Flask app
    :return: the blue print
    """

    def set_host_terminal_winsize(fd: int, row: int, col: int, xpix: int = 0, ypix: int = 0) -> None:
        """
        Set shell window size of the host terminal

        :param fd: the file descriptor of the shell
        :param row: the number of rows of the new window size
        :param col: the number of cols of the new window size
        :param xpix: the number of x pixels of the new size
        :param ypix: the number of y pixels of the new size
        :return:
        """
        winsize = struct.pack("HHHH", row, col, xpix, ypix)
        fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)

    def read_and_forward_host_terminal_output() -> None:
        """
        Reads output from a given file descriptor and sends the output to the web socket

        :return: None
        """
        max_read_bytes = 1024 * 20
        while True:
            socketio.sleep(0.01)
            if app.config[api_constants.MGMT_WEBAPP.HOST_TERMINAL_FD]:
                timeout_sec = 0
                (data_ready, _, _) = select.select([app.config[api_constants.MGMT_WEBAPP.HOST_TERMINAL_FD]],
                                                   [], [], timeout_sec)
                if data_ready:
                    output = os.read(app.config[api_constants.MGMT_WEBAPP.HOST_TERMINAL_FD], max_read_bytes).decode(
                        errors="ignore")
                    socketio.emit(api_constants.MGMT_WEBAPP.WS_HOST_TERMINAL_OUTPUT_MSG,
                                  {api_constants.MGMT_WEBAPP.OUTPUT_PROPERTY: output},
                                  namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                            f"{api_constants.MGMT_WEBAPP.WS_HOST_TERMINAL_NAMESPACE}")

    @socketio.on(api_constants.MGMT_WEBAPP.WS_HOST_TERMINAL_INPUT_MSG,
                 namespace=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.WS_HOST_TERMINAL_NAMESPACE}")
    def host_terminal_input(data) -> None:
        """
        Receives input msg on a websocket and writes it to the PTY representing the bash shell of the Host terminal.
        The pty sees this as if you are typing in a real terminal.

        :param data: the input data to write
        :return: None
        """
        if app.config[api_constants.MGMT_WEBAPP.HOST_TERMINAL_FD]:
            os.write(app.config[api_constants.MGMT_WEBAPP.HOST_TERMINAL_FD],
                     data[api_constants.MGMT_WEBAPP.INPUT_PROPERTY].encode())

    @socketio.on(api_constants.MGMT_WEBAPP.WS_RESIZE_MSG,
                 namespace=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.WS_HOST_TERMINAL_NAMESPACE}")
    def host_terminal_resize(data) -> None:
        """
        Handler when receiving a message on a websocket to resize the PTY window of a host terminal.
        The handler parses the data and resizes the window accordingly.

        :param data: data with information about the new PTY size
        :return: None
        """
        if app.config[api_constants.MGMT_WEBAPP.HOST_TERMINAL_FD]:
            set_host_terminal_winsize(app.config[api_constants.MGMT_WEBAPP.HOST_TERMINAL_FD],
                                      data[api_constants.MGMT_WEBAPP.ROWS_PROPERTY],
                                      data[api_constants.MGMT_WEBAPP.COLS_PROPERTY])

    @socketio.on(api_constants.MGMT_WEBAPP.WS_CONNECT_MSG,
                 namespace=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.WS_HOST_TERMINAL_NAMESPACE}")
    def host_terminal_connect() -> None:
        """
        Handler for new websocket connection requests for the /host-terminal namespace.

        First checks if the user is authorized and then sets up the connection

        :return: None
        """
        authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
        if authorized is not None or (constants.CONFIG_FILE.PARSED_CONFIG is None
                                      or not constants.CONFIG_FILE.PARSED_CONFIG.allow_host_shell):
            raise ConnectionRefusedError()
        if app.config[api_constants.MGMT_WEBAPP.HOST_TERMINAL_CHILD_PID]:
            return
        (child_pid, fd) = pty.fork()
        if child_pid == 0:
            subprocess.run(app.config[api_constants.MGMT_WEBAPP.HOST_TERMINAL_CMD])
        else:
            app.config[api_constants.MGMT_WEBAPP.HOST_TERMINAL_FD] = fd
            app.config[api_constants.MGMT_WEBAPP.HOST_TERMINAL_CHILD_PID] = child_pid
            set_host_terminal_winsize(fd, 50, 50)
            socketio.start_background_task(target=read_and_forward_host_terminal_output)

    host_terminal_bp = Blueprint('main', __name__)
    return host_terminal_bp
