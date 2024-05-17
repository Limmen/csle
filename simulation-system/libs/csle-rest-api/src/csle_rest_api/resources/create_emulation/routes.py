"""
Routes and sub-resources for the /create-emulation resource
"""
from typing import Tuple
import csle_common.constants.constants as constants
from flask import Blueprint, jsonify, request, Response
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
create_emulation_bp = Blueprint(
    api_constants.MGMT_WEBAPP.CREATE_EMULATION_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CREATE_EMULATION_RESOURCE}")


@create_emulation_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def create_emulation() -> Tuple[Response, int]:
    """
    The /create-emulation resource.

    :return: The given policy or deletes the policy
    """
    print("Create emulation")
    requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    response = jsonify({"TEST": "TEST"})
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
