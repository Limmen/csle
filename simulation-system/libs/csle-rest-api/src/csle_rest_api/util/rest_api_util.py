from typing import Tuple, Union
from flask import Response, jsonify
import paramiko
import csle_common.constants.constants as constants
from csle_common.dao.management.management_user import ManagementUser
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_rest_api.constants.constants as api_constants


def check_if_user_is_authorized(request, requires_admin: bool = False) -> Union[None, Tuple[Response, int]]:
    """
    Checks if a user request is authorized

    :param request: the request to check
    :param requires_admin: boolean flag indicating whether only admins are authorized or not
    :return: the non-authorized response or None
    """
    # Extract token and check if user is authorized
    token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
    token_obj = MetastoreFacade.get_session_token_metadata(token=token)
    if token_obj is None:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.UNAUTHORIZED_STATUS_CODE

    user = None
    if requires_admin:
        user = MetastoreFacade.get_management_user_by_username(username=token_obj.username)
    if token_obj is None or token_obj.expired(valid_length_hours=api_constants.SESSION_TOKENS.EXPIRE_TIME_HOURS) \
            or (requires_admin and user is not None and not user.admin):
        if token_obj is not None:
            MetastoreFacade.remove_session_token(session_token=token_obj)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.UNAUTHORIZED_STATUS_CODE
    else:
        return None


def check_if_user_edit_is_authorized(request, user: ManagementUser) -> Union[None, ManagementUser,
                                                                             Tuple[Response, int]]:
    """
    Check if a user is authorized to edit another user

    :param request: the request to extract the user from
    :return: the non-authorized response or the user
    """

    # Extract token and check if user is authorized
    token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
    token_obj = MetastoreFacade.get_session_token_metadata(token=token)
    request_user = None
    if token_obj is not None:
        request_user = MetastoreFacade.get_management_user_by_username(username=token_obj.username)
    if token_obj is None or token_obj.expired(valid_length_hours=api_constants.SESSION_TOKENS.EXPIRE_TIME_HOURS) \
            or request_user is None or (not request_user.admin and request_user.username != user.username):
        if token_obj is not None:
            MetastoreFacade.remove_session_token(session_token=token_obj)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.UNAUTHORIZED_STATUS_CODE
    else:
        return request_user


def set_container_terminal_winsize(ssh_channel: paramiko.Channel, row: int, col: int, xpix: int = 0, ypix: int = 0) \
        -> None:
    """
    Set shell window size of the host terminal

    :param ssh_channel: the ssh_channel of the shell
    :param row: the number of rows of the new window size
    :param col: the number of cols of the new window size
    :param xpix: the number of x pixels of the new size
    :param ypix: the number of y pixels of the new size
    :return:
    """
    ssh_channel.resize_pty(width=col, height=row, width_pixels=xpix, height_pixels=ypix)


def ssh_connect(ip: str) -> paramiko.SSHClient:
    """
    Sets up an SSH connection to a given IP using the CSLE admin account

    :param ip: the IP to connect to
    :return: the created ssh connection
    """
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(ip, username=constants.CSLE_ADMIN.SSH_USER, password=constants.CSLE_ADMIN.SSH_PW)
    transport = conn.get_transport()
    if transport is not None:
        transport.set_keepalive(5)
    else:
        raise ValueError("Could not connect with SSH")
    return conn
