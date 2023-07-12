"""
Routes and sub-resources for the /login resource
"""
from typing import Tuple
import json
import secrets
import time
import bcrypt
import csle_common.constants.constants as constants
from csle_common.dao.management.session_token import SessionToken
from csle_common.metastore.metastore_facade import MetastoreFacade
from flask import Blueprint, jsonify, request, Response
import csle_rest_api.constants.constants as api_constants

# Creates a blueprint "sub application" of the main REST app
login_bp = Blueprint(api_constants.MGMT_WEBAPP.LOGIN_RESOURCE, __name__,
                     url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.LOGIN_RESOURCE}")


@login_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def read_login() -> Tuple[Response, int]:
    """
    The /login resource

    :return: Authenticates the login information and returns the result
    """
    token = secrets.token_urlsafe(32)
    json_data = json.loads(request.data)
    if api_constants.MGMT_WEBAPP.USERNAME_PROPERTY not in json_data:
        response_str = f"{api_constants.MGMT_WEBAPP.USERNAME_PROPERTY} not provided"
        return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                constants.HTTPS.BAD_REQUEST_STATUS_CODE)
    username = json_data[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY]
    user_account = MetastoreFacade.get_management_user_by_username(username=username)
    response_code = constants.HTTPS.UNAUTHORIZED_STATUS_CODE
    response = jsonify({})
    if user_account is not None:
        if api_constants.MGMT_WEBAPP.PASSWORD_PROPERTY not in json_data:
            response_str = f"{api_constants.MGMT_WEBAPP.PASSWORD_PROPERTY} not provided"
            return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                    constants.HTTPS.BAD_REQUEST_STATUS_CODE)
        password = json_data[api_constants.MGMT_WEBAPP.PASSWORD_PROPERTY]
        byte_pwd = password.encode("utf-8")
        pw_hash = bcrypt.hashpw(byte_pwd, user_account.salt.encode("utf-8")).decode("utf-8")
        if user_account.password == pw_hash:
            response_code = constants.HTTPS.OK_STATUS_CODE
            new_token = MetastoreFacade.get_session_token_by_username(username=username)
            ts = time.time()
            if new_token is None:
                new_token = SessionToken(token=token, username=username, timestamp=ts)
                MetastoreFacade.save_session_token(session_token=new_token)
            else:
                new_token.timestamp = ts
                MetastoreFacade.update_session_token(
                    session_token=new_token, token=new_token.token
                )
            data_dict = {
                api_constants.MGMT_WEBAPP.TOKEN_PROPERTY: new_token.token,
                api_constants.MGMT_WEBAPP.ADMIN_PROPERTY: user_account.admin,
                api_constants.MGMT_WEBAPP.USERNAME_PROPERTY: user_account.username,
                api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY: user_account.first_name,
                api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY: user_account.last_name,
                api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY: user_account.organization,
                api_constants.MGMT_WEBAPP.EMAIL_PROPERTY: user_account.email,
                api_constants.MGMT_WEBAPP.ID_PROPERTY: user_account.id,
            }
            response = jsonify(data_dict)
    response.headers.add(
        api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*"
    )
    return response, response_code
