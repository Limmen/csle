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
import paramiko
import csle_rest_api.constants.constants as api_constants
import csle_common.constants.constants as constants
from csle_rest_api import socketio


def get_container_terminal_bp(app):
    """
    Gets the blue print of the Web socket API for the container terminal

    :param app: the Flask app
    :return: the blue print
    """

    def ssh_connect() -> paramiko.SSHClient:
        print("Connecting")
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect("15.9.2.2", username="csle_admin", password="csle@admin-pw_191")
        conn.get_transport().set_keepalive(5)
        print("Connected successfully")
        return conn

    def set_container_terminal_winsize(fd: int, row: int, col: int, xpix: int = 0, ypix: int = 0) -> None:
        """
        Set shell window size of the container terminal

        :param fd: the file descriptor of the shell
        :param row: the number of rows of the new window size
        :param col: the number of cols of the new window size
        :param xpix: the number of x pixels of the new size
        :param ypix: the number of y pixels of the new size
        :return:
        """
        winsize = struct.pack("HHHH", row, col, xpix, ypix)
        fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)

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
                print("data ready")
                output = ssh_channel.recv(max_read_bytes).decode(errors="ignore")
                print(f"read data:{output}")
                socketio.emit(api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_OUTPUT_MSG,
                              {api_constants.MGMT_WEBAPP.OUTPUT_PROPERTY: output},
                              namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                                        f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")

    @socketio.on(api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_INPUT_MSG,
                 namespace=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
    def container_terminal_input(data) -> None:
        """
        Receives input msg on a websocket and writes it to the PTY representing the bash shell of the Container terminal.
        The pty sees this as if you are typing in a real terminal.

        :param data: the input data to write
        :return: None
        """
        cmd = data[api_constants.MGMT_WEBAPP.INPUT_PROPERTY].encode()
        ssh_channel = app.config[api_constants.MGMT_WEBAPP.CONTAINER_TERMINAL_SSH_SHELL]
        print(f"terminal input: {cmd}")
        ssh_channel.send(cmd)
        # if app.config[api_constants.MGMT_WEBAPP.CONTAINER_TERMINAL_FD]:
        #     os.write(app.config[api_constants.MGMT_WEBAPP.CONTAINER_TERMINAL_FD],
        #              data[api_constants.MGMT_WEBAPP.INPUT_PROPERTY].encode())

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
        print("terminal resize")
        # if app.config[api_constants.MGMT_WEBAPP.CONTAINER_TERMINAL_FD]:
        #     set_container_terminal_winsize(app.config[api_constants.MGMT_WEBAPP.CONTAINER_TERMINAL_FD],
        #                               data[api_constants.MGMT_WEBAPP.ROWS_PROPERTY],
        #                               data[api_constants.MGMT_WEBAPP.COLS_PROPERTY])

    @socketio.on(api_constants.MGMT_WEBAPP.WS_CONNECT_MSG,
                 namespace=f"{constants.COMMANDS.SLASH_DELIM}"
                           f"{api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE}")
    def container_terminal_connect() -> None:
        """
        Handler for new websocket connection requests for the /container-terminal namespace.

        First checks if the user is authorized and then sets up the connection

        :return: None
        """
        print("terminal connect")
        authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=False)
        if authorized is not None or (constants.CONFIG_FILE.PARSED_CONFIG is None):
            raise ConnectionRefusedError()

        term = u'xterm'
        ssh_conn = ssh_connect()
        ssh_channel = ssh_conn.invoke_shell(term=term)
        ssh_channel.setblocking(0)
        print("shell created")
        app.config[api_constants.MGMT_WEBAPP.CONTAINER_TERMINAL_SSH_SHELL] = ssh_channel
        app.config[api_constants.MGMT_WEBAPP.CONTAINER_TERMINAL_SSH_CONNECTION] = ssh_conn
        # set_container_terminal_winsize(fd, 50, 50)
        socketio.start_background_task(target=read_and_forward_container_terminal_output)

    container_terminal_bp = Blueprint(api_constants.MGMT_WEBAPP.WS_CONTAINER_TERMINAL_NAMESPACE, __name__)
    return container_terminal_bp
