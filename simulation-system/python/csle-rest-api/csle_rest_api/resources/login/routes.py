"""
Routes and sub-resources for the /login resource
"""
import json
import secrets
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants

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
    password = json.loads(request.data)[api_constants.MGMT_WEBAPP.PASSWORD_PROPERTY]
    data_dict = {
        api_constants.MGMT_WEBAPP.TOKEN_PROPERTY: token
    }
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response
