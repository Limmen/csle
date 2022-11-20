"""
Routes and sub-resources for the /config resource
"""
from flask import Blueprint, jsonify, request
import json
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util
from csle_common.dao.emulation_config.config import Config
from csle_common.logging.log import Logger


# Creates a blueprint "sub application" of the main REST app
config_bp = Blueprint(
    api_constants.MGMT_WEBAPP.CONFIG_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CONFIG_RESOURCE}")


@config_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                              api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def config():
    """
    The /config resource.

    :return: The CSLE configuration
    """
    requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        config = {}
        try:
            config = Config.read_config_file()
        except Exception as e:
            Logger.__call__().get_logger().info(f"There was an error reading the config file: {str(e)}, {repr(e)}")
        response = jsonify(config.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        json_data = json.loads(request.data)
        # Verify payload
        if api_constants.MGMT_WEBAPP.CONFIG_RESOURCE not in json_data:
            return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
        config = json_data[api_constants.MGMT_WEBAPP.CONFIG_RESOURCE]
        Config.save_config_file(config=config)
        Config.set_config_parameters_from_config_file()
        response = jsonify(config.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE