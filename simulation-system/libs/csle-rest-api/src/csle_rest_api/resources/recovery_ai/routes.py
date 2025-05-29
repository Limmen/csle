"""
Routes and sub-resources for the /recovery-ai resource
"""

from typing import Tuple
from flask import Blueprint, Response, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
recovery_ai_bp = Blueprint(
    api_constants.MGMT_WEBAPP.RECOVERY_AI_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.RECOVERY_AI_RESOURCE}")


@recovery_ai_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def recovery_ai() -> Tuple[Response, int]:
    """
    The /recovery-ai resource

    :return: Returns a recovery AI
    """
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=False)
    if authorized is not None:
        return authorized
    response = jsonify({})
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
