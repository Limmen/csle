"""
Routes and sub-resources for the /file resource
"""
import json
import os
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants

# Creates a blueprint "sub application" of the main REST app
file_bp = Blueprint(
    api_constants.MGMT_WEBAPP.FILE_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.FILE_RESOURCE}")


@file_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def read_file():
    """
    The /file resource

    :return: Reads a given file and returns its contents
    """
    path = json.loads(request.data)[api_constants.MGMT_WEBAPP.PATH_PROPERTY]
    data = ""
    if os.path.exists(path):
        with open(path, 'r') as fp:
            data = fp.read()
    data_dict = {api_constants.MGMT_WEBAPP.LOGS_PROPERTY: data}
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
