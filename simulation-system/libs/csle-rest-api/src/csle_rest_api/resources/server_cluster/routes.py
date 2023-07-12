"""
Routes and sub-resources for the /server-cluster resource
"""
from typing import Tuple
from flask import Blueprint, jsonify, request, Response
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util
from csle_common.dao.emulation_config.config import Config
from csle_common.logging.log import Logger


# Creates a blueprint "sub application" of the main REST app
server_cluster_bp = Blueprint(
    api_constants.MGMT_WEBAPP.SERVER_CLUSTER_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SERVER_CLUSTER_RESOURCE}")


@server_cluster_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def server_cluster() -> Tuple[Response, int]:
    """
    The /server-cluster resource.

    :return: The CSLE server cluster configuration
    """
    requires_admin = False
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized
    try:
        config = Config.read_config_file()
        response = jsonify(config.cluster_config.to_dict())
    except Exception as e:
        Logger.__call__().get_logger().info(f"There was an error reading the config file: {str(e)}, {repr(e)}")
        response = jsonify({})
        return response, constants.HTTPS.INTERNAL_SERVER_ERROR_STATUS_CODE
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
