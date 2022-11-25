"""
Routes and sub-resources for the /version resource
"""
from flask import Blueprint, jsonify
from importlib.metadata import version as meta_version
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants


# Creates a blueprint "sub application" of the main REST app
version_bp = Blueprint(
    api_constants.MGMT_WEBAPP.VERSION_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.VERSION_RESOURCE}")


@version_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def version():
    """
    The /version resource.

    :return: The version of CSLE management system
    """
    csle_version = meta_version('csle_rest_api')
    csle_version_dict = {}
    csle_version_dict[api_constants.MGMT_WEBAPP.VERSION_PROPERTY] = csle_version
    response = jsonify(csle_version_dict)
    return response, constants.HTTPS.OK_STATUS_CODE
