"""
Routes and sub-resources for the /login resource
"""
import time
import json
import secrets
import bcrypt
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.management.session_token import SessionToken

# Creates a blueprint "sub application" of the main REST app
login_bp = Blueprint(
    api_constants.MGMT_WEBAPP.LOGIN_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.LOGIN_RESOURCE}")


@login_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def read_login():
    """
    The /login resource

    :return: Reads a given login and returns its contents
    """
    token = secrets.token_urlsafe(32)
    username = json.loads(request.data)[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY]
    user_account = MetastoreFacade.get_management_user_by_username(username=username)
    response_code = constants.HTTPS.UNAUTHORIZED_STATUS_CODE
    response = jsonify({})
    if user_account is not None:
        password = json.loads(request.data)[api_constants.MGMT_WEBAPP.PASSWORD_PROPERTY]
        byte_pwd = password.encode('utf-8')
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
                MetastoreFacade.update_session_token(session_token=new_token, token=new_token.token)
            data_dict = {
                api_constants.MGMT_WEBAPP.TOKEN_PROPERTY: new_token.token,
                api_constants.MGMT_WEBAPP.ADMIN_PROPERTY: user_account.admin,
                api_constants.MGMT_WEBAPP.USERNAME_PROPERTY: user_account.username
            }
            response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, response_code
